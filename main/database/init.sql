CREATE SCHEMA IF NOT EXISTS test_schema;

SET search_path TO test_schema;

CREATE TABLE IF NOT EXISTS users
(
    slack_id VARCHAR(20) PRIMARY KEY, -- TODO change to a fixed length string
    name TEXT
);

CREATE TABLE IF NOT EXISTS channels
(
    id VARCHAR(20) PRIMARY KEY, -- TODO change to a fixed length string
    name TEXT
);

CREATE TABLE IF NOT EXISTS messages
(
    id            VARCHAR(50) PRIMARY KEY, -- TODO: change to a fixed length string
    time          TIMESTAMP,
    from_slack_id VARCHAR(20) REFERENCES users (slack_id) ON DELETE NO ACTION,
    to_slack_id   VARCHAR(20) REFERENCES users (slack_id) ON DELETE NO ACTION,
    channel_id    VARCHAR(20) REFERENCES channels (id) ON DELETE CASCADE,
    text       TEXT
);

CREATE TABLE IF NOT EXISTS corp_values
(
    id         SERIAL PRIMARY KEY,
    corp_value TEXT
);

CREATE TABLE IF NOT EXISTS kudos
(
    message_id    VARCHAR(30) REFERENCES messages (id) ON DELETE CASCADE,
    corp_value_id INTEGER REFERENCES corp_values (id) ON DELETE CASCADE
);
