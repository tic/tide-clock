import math
from datetime import datetime
from tide_clock.tides import Tide, interpolate_tide_height

def generate_display_image(last_tide: Tide, next_tide: Tide, later_tide: Tide):
  current_height = interpolate_tide_height(last_tide, next_tide, datetime.now())
  portion_of_max = math.fabs(current_height / (last_tide.height - next_tide.height))

  height_str = "{:.3f}'".format(current_height)
  pct_str = '{:.2%}'.format(portion_of_max)

def display(image):
  pass
