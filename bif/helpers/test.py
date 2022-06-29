import pandas as pd
import urllib
import datetime
from helper_functions import *
from sqlalchemy import update
import json
from helper_classes import DB
from tables import UploadPath
import easyocr
import os
import collections
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

with open('../../config.json', 'r') as fh:
    config = json.load(fh)

connection_string = (
    f'Trusted_Connection={config["localDB"]["trusted_connection"]};'
    f'DRIVER={config["localDB"]["driver"]};'
    f'server={config["localDB"]["server"]};'
    f'database={config["localDB"]["database"]};'
)

base_path = os.path.abspath(os.getcwd())
base_data_path = os.path.join(base_path, "bif", "output")
user_initials_path = os.path.join(base_data_path, 'mha')
jpg_path = os.path.join(user_initials_path, f'project_id_2', "jpg")

reader = easyocr.Reader(['en', 'da'], gpu=False)
path_pic = r'../data/page_1.jpg'


#path_pic = r'G:\Programming\ArbejdeCarve\BIF\bif\output\mha\project_id_2\jpg\NV11_Konto21090813310_1_1.jpg'




d = collections.defaultdict()

d['page_1.jpg'] = {}
d['page_1.jpg']['text'] = []
d['page_1.jpg']["mark"] = None

result = reader.readtext(path_pic)

point = Point(750, 100)

for t in result:
    coord = t[0]
    text = t[1]

    if Polygon(coord).contains(point):
        d['page_1.jpg']["mark"] = True

    d['page_1.jpg']['text'].append(text)


with open('json_data.json', 'w') as outfile:
    json.dump(d, outfile)

print(result)

