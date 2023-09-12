import pytz
from datetime import datetime

def get_timezone_difference_hours(first_timezone, second_timezone):
    try:
        # Создаем объекты часовых поясов для первого и второго городов
        first_city_timezone = pytz.timezone(first_timezone)
        second_city_timezone = pytz.timezone(second_timezone)

        # Получаем смещение первого города относительно UTC в часах
        first_city_offset_hours = first_city_timezone.utcoffset(datetime.now()).total_seconds() // 3600

        # Получаем смещение второго города относительно UTC в часах
        second_city_offset_hours = second_city_timezone.utcoffset(datetime.now()).total_seconds() // 3600

        # Возвращаем разницу в формате "+X" или "-X"
        if first_city_offset_hours < second_city_offset_hours:
            return f"+{second_city_offset_hours - first_city_offset_hours}"
        else:
            return f"-{first_city_offset_hours - second_city_offset_hours}"
    
    except pytz.exceptions.UnknownTimeZoneError:
        return "Unknown timezone"
