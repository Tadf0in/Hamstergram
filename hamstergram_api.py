"""
API de messagerie pour Hamstramgram.

GitHub : https://github.com/Tadf0in/Hamstergram
"""


def add_friend(friend_name):
    """ Fonction pour ajouter un utilisateur en ami.

    In : friend_name (str) : correspond au nom d'utilisateur d'un utilisateur enregistré
    Out :
    Retourne -1 si les conditions ne sont pas respectées
    """
    if type(friend_name) != str():
        return -1