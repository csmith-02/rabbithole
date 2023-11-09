CREATE DATABASE rabbithole;

CREATE TABLE users (
    user_id SERIAL NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_pfpic VARCHAR(255),
    user_hashpw VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE (user_name, user_email)
);

CREATE TABLE community (
    community_id SERIAL NOT NULL,
    community_name VARCHAR(255),
    pfpic VARCHAR(255),
    PRIMARY KEY (community_id),
    UNIQUE (community_name)
);

CREATE TABLE user_community (
    is_owner BOOLEAN NULL,
    user_id SERIAL NOT NULL ,
    community_id SERIAL NOT NULL,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users(user_id),
    CONSTRAINT fk_community_id
        FOREIGN KEY (community_id)
            REFERENCES community(community_id) ON DELETE CASCADE
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
        FOREIGN KEY (user_id)
            REFERENCES users(user_id),
    CONSTRAINT fk_community
        FOREIGN KEY (community_id)
            REFERENCES community(community_id)
);