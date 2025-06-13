#!/usr/bin/env python3
import os
import webbrowser
import sys

def open_index():
    # Ermittle den Pfad dieses Skripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Baue den Pfad zur index.html auf (im selben Verzeichnis)
    index_path = os.path.join(script_dir, "index.html")

    if not os.path.isfile(index_path):
        print(f"Fehler: '{index_path}' wurde nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    # Erstelle eine file://-URL für die index.html
    file_url = f"file://{index_path}"

    # Öffne die Datei im Standard-Webbrowser
    webbrowser.open(file_url)

if __name__ == "__main__":
    open_index()
