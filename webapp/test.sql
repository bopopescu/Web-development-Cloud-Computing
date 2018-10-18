use Test;
CREATE TABLE userinfo (
	userName varchar(30) NOT NULL UNIQUE,
    userEmail varchar(255) NOT NULL UNIQUE,
    userPwd varchar(255) NOT NULL,
    userSalt varchar(255) NOT NULL,
    PRIMARY KEY (userName)
);
