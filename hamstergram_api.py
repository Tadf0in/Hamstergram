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
    db = _creer_connexion('test.db')
    cur = db.cursor()
    cur.execute(query)
    response = cur.fetchall()
    print(response)
    db.commit()
    db.close()
    return response

def add_user(username : str, name : str, mail : str, password : str, bio : str =''):
    """Ajoute un nouvel utilisateur
    In : username : nom d'utilisateur 
        name : nom de l'utilisateur
        mail : email utilisateur
        password : mot de passe
        bio : biographie éventuelle de l'utilisateur

    Out :
        Retourne -1 si il y a une erreur
        Retourne 0 si l'utilisateur a bien été supprimé 
    """
    if not isinstance(username, str) or not isinstance(name, str) or not isinstance(mail, str) or not isinstance(password, str):
        return -1  # si jamais le type n'es pas bon, on renvoie une erreur

    query = f"""
        SELECT name FROM USERS
        WHERE username = '{username}';
        """
    if _execute(query) == [] :  # On vérifie que le nom d'utilisateur n'existe pas déjà
        query = f"""
        SELECT name FROM USERS
        WHERE mail = '{mail}';
        """
        if _execute(query) == []:  # si il n'existe pas, on vérifie que l'email n'existe pas déjà
            query = f"""INSERT INTO USERS(username, name, mail, password) 
                    VALUES ('{username}', '{name}', '{mail}', '{password}'"""

            if bio != "":
                query += f',{bio});'
            else:
                query += ');'
        
            _execute(query)

            return 0  # Pas d'erreur, on renvoie 0
        else:
            return -1  # On renvoie -1 car l'email existe déjà
    else:
        return -1  # On renvoie -1 car l'utilisateur existe déjà


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


def add_friend():
    pass


def start_disc():
    pass


def create_group():
    pass


if __name__ == '__main__':
    # Tests pour add_user() :
    assert add_user('JexisteDeja', 'eoiokdeo', 'existe.deja@mail.fr', 'deded') == -1
    assert add_user('JeNexistePas', 'dedede', 'moinonplus@gmail.com', 'azerty') == 0