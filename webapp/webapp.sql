CREATE DATABASE Test;
CREATE TABLE UserInfo (
	userName varchar(30) NOT NULL,
    userEmail varchar(255) NOT NULL,
    userPwd varchar(255) NOT NULL,
    userSalt varchar(255) NOT NULL,
    PRIMARY KEY (userName)
);

CREATE TABLE user2Images (
    userName varchar(30) NOT NULL,
    Thumbnail varchar(500) NOT NULL,
    original varchar(500) NOT NULL,
    trans_a varchar(500) NOT NULL,
    trans_b varchar(500) NOT NULL,
    trans_c varchar(500) NOT NULL,
    CONSTRAINT P_KEY PRIMARY KEY (userName,Thumbnail)
);




