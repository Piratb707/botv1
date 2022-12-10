import sqlite3 

async def db_connect() -> None:
    global db, cur

    db = sqlite3.connect("tournament.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS tournament(name, nlogin)")

    db.commit()

async def get_all_members():

    members = cur.execute("SELECT nlogin FROM tournament").fetchall()

    return members

async def register_to_tournament(state):

    async with state.proxy() as data:
        regUser = cur.execute("INSERT INTO tournament VALUES(?, ?)", (data['name'], data['nlogin']))
        db.commit()

    return regUser