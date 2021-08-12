'''
Database File
'''

import mysql.connector
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.disconnect()

def resetDB():
    with mysql.connector.connect(**current_app.config['DATABASE']) as db:
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS Users")
        cursor.execute("""
                        CREATE TABLE `Users` (
                            `id` int NOT NULL AUTO_INCREMENT,
                            `username` varchar(20) DEFAULT NULL,
                            `password_hash` text NOT NULL,
                            PRIMARY KEY (`id`),
                            UNIQUE KEY `username` (`username`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """)
        db.commit() # TODO - need this? and issues with 'db' name shadowing?

def init_app(app):
    app.teardown_appcontext(close_db)

if __name__ == "__main__":
    print("Resetting database...")
    resetDB()
