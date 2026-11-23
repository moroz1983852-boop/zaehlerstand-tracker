# ⚡ Zählerstand-Tracker

Eine kleine Webanwendung zum Erfassen von Stromzählerständen. Aus den Zählerständen berechnet das Backend den Verbrauch, rechnet ihn auf ein Jahr hoch und empfiehlt einen passenden monatlichen Abschlag. So sieht man früh, ob am Jahresende eine Nachzahlung droht.

## 🛠 Technologiestack

* **Backend:** Python 3.12, FastAPI, Pydantic, Uvicorn
* **Datenbank:** SQLite (keine Installation nötig)
* **Tests:** pytest mit FastAPI TestClient (10 Tests)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

## 🚀 Funktionen

- 📝 **Zählerstände erfassen** mit Prüfung: kein Datum in der Zukunft, kein doppelter Tag, und ein Zähler kann nicht rückwärts laufen
- 📊 **Auswertung:** Verbrauch im Zeitraum, Durchschnitt pro Tag und Hochrechnung auf ein Jahr
- 💶 **Abschlagsempfehlung** auf Basis von Arbeitspreis und Grundpreis, aufgerundet auf volle Euro
- 🗑 **Löschen** falsch erfasster Werte
- 📖 **API-Dokumentation** automatisch unter `/docs`

## 💻 Installation & Start

```bash
git clone https://github.com/moroz1983852-boop/zaehlerstand-tracker.git
cd zaehlerstand-tracker

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload
```

Danach im Browser öffnen: http://localhost:8000

Tests ausführen:

```bash
pytest
```

## 🔌 API-Endpunkte

| Methode | Pfad | Beschreibung |
|---|---|---|
| `GET` | `/api/readings` | Alle Zählerstände, nach Datum sortiert |
| `POST` | `/api/readings` | Neuen Zählerstand speichern |
| `DELETE` | `/api/readings/{id}` | Zählerstand löschen |
| `GET` | `/api/summary?price_ct=35&base_fee=12` | Auswertung mit Hochrechnung und Abschlag |

Fehler werden mit passenden HTTP-Statuscodes beantwortet: `400` bei ungültigen Werten, `404` wenn eine ID nicht existiert und `409` bei einem doppelten Datum.

## 📁 Aufbau

| Datei | Aufgabe |
|---|---|
| `main.py` | API-Endpunkte und Prüfung der Eingaben |
| `database.py` | SQL-Zugriffe auf die SQLite-Datenbank |
| `calculations.py` | Berechnungen (Durchschnitt, Jahreskosten, Abschlag) ohne Datenbank |
| `models.py` | Pydantic-Modelle für Anfragen und Antworten |
| `static/` | Weboberfläche |
| `tests/` | Tests für Berechnungen und API |

Die Berechnungen liegen bewusst in einer eigenen Datei ohne Datenbankzugriff. Dadurch lassen sie sich direkt testen. Für die API-Tests bekommt jeder Test über die Umgebungsvariable `DB_PATH` eine eigene, leere Datenbank.
