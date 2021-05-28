
USE orders;

DROP TABLE IF EXISTS shipping;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;

-- Tables
CREATE TABLE users(
	user_id VARCHAR(36) NOT NULL,
	user_name VARCHAR(50) NOT NULL,
	user_last_name VARCHAR(50) NOT NULL,
	user_gov_id VARCHAR(20) NOT NULL, 
	user_email VARCHAR(30) NOT NULL UNIQUE,
	user_password VARCHAR(30) NOT NULL,
	user_company VARCHAR(20),
	PRIMARY KEY(user_id)
);

CREATE TABLE orders(
	order_id VARCHAR(36) NOT NULL,
	orders_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	orders_subtotal INT NOT NULL,
	orders_taxes INT NOT NULL,
	orders_total INT NOT NULL,
	orders_paid BOOLEAN NOT NULL,
	user_id VARCHAR(36) NOT NULL,
	PRIMARY KEY(order_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE shipping(
	shipping_id VARCHAR(36) NOT NULL,
	shipping_address VARCHAR(60) NOT NULL,
	shipping_city VARCHAR(15) NOT NULL,
	shipping_state VARCHAR(15) NOT NULL,
	shipping_country VARCHAR(20) NOT NULL,
	shipping_cost INT NOT NULL,
	order_id VARCHAR(36) NOT NULL,
	PRIMARY KEY(shipping_id),
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE payment(
	payment_id VARCHAR(36) NOT NULL,
	payment_type ENUM('cash', 'credit card', 'bank check') NOT NULL,
	payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	payment_txn_id INT NOT NULL, -- transaction id
	payment_total INT NOT NULL,
	payment_status ENUM('ok', 'failed', 'process') NOT NULL,
	order_id VARCHAR(36) NOT NULL,
	PRIMARY KEY(payment_id),
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
