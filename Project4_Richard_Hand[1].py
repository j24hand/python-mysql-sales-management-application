# Import MySQL connector
import mysql.connector

# Database connection info
mHost = "localhost"
mUsername = "root"
mPassword = "root"
mSchema = "project4"

# Global variables to track logged-in user
currentUserID = None
currentUsername = None
currentRole = None


# Register a new user using stored procedure
def registerNewUser():
    connection = None
    cursor = None

    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=mHost,
            user=mUsername,
            password=mPassword,
            database=mSchema
        )
        cursor = connection.cursor()

        # Get user input
        username = input("What is your desired username?\n>> ")
        password = input("What is your desired password?\n>> ")

        # Call stored procedure
        cursor.callproc("registerNewUser", [username, password])
        connection.commit()

        print("Account created successfully.")

    # Handle duplicate username error
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print("That username already exists. Please choose another username.")
        else:
            print("Database error:", err)

    # Always close connection
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Login user and store session info
def loginWithCreds():
    global currentUserID, currentUsername, currentRole

    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    # Get login credentials
    username = input("What is your username?\n>> ")
    password = input("What is your password?\n>> ")

    # Call login stored procedure
    cursor.callproc("loginWithCreds", [username, password])

    found = False

    # Process results from stored procedure
    for result in cursor.stored_results():
        row = result.fetchone()
        if row:
            currentUserID = row[0]
            currentUsername = row[1]
            currentRole = row[2]
            found = True

    # If login successful
    if found:
        cursor.close()
        connection.close()
        return True
    else:
        print("Invalid login")
        cursor.close()
        connection.close()
        return False


# Add new product admin
def submitNewProduct():
    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    # Get product info
    productName = input("What is the product name?\n>> ")
    productPrice = float(input("What is the product price?\n>> "))

    # Call stored procedure
    cursor.callproc("submitNewProduct", [productName, productPrice])
    connection.commit()

    print("Product added successfully.")

    cursor.close()
    connection.close()


# Edit existing product admin
def editExistingProduct():
    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    # Get updated product info
    productID = int(input("What product ID do you want to edit?\n>> "))
    productName = input("What is the product name?\n>> ")
    productPrice = float(input("What is the product price?\n>> "))

    # Call stored procedure
    cursor.callproc("editExistingProduct", [productID, productName, productPrice])
    connection.commit()

    print("Product updated successfully.")

    cursor.close()
    connection.close()


# Display all products
def getAllProducts():
    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    cursor.callproc("getAllProducts")

    print("Now displaying all products.")

    # Print all rows
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            print(row[0], row[1], row[2])

    cursor.close()
    connection.close()


# Show total sales
def getSalesTotal():
    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    cursor.callproc("getSalesTotal")

    # Print result
    for result in cursor.stored_results():
        row = result.fetchone()
        if row and row[0] is not None:
            print(f"The total Sales is ${row[0]}.")
        else:
            print("The total Sales is $0.00.")

    cursor.close()
    connection.close()


# Submit an order customer
def submitOrder():
    global currentUserID

    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    # Validate product ID input
    while True:
        try:
            productID = int(input("What product ID do you want to order?\n>> "))
            break
        except ValueError:
            print("Please enter a valid product ID number.")

    # Validate quantity input
    while True:
        try:
            quantity = int(input("How many do you want to order?\n>> "))
            break
        except ValueError:
            print("Please enter a valid quantity.")

    # Call stored procedure
    cursor.callproc("submitOrder", [currentUserID, productID, quantity])
    connection.commit()

    # Get product info to display order summary
    cursor.callproc("getAllProducts")
    productName = ""
    productPrice = 0

    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            if row[0] == productID:
                productName = row[1]
                productPrice = row[2]

    total = productPrice * quantity
    print(f"Your order of {quantity} {productName} has been placed for a total of ${total:.2f}.")

    cursor.close()
    connection.close()


# View customer orders
def viewCustomerOrders():
    global currentUserID

    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    cursor.callproc("viewCustomerOrders", [currentUserID])

    print("Now displaying all of your orders.")

    # Print orders
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            print(f"{row[0]} {row[1]}x {row[2]} ${row[3]}")

    cursor.close()
    connection.close()


# Cancel an order
def cancelOrder():
    connection = mysql.connector.connect(
        host=mHost,
        user=mUsername,
        password=mPassword,
        database=mSchema
    )
    cursor = connection.cursor()

    # Validate input
    while True:
        try:
            saleID = int(input("Which order would you like to cancel?\n>> "))
            break
        except ValueError:
            print("Please enter a valid order ID.")

    cursor.callproc("cancelOrder", [saleID])
    connection.commit()

    print("The order has been cancelled.")

    cursor.close()
    connection.close()


# Main program loop
while True:
    print("Welcome. Please choose an option.")
    print("1 = Register New User")
    print("2 = Login with Existing Account")

    choice = input(">> ")

    if choice == "1":
        registerNewUser()

    elif choice == "2":
        success = loginWithCreds()

        # Admin menu
        if success and currentRole == 1:
            while True:
                print(f"Welcome, {currentUsername}. What do you want to do?")
                print("1 = Add New Product")
                print("2 = Edit Existing Product")
                print("3 = See All Products")
                print("4 = View Sales Total")
                print("5 = Logout")

                adminChoice = input(">> ")

                if adminChoice == "1":
                    submitNewProduct()
                elif adminChoice == "2":
                    editExistingProduct()
                elif adminChoice == "3":
                    getAllProducts()
                elif adminChoice == "4":
                    getSalesTotal()
                elif adminChoice == "5":
                    currentUserID = None
                    currentUsername = None
                    currentRole = None
                    break

        # Customer menu
        elif success and currentRole == 2:
            while True:
                print(f"Welcome, {currentUsername}. What do you want to do?")
                print("1 = Submit New Order")
                print("2 = Cancel Existing Order")
                print("3 = View My Orders")
                print("4 = See All Products")
                print("5 = Logout")

                customerChoice = input(">> ")

                if customerChoice == "1":
                    submitOrder()
                elif customerChoice == "2":
                    cancelOrder()
                elif customerChoice == "3":
                    viewCustomerOrders()
                elif customerChoice == "4":
                    getAllProducts()
                elif customerChoice == "5":
                    currentUserID = None
                    currentUsername = None
                    currentRole = None
                    break