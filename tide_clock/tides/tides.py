from datetime import datetime, timezone, timedelta
import requests

def format_tide(tide):
  zoneless_dt = datetime.fromisoformat(tide['t'])
  zoned_dt = datetime(
    year = zoneless_dt.year,
    month = zoneless_dt.month,
    day = zoneless_dt.day,
    hour = zoneless_dt.hour,
    minute = zoneless_dt.minute,
    tzinfo=timezone.utc
  )

  return {
    'timestamp': int(zoned_dt.timestamp()),
    'height': float(tide['v']),
    'type': tide['type']
  }

def get_tide_data(station_id: str, start_date: datetime = datetime.now(), end_date: datetime = datetime.now() + timedelta(days=1)):
  querystring_args = {
    'begin_date': start_date.strftime('%Y%m%d'),
    'end_date': end_date.strftime('%Y%m%d'),
    'product': 'predictions',
    'time_zone': 'gmt', # valid options: ['gmt', 'lst', 'lst_ldt'] (local standard time / local daylight time)
    'station': station_id,
    'interval': 'hilo',
    'units': 'english',
    'format': 'json',
    'datum': 'MLLW',
  }

  response = requests.get('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter', querystring_args)
  data = response.json()
  tides = [format_tide(prediction) for prediction in data['predictions']]

  return tides
