import os
import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for, flash


def create_app(test_config=None):
    """
    Application factory.  Creates and configures a Flask application
    instance. Uses a SQLite database stored in the data directory.
    """
    app = Flask(__name__)
    # secret key for flash messages; in a production deployment this should
    # be configured via an environment variable. Here it is hard‑coded for
    # simplicity since no sensitive sessions are stored.
    app.config['SECRET_KEY'] = 'change-this-secret-key'
    # determine absolute path to the SQLite database file
    app.config['DATABASE'] = os.path.join(app.root_path, 'data', 'sites.db')

    # ensure the data directory exists
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    def get_db():
        """Open a new database connection if there is none yet for the
        current application context."""
        if 'db' not in g:
            g.db = sqlite3.connect(
                app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        """Closes the database at the end of the request."""
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db():
        """Create the tables and insert sample data if the database is empty."""
        db = get_db()
        with db:
            # create tables
            db.execute(
                '''CREATE TABLE IF NOT EXISTS sites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    verification_type TEXT,
                    context TEXT,
                    date_in_effect TEXT,
                    status TEXT,
                    country TEXT,
                    sources TEXT
                )'''
            )
            db.execute(
                '''CREATE TABLE IF NOT EXISTS alternatives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_id INTEGER NOT NULL,
                    alt_name TEXT NOT NULL,
                    alt_url TEXT NOT NULL,
                    alt_description TEXT,
                    FOREIGN KEY (site_id) REFERENCES sites(id)
                )'''
            )
            # check if there is at least one site; if not, insert sample data
            cur = db.execute('SELECT COUNT(*) FROM sites')
            count = cur.fetchone()[0]
            if count == 0:
                # Sample data inspired by current events (fictional descriptions)
                sample_sites = [
                    {
                        'name': 'Pornhub',
                        'url': 'https://www.pornhub.com',
                        'category': 'Adulte',
                        'description': 'Plateforme de vidéos pour adultes populaire.',
                        'verification_type': 'Selfie vidéo ou pièce d’identité via un prestataire',
                        'context': 'Conformité à la loi française 2024 ; blocage complet en France en signe de protestation.',
                        'date_in_effect': 'juillet 2024',
                        'status': 'Bloqué en France ; accessible sans vérification hors France',
                        'country': 'FR',
                        'sources': 'Politico.eu, TF1 Info, AP News'
                    },
                    {
                        'name': 'Reddit',
                        'url': 'https://www.reddit.com',
                        'category': 'Réseaux sociaux',
                        'description': 'Forum communautaire regroupant des discussions sur des milliers de sujets.',
                        'verification_type': 'Vérification d’âge via service tiers (Persona) – scan d’une pièce d’identité ou selfie vidéo',
                        'context': 'Conformité à l’Online Safety Act 2023 (R.-Uni)',
                        'date_in_effect': 'juillet 2024',
                        'status': 'Vérification requise au Royaume‑Uni seulement',
                        'country': 'UK',
                        'sources': 'Tom’s Guide'
                    },
                    {
                        'name': 'Spotify',
                        'url': 'https://www.spotify.com',
                        'category': 'Streaming',
                        'description': 'Service de streaming musical et de podcasts.',
                        'verification_type': 'Contrôle d’âge via Yoti pour certains clips 18+',
                        'context': 'Volonté de respecter les réglementations sur le contenu adulte',
                        'date_in_effect': '2024',
                        'status': 'Vérification appliquée de manière sélective pour les clips 18+',
                        'country': 'International',
                        'sources': 'Tom’s Guide'
                    },
                    {
                        'name': 'X (Twitter)',
                        'url': 'https://twitter.com',
                        'category': 'Réseaux sociaux',
                        'description': 'Réseau social de micro‑blogging.',
                        'verification_type': 'Demande d’identité ou de carte bancaire pour accéder à certains contenus sensibles',
                        'context': 'Déploiement progressif en réponse aux lois britanniques',
                        'date_in_effect': '2024',
                        'status': 'Implémenté au Royaume‑Uni ; tests dans d’autres régions',
                        'country': 'UK',
                        'sources': 'Tom’s Guide'
                    }
                ]
                # insert sites
                for site in sample_sites:
                    db.execute(
                        '''INSERT INTO sites
                            (name, url, category, description, verification_type, context, date_in_effect, status, country, sources)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (
                            site['name'], site['url'], site['category'], site['description'],
                            site['verification_type'], site['context'], site['date_in_effect'],
                            site['status'], site['country'], site['sources']
                        )
                    )
                # commit sample data and retrieve inserted site ids
                db.commit()
                # set alternatives
                # find site ids
                porn_id = db.execute('SELECT id FROM sites WHERE name=?', ('Pornhub',)).fetchone()['id']
                reddit_id = db.execute('SELECT id FROM sites WHERE name=?', ('Reddit',)).fetchone()['id']
                spotify_id = db.execute('SELECT id FROM sites WHERE name=?', ('Spotify',)).fetchone()['id']
                twitter_id = db.execute('SELECT id FROM sites WHERE name=?', ('X (Twitter)',)).fetchone()['id']
                sample_alternatives = [
                    # alternatives for Pornhub
                    {
                        'site_id': porn_id,
                        'alt_name': 'YouPorn',
                        'alt_url': 'https://www.youporn.com',
                        'alt_description': 'Site de vidéos pour adultes accessible sans vérification intrusive (confirmation 18+ classique).'
                    },
                    {
                        'site_id': porn_id,
                        'alt_name': 'SpankBang',
                        'alt_url': 'https://spankbang.com',
                        'alt_description': 'Plateforme pour adultes offrant un contenu similaire, sans pièce d’identité requise.'
                    },
                    # alternatives for Reddit
                    {
                        'site_id': reddit_id,
                        'alt_name': 'Lemmy',
                        'alt_url': 'https://join-lemmy.org',
                        'alt_description': 'Alternative open‑source fédérée à Reddit ; pas de vérification centrale.'
                    },
                    {
                        'site_id': reddit_id,
                        'alt_name': 'Kbin',
                        'alt_url': 'https://kbin.social',
                        'alt_description': 'Alternative communautaire aux forums, sans demande d’ID.'
                    },
                    # alternatives for Spotify
                    {
                        'site_id': spotify_id,
                        'alt_name': 'Bandcamp',
                        'alt_url': 'https://bandcamp.com',
                        'alt_description': 'Plateforme de musique indépendante avec simple confirmation 18+ pour les contenus explicites.'
                    },
                    # alternatives for Twitter
                    {
                        'site_id': twitter_id,
                        'alt_name': 'Mastodon',
                        'alt_url': 'https://joinmastodon.org',
                        'alt_description': 'Réseau social décentralisé ; aucune vérification globale, chaque instance définit ses règles.'
                    },
                    {
                        'site_id': twitter_id,
                        'alt_name': 'Bluesky',
                        'alt_url': 'https://blueskyweb.xyz',
                        'alt_description': 'Réseau social alternatif plus ouvert ; encore sans vérification obligatoire en dehors du Royaume‑Uni.'
                    }
                ]
                for alt in sample_alternatives:
                    db.execute(
                        '''INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description) VALUES (?, ?, ?, ?)''',
                        (alt['site_id'], alt['alt_name'], alt['alt_url'], alt['alt_description'])
                    )
                db.commit()

    # initialize the database at startup
    with app.app_context():
        init_db()

    # expose the get_db function on the app for use in other modules
    app.get_db = get_db

    @app.route('/')
    def index():
        """Home page: display search bar and highlights."""
        db = get_db()
        # fetch categories (unique)
        categories = [row['category'] for row in db.execute('SELECT DISTINCT category FROM sites').fetchall()]
        # fetch most recent sites (limit 4)
        recent_sites = db.execute('SELECT id, name, category, verification_type FROM sites ORDER BY id DESC LIMIT 4').fetchall()
        return render_template('index.html', categories=categories, recent_sites=recent_sites)

    @app.route('/sites')
    def sites():
        """List sites filtered by query parameters q (search), category and country."""
        db = get_db()
        q = request.args.get('q', '').strip()
        category = request.args.get('category', '')
        country = request.args.get('country', '')
        # build SQL query dynamically
        query = 'SELECT * FROM sites WHERE 1=1'
        params = []
        if q:
            query += ' AND LOWER(name) LIKE ?'
            params.append(f'%{q.lower()}%')
        if category:
            query += ' AND category = ?'
            params.append(category)
        if country:
            query += ' AND country = ?'
            params.append(country)
        # order by name ascending
        query += ' ORDER BY name COLLATE NOCASE ASC'
        sites_list = db.execute(query, params).fetchall()
        # gather list of categories and countries for filter options
        categories = [row['category'] for row in db.execute('SELECT DISTINCT category FROM sites').fetchall()]
        countries = [row['country'] for row in db.execute('SELECT DISTINCT country FROM sites').fetchall()]
        return render_template('sites.html', sites=sites_list, categories=categories, countries=countries, selected_category=category, selected_country=country, q=q)

    @app.route('/site/<int:site_id>')
    def site_detail(site_id):
        """Show details for a particular site."""
        db = get_db()
        site = db.execute('SELECT * FROM sites WHERE id = ?', (site_id,)).fetchone()
        if site is None:
            return render_template('not_found.html'), 404
        alternatives = db.execute('SELECT * FROM alternatives WHERE site_id = ?', (site_id,)).fetchall()
        return render_template('site_detail.html', site=site, alternatives=alternatives)

    @app.route('/about')
    def about():
        """About page describing the project."""
        return render_template('about.html')

    @app.route('/suggest', methods=['GET', 'POST'])
    def suggest():
        """
        Page allowing users to suggest a new site or alternative. Suggestions are not stored persistently
        but a success message is shown to simulate future handling.
        """
        if request.method == 'POST':
            flash('Merci pour votre suggestion ! Nous la prendrons en compte après vérification.', 'success')
            return redirect(url_for('suggest'))
        return render_template('suggest.html')

    return app


if __name__ == '__main__':
    # run the application for local testing
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)