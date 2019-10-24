CREATE DATABASE pitch;
\c pitch

CREATE TABLE message_types (
  id INT PRIMARY KEY NOT NULL,
  description TEXT
);

INSERT INTO message_types (id, description) VALUES (1, 'Order add'), (2, 'Order execute');