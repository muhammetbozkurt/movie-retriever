import sqlite3

import pandas as pd

class MovieRetriever():
    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.db = self.connect2DB()

    def connect2DB(self):
        return sqlite3.connect(self.db_path)

    def __del__(self):
        self.db.close()


    async def retrieve_movies(self, query: str, csv_path: str | None = None) -> pd.DataFrame:
        """retrieve movie name respect to 

        Args:
            query (str): query string
            csv_path (str, optional): if given save retrieved dataframe to path. Defaults to None.

        Returns:
            pd.DataFrame: retrieved movies from database
        """

        res = pd.read_sql_query(query, self.db)


        if csv_path is not None:
            res.to_csv(csv_path)

        return res
