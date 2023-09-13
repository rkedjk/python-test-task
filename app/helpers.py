# Function to calculate the time zone difference in hours between two cities

import pytz
from datetime import datetime

def get_timezone_difference_hours(first_timezone, second_timezone):
    """
    Calculate the time zone difference in hours between two cities.

    Args:
        first_timezone (str): Time zone of the first city.
        second_timezone (str): Time zone of the second city.

    Returns:
        str: Time zone difference in hours as a string in the format "+X" or "-X", or "Unknown timezone" if the
             provided time zone is invalid.

    This function takes two time zone names as input and calculates the time zone difference in hours between them.
    It creates timezone objects for both cities using the `pytz` library, obtains their offsets from UTC,
    and returns the difference as a string indicating the time zone offset. If an invalid time zone is provided,
    it returns "Unknown timezone".
    """
    try:
        # Create timezone objects for the first and second cities
        first_city_timezone = pytz.timezone(first_timezone)
        second_city_timezone = pytz.timezone(second_timezone)

        # Get the offset of the first city from UTC in hours
        first_city_offset_hours = first_city_timezone.utcoffset(datetime.now()).total_seconds() // 3600

        # Get the offset of the second city from UTC in hours
        second_city_offset_hours = second_city_timezone.utcoffset(datetime.now()).total_seconds() // 3600

        # Return the difference in the format "+X" or "-X"
        if first_city_offset_hours < second_city_offset_hours:
            return f"+{second_city_offset_hours - first_city_offset_hours}"
        else:
            return f"-{first_city_offset_hours - second_city_offset_hours}"

    except pytz.exceptions.UnknownTimeZoneError:
        return "Unknown timezone"
