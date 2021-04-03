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
CREATE TABLE item_images
(
    item_id INT,
    image_id VARCHAR(10),
    PRIMARY KEY(image_id, item_id),
    CONSTRAINT image_item_fk FOREIGN KEY(item_id) REFERENCES item(item_id)
);

