BEGIN;
DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
  id integer PRIMARY KEY AUTOINCREMENT,
  title varchar(255),
  release_date integer
);
DROP TABLE IF EXISTS genres;
CREATE TABLE genres (
  id integer PRIMARY KEY AUTOINCREMENT,
  name varchar(255)
);
DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  id integer PRIMARY KEY AUTOINCREMENT,
  user_id integer,
  rating integer,
  movie_id integer NOT NULL,
  FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
);
DROP TABLE IF EXISTS genres_movies;
CREATE TABLE genres_movies (
  id integer PRIMARY KEY AUTOINCREMENT,
  movie_id integer NOT NULL,
  genre_id integer NOT NULL,
  FOREIGN KEY(movie_id) REFERENCES movies(movie_id),
  FOREIGN KEY(genre_id) REFERENCES genres(id)
);
COMMIT;