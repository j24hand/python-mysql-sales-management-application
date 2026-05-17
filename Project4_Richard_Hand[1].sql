-- Richard Hand 
-- CGS2545C-26Spring 0001
-- Assignment: Project 4
-- 4/26/2026


-- Select the project4 database
USE project4;


-- Create stored procedure to register a new customer user
DELIMITER $$

CREATE PROCEDURE registerNewUser(
    IN U_name VARCHAR(255),
    IN U_Pass VARCHAR(255)
)
BEGIN 
    -- Insert a new user into the users table with customer role 2
    INSERT INTO users(username, pass, userRole)
    VALUES (U_name, U_Pass, 2);
END $$

DELIMITER ;


-- Create stored procedure to login with username and password
DELIMITER $$

CREATE PROCEDURE loginWithCreds(
    IN p_username VARCHAR(255),
    IN p_pass VARCHAR(255)
)
BEGIN
    -- Return the user id, username, and role if the login matches
    SELECT id, username, userRole
    FROM users
    WHERE username = p_username AND pass = p_pass;
END $$

DELIMITER ;


-- Create stored procedure to edit an existing product
DELIMITER $$

CREATE PROCEDURE editExistingProduct(
    IN p_id INT,
    IN p_name VARCHAR(255),
    IN p_price DECIMAL(10,2)
)
BEGIN
    -- Update the selected product with the new name and price
    UPDATE product
    SET prodName = p_name,
        price = p_price
    WHERE id = p_id;
END $$

DELIMITER ;


-- Create stored procedure to get the total of all sales
DELIMITER $$

CREATE PROCEDURE getSalesTotal()
BEGIN
    -- Add up all totals from the sale table
    SELECT SUM(total) AS T_sales
    FROM sale;
END $$

DELIMITER ;


-- Create stored procedure to display all products
DELIMITER $$

CREATE PROCEDURE getAllProducts()
BEGIN
    -- Return all product ids, names, and prices
    SELECT id, prodName, price
    FROM product;
END $$

DELIMITER ;


-- Create stored procedure to submit a customer order
DELIMITER $$

CREATE PROCEDURE submitOrder(
    IN p_userID INT,
    IN p_prodID INT,
    IN p_qty INT
)
BEGIN
    -- Insert a new sale using the selected product and quantity
    INSERT INTO sale(prodID, userID, qty, total)
    SELECT id, p_userID, p_qty, price * p_qty
    FROM product
    WHERE id = p_prodID;
END $$

DELIMITER ;


-- Create stored procedure to view all orders for one customer
DELIMITER $$

CREATE PROCEDURE viewCustomerOrders(
    IN p_userID INT
)
BEGIN
    -- Return the sale id, quantity, product name, and total for the customer
    SELECT s.saleID, s.qty, p.prodName, s.total
    FROM sale s
    JOIN product p ON s.prodID = p.id
    WHERE s.userID = p_userID;
END $$

DELIMITER ;


-- Create stored procedure to cancel an order
DELIMITER $$

CREATE PROCEDURE cancelOrder(
    IN p_saleID INT
)
BEGIN
    -- Delete the selected sale record
    DELETE FROM sale
    WHERE saleID = p_saleID;
END $$

DELIMITER ;


-- Create stored procedure to add a new product
DELIMITER $$

CREATE PROCEDURE submitNewProduct(
    IN p_name VARCHAR(255),
    IN p_price DECIMAL(10,2)
)
BEGIN
    -- Insert a new product with the given name and price
    INSERT INTO product(prodName, price)
    VALUES (p_name, p_price);
END $$

DELIMITER ;