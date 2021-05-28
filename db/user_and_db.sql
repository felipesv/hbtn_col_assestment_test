-- Database name
CREATE DATABASE orders;

-- User
CREATE USER 'hbtn_orders'@'localhost' IDENTIFIED BY '12345678';
CREATE USER 'hbtn_orders'@'%' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON *.* TO 'hbtn_orders'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'hbtn_orders'@'%';
