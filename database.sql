-- Create the image_db database if it doesn't exist
CREATE DATABASE IF NOT EXISTS image_db;

-- Use the image_db database
USE image_db;

-- Create a table to store uploaded images
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store object tags associated with images
CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT,
    tag_name VARCHAR(255) NOT NULL,
    confidence FLOAT,
    FOREIGN KEY (image_id) REFERENCES images(id)
);

-- Sample data for testing purposes
INSERT INTO images (filename, filepath) VALUES ('example.jpg', 'static/images/example.jpg');
INSERT INTO tags (image_id, tag_name, confidence) VALUES (1, 'cat', 0.95);
INSERT INTO tags (image_id, tag_name, confidence) VALUES (1, 'animal', 0.88);
