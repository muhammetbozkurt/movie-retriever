import queue
from fastapi import FastAPI, Query
from api import MovieRetriever
from Queries import OneLinkQuery, GetQueries


app = FastAPI()
movieRetriever = MovieRetriever("movies_20m.db")

@app.get("/oneLink2RuleThemAll")
async def oneLink(year: int = -9999, sign: str = '>', genre: str | None = None, rating: float | None = None):

    query = OneLinkQuery.query_builder(year, sign, genre, rating)
    df = await movieRetriever.retrieve_movies(query=query)
    return df.to_json()

@app.get("/year/{year}")
async def year(year: int, sign: str = "after"):
    sign = ">" if sign == "after" else "<" if sign == "before" else "="
    query = GetQueries.YEAR_QUERY.format(sign=sign, year=year)
    df = await movieRetriever.retrieve_movies(query=query)
    return df.to_json()

@app.get("/rating/{rating}")
async def rating(rating: float):
    query = GetQueries.RATE_QUERY.format(rating=rating)
    df = await movieRetriever.retrieve_movies(query=query)
    return df.to_json()

@app.get("/genre/{genre}")
async def rating(genre: str):
    query = GetQueries.GENRE_QUERY.format(genre=genre)
    df = await movieRetriever.retrieve_movies(query=query)
    return df.to_json()

@app.get("/listGenres/")
async def rating():
    query = GetQueries.LIST_GENRES
    df = await movieRetriever.retrieve_movies(query=query)
    return df.to_json()