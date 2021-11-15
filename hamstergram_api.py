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
    cursor = db.cursor()
    for query in sqlQueries:
        cursor.execute(query)

    # commit des modifications
    db.commit()

def _execute(query):
    """
    Exécute la requête dans la bdd
    In : query (str) : requête sql
    """
    db = _creer_connexion('hamstergram.db')
    cur = db.cursor()
    cur.execute(query)
    response = cur.fetchall()
    db.commit()
    db.close()
    return response


def add_user():
    pass

def remove_user(username):
    """ Supprime l'utilisateur 
    In : username (str) : username d'un utilisateur inscrit
    Out :
        Retourne -1 si l'username est invalide
        Retourne 0 si l'utilisateur a bien été supprimé
    """
    if type(username) != str :
        return -1 # Username invalide car pas str
    else :
        query = f"""
        SELECT name FROM USERS
        WHERE username = '{username}';
        """
        if _execute(query) == [] :
            return -1 # Username invalide car non inscrit
        else :
            query = f"""
            DELETE FROM USERS 
            WHERE username = '{username}';
            """
            _execute(query)
            return 0

def add_friend(user_name, friend_name):
    """ Créer une relation d'amitié entre 2 utilisateurs
    In : user_name (str) : Username du 1er utilisateur concerné
         friend_name (str) : Username du 2eme utilisateur concerné
    Out : 
        Retourne -1 si un des username est invalide ou si déjà amis
        Retourne 0 si les utilisateurs ont bien été ajoutés en amis
    """

def start_disc():
    pass

def create_group():
    pass

if __name__ == '__main__':
    # Tests pour remove_user() :
    _update_db(_creer_connexion('test.db'), 'test.sql')
    assert remove_user(1) == -1
    assert remove_user('JeNexistePas') == -1 # JeNexistePas n'est pas présent dans la bdd
    assert remove_user('JexisteDeja') == 0
    print("Tests passés pour remove_user")
