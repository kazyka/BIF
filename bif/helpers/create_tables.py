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

if not table_exist:
    upload_table_query = """
    CREATE TABLE UploadPath (
                [ID] [bigint] IDENTITY(1,1) NOT NULL,
                UploadDate datetime2(7) NULL,
                PdfName nvarchar(MAX) NULL,
                PathToFile nvarchar(MAX) NULL,
                CPR bigint NULL,
                UserInitials nvarchar(MAX) NULL,
                OCRStartDate datetime2(7)  NULL,
                OCREndDate datetime2(7)  NULL
                )
    """
    create_table(connection_string, upload_table_query)

table_exist = db.check_table_exist("ProcessedData")
if not table_exist:
    upload_table_query = """
    CREATE TABLE ProcessedData (
                [ID] [bigint] IDENTITY(1,1) NOT NULL,
                UniqueId Int NULL,
                Page Int NULL,
                Email nvarchar(MAX) NULL,
                PageMark Bit NULL,
                JournalType nvarchar(MAX) NULL,
                CreateDate datetime2(7)  NULL,
                DeleteDate datetime2(7)  NULL,
                Content nvarchar(MAX) NULL
                )
    """
    create_table(connection_string, upload_table_query)

db.close()
