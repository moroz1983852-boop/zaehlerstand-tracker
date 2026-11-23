from datetime import date

from pydantic import BaseModel, Field


class ReadingCreate(BaseModel):
    reading_date: date
    value_kwh: float = Field(ge=0, description="Zählerstand in kWh")


class Reading(ReadingCreate):
    id: int


class Summary(BaseModel):
    readings_count: int
    period_days: int
    consumption_kwh: float
    average_per_day_kwh: float
    forecast_year_kwh: float
    forecast_year_cost_eur: float
    monthly_advance_eur: int
