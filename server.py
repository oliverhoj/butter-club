"""Butter Club: dependency-free web server and shared reservation storage."""
import argparse
import csv
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = Path(os.environ.get('DATABASE_PATH', str(ROOT / 'data' / 'reservations.sqlite3')))

def connect():
    return sqlite3.connect(DB, timeout=10)

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/api/reservations':
            return self.reply(404, {'error': 'Siden findes ikke.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 4096:
                raise ValueError('Beskeden er for lang eller tom.')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('Ugyldig bestilling.')
            name, note, time, booking_id = (data.get(k, '') for k in ('name', 'note', 'time', 'id'))
            guests = data.get('guests')
            if not all(isinstance(v, str) for v in (name, note, time, booking_id)):
                raise ValueError('Ugyldig bestilling.')
            name, note = name.strip(), note.strip()
            if not 1 <= len(name) <= 70 or len(note) > 500:
                raise ValueError('Skriv et navn på højst 70 tegn og en besked på højst 500 tegn.')
            if type(guests) is not int or not 1 <= guests <= 6:
                raise ValueError('Vælg mellem 1 og 6 personer.')
            if not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', time) or not '16:00' <= time <= '23:30':
                raise ValueError('Vælg et tidspunkt mellem 16.00 og 23.30.')
            if not re.fullmatch(r'[a-f0-9-]{36}', booking_id):
                raise ValueError('Ugyldigt reservationsnummer. Opdater siden og prøv igen.')
            with connect() as db:
                existing = db.execute('SELECT name, guests, time, note FROM reservations WHERE id = ?', (booking_id,)).fetchone()
                if existing and existing != (name, guests, time, note):
                    raise ValueError('Reservationsnummeret er allerede brugt. Opdater siden.')
                if not existing:
                    db.execute('INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?)', (booking_id, name, guests, time, note, datetime.now(timezone.utc).isoformat()))
            self.reply(200 if existing else 201, {'saved': True, 'id': booking_id})
        except (ValueError, TypeError, UnicodeError) as error:
            self.reply(400, {'error': str(error)})
        except sqlite3.Error:
            self.reply(503, {'error': 'Køkkenets gæsteliste er midlertidigt utilgængelig. Prøv igen.'})

    def reply(self, status, value):
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def list_directory(self, path):
        self.send_error(404)

def main():
    parser = argparse.ArgumentParser(description='Butter Club — middag med vennerne')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', '8000')))
    parser.add_argument('--host', default=os.environ.get('HOST', '127.0.0.1'))
    parser.add_argument('--list', action='store_true', help='Vis gæstelisten i terminalen')
    parser.add_argument('--export', action='store_true', help='Eksporter gæstelisten som CSV')
    args = parser.parse_args()
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS reservations (id TEXT PRIMARY KEY, name TEXT NOT NULL, guests INTEGER NOT NULL, time TEXT NOT NULL, note TEXT NOT NULL, created_at TEXT NOT NULL)')
        if args.list or args.export:
            rows = db.execute('SELECT name, guests, time, note FROM reservations ORDER BY time, created_at').fetchall()
            if args.export:
                target = ROOT / 'gaesteliste.csv'
                with target.open('w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Navn', 'Personer', 'Tidspunkt', 'Besked'])
                    # Avoid spreadsheet formula execution from visitor-entered text.
                    writer.writerows([["'" + v if isinstance(v, str) and v.lstrip().startswith(('=', '+', '-', '@')) else v for v in row] for row in rows])
                print('Gæsteliste gemt:', target)
            else:
                for name, guests, time, note in rows:
                    print(f'{time} · {name} · {guests} person(er)' + (f' · {note}' if note else ''))
                print(f'\nI alt: {sum(row[1] for row in rows)} gæster / {len(rows)} reservationer')
            return
    server = ThreadingHTTPServer((args.host, args.port), partial(Handler, directory=str(ROOT / 'public')))
    print(f'Butter Club er åben: http://{args.host}:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
