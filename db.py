import sqlite3 

async def db_connect() -> None:
    global db, cur

    db = sqlite3.connect("tournament.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS tournament(user, TEXT)")

    db.commit()

async def get_all_members():

    members = cur.execute("SELECT * FROM tournament").fetchall()

    return members

async def register_to_tournament(user):

    regUser = cur.execute("INSERT INTO tournament (?)", (user,))
    db.commit()

    return regUser