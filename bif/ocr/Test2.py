from pdf2image import convert_from_path
import easyocr
import numpy as np
import PIL
from PIL import ImageDraw
import spacy

reader = easyocr.Reader(['da'], gpu=True)

result = reader.readtext('page_1.jpg')

print(result)

# images = convert_from_path('SNV115.pdf')
#
#
# bounds = reader.readtext(np.array(images[0]))
#
#
# def draw_boxes(image, bounds, color='yellow', width=2):
#     draw = ImageDraw.Draw(image)
#     for bound in bounds:
#         p0, p1, p2, p3 = bound[0]
#         draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
#
#     return image
#
# draw_boxes(images[0], bounds)