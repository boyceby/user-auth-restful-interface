'''
Database File
'''

import mysql.connector
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.disconnect()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) # TODO - not sure if mysql connection offers 'executescript' (what / is something needed in place of this?)

def init_app(app):
    app.teardown_appcontext(close_db)
