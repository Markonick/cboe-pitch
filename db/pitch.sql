CREATE DATABASE pitch;
\c pitch

CREATE TABLE message_type (
  id INT PRIMARY KEY NOT NULL,
  description TEXT
);

CREATE TABLE message_metadata (
  id SERIAL PRIMARY KEY NOT NULL,
  total INT
);

INSERT INTO message_type (id, description) VALUES 
(0, 'Symbol Clear'), 
(1, 'Add Order (Short)'), 
(2, 'Add Order (Long)'), 
(3, 'Order Executed'), 
(4, 'Order Cancel'), 
(5, 'Trade (Short)'), 
(6, 'Trade (Long)'), 
(7, 'Trade Break'), 
(8, 'Trading Status'), 
(9, 'Auction Update'), 
(10, 'Auction Summary');