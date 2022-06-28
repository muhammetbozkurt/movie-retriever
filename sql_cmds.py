INSERT_SQL_TEMPLATE = "INSERT INTO {TABLE} {COLOUMS} VALUES ({VALUES});"
MOVIES_FROM_GENRE_QUERY = "SELECT title FROM genres JOIN genres_movies on genres.id = genre_id JOIN movies on movies.id=movie_id WHERE genres.name = '{genre}';"


MOVIES_GENRE_TABLE = ("(SELECT * from genres JOIN genres_movies on genres.id = genre_id JOIN movies on movies.id=movie_id WHERE genres.name = '{genre}')", "genre_sub", "movie_id")
DATE_AFTER = ("(SELECT * from movies WHERE movies.release_date {sign} {year})", "sub_year", "id")
MOVIES_FROM_RATING_SUB = ("(SELECT movie_id from ratings GROUP BY movie_id HAVING(rating)>{rating})",  "rating_sub", "movie_id")

CONJ = "{begin} JOIN {sec_sub} AS {sec_sub_name} ON {first_sub_name}.{first_sub_id}={sec_sub_name}.{sec_sub_id}"

BEGIN = "SELECT {name}.title FROM {entry} AS {name}"
