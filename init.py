import sqlite3


def get_ready_query(file_name: str = "init.sql") -> str:
    """reads ready query from file

    Args:
        file_name (str, optional): ame of the file that contains query string. Defaults to "init.sql".

    Returns:
        str: query string
    """
    queries = None
    with open("init.sql", "r") as f:
        queries = f.read()
    return queries


def init_db(con: sqlite3.Connection):
    cur = con.cursor()
    init_query = get_ready_query()
    cur.executescript(init_query)
    con.commit()



"""con = sqlite3.connect('/home/bzkrt/WS/pc/movie-service/test.db')

cur = con.cursor()


init_query = get_ready_query()

print(init_query)

cur.executescript(init_query)
con.commit()
con.close()"""