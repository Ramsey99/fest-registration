
-- Create the database
CREATE DATABASE IF NOT EXISTS event_database;
USE event_database;

-- Create the registrations table
CREATE TABLE IF NOT EXISTS registrations (
    roll VARCHAR(20) PRIMARY KEY,
    fullname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phno VARCHAR(15) NOT NULL,
    stream VARCHAR(10) NOT NULL,
    event VARCHAR(20) NOT NULL
);

-- Create an index on the email column for faster searches
CREATE INDEX idx_email ON registrations(email);

-- Create a view to list all registrations
CREATE VIEW view_registrations AS
SELECT roll, fullname, email, phno, stream, event FROM registrations;

-- Create a stored procedure to add a new registration with a duplicate check
DELIMITER //
CREATE PROCEDURE add_registration(
    IN p_roll VARCHAR(20),
    IN p_fullname VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_phno VARCHAR(15),
    IN p_stream VARCHAR(10),
    IN p_event VARCHAR(20)
)
BEGIN
    DECLARE existing_roll INT;
    
    -- Check if the roll already exists
    SELECT COUNT(*) INTO existing_roll FROM registrations WHERE roll = p_roll;

    IF existing_roll = 0 THEN
        -- If roll does not exist, insert the new registration
        INSERT INTO registrations (roll, fullname, email, phno, stream, event)
        VALUES (p_roll, p_fullname, p_email, p_phno, p_stream, p_event);
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

-- Test cases
SHOW DATABASES;
SHOW TABLES;
DESCRIBE registrations;
SELECT * FROM registrations;

-- Uncomment the following line if you want to drop the database
-- DROP DATABASE event_database;
