CREATE DATABASE rabbithole;

CREATE TABLE users (
    user_id SERIAL NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_pfpic VARCHAR(255),
    user_bio TEXT NULL,
    user_hashpw VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE (user_name, user_email)
);

CREATE TABLE community (
    community_id SERIAL NOT NULL,
    community_name VARCHAR(255),
    pfpic VARCHAR(255),
    owner_id SERIAL NOT NULL,
    PRIMARY KEY (community_id),
    CONSTRAINT fk_owner_id
        FOREIGN KEY (owner_id)
            REFERENCES users(user_id),
    UNIQUE (community_name)
);

CREATE TABLE user_community (
    user_id SERIAL NOT NULL ,
    community_id SERIAL NOT NULL,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users(user_id),
    CONSTRAINT fk_community_id
        FOREIGN KEY (community_id)
            REFERENCES community(community_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, community_id)
);

CREATE TABLE post (
    post_id SERIAL NOT NULL,
    post_time_created DATE NOT NULL,
    post_title VARCHAR(255) NOT NULL,
    post_image VARCHAR(255) NULL,
    post_content VARCHAR(255) NOT NULL,
    user_id SERIAL NOT NULL,
    community_id SERIAL NOT NULL,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id, community_id)
            REFERENCES user_community(user_id, community_id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, user_id, community_id)
);