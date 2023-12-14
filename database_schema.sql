CREATE DATABASE rabbithole;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    pfpic VARCHAR(255) NULL,
    bio TEXT NULL,
    hashpw VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (username, email)
);

CREATE TABLE IF NOT EXISTS community (
    id SERIAL NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    subject VARCHAR(255) NOT NULL,
    pfpic VARCHAR(255) NULL,
    owner_id SERIAL NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_owner_id
        FOREIGN KEY (owner_id)
            REFERENCES users(id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS user_community (
    uc_id SERIAL NOT NULL,
    user_id SERIAL NOT NULL ,
    community_id SERIAL NOT NULL,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users(id),
    CONSTRAINT fk_community_id
        FOREIGN KEY (community_id)
            REFERENCES community(id) ON DELETE CASCADE,
    PRIMARY KEY (uc_id),
    UNIQUE(user_id, community_id)
);

CREATE TABLE IF NOT EXISTS post (
    id SERIAL NOT NULL,
    time_created VARCHAR(25) NOT NULL,
    title VARCHAR(255) NOT NULL,
    image VARCHAR(255) NULL,
    content TEXT NOT NULL,
    uc_id SERIAL NOT NULL,
    owner VARCHAR(255) NOT NULL,
    reply_count INTEGER NOT NULL,
    community VARCHAR(255) NOT NULL,
    CONSTRAINT fk_uc_id
        FOREIGN KEY (uc_id)
            REFERENCES user_community(uc_id) ON DELETE CASCADE,
    CONSTRAINT fk_owner
        FOREIGN KEY (owner)
            REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_community
        FOREIGN KEY (community)
            REFERENCES community(name),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS reply (
    id SERIAL NOT NULL,
    time_created VARCHAR(25) NOT NULL,
    content TEXT NOT NULL,
    post_id SERIAL NOT NULL,
    owner VARCHAR(255) NOT NULL,
    CONSTRAINT fk_owner
        FOREIGN KEY (owner)
            REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_post_id
        FOREIGN KEY (post_id)
            REFERENCES post(id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);