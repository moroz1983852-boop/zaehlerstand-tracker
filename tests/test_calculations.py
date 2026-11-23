from datetime import date

import pytest

from calculations import average_daily_consumption, monthly_advance, yearly_cost
from models import Reading


def reading(day: date, value: float) -> Reading:
    return Reading(id=0, reading_date=day, value_kwh=value)


def test_durchschnitt_pro_tag():
    readings = [reading(date(2026, 1, 1), 1000), reading(date(2026, 1, 11), 1080)]
    assert average_daily_consumption(readings) == 8.0


def test_mindestens_zwei_zaehlerstaende_noetig():
    with pytest.raises(ValueError):
        average_daily_consumption([reading(date(2026, 1, 1), 1000)])


def test_jahreskosten_mit_grundpreis():
    assert yearly_cost(2500, 30, 10) == 870.0


def test_abschlag_wird_aufgerundet():
    assert monthly_advance(870.0) == 73
