"""
This module contains a minimal web application implementing the StopIDCheck
prototype.  The application is written with Flask so it can be easily run
locally or deployed to a service such as Render or Railway.

The primary goal of this MVP is to provide a read–only catalogue of web
sites which enforce an intrusive age or identity verification and to offer
privacy‑friendly alternatives.  Additionally a simple suggestion form is
provided so that visitors can propose new entries.  An administration
interface is included to review and publish suggestions.  All data is
persisted in a local SQLite database for simplicity.

The code has been extensively commented to make it self‑documenting.  Each
route handler contains a docstring explaining its purpose and relevant
implementation details.  Helper functions such as the database connection
are also documented.
"""

import os
import sqlite3
from typing import List, Dict, Any

from flask import Flask, render_template, request, g, redirect, url_for, flash, session


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory for the StopIDCheck MVP.

    This function follows the Flask application factory pattern and
    encapsulates all configuration, route registration and database setup.
    Returning a new app instance each time makes the code easier to test
    and simplifies configuration of different environments.  A `test_config`
    dictionary can be passed to override any default configuration
    variables.
    """
    app = Flask(__name__)

    # ------------------------------------------------------------------
    # Configuration
    #
    # Configuration values control the behaviour of the application.  When
    # deploying to a hosting provider you should set these values via
    # environment variables.  The SECRET_KEY is used by Flask to
    # sign session cookies; never expose it publicly.  The path to the
    # SQLite database lives inside the `data` subdirectory of this module.
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'change-this-secret-key'),
        DATABASE=os.path.join(app.root_path, 'data', 'sites.db'),
        ADMIN_USER=os.environ.get('ADMIN_USER', 'admin'),
        ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD', 'password'),
    )
    # If a test configuration is provided, override defaults.  This is
    # useful when writing unit tests.
    if test_config is not None:
        app.config.update(test_config)

    # Ensure that the directory for the database exists.  This call is
    # idempotent; if the directory already exists nothing happens.
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    # ------------------------------------------------------------------
    # Database helper functions
    #
    # The following helper functions wrap access to the SQLite database.
    # Using g (Flask's application context) ensures that each request
    # reuses the same database connection and that it is closed cleanly
    # after the request finishes.
    def get_db() -> sqlite3.Connection:
        """Open a new database connection if none exists for the current context.

        When called for the first time in a request this function creates
        a new connection to the SQLite database file and configures it to
        return rows as dictionaries.  The connection is stored on the
        `g` object so subsequent calls in the same request return the same
        connection.  See https://flask.palletsprojects.com/en/latest/appcontext/
        for details about the application context.
        """
        if 'db' not in g:
            g.db = sqlite3.connect(
                app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            # Rows will behave like dicts so we can access columns by name.
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception: Exception | None) -> None:
        """Close the database connection at the end of the request.

        Flask automatically calls functions decorated with
        `@app.teardown_appcontext` when the application context is torn down.
        We remove the connection from `g` and close it if it exists.  This
        prevents connections from leaking between requests.
        """
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db() -> None:
        """Initialise the database schema and insert a few sample entries.

        Executing this function will create the `sites`, `alternatives` and
        `suggestions` tables if they do not already exist.  A handful of
        well‑known web sites are inserted into the `sites` table on the
        first run to demonstrate the application.  Running this function
        repeatedly is safe because it checks whether the `sites` table is
        empty before seeding the sample data.
        """
        db = get_db()
        with db:
            # Create the core tables.  If a table already exists the IF NOT
            # EXISTS clause prevents an error from being raised.
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
            # Seed sample data on first run
            count = db.execute('SELECT COUNT(*) FROM sites').fetchone()[0]
            if count == 0:
                sample_sites: List[Dict[str, Any]] = [
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
                # Bulk insert the sample sites
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
                # Commit before inserting alternatives to reference the generated IDs
                db.commit()
                # Retrieve the IDs for the inserted sites
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
                    {'site_id': spotify_id, 'alt_name': 'SoundCloud', 'alt_url': 'https://soundcloud.com', 'alt_description': 'Service de streaming audio orienté vers les créateurs ; pas de contrôle d’identité généralisé.'},
                    {'site_id': twitter_id, 'alt_name': 'Mastodon', 'alt_url': 'https://mastodon.social', 'alt_description': 'Réseau social décentralisé où chaque instance peut définir ses règles.'}
                ]
                for alt in sample_alts:
                    db.execute(
                        '''INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description)
                           VALUES (?, ?, ?, ?)''',
                        (alt['site_id'], alt['alt_name'], alt['alt_url'], alt['alt_description'])
                    )
                db.commit()

    # Initialise database when the application starts
    with app.app_context():
        init_db()

    # ------------------------------------------------------------------
    # Helper functions and context processors
    #
    # To support advanced filtering, country flag display and multi-select
    # dropdowns, we define a few helper functions and inject data into the
    # template context.  These helpers are available in all templates.

    @app.context_processor
    def inject_filter_data():
        """Inject lists of filter values and a flag helper into the template context.

        - categories: list of unique categories for filter drop-downs.
        - verification_types: predefined list of verification keywords for
          filtering and suggestion drop-downs.  These correspond to
          broad methods used across sites (e.g. ID, selfie, card check).
        - countries: list of unique country codes encountered in the
          database, plus a few common regions.  Display order is
          alphabetical.
        - flag_emoji: function mapping a country code string to one or
          more flag emojis.  Multiple country codes separated by commas
          will return all relevant flags.
        """
        db = get_db()
        # Collect distinct categories from the DB for filters and forms
        cat_rows = db.execute('SELECT DISTINCT category FROM sites').fetchall()
        categories = sorted({row['category'] for row in cat_rows})
        # Predefine common verification keywords used across the site entries
        verification_types = [
            'Pièce d’identité', 'Selfie', 'Selfie vidéo', 'Estimation faciale',
            'Carte bancaire', 'Numéro de téléphone', 'Yoti', 'Persona',
            'Veriff', 'FaceTec', 'Stripe', 'k‑iD', 'Pas d’ID requis'
        ]
        # Collect unique country codes from DB.  Split by commas and strip spaces.
        country_set: set[str] = set()
        for row in db.execute('SELECT country FROM sites').fetchall():
            if row['country']:
                for code in row['country'].split(','):
                    country_set.add(code.strip())
        # Add a few generic regions
        country_set.update({'International', 'UE', 'EU'})
        countries = sorted(country_set)

        def flag_emoji(country_string: str) -> str:
            """Return flag emoji(s) for a comma-separated country code string.

            Supports ISO country codes like 'FR' (🇫🇷), 'UK' (🇬🇧),
            'AU' (🇦🇺), 'US' (🇺🇸) as well as 'UE'/'EU' (🇪🇺).  If multiple
            codes are provided they will be concatenated with spaces.
            If a code is unknown, it returns an empty string for that code.
            """
            if not country_string:
                return ''
            mapping = {
                'FR': '🇫🇷',
                'UK': '🇬🇧',
                'AU': '🇦🇺',
                'US': '🇺🇸',
                'EU': '🇪🇺',
                'UE': '🇪🇺',
                'UK, FR': '🇬🇧 🇫🇷',
                'FR, UK': '🇫🇷 🇬🇧',
                'International': '🌍'
            }
            # If the entire string matches a mapping, return it directly
            if country_string in mapping:
                return mapping[country_string]
            # Otherwise parse each code individually
            flags: list[str] = []
            for code in country_string.split(','):
                code = code.strip()
                if code in mapping:
                    flags.append(mapping[code])
                else:
                    # Build Unicode flag for 2-letter code if possible
                    if len(code) == 2 and code.isalpha():
                        # Convert letters to regional indicator symbols
                        base = ord('🇦') - ord('A')
                        flag_chars = ''.join(chr(base + ord(ch.upper())) for ch in code)
                        flags.append(flag_chars)
            return ' '.join(flags)

        return dict(
            categories=categories,
            verification_types=verification_types,
            countries=countries,
            flag_emoji=flag_emoji,
        )

    def compute_severity(site_row: sqlite3.Row) -> tuple[str, str]:
        """Compute a severity label and a corresponding CSS class based on site data.

        Severity levels:
            - low (green): optional verification, not restricted to a single country
            - medium (yellow): verification planned or experimental, or
              mandatory but limited to certain content types
            - high (orange): mandatory verification or geo‑blocking in specific regions
            - very-high (red): strict mandatory verification combined with blocking

        The function returns a tuple (label, css_class).
        """
        status = (site_row['status'] or '').lower()
        country = (site_row['country'] or '').lower()
        # Default values
        label = 'Moyen'
        css_class = 'severity-medium'
        # Determine if verification is optional (facultatif) or required (obligatoire)
        is_optional = any(word in status for word in ['facultatif', 'facultative', 'optionnel', 'optionnelle', 'optionnelle', 'optionnelle'])
        is_mandatory = any(word in status for word in ['obligatoire', 'requise', 'vérification requise', 'mandatory', 'requis'])
        is_blocked = any(word in status for word in ['bloqué', 'blocage', 'non accessible', 'blocage complet'])
        # Determine if the country list implies global or local scope
        # Consider multiple codes or explicit 'international' as global
        country_codes = [c.strip() for c in country.split(',') if c.strip()]
        is_global = False
        if not country_codes or any(code in ['international', 'global', 'monde'] for code in country_codes):
            is_global = True
        elif len(country_codes) > 1:
            is_global = True
        # Compute severity according to rules
        if is_blocked:
            label = 'Très élevé'
            css_class = 'severity-very-high'
        elif is_mandatory:
            # Mandatory verification.  If it applies globally or multiple regions, severity very high
            if is_global:
                label = 'Très élevé'
                css_class = 'severity-very-high'
            else:
                label = 'Élevé'
                css_class = 'severity-high'
        elif is_optional:
            # Optional verification.  If global scope, severity low; if localized, medium
            if is_global:
                label = 'Faible'
                css_class = 'severity-low'
            else:
                label = 'Moyen'
                css_class = 'severity-medium'
        else:
            # Unknown or planned/experimental status; treat as medium
            label = 'Moyen'
            css_class = 'severity-medium'
        return label, css_class

    # ------------------------------------------------------------------
    # Routes
    #
    # The following route handlers implement the views of our MVP.  Each
    # handler fetches data from the database and renders an HTML template
    # defined in the templates/ directory.

    @app.route('/')
    def index() -> str:
        """Render the home page with search and category overview.

        The home page provides a high‑level introduction and an entry point
        to search the database.  It also displays a list of recently added
        sites and the list of unique categories present in the database.
        """
        db = get_db()
        # Retrieve categories for the filter list.  DISTINCT ensures each
        # category appears only once.
        categories = [row['category'] for row in db.execute('SELECT DISTINCT category FROM sites ORDER BY category')]
        # Retrieve the five most recent sites by descending id (i.e. order of insertion)
        recent_sites = db.execute('SELECT * FROM sites ORDER BY id DESC LIMIT 5').fetchall()
        return render_template('index.html', categories=categories, recent_sites=recent_sites)

    @app.route('/sites')
    def list_sites() -> str:
        """Display all sites with optional multi‑filtering and search.

        This view accepts multiple query parameters to refine the site list:

        - `category`: one or more categories selected via a multi‑select.
        - `verification_type`: one or more verification keywords (e.g. "Pièce d’identité",
          "Selfie").  The filter matches rows whose `verification_type` contains
          any of the selected keywords.
        - `country`: one or more country codes; matches rows where the `country`
          field contains any selected code.
        - `q`: free‑text search term applied across several columns (name,
          description, verification_type, context, country, sources).

        The resulting rows are ordered alphabetically by name and enhanced with
        a computed severity label and CSS class.  These values are used in
        the template to display coloured severity indicators.
        """
        db = get_db()
        # Parse multi‑select parameters.  Flask returns a list for each key if
        # multiple values are provided.
        categories = request.args.getlist('category')
        verifs = request.args.getlist('verification_type')
        countries = request.args.getlist('country')
        query = request.args.get('q')

        sql = 'SELECT * FROM sites'
        params: list[str] = []
        conditions: list[str] = []
        # Filter by categories (exact match)
        if categories:
            placeholders = ','.join('?' * len(categories))
            conditions.append(f'category IN ({placeholders})')
            params.extend(categories)
        # Filter by verification keywords: match if any keyword appears in
        # verification_type column.  We construct OR conditions.
        if verifs:
            like_conditions = []
            for keyword in verifs:
                like_conditions.append('verification_type LIKE ?')
                params.append(f'%{keyword}%')
            conditions.append('(' + ' OR '.join(like_conditions) + ')')
        # Filter by countries: match if any selected code appears in the
        # country column (which may contain comma‑separated values).
        if countries:
            country_conditions = []
            for code in countries:
                country_conditions.append('country LIKE ?')
                params.append(f'%{code}%')
            conditions.append('(' + ' OR '.join(country_conditions) + ')')
        # Free text search
        if query:
            conditions.append('(' + ' OR '.join([
                'name LIKE ?', 'description LIKE ?', 'verification_type LIKE ?',
                'context LIKE ?', 'country LIKE ?', 'sources LIKE ?'
            ]) + ')')
            like_expr = f'%{query}%'
            params.extend([like_expr] * 6)
        if conditions:
            sql += ' WHERE ' + ' AND '.join(conditions)
        sql += ' ORDER BY name'
        rows = db.execute(sql, params).fetchall()
        # Compute severity for each row and convert to dict for easier use in Jinja
        sites = []
        for row in rows:
            label, css_class = compute_severity(row)
            # Convert row to dict and attach severity fields
            d = dict(row)
            d['severity_label'] = label
            d['severity_class'] = css_class
            sites.append(d)
        # Selected filters for template to persist selections
        selected = {
            'category': categories,
            'verification_type': verifs,
            'country': countries
        }
        return render_template('site_list.html', sites=sites, selected=selected, query=query)

    @app.route('/site/<int:site_id>')
    def view_site(site_id: int) -> str:
        """Display details of a single site along with its alternatives.

        A single site is looked up by primary key.  If no site is found
        matching the given ID we abort with a 404.  Alternatives are
        fetched via a simple join on the `alternatives` table.
        """
        db = get_db()
        site_row = db.execute('SELECT * FROM sites WHERE id=?', (site_id,)).fetchone()
        if site_row is None:
            return render_template('404.html'), 404
        # Compute severity for this site to display indicator on detail page
        severity_label, severity_class = compute_severity(site_row)
        # Convert to dict and attach severity
        site = dict(site_row)
        site['severity_label'] = severity_label
        site['severity_class'] = severity_class
        alternatives = db.execute('SELECT * FROM alternatives WHERE site_id=?', (site_id,)).fetchall()
        return render_template('site_detail.html', site=site, alternatives=alternatives)

    @app.route('/suggest', methods=['GET', 'POST'])
    def suggest() -> str:
        """Handle the form allowing visitors to suggest new entries.

        On GET requests the form is rendered.  On POST the submitted data
        are validated for minimal completeness and stored into the
        `suggestions` table as JSON for the alternatives.  The admin can
        later review and publish these suggestions.
        """
        if request.method == 'POST':
            # Retrieve basic fields from the form.  We normalise whitespace to
            # avoid storing accidental leading/trailing spaces.
            name = request.form.get('name', '').strip()
            url = request.form.get('url', '').strip()
            # Category, verification type and country can be selected as
            # multi‑selects.  Use getlist() to capture all selected values.
            category_list = [c.strip() for c in request.form.getlist('category') if c.strip()]
            verification_list = [v.strip() for v in request.form.getlist('verification_type') if v.strip()]
            country_list = [c.strip() for c in request.form.getlist('country') if c.strip()]
            description = request.form.get('description', '').strip()
            # Convert alternatives lines into a list of dicts.  Each line is
            # expected to contain at least a name and URL separated by pipes.
            alternatives_raw = request.form.get('alternatives', '').strip()
            alternatives_list: List[Dict[str, str]] = []
            if alternatives_raw:
                for line in alternatives_raw.splitlines():
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 2:
                        alt = {
                            'name': parts[0],
                            'url': parts[1],
                            'description': parts[2] if len(parts) > 2 else ''
                        }
                        alternatives_list.append(alt)
            # At least one category is required, as well as name and URL.
            if not (name and url and category_list):
                flash('Veuillez remplir les champs obligatoires (nom, url, catégorie).', 'error')
            else:
                db = get_db()
                import json
                # Join selected values with commas for storage.  The admin and
                # list views split these strings back into separate tokens.
                category = ', '.join(category_list)
                verification_type = ', '.join(verification_list)
                country = ', '.join(country_list)
                db.execute(
                    '''INSERT INTO suggestions (name, url, category, verification_type, country, description, alternatives_json)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (name, url, category, verification_type, country, description, json.dumps(alternatives_list))
                )
                db.commit()
                flash('Merci pour votre suggestion ! Elle sera revue par un administrateur.', 'success')
                return redirect(url_for('index'))
        # Render the suggestion form with available filter values for the drop‑downs.
        return render_template('suggest.html')

    # ------------------- Admin routes ------------------------------------
    # A very simple authentication mechanism protects the admin area.
    # In a real application you should implement proper password hashing
    # and avoid storing credentials in plain text.

    @app.route('/login', methods=['GET', 'POST'])
    def login() -> str:
        """Render and process the login form for the administrator.

        If the posted credentials match the configured admin user/password
        then a session flag is set and the admin is redirected to the
        dashboard.  Otherwise an error message is flashed.  Sessions
        persist across requests via secure cookies.
        """
        if request.method == 'POST':
            user = request.form.get('username', '')
            password = request.form.get('password', '')
            if user == app.config['ADMIN_USER'] and password == app.config['ADMIN_PASSWORD']:
                session['logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            flash('Identifiants incorrects.', 'error')
        return render_template('login.html')

    @app.route('/logout')
    def logout() -> str:
        """Clear the session and redirect to the home page."""
        session.clear()
        return redirect(url_for('index'))

    def login_required(view_func):
        """Decorator to protect routes that require administrator login."""
        from functools import wraps
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            return view_func(*args, **kwargs)
        return wrapper

    @app.route('/admin')
    @login_required
    def admin_dashboard() -> str:
        """Display pending suggestions for the administrator to review."""
        db = get_db()
        suggestions = db.execute('SELECT * FROM suggestions ORDER BY submitted_at DESC').fetchall()
        return render_template('admin.html', suggestions=suggestions)

    @app.route('/admin/approve/<int:suggestion_id>')
    @login_required
    def approve_suggestion(suggestion_id: int) -> str:
        """Publish a suggestion: move it into the main tables and remove it."""
        db = get_db()
        suggestion = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        if suggestion is None:
            flash('Suggestion introuvable.', 'error')
            return redirect(url_for('admin_dashboard'))
        import json
        # Insert the site
        db.execute(
            '''INSERT INTO sites (name, url, category, description, verification_type, context, date_in_effect, status, country, sources)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                suggestion['name'], suggestion['url'], suggestion['category'], suggestion['description'],
                suggestion['verification_type'], '', '', '', suggestion['country'], ''
            )
        )
        site_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        # Insert alternatives
        alts = json.loads(suggestion['alternatives_json']) if suggestion['alternatives_json'] else []
        for alt in alts:
            db.execute(
                '''INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description)
                   VALUES (?, ?, ?, ?)''',
                (site_id, alt['name'], alt['url'], alt.get('description', ''))
            )
        # Delete suggestion
        db.execute('DELETE FROM suggestions WHERE id=?', (suggestion_id,))
        db.commit()
        flash('Suggestion approuvée et ajoutée à la base.', 'success')
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/delete/<int:suggestion_id>')
    @login_required
    def delete_suggestion(suggestion_id: int) -> str:
        """Discard a suggestion without publishing it."""
        db = get_db()
        db.execute('DELETE FROM suggestions WHERE id=?', (suggestion_id,))
        db.commit()
        flash('Suggestion supprimée.', 'success')
        return redirect(url_for('admin_dashboard'))

    # Return the configured app instance
    return app


if __name__ == '__main__':
    # When executed via `python app.py` a development server is started.
    # The environment variable FLASK_ENV=development enables live reload and
    # debug mode.  In production use a WSGI server such as gunicorn to run
    # the application instead of the built‑in development server.
    app = create_app()
    # Binding to 0.0.0.0 makes the app accessible on all network interfaces.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)