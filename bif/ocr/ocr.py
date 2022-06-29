import datetime
import os
import sys
from glob import glob
from typing import List, Tuple, Dict

from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import easyocr
import collections
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import logging

logger = logging.getLogger(__name__)


def create_folder(user_initials: str, project_id: str, base_path: str = None) -> Tuple[str, str]:
    """
    Creates a folder in the base_path.
    Example
    E:\\bif\output\<user_initials>\project_id_<id>\pdf\
    E:\\bif\output\<user_initials>\project_id_<id>\jpg\
    :param user_initials: The user initials
    :param project_id: Project ID. Taken from the SQL ID
    :param base_path: The Base path
    :return: Tuple path of pdf and png (pdf, png)
    """
    if base_path is None:
        raise Warning("You should define a base directory")

    base_data_path = os.path.join(base_path, "bif", "output")
    user_initials_path = os.path.join(base_data_path, user_initials)
    pdf_path = os.path.join(user_initials_path, f'project_id_{project_id}', "pdf")
    jpg_path = os.path.join(user_initials_path, f'project_id_{project_id}', "jpg")

    logger.info("Trying to create pdf folder")
    try:
        if os.path.isdir(pdf_path):
            files = glob(os.path.join(pdf_path, "*.pdf"))
            for file in files:
                os.unlink(file)

            os.rmdir(pdf_path)

        os.makedirs(pdf_path)
    except Exception as e:
        logger.warning(f'Failed to delete and create for reason {e}')

    logger.info("Trying to create picture folder")
    try:
        if os.path.isdir(jpg_path):
            files = glob(os.path.join(jpg_path, "*.jpg"))
            for file in files:
                os.unlink(file)

            os.rmdir(jpg_path)

        os.makedirs(jpg_path)
    except Exception as e:
        logger.warning(f'Failed to delete and create for reason {e}')

    return pdf_path, jpg_path


def split_pdf(path: str, output_dir: str = None) -> None:
    """
    Splits the pdf into multiple smaller pdfs.
    :param path: The path to the master-PDF
    :param output_dir: Output of the split pdf
    :return:
    """
    if output_dir is None:
        raise Warning("You should define an output directory")

    reader = PdfReader(path)
    number_of_pages = len(reader.pages)

    file_name = path.split("/")[-1]

    for i in range(number_of_pages):
        output = PdfWriter()
        output.add_page(reader.getPage(i))
        output_name = f"{os.path.basename(file_name.replace('.pdf', ''))}_{i + 1}.pdf"

        output_name = os.path.join(output_dir, output_name)
        with open(output_name, 'wb') as outputStream:
            output.write(outputStream)


def convert_to_img(path: str, output_dir: str = None) -> None:
    """
    converts PDF to img files
    :param path: path to the PDFs
    :param output_dir: Output for the img
    :return:
    """

    files = glob(os.path.join(path, "*.pdf"))
    for idx, file in enumerate(files):
        page = convert_from_path(file, 500, poppler_path=r"C:\poppler-22.04.0\Library\bin")
        output_name = f"{os.path.basename(file.replace('.pdf', ''))}_{idx + 1}.jpg"
        output_name = os.path.join(output_dir, output_name)
        page[0].save(output_name, 'JPEG')


def extract_text(path: str, email: str, uid: int) -> Dict:
    """
    OCR on the Images
    :param path: The path to the folder of the pictures we wish to extract
    :param email: Email information
    :param uid: ID from the table. Is used for unique ID cases
    :return:
    """

    reader = easyocr.Reader(['da'])
    files = glob(os.path.join(path, "*.jpg"))

    d = collections.defaultdict()

    # TODO
    #   Fix Points
    #   Where we expect crucial text to be
    #   Remember to find the true point inside the square.
    point = Point(3175, 350)

    for file in files:

        page = file.split("\\")[-1].split("_")[-2]

        d[file] = {}
        d[file]["UniqueId"] = uid
        d[file]['Page'] = int(page)
        d[file]["Email"] = email
        d[file]["PageMark"] = None
        d[file]["JournalType"] = None
        d[file]['CreateDate'] = datetime.datetime.today().date()
        d[file]['DeleteDate'] = None

        d[file]["raw_text"] = []

        result = reader.readtext(file)

        for t in result:
            coord = t[0]
            text = t[1]

            if Polygon(coord).contains(point):
                logger.debug("Coord is True")
                if "læ" in text.lower():
                    logger.debug("LÆ Caught")
                    d[file]["PageMark"] = True
                    d[file]["JournalType"] = "LÆ"

            d[file]["raw_text"].append(text)

        # used for Elastic Search
        d[file]['Content'] = ' '.join(d[file]['raw_text'])

    for k in d.keys():
        my_di = d[k]
        try:
            del my_di["raw_text"]
        except Exception as e:
            logger.info(f"Could not delete key: {e}")

    return d
