import os
import sqlite3
import json
from flask import Flask, render_template, request, g, redirect, url_for, flash, session


def create_app(test_config=None):
    """
    Application factory creating a Flask application instance.  The app uses
    SQLite for persistence.  Besides listing sites, it supports user
    suggestions and an admin interface to approve or reject suggestions.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')
    app.config['DATABASE'] = os.path.join(app.root_path, 'data', 'sites.db')

    # Administrator credentials (in a real deployment store them securely)
    app.config['ADMIN_USER'] = os.environ.get('ADMIN_USER', 'admin')
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'password')

    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    # Database helpers
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db():
        """Initialise the database with the required tables and sample data."""
        db = get_db()
        with db:
            # Create tables
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
            db.execute(
                '''CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    category TEXT NOT NULL,
                    verification_type TEXT,
                    country TEXT,
                    description TEXT,
                    alternatives_json TEXT,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )'''
            )
            # Insert sample data if empty
            count = db.execute('SELECT COUNT(*) FROM sites').fetchone()[0]
            if count == 0:
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
                db.commit()
                # Insert alternatives for sample data
                porn_id = db.execute('SELECT id FROM sites WHERE name=?', ('Pornhub',)).fetchone()['id']
                reddit_id = db.execute('SELECT id FROM sites WHERE name=?', ('Reddit',)).fetchone()['id']
                spotify_id = db.execute('SELECT id FROM sites WHERE name=?', ('Spotify',)).fetchone()['id']
                twitter_id = db.execute('SELECT id FROM sites WHERE name=?', ('X (Twitter)',)).fetchone()['id']
                sample_alts = [
                    {'site_id': porn_id, 'alt_name': 'YouPorn', 'alt_url': 'https://www.youporn.com', 'alt_description': 'Site de vidéos pour adultes accessible sans vérification intrusive (confirmation 18+ classique).'},
                    {'site_id': porn_id, 'alt_name': 'SpankBang', 'alt_url': 'https://spankbang.com', 'alt_description': 'Plateforme pour adultes offrant un contenu similaire, sans pièce d’identité requise.'},
                    {'site_id': reddit_id, 'alt_name': 'Lemmy', 'alt_url': 'https://join-lemmy.org', 'alt_description': 'Alternative open‑source fédérée à Reddit ; pas de vérification centrale.'},
                    {'site_id': reddit_id, 'alt_name': 'Kbin', 'alt_url': 'https://kbin.social', 'alt_description': 'Alternative communautaire aux forums, sans demande d’ID.'},
                    {'site_id': spotify_id, 'alt_name': 'Bandcamp', 'alt_url': 'https://bandcamp.com', 'alt_description': 'Plateforme de musique indépendante avec simple confirmation 18+ pour les contenus explicites.'},
                    {'site_id': twitter_id, 'alt_name': 'Mastodon', 'alt_url': 'https://joinmastodon.org', 'alt_description': 'Réseau social décentralisé ; aucune vérification globale, chaque instance définit ses règles.'},
                    {'site_id': twitter_id, 'alt_name': 'Bluesky', 'alt_url': 'https://blueskyweb.xyz', 'alt_description': 'Réseau social alternatif plus ouvert ; encore sans vérification obligatoire en dehors du Royaume‑Uni.'}
                ]
                for alt in sample_alts:
                    db.execute('INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description) VALUES (?, ?, ?, ?)',
                               (alt['site_id'], alt['alt_name'], alt['alt_url'], alt['alt_description']))
                db.commit()

    with app.app_context():
        init_db()

    # Expose DB helper for tests
    app.get_db = get_db

    # Routes
    @app.route('/')
    def index():
        db = get_db()
        categories = [row['category'] for row in db.execute('SELECT DISTINCT category FROM sites').fetchall()]
        recent_sites = db.execute('SELECT id, name, category, verification_type FROM sites ORDER BY id DESC LIMIT 4').fetchall()
        return render_template('index.html', categories=categories, recent_sites=recent_sites)

    @app.route('/sites')
    def sites():
        db = get_db()
        q = request.args.get('q', '').strip().lower()
        category = request.args.get('category', '')
        country = request.args.get('country', '')
        query = 'SELECT * FROM sites WHERE 1=1'
        params = []
        if q:
            query += ' AND LOWER(name) LIKE ?'
            params.append(f'%{q}%')
        if category:
            query += ' AND category = ?'
            params.append(category)
        if country:
            query += ' AND country = ?'
            params.append(country)
        query += ' ORDER BY name COLLATE NOCASE ASC'
        sites_list = db.execute(query, params).fetchall()
        categories = [row['category'] for row in db.execute('SELECT DISTINCT category FROM sites').fetchall()]
        countries = [row['country'] for row in db.execute('SELECT DISTINCT country FROM sites').fetchall()]
        return render_template('sites.html', sites=sites_list, categories=categories, countries=countries, selected_category=category, selected_country=country, q=q)

    @app.route('/site/<int:site_id>')
    def site_detail(site_id):
        db = get_db()
        site = db.execute('SELECT * FROM sites WHERE id = ?', (site_id,)).fetchone()
        if site is None:
            return render_template('not_found.html'), 404
        alts = db.execute('SELECT * FROM alternatives WHERE site_id = ?', (site_id,)).fetchall()
        return render_template('site_detail.html', site=site, alternatives=alts)

    @app.route('/about')
    def about():
        return render_template('about.html')

    # User suggestion form
    @app.route('/suggest', methods=['GET', 'POST'])
    def suggest():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            url_field = request.form.get('url', '').strip()
            category = request.form.get('category', '').strip()
            verification_type = request.form.get('verification_type', '').strip()
            country = request.form.get('country', '').strip()
            description = request.form.get('description', '').strip()
            alternatives_text = request.form.get('alternatives', '').strip()
            # parse alternatives: one per line "name | url | description"
            alternatives = []
            if alternatives_text:
                for line in alternatives_text.splitlines():
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 2:
                        alt_desc = parts[2] if len(parts) > 2 else ''
                        alternatives.append({
                            'name': parts[0],
                            'url': parts[1],
                            'description': alt_desc
                        })
            # insert suggestion into database
            db = get_db()
            db.execute(
                'INSERT INTO suggestions (name, url, category, verification_type, country, description, alternatives_json) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, url_field, category, verification_type, country, description, json.dumps(alternatives))
            )
            db.commit()
            flash('Merci, votre suggestion a été soumise pour validation par un administrateur.', 'success')
            return redirect(url_for('suggest'))
        return render_template('suggest.html')

    # Admin login
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            if username == app.config['ADMIN_USER'] and password == app.config['ADMIN_PASSWORD']:
                session['admin'] = True
                flash('Connexion réussie.', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Identifiants invalides.', 'danger')
        return render_template('admin_login.html')

        
    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin', None)
        flash('Déconnexion effectuée.', 'success')
        return redirect(url_for('index'))

    def admin_required(f):
        from functools import wraps
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('admin'):
                return redirect(url_for('admin_login'))
            return f(*args, **kwargs)
        return wrapper

    # Admin dashboard listing suggestions
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        db = get_db()
        rows = db.execute('SELECT * FROM suggestions ORDER BY submitted_at DESC').fetchall()
        # Convert rows to dictionaries and parse alternatives JSON once here to avoid using json in template
        suggestions = []
        for row in rows:
            data = dict(row)
            alt_json = data.get('alternatives_json')
            try:
                alternatives = json.loads(alt_json) if alt_json else []
            except Exception:
                alternatives = []
            data['alternatives'] = alternatives
            suggestions.append(data)
        return render_template('admin_dashboard.html', suggestions=suggestions)

    # Admin action on suggestion
    @app.route('/admin/suggestion/<int:sug_id>/<action>', methods=['POST'])
    @admin_required
    def admin_suggestion_action(sug_id, action):
        db = get_db()
        sug = db.execute('SELECT * FROM suggestions WHERE id = ?', (sug_id,)).fetchone()
        if not sug:
            flash('Suggestion introuvable.', 'danger')
            return redirect(url_for('admin_dashboard'))
        if action == 'accept':
            # Insert new site and alternatives
            cur = db.execute(
                'INSERT INTO sites (name, url, category, description, verification_type, context, date_in_effect, status, country, sources) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (sug['name'], sug['url'], sug['category'], sug['description'], sug['verification_type'], '', '', 'En attente de précisions', sug['country'], '')
            )
            site_id = cur.lastrowid
            # insert alternatives if provided
            alts = json.loads(sug['alternatives_json']) if sug['alternatives_json'] else []
            for alt in alts:
                db.execute('INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description) VALUES (?, ?, ?, ?)',
                           (site_id, alt.get('name'), alt.get('url'), alt.get('description')))
            db.commit()
            flash('Suggestion acceptée et ajoutée à la base.', 'success')
        elif action == 'reject':
            flash('Suggestion rejetée.', 'warning')
        # Remove suggestion from table
        db.execute('DELETE FROM suggestions WHERE id = ?', (sug_id,))
        db.commit()
        return redirect(url_for('admin_dashboard'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)