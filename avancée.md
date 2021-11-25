## Hamstergram API

L'api est une api de messagerie pour réseau social. <br>
Elle integrera des fonctions pour créer un utilisateur et en supprimer. <br>
Ajouter et supprimer des amis. <br>
Voir sa liste d'amis et savoir si on est ami avec quelqu'un. <br>
Créer et supprimer un groupe. <br>
Voir les utilisateurs présents dans un groupe. <br>
Envoyer un message à quelqu'un ou dans un groupe.


##### Nino : 
- fonction add_user() pour ajouter un utilisateur
- fonction list_friends() pour voir sa liste d'amis
- fonction remove_friend() pour supprimer quelqu'un en ami
- send_msg() pour envoyer un message à quelqu'un ou dans un groupe
- delete_msg() pour supprimer un message 

##### Louis :
- fonction remove_user() pour supprimer un utilisateur
- fonction is_friend() pour vérifier si des utilisateurs sont déjà amis
- fonction add_friend() pour ajouter quelqu'un en ami
- fonction add_group() pour créer un nouveau groupe
- fonction members_in_group() pour voir la liste des utilisateurs présent dans un groupe
- fonction delete_group() pour supprimer un groupe déjà créé


#### Schéma relationnel :
USERS(<u>username : TEXT</u>, name : TEXT, mail : TEXT (Unique), password : TEXT, bio : TEXT (Null))

FRIENDS(<u>#user_name : TEXT, #friend_name : TEXT</u>)

MESSAGES(<u>id : INT</u>, message : VARCHAR(1000), #sender : TEXT, #receiver : TEXT (Null), #group_id :INT (Null), date : DATETIME (Default : Current_timestamp))

GROUPES(<u>group_id : INT</u>, name : TEXT, members : TEXT)
<u>tettedtgtedgtegdtdggdtge</u>
