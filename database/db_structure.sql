CREATE SCHEMA boutique;
CREATE TABLE account (
    email VARCHAR(320) PRIMARY KEY, 
    name VARCHAR(100), 
    h_password BINARY(60), 
    is_admin BOOLEAN
);
CREATE TABLE category (
    category_id CHAR(4) PRIMARY KEY, 
    category_name VARCHAR(50)
);
CREATE TABLE item ( 
    item_id INT PRIMARY KEY AUTO_INCREMENT, 
    price FLOAT(11,2) UNSIGNED NOT NULL, 
    category_id CHAR(4) NOT NULL, 
    item_name VARCHAR(100) NOT NULL, 
    item_description VARCHAR(1000) NOT NULL, 
    deleted BOOLEAN, 
    CONSTRAINT item_cat_fk FOREIGN KEY(category_id) REFERENCES category(category_id)
);
CREATE TABLE item_size ( 
    item_id INT, 
    size ENUM('one-size', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20') NOT NULL, 
    quantity INT UNSIGNED NOT NULL, 
    PRIMARY KEY(item_id, size), 
    CONSTRAINT size_item_fk FOREIGN KEY(item_id) REFERENCES item(item_id) 
);
CREATE TABLE item_images (
    item_id INT,
    image_id VARCHAR(100),
    PRIMARY KEY(image_id, item_id),
    CONSTRAINT image_item_fk FOREIGN KEY(item_id) REFERENCES item(item_id)
);
CREATE TABLE appointment (
	appt_id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(320) NOT NULL,
	appt_date DATE NOT NULL,	
	appt_start_time ENUM('10', '12', '2', '4') NOT NULL,
	FOREIGN KEY(email) REFERENCES account(email)
);
CREATE TABLE appointment_items (
	appt_id INT,
	item_id INT,
    size ENUM('one-size', '0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20'), 
    quantity INT UNSIGNED NOT NULL, 	
    PRIMARY KEY(appt_id, item_id, size),
    FOREIGN KEY(item_id, size) REFERENCES item_size(item_id, size),
	FOREIGN KEY(appt_id) REFERENCES appointment(appt_id)
);
CREATE TABLE wishlist (
	email VARCHAR(320),
	item_id INT,
	PRIMARY KEY(email, item_id),
	FOREIGN KEY(item_id) REFERENCES item(item_id),
	FOREIGN KEY(email) REFERENCES account(email)
);

DELIMITER $$

CREATE TRIGGER update_inventory 
AFTER INSERT 
ON appointment_items FOR EACH ROW 
BEGIN
    UPDATE item_size SET quantity = (quantity - NEW.quantity) WHERE item_id = NEW.item_id AND size = NEW.size; 
END$$

DELIMITER ;