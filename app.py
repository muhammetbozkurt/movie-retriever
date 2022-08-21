from fastapi import FastAPI
from api import MovieRetriever


app = FastAPI()
movieRetriever = MovieRetriever("movies_20m.db")

print(__name__)

@app.get("/oneLink2RuleThemAll")
async def oneLink(year: int = -9999, sign: str = '>', genre: str | None = None, rating: float | None = None):

    print(f"year: {year}, sign: {sign}, genre: {genre}, rating: {rating}")
    query = movieRetriever.query_builder(year, sign, genre, rating)
    print("-"*20)
    print(query)
    print("-"*20)
    df = await movieRetriever.retrieve_movies(year=year, sign=sign, genre=genre, rating=rating)
    return df.to_json()
