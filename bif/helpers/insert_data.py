import pyodbc
from sqlalchemy import create_engine, select, MetaData, Table, and_, text, inspect, update
import urllib
import datetime
from helper_functions import *
import json
import pandas as pd
from helper_classes import DB
from helper_functions import create_table
from tables import UploadPath


with open('../../config.json', 'r') as fh:
    config = json.load(fh)


database_type = "TestBIFDB"
connection_string = (
    f'Trusted_Connection={config[database_type]["trusted_connection"]};'
    f'DRIVER={config[database_type]["driver"]};'
    f'server={config[database_type]["server"]};'
    f'database={config[database_type]["database"]};'
)

db = DB(connection_string)
table_exist = db.check_table_exist("UploadPath")


if table_exist and False:
    dct = {
        "UploadDate": datetime.datetime(2022, 6, 29),
        "PdfName": "Sag1Mini.pdf",
        "PathToFile": "E:\\Data\\Sag1Mini.pdf",
        "CPR": 1234569999,
        "UserInitials": "mha",
        "OCRStartDate": None,
        "OCREndDate": None
    }
    db.add_dict("UploadPath", dct)

if table_exist and False:
    dct = {
        "UploadDate": datetime.datetime(2022, 6, 15),
        "PdfName": "SNV1152.pdf",
        "PathToFile": "G:\\Programming\\ArbejdeCarve\BIF\\bif\\data\\SNV1152.pdf",
        "CPR": 1234569999,
        "UserInitials": "mha",
        "OCRStartDate": None,
        "OCREndDate": None
    }
    db.add_dict("UploadPath", dct)
    dct = {
        "UploadDate": datetime.datetime(2022, 6, 15),
        "PdfName": "SNV115.pdf",
        "PathToFile": "G:\\Programming\\ArbejdeCarve\\BIFFFFFF\\bif\data\\SNV115.pdf",
        "CPR": 1234569999,
        "UserInitials": "mha",
        "OCRStartDate": None,
        "OCREndDate": None
    }
    db.add_dict("UploadPath", dct)
    dct = {
        "UploadDate": datetime.datetime(2022, 6, 15),
        "PdfName": "SNV115.pdf",
        "PathToFile": "G:\\Programming\\ArbejdeCarve\\BIF\\bif\data\\SNV115.pdf",
        "CPR": 1234569999,
        "UserInitials": "mha",
        "OCRStartDate": None,
        "OCREndDate": None
    }
    db.add_dict("UploadPath", dct)
    dct = {
        "UploadDate": datetime.datetime(2022, 6, 15),
        "PdfName": "SNV11_Konto21090813310.pdf",
        "PathToFile": "G:\\Programming\\ArbejdeCarve\\BIF\\bif\\data\\SNV11_Konto21090813310.pdf",
        "CPR": 1234569999,
        "UserInitials": "mha",
        "OCRStartDate": None,
        "OCREndDate": None
    }
    db.add_dict("UploadPath", dct)


# stmt = update(UploadPath).where(UploadPath.id == "1").values(CPR="1299991111", UserInitials="nso")
# print(stmt)
# db.update(stmt)

t = "SELECT * FROM UploadPath"
data = db.fetch_pd(t)
print(data)

db.close()
