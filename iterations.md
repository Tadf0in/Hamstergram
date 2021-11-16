## Itération 1 :

#### 1)
L'api est une api de messagerie pour réseau social. Elle integrera des fonctions pour créer un utilisateur et en supprimer

Nino : fonction create_user() pour ajouter un utilisateur
Louis : fonction remove_user() pour supprimer un utilisateur

#### 2)

USERS(<u>username : TEXT</u>, name : TEXT, mail : TEXT (Unique), password : TEXT, bio : TEXT (Null))

#### 3)

```py
CREATE TABLE "USERS" (
    "username" TEXT  NOT NULL ,
    "name" TEXT  NOT NULL ,
    "mail" TEXT  NOT NULL ,
    "password" TEXT  NOT NULL ,
    "bio" TEXT  NULL ,
    CONSTRAINT "pk_USERS" PRIMARY KEY (
        "username"
    ),
    CONSTRAINT "uk_USERS_mail" UNIQUE (
        "mail"
    )
)
```

#### 4)

```py
add_user(username : str, name : str, mail : str, password : str, bio : str =''):
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

remove_user(username):
    """ Supprime l'utilisateur 
    In : username (str) : username d'un utilisateur inscrit
    Out :
        Retourne -1 si l'username est invalide
        Retourne 0 si l'utilisateur a bien été supprimé
    """
```

#### 5)

```py
if __name__ == '__main__':
    # Tests pour add_user() :
    assert add_user('JexisteDeja', 'eoiokdeo', 'existe.deja@mail.fr', 'deded') == -1
    assert add_user('JeNexistePas', 'dedede', 'moinonplus@gmail.com', 'azerty') == 0

    # Tests pour remove_user() :
    _update_db(_creer_connexion('test.db'), 'test.sql')
    assert remove_user(1) == -1
    assert remove_user('JeNexistePas') == -1 # JeNexistePas n'est pas présent dans la bdd
    assert remove_user('JexisteDeja') == 0
    print("Tests passés pour remove_user")
```

test.sql : 
```sql
INSERT INTO USERS (username, name, mail, password) VALUES ('JexisteDeja', 'Existe Deja', 'existe.deja@mail.fr', 'azerty123');
```

#### 6)

```py
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
```
