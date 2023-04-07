import datetime
import lunardate

def convert(date_str):
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
    lunar_date = lunardate.LunarDate.fromSolarDate(date_obj.year, date_obj.month, date_obj.day)
    return '{}/{}/{}'.format(lunar_date.day, lunar_date.month, lunar_date.year)