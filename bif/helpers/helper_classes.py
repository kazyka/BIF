import pyodbc
from typing import List, Tuple, Any
from sqlalchemy import create_engine, select, MetaData, Table, and_, text, inspect, orm
import json
import pandas as pd
import urllib


class DB:
    def __init__(self, connection_string):
        # https://docs.sqlalchemy.org/en/14/core/engines.html#microsoft-sql-server
        connection_uri = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}"
        self.engine = create_engine(connection_uri, fast_executemany=True)
        self.connection = self.engine.connect()

    def close(self):
        """
        Closes the connection to the server
        """
        self.connection.close()

    def fetch(self, stmt: orm.query) -> Any:
        return self.engine.execute(stmt)

    def fetch_pd(self, query: text) -> pd.DataFrame:
        """
        An example on how to fetch something from a table

        "SELECT * FROM UploadPath"

        :param query: The query is a normal SQL query to fetch data from the server
        :return: Pandas dataframe with the wanted information from the table
        """
        return pd.read_sql(text(query), self.connection)

    def add_dict(self, table: str, dct: dict, if_exists: str = "append") -> None:
        """

        :param table: Where to add it in the SQL database.
        :param dct: Dictionary with the data. 
        :param if_exists: {‘fail’, ‘replace’, ‘append’}, default ‘fail’
                            How to behave if the table already exists.
                            fail: Raise a ValueError.
                            replace: Drop the table before inserting new values.
                            append: Insert new values to the existing table.
        :return:
        """
        dct = {k: [v] for k, v in dct.items()}
        df = pd.DataFrame(dct)
        df.to_sql(table, con=self.engine, if_exists=if_exists, index=False)

    def update(self, stmt: orm.query) -> None:
        """
        Example on how a statement can be written:
        stmt = update(UploadPath).where(UploadPath.id == "1").values(CPR="1299991111", UserInitials="nso")

        :param stmt: Statement written as sqlalchemy ORM logic
        :return:
        """
        self.engine.execute(stmt)

    def check_table_exist(self, tablename: str) -> bool:
        """

        :param tablename: The tablename you are trying to test if it exist in the database
        :return: Boolean value. True if the table exist. False if the table does not exist
        """
        insp = inspect(self.connection)
        return insp.has_table(tablename, schema="dbo")

    def create_table(self, query: str) -> None:
        """
        Not implementet yet. Use the function create_table from helper_functions instead.
        :param query:
        :return:
        """
        pass
