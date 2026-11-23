from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

import calculations
import database
from models import Reading, ReadingCreate, Summary


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(title="Zählerstand-Tracker", lifespan=lifespan)


@app.get("/api/readings", response_model=list[Reading])
def list_readings():
    return database.get_all_readings()


@app.post("/api/readings", response_model=Reading, status_code=201)
def create_reading(reading: ReadingCreate):
    if reading.reading_date > date.today():
        raise HTTPException(status_code=400, detail="Das Datum darf nicht in der Zukunft liegen.")

    for existing in database.get_all_readings():
        if existing.reading_date == reading.reading_date:
            raise HTTPException(status_code=409, detail="Für diesen Tag gibt es bereits einen Zählerstand.")
        if existing.reading_date < reading.reading_date and existing.value_kwh > reading.value_kwh:
            raise HTTPException(
                status_code=400,
                detail=f"Der Zählerstand ist kleiner als am {existing.reading_date:%d.%m.%Y} "
                       f"({existing.value_kwh:g} kWh).",
            )
        if existing.reading_date > reading.reading_date and existing.value_kwh < reading.value_kwh:
            raise HTTPException(
                status_code=400,
                detail=f"Der Zählerstand ist größer als am späteren {existing.reading_date:%d.%m.%Y} "
                       f"({existing.value_kwh:g} kWh).",
            )

    return database.add_reading(reading.reading_date.isoformat(), reading.value_kwh)


@app.delete("/api/readings/{reading_id}", status_code=204)
def remove_reading(reading_id: int):
    if not database.delete_reading(reading_id):
        raise HTTPException(status_code=404, detail=f"Zählerstand mit ID {reading_id} nicht gefunden.")


@app.get("/api/summary", response_model=Summary)
def get_summary(
    price_ct: float = Query(35.0, gt=0, description="Arbeitspreis in Cent pro kWh"),
    base_fee: float = Query(12.0, ge=0, description="Grundpreis in Euro pro Monat"),
):
    readings = database.get_all_readings()
    try:
        per_day = calculations.average_daily_consumption(readings)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    forecast_kwh = per_day * calculations.DAYS_PER_YEAR
    cost = calculations.yearly_cost(forecast_kwh, price_ct, base_fee)

    return Summary(
        readings_count=len(readings),
        period_days=(readings[-1].reading_date - readings[0].reading_date).days,
        consumption_kwh=round(readings[-1].value_kwh - readings[0].value_kwh, 1),
        average_per_day_kwh=round(per_day, 2),
        forecast_year_kwh=round(forecast_kwh),
        forecast_year_cost_eur=round(cost, 2),
        monthly_advance_eur=calculations.monthly_advance(cost),
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
