import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import db 

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/info')
def show_entries():
    db = db()
    cur = db.execute("SELECT * FROM tournament")
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
