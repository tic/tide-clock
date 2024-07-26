from os import getenv
from dotenv import load_dotenv

load_dotenv()

missing_keys = []

def env(key: str, default='') -> str:
  try:
    value = getenv(key)
    if value is None:
      raise KeyError
    return value
  except KeyError:
    missing_keys.append(key)
    return default

def get_config():
  try:
    return {
      'station_id': env('TIDE_CLOCK_STATION_ID'),
    }
  finally:
    if len(missing_keys) > 0:
      print('[WARN] project was launched with missing environment variables:')
      print('       -', '\n       - '.join(missing_keys))
