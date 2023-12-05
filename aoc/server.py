from datetime import datetime, timezone, timedelta
import requests
from . import cache

url = 'http://adventofcode.com/2023'
tz = timezone(timedelta(hours = -5), 'EST')

def last_available_day():
    now = datetime.now(tz)
    if now.year < 2023 or (now.year == 2023 and now.month < 12):
        return 0
    if now.year == 2023 and now.month == 12 and now.day <= 25:
        return now.day
    return 25

@cache.cached('inputs/{session}/day{day}.txt')
def fetch_input(day, session):
    res = requests.get(f'{url}/day/{day}/input', cookies={ 'session': session })
    res.raise_for_status()
    return res.text
