## Hamstergram API

L'api est une api de messagerie pour réseau social. <br>
Elle integrera des fonctions pour créer un utilisateur et en supprimer. <br>
Ajouter et supprimer des amis. <br>
Voir sa liste d'amis et savoir si on est ami avec quelqu'un.


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

DISCUSSIONS(<u>#sender_name : TEXT, #receiver_name : TEXT</u>)

MESSAGES(<u>#disc_id : INT, msg_id = INT<u>, content : VARCHAR(1000))
