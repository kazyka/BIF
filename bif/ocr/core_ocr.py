
import datetime
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from bif.ocr.ocr import *
import json
import pandas as pd
from bif.helpers.helper_classes import DB
from bif.helpers.tables import UploadPath
from sqlalchemy import select, update
import logging
import json

logger = logging.getLogger(__name__)


def core_ocr(config_file: str, db_type: str, base_path: str) -> None:
    with open(config_file, 'r') as fh:
        config = json.load(fh)

    connection_string = (
        f'Trusted_Connection={config[db_type]["trusted_connection"]};'
        f'DRIVER={config[db_type]["driver"]};'
        f'server={config[db_type]["server"]};'
        f'database={config[db_type]["database"]};'
    )

    logger.info(f'Initializing the Database Class')
    db = DB(connection_string)

    query = "SELECT ID FROM UploadPath WHERE OCRStartDate is NULL"
    unprocessed_ids = db.fetch_pd(query)

    logger.info(f'All IDs with date Null: {unprocessed_ids["ID"].tolist()}')

    for idx, current_id in enumerate(unprocessed_ids['ID'].tolist()):

        stmt = select(UploadPath).where(UploadPath.id == current_id)

        # print(stmt)
        current_row = db.fetch(stmt).all()

        # print(current_row)

        # define columns
        file_name = current_row[0][2]
        file_location = current_row[0][3]
        user_initials = current_row[0][5]
        ocr_start_date = current_row[0][6]

        if not os.path.isfile(file_location):
            set_date_start = datetime.datetime(1980, 1, 1, 0, 0)
            stmt = update(UploadPath).where(UploadPath.id == current_id).values(OCRStartDate=set_date_start)
            db.update(stmt)
            logger.info("File does not exist at location")
            continue

        if ocr_start_date is not None:
            continue

        # set_date_start = datetime.datetime.combine(datetime.datetime.utcnow().date(), datetime.time(0, 0, 0))
        set_date_start = datetime.datetime.utcnow()
        stmt = update(UploadPath).where(UploadPath.id == current_id).values(OCRStartDate=set_date_start)
        db.update(stmt)

        pdf_path, jpg_path = create_folder(user_initials, str(current_id), base_path)

        # Splits the
        split_pdf(file_location, pdf_path)

        convert_to_img(pdf_path, jpg_path)

        all_text = extract_text(jpg_path, f"{user_initials}@carve.dk", current_id)

        with open('json_data.json', 'w') as outfile:
            json.dump(all_text, outfile, default=str)

        for k in all_text.keys():
            db.add_dict("ProcessedData", all_text[k])

        # set_date_end = datetime.datetime.combine(datetime.datetime.utcnow().date(), datetime.time(0, 0, 0))
        set_date_end = datetime.datetime.utcnow()
        stmt = update(UploadPath).where(UploadPath.id == current_id).values(OCREndDate=set_date_end)
        db.update(stmt)

        # TODO
        #   Delete the File for Project ID
        #   pdf_path, jpg_path
        #   file_location

    db.close()
