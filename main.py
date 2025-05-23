#!/usr/bin/env python3
"""
main.py – Startet den Brownschen Pfad‑Simulator.

Standardverhalten:
    python main.py           → öffnet die Auswahl‑Seite (index.html)

Direkter Aufruf einer Geometrie:
    python main.py --annulus        # Ringgebiet direkt anzeigen
    python main.py --slit           # Schlitzscheibe direkt anzeigen

Oder ganz allgemein:
    python main.py --file annulus.html
"""

from __future__ import annotations
import argparse
import sys
import webbrowser
from pathlib import Path


def open_html(html_file: str | Path):
    path = Path(html_file).expanduser().resolve()
    if not path.exists():
        sys.exit(f"Fehler: {path} nicht gefunden.")
    webbrowser.open(path.as_uri())
    print(f"Browser geöffnet → {path.name}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Öffnet die Brownian-HTML-Oberfläche.")
    g = p.add_mutually_exclusive_group()
    g.add_argument('--annulus', action='store_true', help='Annulus direkt öffnen')
    g.add_argument('--slit',    action='store_true', help='Schlitzscheibe direkt öffnen')
    p.add_argument('--file', '-f', default=None, help='Beliebige HTML-Datei öffnen')
    return p.parse_args()


def main():
    args = parse_args()
    base = Path(__file__).resolve().parent

    if args.file:
        target = Path(args.file)
    elif args.annulus:
        target = base / 'annulus.html'
    elif args.slit:
        target = base / 'slit_disc.html'
    else:
        target = base / 'index.html'   # Auswahl‑Seite

    open_html(target)


if __name__ == '__main__':
    main()
