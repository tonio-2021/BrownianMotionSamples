#!/usr/bin/env python3
"""
main.py – Startet die interaktive Brownian-Motion-Web-App.

Funktionen
----------
* Sucht (standardmäßig) nach »index2.html« im selben Verzeichnis wie main.py.
* Öffnet diese Datei im Standard-Webbrowser.
* Optional kannst du über --file eine andere HTML-Datei angeben.

Aufruf
------
    python main.py                 # öffnet index2.html
    python main.py --file demo.html

Abhängigkeit
------------
Nur das Standard-Python-Modul »webbrowser« (keine externen Pakete).
"""

from __future__ import annotations

import argparse
import sys
import webbrowser
from pathlib import Path


def open_html(html_path: Path) -> None:
    """Öffnet die übergebene HTML-Datei im Standardbrowser."""
    if not html_path.exists():
        sys.exit(f"Fehler: {html_path} nicht gefunden.")

    webbrowser.open(html_path.as_uri())
    print(f"Browser geöffnet → {html_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Öffnet die Browian-HTML-Oberfläche.")
    parser.add_argument(
        "--file",
        "-f",
        dest="file",
        default="index2.html",
        help="HTML-Datei, die geöffnet werden soll (Standard: index2.html)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    html_path = (base_dir / args.file).resolve()
    open_html(html_path)


if __name__ == "__main__":
    main()
