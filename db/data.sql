USE orders;

INSERT INTO users
	(user_name, user_last_name, user_gov_id, user_email, user_password, user_company)
VALUES 
	('Jhon', 'Doe', "1F2G45J8K2", 'jhon.doe@xmail.com', '123', 'Apple'),
	('Sara', 'Bush', "5T3Y4U5H4I6", 'sara.bsh@xmail.com', '123', 'Facebook'),
	('Maxi', 'Tyler', "8R7B3N3I5P7", 'max.tyler@xmail.com', '123', 'Tesla'),
	('Jordan', 'Caicedo', "4D391K3M49M", 'jordan.c@xmail.com', '123', 'Tesla');

INSERT INTO orders
	(orders_subtotal, orders_taxes, orders_total, orders_paid, user_id)
VALUES 
	(50, 50, 100, TRUE, 1),
	(50, 20, 70, TRUE, 2),
	(170, 30, 200, FALSE, 3),
	(190, 30, 220, TRUE, 4);

INSERT INTO shipping
	(shipping_address, shipping_city, shipping_state, shipping_country, shipping_cost, order_id)
VALUES 
	('Street x No. 1234412', 'NY', 'NY', 'United States', 100, 1),
	('Street y No. 4434344', 'Las Vegas', 'Nevada', 'United States', 230, 2),
	('Street z No. 6565656', 'LA', 'California', 'United States', 200, 3),
	('Street z No. 6565656', 'LA', 'California', 'United States', 200, 4);

INSERT INTO payment
	(payment_type, payment_txn_id, payment_total, payment_status, order_id)
VALUES 
	('cash', 12352, 200, 'ok', 1),
	('credit card', 12463, 300, 'ok', 2),
	('bank check', 14563, 400, 'process', 3),
	('cash', 11830, 440, 'process', 4);
