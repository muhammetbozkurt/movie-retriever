import sqlite3
import argparse

import pandas as pd

from functools import reduce
from sql_cmds import INSERT_SQL_TEMPLATE
from init import init_db


def make_it_beatiful_for_sql(name: str) -> str:
    parts = name.split("'")
    if(len(parts) == 1):
        return name
    return reduce(lambda f,s: f"{f}''{s}", parts)

def extract_name_year(title_str: str) -> tuple:
    start_index = title_str.rfind('(')
    if start_index < 0:
        return (title_str, None)
    end_index = title_str.rfind(')')
    try:
        return (title_str[:start_index - 1] ,int(title_str[start_index + 1: end_index]))
    except:
        return (title_str, None)

def extract_genres(genre_str: str) -> set:
    return set(genre_str.split('|'))

def insert_genres(genres: set, connection: sqlite3.Connection) -> None:
    cur = connection.cursor()
    
    for genre in genres:
        cur.execute(INSERT_SQL_TEMPLATE.format(TABLE="genres", COLOUMS="(name)", VALUES=(f'"{genre}"')))
    connection.commit()

def insert_movies(name_year, connection) -> None:
    cur = connection.cursor()
    for name, year in name_year:
        year = -1 if year is None else year
        sql = INSERT_SQL_TEMPLATE.format(TABLE="movies", COLOUMS="(title, release_date)", VALUES=f"'{make_it_beatiful_for_sql(name)}', {year}")
        cur.execute(sql)
    connection.commit()

def insert_genres_movies(df, connection) -> None:
    for _, row in df.iterrows():
        genres = row["genres"].split("|")
        cur = connection.cursor()
        
        for genre in genres:
            genre_id = cur.execute(f'SELECT id FROM genres where name="{genre}";').fetchone()[0]
            cur.execute(INSERT_SQL_TEMPLATE.format(TABLE="genres_movies", COLOUMS="(movie_id, genre_id)", VALUES=f'{row["movieId"]}, {genre_id}'))
        connection.commit()

def get_all_genres(movies_df: pd.DataFrame) -> set:
    return reduce(lambda x, y: x.union(y), movies_df["genres"].map(extract_genres))

def insert_ratings(ratings_df: pd.DataFrame, connection: sqlite3.Connection) -> None:

    cur = connection.cursor()
    for _, row in ratings_df.iterrows():
        cur.execute(INSERT_SQL_TEMPLATE.format(TABLE="ratings", COLOUMS="(user_id, rating, movie_id)", VALUES=(f'{row["userId"]}, {row["rating"]}, {row["movieId"]}')))
    connection.commit()

def ingest_movies(con: sqlite3.Connection, movies_csv_path = "ml-20m") -> None:
    movies_df = pd.read_csv(f"{movies_csv_path}/movies.csv")
    movies_df["title"] = movies_df["title"].map(extract_name_year)
    genres = get_all_genres(movies_df)

    insert_genres(genres, con)
    insert_movies( movies_df["title"], con)
    insert_genres_movies(movies_df, con)

def ingest_ratings(con: sqlite3.Connection, ratings_csv_path = "ml-20m") -> None:
    ratings_df = pd.read_csv(f"{ratings_csv_path}/ratings.csv")
    ratings_df.drop("timestamp", axis=1, inplace=True)
    ratings_df["user_id"] = ratings_df["userId"]
    ratings_df.drop("userId", axis=1, inplace=True)
    ratings_df["movie_id"] = ratings_df["movieId"]
    ratings_df.drop("movieId", axis=1, inplace=True)
    ratings_df.to_sql(name = "ratings", con= con, if_exists= 'append', index= False, chunksize=1000)

def main(args):
    con = sqlite3.connect(args.database_path)

    init_db(con)
    ingest_movies(con, args.data_path)
    ingest_ratings(con, args.data_path)


    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database-path",
        help='path of database which will be created',
        default="movies_20m.db",
    )
    parser.add_argument(
        "--data-path",
        help='path of folder which contains movilens data',
        default="ml-20m",
    )

    args = parser.parse_args()
    main(args)