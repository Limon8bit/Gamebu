CREATE USER admin WITH password 'admin';
CREATE DATABASE prod_db;
GRANT ALL privileges ON DATABASE prod_db TO admin;