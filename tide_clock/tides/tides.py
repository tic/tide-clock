from typing import TypedDict, List
from datetime import datetime, timezone, timedelta
import requests
import math

class TideResponse(TypedDict):
  t: str
  v: str
  type: str

class Tide:
  timestamp: int
  type: str
  height: float

  def __init__(self, raw_tide: TideResponse):
    self.type = raw_tide['type']
    self.height = float(raw_tide['v'])

    zoneless_dt = datetime.fromisoformat(raw_tide['t'])
    zoned_dt = datetime(
      year = zoneless_dt.year,
      month = zoneless_dt.month,
      day = zoneless_dt.day,
      hour = zoneless_dt.hour,
      minute = zoneless_dt.minute,
      tzinfo=timezone.utc
    )

    self.timestamp = int(zoned_dt.timestamp())

  def __str__(self):
    return f"{datetime.fromtimestamp(self.timestamp).strftime('%xT%X')} {'{:.3f}'.format(self.height)} {self.type}"

  def toJSON(self):
    return {
      'timestamp': self.timestamp,
      'height': self.height,
      'type': self.type,
    }

class InterpolationException(Exception):
  def __init__(self, message: str, range_start: int, range_end: int, requested: float) -> None:
    super().__init__(message)
    self.range_start = range_start
    self.range_end = range_end
    self.requested = requested

def get_tide_data(station_id: str, start_date: datetime = datetime.now(), end_date: datetime = datetime.now() + timedelta(days=1)) -> List[Tide]:
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

  return [Tide(prediction) for prediction in data['predictions']]

def interpolate_tide_height(tide_a: Tide, tide_b: Tide, date_input: datetime | int | float):
  # Always ensure tide A comes before tide B
  if tide_a.timestamp > tide_b.timestamp:
    tmp = tide_a
    tide_a = tide_b
    tide_b = tmp

  # Convert provided date to a number
  timestamp_input = date_input.timestamp() if isinstance(date_input, datetime) else date_input

  # Can't interpolate outside of the given data
  if timestamp_input > tide_b.timestamp or timestamp_input < tide_a.timestamp:
    raise InterpolationException(
      'cannot interpolate a time outside the range of provided data',
      tide_a.timestamp,
      tide_b.timestamp,
      timestamp_input,
    )

  # Between a given high and low tide, the height more or less follows a sine curve.
  # This function retrieves the height at a given time using a scaled cosine function.
  # Providing 0 gives the height of Tide A, and each additional x is 1 second later.
  get_height = lambda x: ((tide_a.height - tide_b.height) / 2) * math.cos(math.pi * x / (tide_b.timestamp - tide_a.timestamp)) + (tide_a.height + tide_b.height) / 2
  return get_height(timestamp_input - tide_a.timestamp)

def find_bounding_tides(tides: List[Tide], date_input: datetime | int | float):
  # Convert provided date to a number
  timestamp_input = date_input.timestamp() if isinstance(date_input, datetime) else date_input

  # Bounding tides requires at least 2 input tides
  if len(tides) < 2:
    return [None, None]

  # Provided timestamp must be between the first and last tide
  if tides[0].timestamp > timestamp_input or tides[-1].timestamp < timestamp_input:
    return [None, None]

  tide_a = tides[0]
  tide_b = None
  index_b = 1

  for tide in tides[1:]:
    if tide.timestamp > timestamp_input:
      tide_b = tide
      return [tide_a, tide_b, index_b]
    else:
      index_b += 1
      tide_a = tide

  return [None, None, None]
