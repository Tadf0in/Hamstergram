## Hamstergram API

L'api est une api de messagerie pour réseau social. 
Elle integrera des fonctions pour créer un utilisateur et en supprimer. 
Ajouter et supprimer des amis, voir sa liste d'amis.


##### Nino : 
- fonction add_user() pour ajouter un utilisateur
- fonction list_friends() pour voir sa liste d'amis
- fonction remove_friend() pour supprimer quelqu'un en ami

##### Louis :
- fonction remove_user() pour supprimer un utilisateur
- fonction is_friend() pour vérifier si des utilisateurs sont déjà amis
- fonction add_friend() pour ajouter quelqu'un en ami


#### Schéma relationnel :
USERS(<u>username : TEXT</u>, name : TEXT, mail : TEXT (Unique), password : TEXT, bio : TEXT (Null))

FRIENDS(<u>#user_name : TEXT, #friend_name : TEXT</u>)
