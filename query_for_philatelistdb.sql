-- Create the philatelist_db database if it doesn't exist
CREATE DATABASE IF NOT EXISTS philatelist_db;
USE philatelist_db;

-- Buyers table to store buyer information
CREATE TABLE IF NOT EXISTS buyers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sellers table to store seller information
CREATE TABLE IF NOT EXISTS sellers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stamps table to store stamp listings from sellers
CREATE TABLE IF NOT EXISTS stamps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    year_of_manufacture INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    photo_filename VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES sellers(id) ON DELETE CASCADE
);

-- Purchases table to track purchases made by buyers
CREATE TABLE IF NOT EXISTS purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    stamp_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES buyers(id) ON DELETE CASCADE,
    FOREIGN KEY (stamp_id) REFERENCES stamps(id) ON DELETE CASCADE
);

-- View to show available stamps for buyers
CREATE VIEW available_stamps AS
SELECT s.id, s.name, s.year_of_manufacture, s.price, s.description, s.photo_filename
FROM stamps AS s
JOIN sellers AS se ON se.id = s.seller_id;

-- View to show sales made by sellers
CREATE VIEW seller_sales AS
SELECT p.id, s.name AS stamp_name, p.quantity, p.total_amount, p.purchase_date
FROM purchases AS p
JOIN stamps AS s ON s.id = p.stamp_id
WHERE s.seller_id = p.buyer_id;
