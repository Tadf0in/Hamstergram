"""
API de messagerie pour Hamstramgram.

GitHub : https://github.com/Tadf0in/Hamstergram
"""

import sqlite3

def _creer_connexion(db_file):
    """ Crée une connexion à la base de données SQLite spécifiée par db_file.
        Le fichier est créé s'il n'existe pas.

    In : db_file (str) : Chemin vers un fichier .db
    Out : objet connexion ou None
    """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except sqlite3.Error as e:
        print(e)

    return None

def _update_db(db, sql_file):
    """ Execute les requêtes SQL de sql_file pour modifier la DB db
    In : db (objet connexion)
         sql_file (str) : Chemin vers un fichier SQL (.sql)
    Out : 
    """
    # Lecture du fichier et placement des requetes dans un tableau
    createFile = open(sql_file, 'r')
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Execution de toutes les requetes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        cursor.execute(query)

    # commit des modifications
    conn.commit()

def add_user():
    pass


def add_friend():
    pass


def start_disc():
    pass


def create_group():
    pass


if __name__ == '__main__':
    assert 1 == 1
