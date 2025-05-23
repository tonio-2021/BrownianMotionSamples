# Brownscher Pfad‑Simulator

Dieses kleine Projekt demonstriert Brownsche Bewegung in zwei 2‑D‑Gebieten:

* **Annulus** – Ringfläche zwischen zwei konzentrischen Kreisen
* **Schlitzscheibe** – Kreis mit radialem Schlitz (wie von einer Nadel
  durchstochen)

Die Simulation läuft komplett in JavaScript.  Python wird lediglich genutzt,
um die gewünschte HTML‑Datei bequem im Standard­browser zu öffnen.

---

\## Dateiübersicht

| Datei            | Zweck                                                                      |
| ---------------- | -------------------------------------------------------------------------- |
| `main.py`        | Startskript – öffnet `index.html` oder direkt eine Simulations­seite.      |
| `index.html`     | Auswahl­seite mit Buttons *Annulus* / *Schlitzscheibe*.                    |
| `annulus.html`   | Simulation im Ringgebiet; Startpunkt per Drag‑and‑Drop; Multiplikator etc. |
| `slit_disc.html` | Simulation in der Schlitzscheibe; zusätzlicher Regler für Schlitzbreite.   |
| `README.md`      | Diese Anleitung.                                                           |

---

\## Installation

Es reicht eine Python‑Standard­installation ≥ 3.8.  Externe Pakete sind nicht
nötig.

```bash
# (optional) virtuelle Umgebung anlegen
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

---

\## Schnellstart

```bash
# 1 – Auswahl­seite öffnen (Empfehlung)
python main.py

# 2 – Direkt das Ringgebiet starten
python main.py --annulus

# 3 – Direkt die Schlitzscheibe starten
python main.py --slit

# 4 – Beliebige HTML‑Datei öffnen
python main.py --file annulus.html
```

---

\## Bedienelemente

| Element                               | Funktion                                    |
| ------------------------------------- | ------------------------------------------- |
| **Multiplikator‑Button**              | 1× / 3× / 5× / 10× / 100× Pfade pro Klick   |
| **Neue Pfade**                        | Startet sofort die angegebene Anzahl Pfade  |
| **Pfade aus‑/einblenden**             | Versteckt oder zeigt Pfadverläufe           |
| **Reset**                             | Löscht alle Pfade                           |
| **Startpunkt (grüner Punkt)**         | Per Maus frei im Gebiet verschiebbar        |
| **Schlitz‑Regler** *(Schlitzscheibe)* | Schlitzbreite von 2 px bis 40 px einstellen |

---

\## Anpassungen & Erweiterungen

* **Farben / Canvas‑Größe** – direkt in den HTML‑Dateien anpassen.
* **Gebiets­geometrie** – Funktion `inDomain()` anpassen oder ersetzen.
* **Simulations­parameter** – `STEP_SCALE`, `MAX_STEPS` etc. im Skript ändern.

---

\## Lizenz

MIT License – nutze und modifiziere das Projekt nach Belieben.
