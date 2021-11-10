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


def add_user():
    pass

def remove_user(username):
    """ Supprime l'utilisateur 
    In : username (str) : username d'un utilisateur inscrit
    Out :
        Retourne -1 si les conditions ne sont pas respectées
    """
    if type(username) != str():
        return -1
    else :
        db = _creer_connexion('hamstergram.db')
        cur = db.cursor()
        query = f"""
        DELETE FROM USERS 
        WHERE username ='{username}'
        """
        cur.execute(query)
        db.close()


def add_friend():
    pass


def start_disc():
    pass


def create_group():
    pass


if __name__ == '__main__':
    assert 1 == 1