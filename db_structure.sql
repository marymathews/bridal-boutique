CREATE SCHEMA boutique;
CREATE TABLE account (
    email VARCHAR(320) PRIMARY KEY, 
    name VARCHAR(100), 
    h_password BINARY(60), 
    is_admin BOOLEAN
);
CREATE TABLE category (
    category_id CHAR(4) PRIMARY KEY, 
    category_name VARCHAR(20), 
    frame_id VARCHAR(10)
);
CREATE TABLE item ( 
    item_id INT PRIMARY KEY AUTO_INCREMENT, 
    quantity INT NOT NULL, 
    price FLOAT(11,2) NOT NULL, 
    category_id CHAR(4) NOT NULL, 
    item_name VARCHAR(30) NOT NULL, 
    item_description VARCHAR(300) NOT NULL, 
    deleted BOOLEAN, 
    CONSTRAINT item_cat_fk FOREIGN KEY(category_id) REFERENCES category(category_id)
);
CREATE TABLE item_size ( 
    item_id INT, 
    size ENUM('0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20') NOT NULL, 
    PRIMARY KEY(item_id, size), 
    CONSTRAINT size_item_fk FOREIGN KEY(item_id) REFERENCES item(item_id) 
);
CREATE TABLE item_images (
    item_id INT,
    image_id VARCHAR(10),
    PRIMARY KEY(image_id, item_id),
    CONSTRAINT image_item_fk FOREIGN KEY(item_id) REFERENCES item(item_id)
);
CREATE TABLE tag ( 
    tag_id INT PRIMARY KEY AUTO_INCREMENT, 
    tag_name VARCHAR(30) NOT NULL 
);
CREATE TABLE item_tag (
	item_id INT,
	tag_id INT,
	PRIMARY KEY(item_id, tag_id),
	FOREIGN KEY(item_id) REFERENCES item(item_id),
	FOREIGN KEY(tag_id) REFERENCES tag(tag_id)
);
CREATE TABLE appointment (
	appt_id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(320) NOT NULL,
	appt_date DATE NOT NULL,	
	appt_start_time TIME NOT NULL,
	FOREIGN KEY(email) REFERENCES account(email)
);
CREATE TABLE appointment_items (
	appt_id INT,
	item_id INT,
	PRIMARY KEY(appt_id, item_id),
    FOREIGN KEY(item_id) REFERENCES item(item_id),
	FOREIGN KEY(appt_id) REFERENCES appointment(appt_id)
);
CREATE TABLE wishlist (
	email VARCHAR(320),
	item_id INT,
	PRIMARY KEY(email, item_id),
	FOREIGN KEY(item_id) REFERENCES item(item_id),
	FOREIGN KEY(email) REFERENCES account(email)
);


