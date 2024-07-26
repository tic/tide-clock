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

  img = Image.new("P", (250, 122), 'white')
  draw = ImageDraw.Draw(img)

  # Relative height bar
  draw.line([(20, 0), (20, 122)], 'black', 4)
  draw.rectangle([(0, 122 - round(122 * portion_of_max)), (18, 122)], 'red')
  draw.line([(1, 0), (1, 122)], 'black', 4)

  # Vertical text is hard :(
  # htext = Image.new("L", (122, 122), 'white')
  # ImageDraw.Draw(htext).text((0,0), pct_str, 'black', font_size=18)
  # vtext = htext.rotate(90).crop((0, 0, 20, 122))
  # vtext.show()
  # img.paste(vtext)

  # Last updated timestamp
  draw.text((90, 109), 'Updated', 'black')
  draw.text((140, 109), datetime.now().strftime('%Y-%m-%dT%X'), 'red')

  # Min and max heights
  [min_h, max_h] = sorted([last_tide.height, next_tide.height])
  is_tide_rising = min_h == last_tide.height
  draw.text((25, 105), "{:.3f}'".format(min_h), 'red' if is_tide_rising else 'black', font_size=14)
  draw.text((25, 0), "{:.3f}'".format(max_h), 'black' if is_tide_rising else 'red', font_size=14)

  # Tides
  draw.text((55, 25), get_simple_tide_string(last_tide), 'black', font_size=20)
  draw.text((55, 50), get_simple_tide_string(next_tide), 'black', font_size=20)
  draw.text((55, 75), get_simple_tide_string(later_tide), 'black', font_size=20)

  # Dividers
  draw.line([(22, 21), (250, 21)], 'black', 4)
  draw.line([(22, 102), (250, 102)], 'black', 4)

  return img

def display(img):
  pass
  # inky_display = InkyPHAT("red")
  # inky_display.set_border(inky_display.WHITE)
  # inky_display.set_image(img)
  # inky_display.show()
