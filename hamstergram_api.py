"""
Salut je suis un panneau
"""



def add_friend(friend_name):
    """ Fonction pour ajouter un utilisateur en ami.

    In : friend_name (str) : correspond au nom d'utilisateur d'un utilisateur enregistré
    Out :
    Retourne -1 si les conditions ne sont pas respectées
    """
    if type(friend_name) != str():
        return -1

print(add_friend(12))