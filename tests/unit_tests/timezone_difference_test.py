from app.helpers import get_timezone_difference_hours

import pytz
import pytest
from datetime import datetime

def test_valid_timezones_positive_difference():
    result = get_timezone_difference_hours("America/New_York", "Europe/London")
    assert result == "+5.0"

def test_valid_timezones_negative_difference():
    result = get_timezone_difference_hours("Asia/Tokyo", "America/Los_Angeles")
    assert result == "-17.0"

def test_invalid_timezone():
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        get_timezone_difference_hours("Invalid/Timezone", "Europe/Paris")

def test_valid_timezones_same_offset():
    result = get_timezone_difference_hours("Europe/Moscow", "Europe/Moscow")
    assert result == "Same timezone"

def test_valid_timezones_different_offset():
    result = get_timezone_difference_hours("America/Chicago", "Asia/Kolkata")
    assert result == "+11.0"

def test_valid_timezones_reversed_order():
    result = get_timezone_difference_hours("Europe/London", "America/New_York")
    assert result == "-5.0"

def test_valid_timezones_utc():
    result = get_timezone_difference_hours("UTC", "UTC")
    assert result == "Same timezone"

