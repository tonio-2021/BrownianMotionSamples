# brownian_plot.py
import webbrowser
import http.server
import socketserver
import threading
import os

# -----------------------------------------------------------------------------
# Dieses Skript startet einen lokalen HTTP-Server, der alle HTML-, JS- und CSS-
# Dateien im Verzeichnis ausliefert. Du kannst im Browser zwischen zwei
# Simulationen wählen:
#  - brownian_annulus.html        (Ringgebiet-Annulus)
#  - brownian_twocircles.html     (Zwei verbundene Kreise mit Gang)
#  - index.html                   (Auswahlseite mit Links zu beiden)
#
# Der Server öffnet automatisch index.html im Standardbrowser.
# -----------------------------------------------------------------------------

PORT = 8000
# Verzeichnis, in dem sich diese Datei und die HTML-Assets befinden
HTML_DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML_DIR, **kwargs)


def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"Server läuft unter: {url}")
        # Öffne den Browser nach kurzer Verzögerung
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server wird gestoppt...")
            httpd.server_close()


if __name__ == '__main__':
    start_server()
