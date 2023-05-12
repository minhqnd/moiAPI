import datetime
import lunardate


def convert(date_str):
    """

    Converts a given Gregorian date string to Lunar date string.

    Args:
        date_str (str): A string representing date in "DD/MM/YYYY" format.

    Returns:
        str: A string representing date in Lunar calendar format "DD/MM/YYYY".

    """
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
    lunar_date = lunardate.LunarDate.fromSolarDate(
        date_obj.year, date_obj.month, date_obj.day
    )
    return "{}/{}/{}".format(lunar_date.day, lunar_date.month, lunar_date.year)
