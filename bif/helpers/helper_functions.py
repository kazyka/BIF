import pyodbc


def create_table(connection_string: str, query: str) -> None:
    """
    I used to create a table in an existing database
    The query is a normal SQL query.
    Example

    CREATE TABLE UploadPath (
                [ID] [bigint] IDENTITY(1,1) NOT NULL,
                UploadDate datetime2(7) NULL,
                PdfName nvarchar(MAX) NULL,
                PathToFile nvarchar(MAX) NULL,
                CPR bigint NULL,
                UserInitials nvarchar(MAX) NULL,
                OCRStartDate datetime2(7)  NULL
                OCREndDate datetime2(7)  NULL
                )

    :param connection_string: The Connection string to the database. Normal string
    :param query: SQL query
    :return: Does not return anything
    """
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query)
    cnxn.commit()
    cursor.close()
