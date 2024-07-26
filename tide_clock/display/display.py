import math
from datetime import datetime
from PIL import Image, ImageDraw
# from inky import InkyPHAT
from tide_clock.tides import Tide, interpolate_tide_height

def get_simple_tide_string(tide: Tide):
  type = 'HI' if tide.type == 'H' else 'LO'
  time = datetime.fromtimestamp(tide.timestamp).strftime('%H:%M')
  height = "{:.3f}'".format(tide.height)
  return f'{time}    {type}    {height}'

def generate_display_image(last_tide: Tide, next_tide: Tide, later_tide: Tide):
  current_height = interpolate_tide_height(last_tide, next_tide, datetime.now())
  portion_of_max = math.fabs(current_height / (last_tide.height - next_tide.height))

  height_str = "{:.3f}'".format(current_height)
  pct_str = '{:.2%}'.format(portion_of_max)

  img = Image.new("P", (212, 104), 'white')
  draw = ImageDraw.Draw(img)

  # Relative height bar
  draw.line([(19, 0), (19, 104)], 'black', 2)
  draw.rectangle([(0, 104 - round(104 * portion_of_max)), (18, 104)], 'red')
  draw.line([(0, 0), (0, 104)], 'black', 2)
  print(pct_str)
  # Vertical text is hard :(
  # htext = Image.new("L", (104, 104), 'white')
  # ImageDraw.Draw(htext).text((0,0), pct_str, 'black', font_size=18)
  # vtext = htext.rotate(90).crop((0, 0, 20, 104))
  # vtext.show()
  # img.paste(vtext)

  # Last updated timestamp
  draw.text((75, 89), 'As of', 'black')
  draw.text((104, 89), datetime.now().strftime('%Y-%m-%dT%X'), 'red')

  # Min and max heights
  [min_h, max_h] = sorted([last_tide.height, next_tide.height])
  is_tide_rising = min_h == last_tide.height
  draw.text((24, 86), "{:.3f}'".format(min_h), 'black' if is_tide_rising else 'red', font_size=14)
  draw.text((24, 0), "{:.3f}'".format(max_h), 'red' if is_tide_rising else 'black', font_size=14)

  # Tides
  draw.text((55, 22), get_simple_tide_string(last_tide), 'black', font_size=15)
  draw.text((55, 42), get_simple_tide_string(next_tide), 'black', font_size=15)
  draw.text((55, 62), get_simple_tide_string(later_tide), 'black', font_size=15)

  # Dividers
  draw.line([(21, 18), (212, 18)], 'black', 2)
  draw.line([(21, 84), (212, 84)], 'black', 2)

  return img

def display(img):
  img.show()
  # inky_display = InkyPHAT("red")
  # inky_display.set_border(inky_display.WHITE)
  # inky_display.set_image(img)
  # inky_display.show()
