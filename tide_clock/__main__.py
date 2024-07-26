from datetime import datetime
from tide_clock.config.config import get_config
from tide_clock.tides import get_tide_data, find_bounding_tides
from tide_clock.display import generate_display_image, display

def main():
  config = get_config()

  print('Loading tide data...')
  tides = get_tide_data(config['station_id'])
  print(f'Retrieved {len(tides)} tides!')

  [last_tide, next_tide, index_b] = find_bounding_tides(tides, datetime.now())
  image = generate_display_image(last_tide, next_tide, tides[index_b + 1])
  display(image)

if __name__ == '__main__':
  main()
