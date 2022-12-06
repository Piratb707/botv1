import sqlite3 as sq

async def db_connect() -> None:
    global db, cur

    db= sq.connect("tournament.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXIST tournament(user TEXT)")

    db.commit()

async def register_to_tournament(user,name):

    regUser = cur.execute("INSERT INTO tournament (?,)", (user,))
    db.commit()

    return regUser