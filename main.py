# brownian_plot.py
import webbrowser
import http.server
import socketserver
import threading
import os

# -----------------------------------------------------------------------------
# Dieses Skript startet einen lokalen HTTP-Server, der die HTML-Datei mit der
# Brownschen Bewegung im Ringgebiet ausliefert. Anschließend öffnet es den
# Standardbrowser.
# -----------------------------------------------------------------------------

HTML_FILE = 'brownian_annulus.html'
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)


def start_server():
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f"Server läuft auf http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    # Starte HTTP-Server in eigenem Thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # öffne Browser
    url = f'http://localhost:{PORT}/{HTML_FILE}'
    webbrowser.open(url)

    # Keep main thread alive until KeyboardInterrupt
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("Beende Server...")
        exit(0)
