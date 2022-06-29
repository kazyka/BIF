from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import json

with open('json_data.json', 'r') as fh:
    data = json.load(fh)

for k in data.keys():
    print(data[k].keys())

