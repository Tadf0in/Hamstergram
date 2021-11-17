"""
API de messagerie pour Hamstramgram.

GitHub : https://github.com/Tadf0in/Hamstergram
"""

import sqlite3

if __name__ == '__main__':
    TESTING = True
else :
    TESTING = False

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

def _execute(query, values=None):
    """
    Exécute la requête dans la bdd
    In : query (str) : requête sql
    """
    if TESTING :
        db = _creer_connexion('test.db')
    else :
        db = _creer_connexion('hamstergram.db')
    cur = db.cursor()
    if values == None :
        cur.execute(query)
    else :
        cur.execute(query, values)
    response = cur.fetchall()
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
    if not isinstance(username, str) or not isinstance(name, str) or not isinstance(mail, str) or not isinstance(password, str) or not isinstance(bio, str):
        return -1  # si jamais le type n'es pas bon, on renvoie une erreur

    query = f"""
        SELECT name FROM USERS
        WHERE username = ?;
        """
    if _execute(query, (username,)) == [] :  # On vérifie que le nom d'utilisateur n'existe pas déjà
        query = f"""
        SELECT name FROM USERS
        WHERE mail = ?;
        """
        if _execute(query, (mail,)) == []:  # si il n'existe pas, on vérifie que l'email n'existe pas déjà
            query = f"""INSERT INTO USERS(username, name, mail, password) 
                    VALUES (?, ?, ?, ?"""

            if bio != "":
                query += f',?);'
                _execute(query, (username, name, mail, password, bio,))
            else:
                query += ');'
                _execute(query, (username, name, mail, password,))

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
        WHERE username = ?;
        """
        if _execute(query, (username,)) == [] :
            return -1 # Username invalide car non inscrit
        else :
            query = f"""
            DELETE FROM USERS 
            WHERE username = ?;
            """
            _execute(query, (username,))
            return 0


def add_friend():
    pass


def remove_friend(username : str, friendUsername : str):
    """ La fonction supprime un ami
    In : username = nom de l'utilisateur qui souhaite supprimer un ami
        friendUsername : nom de l'ami en question
    Out :
        Retourne -1 si l'username est invalide
        Retourne 0 si l'ami a bien été supprimé
    """
    # Si les arguments ne sont pas du bon type, on renvoie une erreur
    if not isinstance(username, str) or not isinstance(friendUsername, str):
        return -1

    # On vérifie que l'utilisateur existe et que l'ami a supprime est dans la liste d'amis
    user_exists = False
    for user in _list_users():
        if user[0] == username:
            user_exists = True
            break
    is_friend = False
    for user in list_friends(username):
        if user == friendUsername:
            is_friend = True
            break
    # si l'utilisateur n'existe pas ou que l'autre utilisateur n'est pas notre ami, on renvoie une erreur
    if not user_exists or not is_friend:
        return -1

    # si toutes les conditions sont passées, on supprime l'ami et on renvoie 0
    query = """DELETE FROM FRIENDS WHERE user_name='?' AND friend_name='?'"""
    _execute(query, (username, friendUsername))
    return 0
    
    pass

def start_disc():
    pass

def create_group():
    pass

def _list_users():
    """ determine ce que contient la table USERS
    Out : liste de tous les utilisateurs et de leurs informations
    """
    query = f"""
    SELECT * FROM USERS
    """
    return (_execute(query))

def list_friends(username):
    """ determine les amis d'un utilisateur
    Out : liste des amis d'un utilisateur
    """
    query = f"""
    SELECT friend_name FROM FRIENDS
    WHERE user_name = '?'
    """
    return (_execute(query, (username)))

if __name__ == '__main__':
    from os import remove
    import time

    # Creation d'une BDD temporaire pour les tests
    testDb_file = open('test.db', 'x')
    testDb_file.close()

    # Creation des relations dans la base de données: (On est obligés de le faire en deux fois avec 
    # la methode execute de sqlite 3)
    create_table_users = """CREATE TABLE "USERS" (
            "username" TEXT  NOT NULL ,
            "name" TEXT  NOT NULL ,
            "mail" TEXT  NOT NULL ,
            "password" TEXT  NOT NULL ,
            "bio" TEXT  NULL ,
            CONSTRAINT "pk_USERS" PRIMARY KEY ("username"),
            CONSTRAINT "uk_USERS_mail" UNIQUE ("mail"));
    """
    create_table_friends ="""CREATE TABLE FRIENDS (
            "user_name" TEXT  NOT NULL ,
            "friend_name" TEXT  NOT NULL ,
            CONSTRAINT "pk_FRIENDS" PRIMARY KEY ("user_name","friend_name")
        )
    """
    _execute(create_table_users)
    _execute(create_table_friends)

    # On ajoutes des données dans les relations
    _execute("""
    INSERT INTO USERS (username, name, mail, password) VALUES ('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123')""")
    _execute("""INSERT INTO FRIENDS (user_name, friend_name) VALUES ('JexisteDeja', 'ninobg47')
    """)

    # Tests pour add_user() :
    # On verifie que la table USERS contient les bonnes informations
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None)]
    # On vérifie que en passant des arguments du mauvais type, la fonction renvoie une erreur et que la table USERS n'a pas été modifiée
    assert add_user(1, 1, 1, 1) == -1
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None)]
    # On vérifie qu'essayer d'entrer un utilisateur avec un nom d'utilisateur déjà existant renvoie une erreur et que que la table USERS n'a pas été modifiée
    assert add_user('JexisteDeja', 'eoiokdeo', 'pasmoi@mail.fr', 'deded') == -1
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None)]
    # On vérifie qu'essayer d'entrer un utilisateur dont l'adresse email est déjà utilisée renvoie une erreur et que la table USERS n'a donc pas été modifiée
    assert add_user('JexistePas', 'MoiOnSenFiche', 'existe.deja@mail.fr', 'MoiAussiOnSenFiche', None) == -1
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None)]
    # On vérifie qu'ajouter un utilisateur donc l'adresse email et le nom d'utilisateur n'existent pas ne renvoie pas d'erreur et  que la table USERS a été modifiée en conséquent
    assert add_user('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty') == 0
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty', None)]
    print('Tests passés pour add_user')

    # Tests pour remove_user() :
    # On vérifie que passer un argument de mauvais type renvoie une erreur et ne modifie pas la table USERS
    assert remove_user(1) == -1
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty', None)]
    # On vérifie que supprimer un utilisateur inexistant renvoie une erreur et ne modifie pas la table USERS
    assert remove_user('JeNexistePas') == -1 # JeNexistePas n'est pas présent dans la bdd
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty', None)]
    # On vérifie que supprimer un utilisateur existant ne renvoie pas d'erreur et modifie bien la table USERS
    assert remove_user('NouvelUtilisateur') == 0
    assert _list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None)]
    print("Tests passés pour remove_user")


    # Tests de remove_friend():
    # On teste list_friends
    assert list_friends('JexisteDeja') == [('ninobg74')]
    # On vérifie que si l'argument n'est pas du bon type, la fonction renvoie une erreur et la liste d'amis n'est pas modifiée
    assert remove_friend(1, 1) == -1
    assert list_friends('JexisteDeja') == [('ninobg74')]
    # On vérifie que si on tente de supprimer un ami que l'on a pas, la fonction renvoie une erreur et la liste d'amis n'es pas modifiée
    assert remove_friend('JexisteDeja', 'loulou74490') == -1
    assert list_friends('JexisteDeja') == [('ninobg74')]
    # On vérifie que si on tente de supprimer un ami de qqn qui n'existe pas, la fonction renvoie une erreur et la liste d'amis n'est pas modifiée
    assert remove_friend('JeNexistePas', 'ninobg74') == -1
    assert list_friends('JexisteDeja') == [('ninobg74')]
    # On vérifie que si on supprime un ami, la fonction ne renvoie pas d'erreur et la liste d'amis est modifiée en conséquent
    assert remove_friend('JexisteDeja', 'ninobg74') == 0
    assert list_friends('JexisteDeja') == []
    print("Tests passés pour remover_friend")

    # On supprime la BDD temporaire
    time.sleep(10)
    remove('test.db')