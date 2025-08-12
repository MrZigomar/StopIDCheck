import os
import sqlite3
import json
from pathlib import Path
from flask import Flask, render_template, request, g, redirect, url_for, flash, session

# ---------------------------
# helpers DB path (absolu)
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'data' / 'sites.db'
JSON_PATH = BASE_DIR / 'data' / 'sites.json'


def create_app(test_config=None):
    """
    Flask app avec SQLite. Inclut suggestions utilisateur,
    interface admin, et synchronisation JSON -> DB.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key')
    app.config['DATABASE'] = str(DB_PATH)

    # Identifiants admin (à sécuriser en prod)
    app.config['ADMIN_USER'] = os.environ.get('ADMIN_USER', 'admin')
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'password')

    os.makedirs(BASE_DIR / 'data', exist_ok=True)

    # ------------- DB helpers -------------
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
            g.db.execute('PRAGMA foreign_keys = ON')
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db():
        """Crée les tables + index si besoin."""
        db = get_db()
        with db:
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
                    FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE
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
            # index d'unicité pour UPSERT
            db.execute('CREATE UNIQUE INDEX IF NOT EXISTS ux_sites_name ON sites(name)')
            db.execute('CREATE UNIQUE INDEX IF NOT EXISTS ux_alt_site_name ON alternatives(site_id, alt_name)')

    def _split_tags(val: str):
        return [x.strip() for x in (val or '').split(',') if x.strip()]

    def _normalize(value):
        """Convertit listes/dicts en string pour SQLite."""
        if isinstance(value, list):
            # liste → chaîne lisible
            return ', '.join(str(v) for v in value)
        if isinstance(value, dict):
            # dict → JSON
            return json.dumps(value, ensure_ascii=False)
        # laisse passer str / None / scalaires
        return value if (value is None or isinstance(value, str)) else str(value)

    # -----------------------------
    # SYNC JSON -> DB (UPSERT)
    # -----------------------------
    def sync_from_json(prune: bool = False):
        """
        Lis data/sites.json et met à jour la DB :
          - UPSERT des sites par name
          - UPSERT des alternatives par (site_id, alt_name)
          - prune=True : supprime ce qui n'est plus dans le JSON
        """
        db = get_db()
        if not JSON_PATH.exists():
            flash("Fichier data/sites.json introuvable", "danger")
            return

        with JSON_PATH.open(encoding='utf-8') as f:
            payload = json.load(f)

        sites = payload.get('sites', [])
        keep_site_names = set()

        with db:
            for s in sites:
                name = _normalize(s.get('name', '')).strip()
                if not name:
                    continue

                url = _normalize(s.get('url', '')).strip()

                # le JSON peut contenir list ou string
                category = _normalize(s.get('category', ''))
                country  = _normalize(s.get('country', ''))

                description       = _normalize(s.get('description', ''))
                verification_type = _normalize(s.get('verification_type', ''))
                context           = _normalize(s.get('context', ''))
                date_in_effect    = _normalize(s.get('date_in_effect') or s.get('date_effective') or '')
                status            = _normalize(s.get('status', ''))
                sources           = _normalize(s.get('sources', ''))


                # UPSERT site (par name)
                db.execute("""
                    INSERT INTO sites (name, url, category, description, verification_type, context, date_in_effect, status, country, sources)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                      url=excluded.url,
                      category=excluded.category,
                      description=excluded.description,
                      verification_type=excluded.verification_type,
                      context=excluded.context,
                      date_in_effect=excluded.date_in_effect,
                      status=excluded.status,
                      country=excluded.country,
                      sources=excluded.sources
                """, (name, url, category, description, verification_type, context, date_in_effect, status, country, sources))

                site_id = db.execute("SELECT id FROM sites WHERE name=?", (name,)).fetchone()['id']

                # Alternatives
                keep_alt_names = set()
                for alt in (s.get('alternatives') or []):
                    alt_name = _normalize(alt.get('name', '')).strip()
                    if not alt_name:
                        continue
                    alt_url = _normalize(alt.get('url', '')).strip()
                    alt_desc = _normalize(alt.get('description', ''))
                    db.execute("""
                        INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(site_id, alt_name) DO UPDATE SET
                          alt_url=excluded.alt_url,
                          alt_description=excluded.alt_description
                    """, (site_id, alt_name, alt_url, alt_desc))


                # prune alts absentes
                if prune:
                    if keep_alt_names:
                        placeholders = ','.join('?' * len(keep_alt_names))
                        db.execute(f"DELETE FROM alternatives WHERE site_id=? AND alt_name NOT IN ({placeholders})",
                                   (site_id, *keep_alt_names))
                    else:
                        db.execute("DELETE FROM alternatives WHERE site_id=?", (site_id,))

            # prune sites absents
            if prune:
                if keep_site_names:
                    placeholders = ','.join('?' * len(keep_site_names))
                    # supprimer d'abord alternatives orphelines
                    db.execute(f"DELETE FROM alternatives WHERE site_id IN (SELECT id FROM sites WHERE name NOT IN ({placeholders}))",
                               tuple(keep_site_names))
                    db.execute(f"DELETE FROM sites WHERE name NOT IN ({placeholders})", tuple(keep_site_names))
                else:
                    db.execute("DELETE FROM alternatives")
                    db.execute("DELETE FROM sites")

    # initialisation tables puis synchro
    with app.app_context():
        init_db()
        # au lancement, on synchronise (pas de prune par défaut)
        try:
            sync_from_json(prune=False)
        except Exception as e:
            # ne pas bloquer le démarrage si JSON absent
            print(f"[sync] skipped: {e}")

    # exposer get_db pour tests
    app.get_db = get_db
    app.sync_from_json = sync_from_json

    # ------------- ROUTES -------------
    @app.route('/')
    def index():
        db = get_db()
        # derniers sites
        rows = db.execute('SELECT * FROM sites ORDER BY id DESC LIMIT 4').fetchall()
        recent_sites = []
        for r in rows:
            d = dict(r)
            d['categories'] = _split_tags(d.get('category', ''))
            d['countries'] = _split_tags(d.get('country', ''))
            recent_sites.append(d)

        # tags dynamiques
        cats, ctys = set(), set()
        for r in db.execute('SELECT category, country FROM sites'):
            cats.update(_split_tags(r['category']))
            ctys.update(_split_tags(r['country']))

        return render_template('index.html',
                               categories=sorted(cats),
                               countries=sorted(ctys),
                               recent_sites=recent_sites)

    @app.route('/sites')
    def sites():
        db = get_db()
        q = (request.args.get('q') or '').strip().lower()
        category = (request.args.get('category') or '').strip()
        country = (request.args.get('country') or '').strip()

        query = 'SELECT * FROM sites WHERE 1=1'
        params = []
        if q:
            query += ' AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)'
            params += [f'%{q}%', f'%{q}%']
        if category:
            query += ' AND category LIKE ?'
            params.append(f'%{category}%')
        if country:
            query += ' AND country LIKE ?'
            params.append(f'%{country}%')
        query += ' ORDER BY name COLLATE NOCASE ASC'

        rows = db.execute(query, params).fetchall()
        sites_list = []
        for r in rows:
            d = dict(r)
            d['categories'] = _split_tags(d.get('category', ''))
            d['countries'] = _split_tags(d.get('country', ''))
            sites_list.append(d)

        # tags dynamiques
        cats, ctys = set(), set()
        for r in db.execute('SELECT category, country FROM sites'):
            cats.update(_split_tags(r['category']))
            ctys.update(_split_tags(r['country']))

        return render_template('sites.html',
                               sites=sites_list,
                               categories=sorted(cats),
                               countries=sorted(ctys),
                               selected_category=category,
                               selected_country=country,
                               q=q)

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

    # --------- Suggestions utilisateur ---------
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
            alternatives = []
            if alternatives_text:
                for line in alternatives_text.splitlines():
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 2:
                        alt_desc = parts[2] if len(parts) > 2 else ''
                        alternatives.append({'name': parts[0], 'url': parts[1], 'description': alt_desc})
            db = get_db()
            db.execute(
                'INSERT INTO suggestions (name, url, category, verification_type, country, description, alternatives_json) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, url_field, category, verification_type, country, description, json.dumps(alternatives))
            )
            db.commit()
            flash('Merci, votre suggestion a été soumise pour validation par un administrateur.', 'success')
            return redirect(url_for('suggest'))
        return render_template('suggest.html')

    # -------------- Admin --------------
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

    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        db = get_db()
        rows = db.execute('SELECT * FROM suggestions ORDER BY submitted_at DESC').fetchall()
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

    @app.route('/admin/suggestion/<int:sug_id>/<action>', methods=['POST'])
    @admin_required
    def admin_suggestion_action(sug_id, action):
        db = get_db()
        sug = db.execute('SELECT * FROM suggestions WHERE id = ?', (sug_id,)).fetchone()
        if not sug:
            flash('Suggestion introuvable.', 'danger')
            return redirect(url_for('admin_dashboard'))
        if action == 'accept':
            cur = db.execute(
                'INSERT INTO sites (name, url, category, description, verification_type, context, date_in_effect, status, country, sources) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (sug['name'], sug['url'], sug['category'], sug['description'], sug['verification_type'], '', '', 'En attente de précisions', sug['country'], '')
            )
            site_id = cur.lastrowid
            alts = json.loads(sug['alternatives_json']) if sug['alternatives_json'] else []
            for alt in alts:
                db.execute('INSERT INTO alternatives (site_id, alt_name, alt_url, alt_description) VALUES (?, ?, ?, ?)',
                           (site_id, alt.get('name'), alt.get('url'), alt.get('description')))
            db.commit()
            flash('Suggestion acceptée et ajoutée à la base.', 'success')
        elif action == 'reject':
            flash('Suggestion rejetée.', 'warning')
        db.execute('DELETE FROM suggestions WHERE id = ?', (sug_id,))
        db.commit()
        return redirect(url_for('admin_dashboard'))

    # ----------- Sync via Admin -----------
    @app.route('/admin/sync', methods=['POST'])
    @admin_required
    def admin_sync():
        prune = bool(request.form.get('prune'))
        try:
            sync_from_json(prune=prune)
            flash("Base synchronisée depuis sites.json" + (" (avec purge)" if prune else ""), "success")
        except Exception as e:
            flash(f"Synchronisation impossible : {e}", "danger")
        return redirect(url_for('admin_dashboard'))

    # ----------- CLI -----------
    @app.cli.command("sync-db")
    def cli_sync_db():
        """Synchronise la DB depuis data/sites.json (UPSERT)."""
        with app.app_context():
            sync_from_json(prune=False)
        print("[db] synced from data/sites.json")

    return app


if __name__ == '__main__':
    app = create_app()
    print(f"[db] using {DB_PATH}")
    app.run(debug=True, host='0.0.0.0', port=5000)
