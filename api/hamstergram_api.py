"""
API de messagerie.

GitHub : https://github.com/Tadf0in/Hamstergram
"""
import sqlite3
from PIL import Image # Pour les stories

if __name__ == '__main__':
    TESTING = True
else :
    TESTING = False

    
def _creer_connexion(db_file : str) -> None :
    """ Crée une connexion à la base de données SQLite spécifiée par db_file.
        Le fichier est créé s'il n'existe pas.

    In : db_file : Chemin vers un fichier .db
    Out : objet connexion ou None
    """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def _execute(query : str, values=None) :
    """
    Exécute la requête dans la bdd
    In : query : requête sql
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


def add_user(username : str, name : str, mail : str, password : str, bio : str ='') -> int :
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

    username.replace(";", "")

    if not user_exists(username):  # On vérifie que le nom d'utilisateur n'existe pas déjà
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

    
def remove_user(username : str) -> int :
    """ Supprime l'utilisateur 
    In : username : username d'un utilisateur inscrit
    Out :
        Retourne -1 si l'username est invalide
        Retourne 0 si l'utilisateur a bien été supprimé
    """
    if type(username) != str :
        return -1 # Username invalide car pas str
    else :
        if not user_exists(username):
            return -1 # Username invalide car non inscrit
        else :
            query = f"""
            DELETE FROM USERS 
            WHERE username = ?;
            """
            _execute(query, (username,))
            return 0


def list_users() -> list :
    """ determine ce que contient la table USERS
    Out : liste de tous les utilisateurs et de leurs informations
    """
    query = f"""
    SELECT * FROM USERS
    """
    return (_execute(query))


def user_exists(user : str) :
    """determine si un utilisateur existe
    In : user : nom d'utiliseur a verifier
    Out : True si l'utilisateur existe dans la BDD
          False sinon
          -1 si le paramètre est invalide
    """
    if not isinstance(user, str):
        return -1

    query = """SELECT username FROM USERS WHERE username=?"""
    if _execute(query, (user,)) == []:
        return False
    else:
        return True
        
        
def is_friend(user : str, friend: str) :
    """ Vérifie si 2 utilisateurs sont déjà amis
    In : user : Username de l'utilisateur
         friend : Username du potentiel ami
    Out : (bool) : True = Les 2 utilisateurs sont amis
                    False = Les 2 utilisateurs ne sont pas amis
        Retourne -1 si un des username est invalide
    """
    if type(user) != str or type(friend) != str :
        return -1 # Username invalide car pas str
        
    if not user_exists(user) or not user_exists(friend) :
        return -1 # Un des usernames est invalide
    
    friends = list_friends(user)[0]
    if friends == [] :
        return False # Pas d'amis
    elif friend in friends :
        return True # Amis
    
    return False # Pas amis


def add_friend(user_name : str, friend_name : str) -> int :
    """ Ajoute un ami à un utilisateur
    in : user_name : Username de l'utilisateur
         friend_name : Username de l'ami à ajouter
    Out : 
        Retourne -1 si un username est invalide ou si déjà amis
        Retourne 0 si a bien été ajouté en ami
    """
    if type(user_name) != str or type(friend_name) != str :
        return -1 # Username invalide car pas str
    elif user_name == friend_name :
        return -1 # Usernames identiques
    elif is_friend(user_name, friend_name) or is_friend(user_name, friend_name) == -1:
        return -1 # Déjà amis ou username invalide
    else :
        query = """
        INSERT INTO FRIENDS (user_name, friend_name)
        VALUES (?, ?);
        """
        _execute(query, (user_name, friend_name))
        return 0          

    
def remove_friend(username : str, friendUsername : str) -> int :
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

    # On vérifie que l'ami a supprime est dans la liste d'amis
    is_friend = False
    friend_list = list_friends(username)
    if friend_list == -1:
        return -1
    for i in range(len(friend_list)):
        if friend_list[i] == friendUsername:
            is_friend = True
            break

    # si l'utilisateur n'existe pas ou que l'autre utilisateur n'est pas notre ami, on renvoie une erreur
    if not user_exists(username) or not is_friend:
        return -1

    # si toutes les conditions sont passées, on supprime l'ami et on renvoie 0
    query = """DELETE FROM FRIENDS WHERE user_name=? AND friend_name=?"""
    _execute(query, (username, friendUsername))
    return 0


def list_friends(username : str) -> list :
    """ determine les amis d'un utilisateur
    Out : liste des amis d'un utilisateur
    """
    if not isinstance(username, str):
        return -1  # On renvoie une erreur si username n'est pas du bon format

    if not user_exists(username):
        return -1  # Si l'utilisateur n'est pas dans la BDD on renvoie une erreur
        
    query = f"""
    SELECT friend_name FROM FRIENDS
    WHERE user_name = ?
    """
    friend_list = _execute(query, (username,))
    return [friend_name[0] for friend_name in friend_list]


def send_msg(content : str, sender : str, receiver : str = None, group_id : int = None) -> int :
    """La fonction permet d'envoyer un message dans une discussion ou un groupe
    In : content : contenu du message
         sender : username de l'expéditeur
         receiver : username du destinataire (non utilisé dans le cas des groupes)
         group_id : id du groupe dans lequel le message est envoyé (non utilisé dans le cas des discussions privées)
    Out : -1 en cas d'erreur ou de paramètre invalide
           0 si tout s'est bien déroulé
    """
    if not isinstance(content, str) or not isinstance(sender, str) or (not isinstance(receiver, (str)) and receiver is not None) or \
        (not isinstance(group_id, int) and group_id is not None): 
        return -1  # Les types ne sont pas respectés

    if sender == receiver:
        return -1  # le destinataire et l'expediteur sont la même personne
    
    if (receiver is not None and group_id is not None) or (receiver is None and group_id is None):
        return -1  # On tente d'entrer a la fois un id de groupe et un destinataire ou aucun des deux

    if content == "":
        return -1  # le message est vide

    if not user_exists(sender) or (receiver is not None and not user_exists(receiver)):
        return -1  # Un des utilisateurs n'existe pas

    if group_id is None:
        query = """INSERT INTO MESSAGES (content, sender, receiver) VALUES (?,?,?)"""
        _execute(query, (content, sender, receiver))
    else:
        query = """INSERT INTO MESSAGES (content, sender, group_id) VALUES (?,?,?)"""
        _execute(query, (content, sender, group_id))
    
    return 0


def delete_msg(msg_id : int) -> int :
    """ Supprime un message envoyé, identifié par son id
    In : msg_id : id du message
    Out : 
        -1 si id invalide
        0 si le msg a bien été supprimé
    """
    if type(msg_id) != int :
        return -1 # id incorrect
    query = """SELECT content FROM MESSAGES
    WHERE msg_id = ?;
    """
    if _execute(query, (msg_id,)) == [] :
        return -1 # Message inexistant
    else :
        query = """DELETE FROM MESSAGES
        WHERE msg_id = ?;
        """
        _execute(query, (msg_id,))
        return 0
    
 
def list_msg() -> int :
    """determine la liste des messages dans la table messages
    Out : liste des messages et de leurs infos
    """
    query = """SELECT * FROM MESSAGES"""
    return _execute(query)


def add_group(name : str, owner : str, members : list) -> int :
    """ Créer un nouveau groupe avec au moins 3 participants
    In : name : Nom du groupe
         owner : username du créateur du groupe
         members : liste des usernames des membres présents dans le groupe
    Out :
        -1 si un username est invalide ou si moins de 3
        0 si le groupe a bien été crée
    """
    if len(members) < 2 or type(owner) != str or not user_exists(owner) :
        return -1 # Pas assez ou owner invalide

    people = owner + ';'
    for member in members :
        if type(member) != str :
            return -1 # Username d'un membre pas str
        elif not user_exists(member) :
            return -1 # Username d'un membre invalide
        
        people += member + ';' 
    
    query = """ INSERT INTO GROUPS (name, members)
    VALUES (?, ?);
    """
    _execute(query, (name, people[:-1]))
    return 0


def delete_group(group_id : int) -> int :
    """ Supprime un groupe identifié par son id
    In : group_id : id du groupe a supprimé
    Out :
        -1 si group_id invalide
        0 si le groupe a bien été supprimé
    """
    if type(group_id) != int :
        return -1 # id incorrect
    query = """SELECT name FROM GROUPS
    WHERE group_id = ?;
    """
    if _execute(query, (group_id,)) == [] :
        return -1 # Groupe inexistant
    else :
        query = """DELETE FROM GROUPS
        WHERE group_id = ?;
        """
        _execute(query, (group_id,))
        return 0


def members_in_group(group_id : int) -> list :
    """ Affiche la liste des utilisateurs présents dans un groupe
    In : group_id : id du groupe
    Out : members : liste des utilisateurs
        -1 si id invalide
    """
    query = """SELECT members FROM GROUPS
    WHERE group_id = ?; 
    """
    people = _execute(query ,(group_id,))
    if people == [] :
        return -1 # id invalide
    else :
        people = people[0][0]
    members = []
    for member in people.split(";") :
        members.append(member)
    return sorted(members)


def add_story(user : str, image : str) -> int :
    """ Ajoute une story
    In : user : username de celui qui poste la story
         image : url de l'image affichée en story
    Out :
        -1 si paramètres invalides
        0 si story bien postée
    """
    if type(image) != str or type(user) != str or not user_exists(user) :
        return -1 # Paramètres invalides

    query = """SELECT story_id FROM STORIES
    ORDER BY story_id DESC
    """
    id = _execute(query)
    if id == [] :
        id = 1
    else :
        id = id[0][0] + 1

    url = f'Stories/{id}.png'

    try :
        img = Image.open(image) 
        img.save(url)
    except FileNotFoundError :
        return -1 # Image introuvable

    query = """ INSERT INTO STORIES (story_id, poster, image)
    VALUES (?, ?, ?);
    """
    _execute(query, (id, user, url)) # Ajout de l'id au cas ou la dernière story a été supprimée
    return 0


def delete_story(story_id : int) -> int:
    """ Permet de supprimer une story
    In : story_id : id de la story a supprimer
    Out : -1 si erreur ou argument invalide, 0 sinon
    """
    if isinstance(story_id, int):  # On vérifie le type de l'argument
        query = """SELECT story_id FROM STORIES WHERE story_id=?"""
        if _execute(query, (story_id,)) != []:  # On vérifie que la story existe
            query = """DELETE FROM STORIES WHERE story_id=?"""
            _execute(query, (story_id,))  # On supprime la story 
            return 0  # On renvoie 0 car tout s'est bien passé
    return -1  # Erreur ou arguments invalides


def _test_passed(function_name):
    print("Tests passés pour", str(function_name))
    

if TESTING:
    from os import remove

    # Creation d'une BDD temporaire pour les tests
    testDb_file = open('test.db', 'x')
    testDb_file.close()

    # Creation des relations dans la base de données: (On est obligés de le faire en deux fois avec 
    # la methode execute de sqlite 3)
    create_tables = [
        """CREATE TABLE "USERS" (
            "username"    TEXT NOT NULL,
            "name"    TEXT NOT NULL,
            "mail"    TEXT NOT NULL UNIQUE,
            "password"    TEXT NOT NULL,
            "bio"    TEXT NULL,
            PRIMARY KEY("username")
        );
        """,
        """CREATE TABLE "FRIENDS" (
            "user_name"    TEXT NOT NULL,
            "friend_name"    TEXT NOT NULL,
            PRIMARY KEY("user_name","friend_name"),
            FOREIGN KEY("user_name") REFERENCES "USERS"("username"),
            FOREIGN KEY("friend_name") REFERENCES "USERS"("username")
        );
        """,
        """CREATE TABLE "GROUPS" (
            "group_id"    INTEGER NOT NULL,
            "name"    TEXT NOT NULL,
            "members"    TEXT NOT NULL,
            PRIMARY KEY("group_id" AUTOINCREMENT)
        );
        """,
        """CREATE TABLE "MESSAGES" (
            "msg_id"    INTEGER NOT NULL,
            "content"    VARCHAR(1000) NOT NULL,
            "sender"    TEXT NOT NULL,
            "receiver"    TEXT NULL,
            "group_id"    INTEGER NULL,
            "date"  DATETIME DEFAULT (datetime('now','localtime')),
            FOREIGN KEY("receiver") REFERENCES "USERS"("username"),
            FOREIGN KEY("sender") REFERENCES "USERS"("username"),
            FOREIGN KEY("group_id") REFERENCES "GROUPS"("group_id"),
            CHECK("receiver" NOT NULL OR "group_id" NOT NULL),
            PRIMARY KEY("msg_id" AUTOINCREMENT)
        );
        """,
        """CREATE TABLE "STORIES" (
            "story_id"	INTEGER NOT NULL,
            "poster"	TEXT NOT NULL,
            "image"	TEXT NOT NULL,
            "views"	INTEGER NOT NULL DEFAULT 0,
            "date"	DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
            PRIMARY KEY("story_id" AUTOINCREMENT),
            FOREIGN KEY("poster") REFERENCES "USERS"("username")
        );
        """]

    # On ajoutes des données dans les relations
    inserts = [
        """INSERT INTO USERS (username, name, mail, password) VALUES ('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123'), 
    ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon'),
    ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut')
        """,
    """INSERT INTO FRIENDS (user_name, friend_name) VALUES ('JexisteDeja', 'JeSuisDejaAmi')
        """,
    """INSERT INTO GROUPS (name, members) VALUES ("lol", "ninobg74;JexisteDeja;JeSuisDejaAmi")
        """,
    """INSERT INTO STORIES (poster, image) VALUES ('ninobg74', 'Stories/1.png')
        """]
    
    # On éxécute le code sql
    for create_table in create_tables:
        _execute(create_table)
        
    for insert in inserts:
        _execute(insert)

    # Tests pour add_user() :
    # On verifie que la table USERS contient les bonnes informations
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None)]
    _test_passed("list_users")
    # On vérifie que en passant des arguments du mauvais type, la fonction renvoie une erreur et que la table USERS n'a pas été modifiée
    assert add_user(1, 1, 1, 1) == -1
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None)]
    # On vérifie qu'essayer d'entrer un utilisateur avec un nom d'utilisateur déjà existant renvoie une erreur et que que la table USERS n'a pas été modifiée
    assert add_user('JexisteDeja', 'eoiokdeo', 'pasmoi@mail.fr', 'deded') == -1
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None)]
    # On vérifie qu'essayer d'entrer un utilisateur dont l'adresse email est déjà utilisée renvoie une erreur et que la table USERS n'a donc pas été modifiée
    assert add_user('JexistePas', 'MoiOnSenFiche', 'existe.deja@mail.fr', 'MoiAussiOnSenFiche', None) == -1
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None)]
    # On vérifie qu'ajouter un utilisateur donc l'adresse email et le nom d'utilisateur n'existent pas ne renvoie pas d'erreur et  que la table USERS a été modifiée en conséquent
    assert add_user('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty') == 0
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None),
                            ('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty', None)]
    _test_passed("add_user")

    # Tests pour remove_user() :
    # On vérifie que passer un argument de mauvais type renvoie une erreur et ne modifie pas la table USERS
    assert remove_user(1) == -1
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None),
                            ('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty', None)]
    # On vérifie que supprimer un utilisateur inexistant renvoie une erreur et ne modifie pas la table USERS
    assert remove_user('JeNexistePas') == -1 # JeNexistePas n'est pas présent dans la bdd
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None),
                            ('NouvelUtilisateur', 'dedede', 'nouveau@gmail.com', 'azerty', None)]
    # On vérifie que supprimer un utilisateur existant ne renvoie pas d'erreur et modifie bien la table USERS
    assert remove_user('NouvelUtilisateur') == 0
    assert list_users() == [('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123', None),
                            ('JeSuisDejaAmi', 'Deja Ami', 'jesuisdejaami@gmail.com', 'lesbananescesttropbon', None),
                            ('ninobg74', 'Nino Faust', 'faust.nino@gmail.com', 'jaimelansimaischut', None)]
    _test_passed("remove_user")

    # Tests pour is_friend():
    assert is_friend(1, 1) == -1
    # On teste que la fonction renvoie:
    # Une erreur si l'utilisateur auquel on vérifie si un autre utilisateur est son ami n'existe pas
    assert is_friend("JeNexistePas", "JexisteDeja") == -1
    # Une erreur si l'ami recherché n'existe pas dans la BDD
    assert is_friend("JexisteDeja", "JeNexistePas") == -1
    # False si l'ami existe dans la BDD mais n'est pas notre ami
    assert is_friend("JexisteDeja", "ninobg74") == False
    # True si l'ami existe dans la BDD et est notre ami
    assert is_friend("JexisteDeja", "JeSuisDejaAmi") == True
    _test_passed('is_friend')
    
    # Tests pour list_friends():
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi']
    # assert list_friends(2) == -1 # Pas str
    # assert list_friends('JexistePas') == -1 # Username invalide
    _test_passed("list_friends")

    # Tests pour add_friend():
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi']
    assert add_friend('JexisteDeja', 'JeSuisDejaAmi') == -1 # Déjà amis
    assert add_friend('cortex', 91) == -1 # Username pas str
    assert add_friend('JexisteDeja', 'ninobg74') == 0 # All good
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi','ninobg74'] # On vérifie que ça a bien marché
    _test_passed("add_friend")

    # Tests pour remove_friend():
    # On vérifie que si l'argument n'est pas du bon type, la fonction renvoie une erreur et la liste d'amis n'est pas modifiée
    assert remove_friend(1, 1) == -1
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi','ninobg74']
    # On vérifie que si on tente de supprimer un ami que l'on a pas, la fonction renvoie une erreur et la liste d'amis n'es pas modifiée
    assert remove_friend('JexisteDeja', 'loulou74490') == -1
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi','ninobg74']
    # On vérifie que si on tente de supprimer un ami de qqn qui n'existe pas, la fonction renvoie une erreur et la liste d'amis n'est pas modifiée
    assert remove_friend('JeNexistePas', 'ninobg74') == -1
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi','ninobg74']
    # On vérifie que si on supprime un ami, la fonction ne renvoie pas d'erreur et la liste d'amis est modifiée en conséquent
    assert remove_friend('JexisteDeja', 'ninobg74') == 0
    assert list_friends('JexisteDeja') == ['JeSuisDejaAmi']
    _test_passed('remove_friend')

    # Tests pour add_group() : 
    assert add_group('Groupe de raisin', 'ninobg74', ['JexisteDeja']) == -1 # Que 2 participants => discussion normale pas groupe
    assert add_group('Télétubbies', 'Tinky Winky', ['Dipsy','Lala']) == -1 # Usernames inexistants
    assert add_group('Restez groupir', 'ninobg74', ['JexisteDeja','JeSuisDejaAmi']) == 0 # All good
    _test_passed('add_group')

    # Tests pour members_in_group() :
    assert members_in_group(1) == ['JeSuisDejaAmi', 'JexisteDeja', 'ninobg74']
    assert members_in_group(0) == -1 # Groupe inexistant
    _test_passed('members_in_group')

    # Tests pour delete_group() :
    assert delete_group(0) == -1 # Groupe inexistant
    assert delete_group('1') == -1 # id pas int
    assert delete_group(1) == 0 # All good
    assert members_in_group(1) == -1 # verif que groupe supprimé
    _test_passed('delete_group')

    # Test pour send_msg():
    # (On ne peut pas vérifier que la relation n'est pas modifiée car ce qu'elle contient dépend de l'heure au moment du test)
    # On vérifie que la fonction renvoie une erreur ) si :
    # un ou plusieurs arguments n'est pas du bon type :
    assert send_msg(1, 1) == -1
    # l'expéditeur est le même que le destinataire :
    assert send_msg("Salut", "ninobg74", receiver='ninobg74') == -1
    # On tente de rentrer a la fois un nom de destinataire et un id de groupe:
    assert send_msg("Salut", "ninobg74", receiver='JexisteDeja', group_id='28484389') == -1
    # le message est vide :
    assert send_msg("", "ninobg74", receiver="JexisteDeja") == -1
    # un ou les utilisateurs n'existent pas :
    assert send_msg("Salut", "JeNexistePas", receiver="JexisteDeja") == -1
    assert send_msg("Salut", "JexisteDeja", receiver="JeNexistePas") == -1
    # Si toutes les conditions sont respectées, on vérifie que la fonction en renvoie pas d'erreur pour un groupe et en privé
    assert send_msg("Salut louis", "ninobg74", receiver="JexisteDeja") == 0
    assert send_msg("Salut les gens", "ninobg74", group_id=2) == 0
    _test_passed('send_msg')

    # Tests pour delete_msg() :
    assert delete_msg('Salut') == -1 # Pas int
    assert delete_msg(0) == -1 # Message inexistant
    assert delete_msg(1) == 0 # Good
    _test_passed('delete_msg')

    # Tests pour add_story():
    assert add_story('InconnuAuBataillon', 'image.png') == -1 # Username invalide
    assert add_story(74, 'test.png') == -1 # Username pas str
    assert add_story('JexisteDeja', 12) == -1 # Image pas str
    assert add_story('ninobg74', 'imageinexistante.png') == -1 # Image inexistante
    assert add_story('JexisteDeja', 'Stories/1.png') == 0 # All good
    t = input('')
    remove('Stories/2.png')
    _test_passed("add_story")

    # Tests pour delete_story():
    assert delete_story("salut") == -1
    assert delete_story(1000) == -1
    assert delete_story(1) == 0
    _test_passed("delete_story")


    # On supprime la BDD temporaire
    t = input('')  # wait before deleting test.db
    remove('test.db')
