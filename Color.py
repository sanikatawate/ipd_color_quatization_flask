from colorthief import ColorThief
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
import webcolors
from math import sqrt

import numpy as np
import pandas as pd

def closest_colour(requested_colour):
    differences = {}
    for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
        r, g, b = webcolors.hex_to_rgb(color_hex)
        rd = (r - requested_colour[0]) ** 2
        gd = (g - requested_colour[1]) ** 2
        bd = (b - requested_colour[2]) ** 2
        differences[sum([rd,gd,bd])] = color_name
    return differences[min(differences.keys())]

def get_colour_name(requested_colour):
    try:
        color_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        color_name = closest_colour(requested_colour)
    return color_name

color_names = [
    'black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue',
    'darkturquoise', 'mediumspringgreen', 'lime', 'springgreen', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen',
    'forestgreen', 'seagreen', 'darkslategray', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue',
    'darkslateblue', 'mediumturquoise', 'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'mediumaquamarine',
    'dimgray', 'slateblue', 'olivedrab', 'slategray', 'lightslategray', 'mediumslateblue', 'lawngreen', 'chartreuse',
    'aquamarine', 'maroon', 'purple', 'olive', 'gray', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta',
    'saddlebrown', 'darkseagreen', 'lightgreen', 'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen',
    'sienna', 'brown', 'darkgray', 'lightblue', 'greenyellow', 'paleturquoise', 'lightsteelblue', 'powderblue',
    'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 'mediumvioletred', 'indianred',
    'peru', 'chocolate', 'tan', 'lightgray', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 'crimson', 'gainsboro',
    'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki',
    'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon',
    'antiquewhite', 'linen', 'lightgoldenrodyellow', 'oldlace', 'red', 'magenta', 'deeppink', 'orangered', 'tomato',
    'hotpink', 'coral', 'darkorange', 'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite',
    'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 'papayawhip', 'lavenderblush', 'seashell', 'cornsilk',
    'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white'
]

color_dict = {
    'red': (255, 51, 52),
    'red-orange': (255, 144, 52),
    'orange': (255, 165, 0),
    'yellow-orange': (255, 219, 52),
    'yellow': (255, 255, 51),
    'yellow-green': (180, 241, 52),
    'green': (53, 213, 51),
    'blue-green': (52, 173, 174),
    'blue': (65, 102, 189),
    'blue-purple': (98, 67, 190),
    'purple': (142, 58, 188),
    'red-purple': (217, 49, 144)
}

rule_base = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: []}

color_centers = list(color_dict.values())

def get_distance(color1, color2):
    return sum([(c1-c2)**2 for c1, c2 in zip(color1, color2)])

def get_cluster(color):
    prev = np.inf
    cluster = 0
    count = 0
    for key, rgb_center in color_dict.items():
      curr = get_distance(rgb_center, color)
      if(prev > curr):
        cluster = count
        prev = curr
      count += 1
    return cluster

def get_rule_base():
    for color in color_names:
      cluster = get_cluster(webcolors.name_to_rgb(color))
      rule_base[cluster] = rule_base[cluster]+[color]
    return rule_base

rule_base = get_rule_base()


df = pd.read_csv("furniture.csv")

def suggest_color(color_arr):
    suggested_colors  = []
    for color in color_arr[:5]:
      cluster =  get_cluster(color)
      dic = {}
      for i in rule_base[cluster]:
        dic[i] = get_distance(webcolors.name_to_rgb(i), color)
      sorted_dic = dict(sorted(dic.items(), key=lambda x: x[1]))
      suggested_colors += list(sorted_dic.keys())[:2]
    # suggested_colors += get_contrast_color(color_arr[0], get_cluster(webcolors.name_to_rgb(color_arr[0])))
    return suggested_colors

def filtering(category, length, breadth, height, image_path):
  color_thief = ColorThief(image_path)
  palette = color_thief.get_palette(color_count=10)

  filtered_by_category = df[df['category']==category]
  filtered_by_dim = filtered_by_category[(filtered_by_category['length'] < length) & (filtered_by_category['breadth'] < breadth) & (filtered_by_category['height'] < height)]
  new_df = pd.DataFrame()
  colors = suggest_color(palette)
  for color in colors:
    temp = filtered_by_dim[(filtered_by_dim['color']==color) | (filtered_by_dim['support color']==color)]
    new_df = pd.concat([new_df, temp], ignore_index=True)
  return new_df.to_dict(orient='records')

