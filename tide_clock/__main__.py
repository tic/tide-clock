from tide_clock.config.config import get_config
from tide_clock.tides.tides import get_tide_data
from tide_clock.utilities.print import print_json

def main():
  config = get_config()
  tides = get_tide_data(config['station_id'])
  print_json(tides)

if __name__ == '__main__':
  main()
