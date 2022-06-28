import sqlite3

import pandas as pd

from sql_cmds import DATE_AFTER, BEGIN, CONJ, MOVIES_GENRE_TABLE, MOVIES_FROM_RATING_SUB
from sql_cmds import INSERT_SQL_TEMPLATE
from sql_cmds import INSERT_SQL_TEMPLATE

class MovieRetriever():
    @staticmethod
    def query_builder(year: int = -9999, sign: str = '>', genre: str= None, rating: float= None) -> str:
        """automatically creates query respect to wanted limits. for instance if user wants to add genre limit than this method add
        necessary parts to query.

        Returns:
            str: query string
        """
        begin=BEGIN.format(
            entry=DATE_AFTER[0].format(sign=sign, year=year),
            name=DATE_AFTER[1]
        )
        begin_tuple = DATE_AFTER

        if genre is not None:
            begin = CONJ.format(
                    begin=begin,
                    first_sub_name = begin_tuple[1],
                    first_sub_id = begin_tuple[2],
                    sec_sub=MOVIES_GENRE_TABLE[0].format(genre=genre),
                    sec_sub_name=MOVIES_GENRE_TABLE[1],
                    sec_sub_id=MOVIES_GENRE_TABLE[2]
                )
            begin_tuple = MOVIES_GENRE_TABLE
        
        if rating is not None:
            begin = CONJ.format(
                    begin=begin,
                    first_sub_name = begin_tuple[1],
                    first_sub_id = begin_tuple[2],
                    sec_sub=MOVIES_FROM_RATING_SUB[0].format(rating=rating),
                    sec_sub_name=MOVIES_FROM_RATING_SUB[1],
                    sec_sub_id=MOVIES_FROM_RATING_SUB[2]
                )
        return begin+';'

    @staticmethod
    def retrieve_movies(db_path:str, csv_path: str = None, year: int = -9999, sign: str = '>', genre: str = None, rating: float = None) -> pd.DataFrame:
        """retrieve movie name respect to 

        Args:
            db_path (str): db path
            csv_path (str, optional): if given save retrieved dataframe to path. Defaults to None.
            year (int, optional): year limit for query. Defaults to -9999.
            sign (str, optional): sign is to determine how to limit year. Defaults to '>'.
            genre (str, optional): if exist genre limit will be added to query. Defaults to None.
            rating (float, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: retrieved movies from database
        """
        con = sqlite3.connect(db_path)
        query = MovieRetriever.query_builder(int(year),sign, genre, rating)

        res = pd.read_sql_query(query, con)
        con.close()


        if csv_path is not None:
            res.to_csv(csv_path)

        return res


