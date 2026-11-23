import math

from models import Reading

DAYS_PER_YEAR = 365


def average_daily_consumption(readings: list[Reading]) -> float:
    if len(readings) < 2:
        raise ValueError("Für eine Berechnung werden mindestens zwei Zählerstände benötigt.")

    first, last = readings[0], readings[-1]
    days = (last.reading_date - first.reading_date).days
    if days <= 0:
        raise ValueError("Die Zählerstände müssen an verschiedenen Tagen erfasst sein.")

    return (last.value_kwh - first.value_kwh) / days


def yearly_cost(kwh: float, price_ct_per_kwh: float, base_fee_eur_per_month: float) -> float:
    return kwh * price_ct_per_kwh / 100 + 12 * base_fee_eur_per_month


def monthly_advance(yearly_cost_eur: float) -> int:
    return math.ceil(yearly_cost_eur / 12)
