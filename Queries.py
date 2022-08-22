INSERT_SQL_TEMPLATE = "INSERT INTO {TABLE} {COLOUMS} VALUES ({VALUES});"

class GetQueries:
    GENRE_QUERY_MOVIEID = "SELECT movie_id FROM genres JOIN genres_movies on genres.id = genre_id AND genres.name = '{genre}' JOIN movies on movies.id=movie_id"
    RATE_QUERY_MOVIEID = "SELECT movie_id FROM ratings GROUP BY movie_id HAVING AVG(rating)>{rating}"
    GENRE_QUERY = "SELECT movies.title FROM genres JOIN genres_movies on genres.id = genre_id AND genres.name = '{genre}' JOIN movies on movies.id=movie_id"
    RATE_QUERY = f"SELECT movies.title FROM ({RATE_QUERY_MOVIEID}) AS sub JOIN movies on movies.id=movie_id"
    YEAR_QUERY = "SELECT movies.title FROM movies WHERE movies.release_date {sign} {year}"
    LIST_GENRES = "SELECT name FROM genres"

class OneLinkQuery:

    DATE_AFTER = ("sub_year", "id")
    MOVIES_GENRE_SUB = ("genre_sub", "movie_id")
    MOVIES_FROM_RATING_SUB = ("rating_sub", "movie_id")

    CONJ = "{begin} JOIN ({sec_sub}) AS {sec_sub_name} ON {first_sub_name}.{first_sub_id}={sec_sub_name}.{sec_sub_id}"
    BEGIN = "SELECT {name}.title FROM ({entry}) AS {name}"

    @staticmethod
    def query_builder(year: int = -9999, sign: str = '>', genre: str= None, rating: float= None) -> str:
        """automatically creates query respect to wanted limits. for instance if user wants to add genre limit than this method add
        necessary parts to query.

        Returns:
            str: query string
        """
        begin=OneLinkQuery.BEGIN.format(
            entry=GetQueries.YEAR_QUERY.format(sign=sign, year=year),
            name=OneLinkQuery.DATE_AFTER[0]
        )
        begin_tuple = OneLinkQuery.DATE_AFTER

        if genre is not None:
            begin = OneLinkQuery.CONJ.format(
                    begin=begin,
                    first_sub_name = begin_tuple[0],
                    first_sub_id = begin_tuple[1],
                    sec_sub=GetQueries.GENRE_QUERY_MOVIEID.format(genre=genre),
                    sec_sub_name=OneLinkQuery.MOVIES_GENRE_SUB[0],
                    sec_sub_id=OneLinkQuery.MOVIES_GENRE_SUB[1]
                )
            begin_tuple = OneLinkQuery.MOVIES_GENRE_SUB
        
        if rating is not None:
            begin = OneLinkQuery.CONJ.format(
                    begin=begin,
                    first_sub_name = begin_tuple[0],
                    first_sub_id = begin_tuple[1],
                    sec_sub=GetQueries.RATE_QUERY_MOVIEID.format(rating=rating),
                    sec_sub_name=OneLinkQuery.MOVIES_FROM_RATING_SUB[0],
                    sec_sub_id=OneLinkQuery.MOVIES_FROM_RATING_SUB[1]
                )
        return begin+';'