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