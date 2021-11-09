"""
API de messagerie pour Hamstramgram.

GitHub : https://github.com/Tadf0in/Hamstergram
"""

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



if __name__ == '__main__':
    assert 1 == 1