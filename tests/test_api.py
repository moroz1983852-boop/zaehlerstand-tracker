def test_zaehlerstand_speichern_und_auflisten(client):
    response = client.post("/api/readings", json={"reading_date": "2026-01-01", "value_kwh": 1000})
    assert response.status_code == 201

    readings = client.get("/api/readings").json()
    assert len(readings) == 1
    assert readings[0]["value_kwh"] == 1000


def test_zaehlerstand_darf_nicht_sinken(client):
    client.post("/api/readings", json={"reading_date": "2026-01-01", "value_kwh": 1000})
    response = client.post("/api/readings", json={"reading_date": "2026-02-01", "value_kwh": 900})

    assert response.status_code == 400
    assert "kleiner" in response.json()["detail"]


def test_doppeltes_datum_wird_abgelehnt(client):
    client.post("/api/readings", json={"reading_date": "2026-01-01", "value_kwh": 1000})
    response = client.post("/api/readings", json={"reading_date": "2026-01-01", "value_kwh": 1010})

    assert response.status_code == 409


def test_auswertung_berechnet_abschlag(client):
    client.post("/api/readings", json={"reading_date": "2026-01-01", "value_kwh": 1000})
    client.post("/api/readings", json={"reading_date": "2026-01-11", "value_kwh": 1080})

    summary = client.get("/api/summary", params={"price_ct": 30, "base_fee": 10}).json()

    assert summary["average_per_day_kwh"] == 8.0
    assert summary["forecast_year_kwh"] == 2920
    assert summary["monthly_advance_eur"] == 83


def test_auswertung_ohne_daten_liefert_fehler(client):
    response = client.get("/api/summary")
    assert response.status_code == 400


def test_loeschen_unbekannter_id_liefert_404(client):
    assert client.delete("/api/readings/99").status_code == 404
