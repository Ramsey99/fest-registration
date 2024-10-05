-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS event_database;

-- Use the created database
USE event_database;

-- Create the registrations table with an additional column for profile picture
CREATE TABLE IF NOT EXISTS registrations (
    roll VARCHAR(20) PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phno VARCHAR(15) NOT NULL,
    stream VARCHAR(10) NOT NULL,
    event VARCHAR(20) NOT NULL,
    profile_pic VARCHAR(255) DEFAULT NULL  -- New column for profile picture
);

-- Create an index on the email column for faster searches
CREATE INDEX idx_email ON registrations(email);

-- Create a view to list all registrations
CREATE VIEW view_registrations AS
SELECT roll, fullname, email, phno, stream, event, profile_pic FROM registrations;

-- Create a stored procedure to add a new registration with a duplicate check and profile pic
-- Drop the existing stored procedure if it exists
DROP PROCEDURE IF EXISTS add_registration;

-- Create the updated stored procedure with 7 parameters
DELIMITER //
CREATE PROCEDURE add_registration(
    IN p_roll VARCHAR(20),
    IN p_fullname VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_phno VARCHAR(15),
    IN p_stream VARCHAR(10),
    IN p_event VARCHAR(20),
    IN p_profile_pic VARCHAR(255)  -- Include profile pic as a parameter
)
BEGIN
    DECLARE existing_roll INT;
    
    -- Check if the roll already exists
    SELECT COUNT(*) INTO existing_roll FROM registrations WHERE roll = p_roll;

    IF existing_roll = 0 THEN
        -- If roll does not exist, insert the new registration
        INSERT INTO registrations (roll, fullname, email, phno, stream, event, profile_pic)
        VALUES (p_roll, p_fullname, p_email, p_phno, p_stream, p_event, p_profile_pic);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate entry for roll';
    END IF;
END //
DELIMITER ;


-- Create a stored procedure to delete a registration by roll number
DELIMITER //
CREATE PROCEDURE delete_registration(
    IN p_roll VARCHAR(20)
)
BEGIN
    DELETE FROM registrations WHERE roll = p_roll;
END //
DELIMITER ;

-- Test cases (optional)
SHOW DATABASES;
SHOW TABLES;
DESCRIBE registrations;
SELECT * FROM registrations;
