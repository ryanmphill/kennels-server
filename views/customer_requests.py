import sqlite3
from models import Customer

CUSTOMERS = [
    {
        "id": 1,
        "fullName": "Ryan Tanay",
        "email": "ryantanay@example.com"
    },
    {
        "id": 2,
        "fullName": "Debra Deberson",
        "email": "debradeberson@example.com"
    },
    {
        "id": 3,
        "fullName": "Lawny Lawnmire",
        "email": "lawnylawnmire@example.com"
    },
    {
        "id": 4,
        "fullName": "Hugh Hughbert",
        "email": "hughhughbert@example.com"
    }
]

def get_all_customers():
    """Get all the customers"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
        FROM CUSTOMER a
        """)

        # Initialize an empty list to hold all customer representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # class above.
            customer = Customer(row['id'], row['name'], row['address'],
                                row['email'], row['password'])

            customers.append(customer.__dict__)

    return customers


def get_single_customer(id):
    """Function to return single item"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email,
            a.password
        FROM CUSTOMER a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        customer = Customer(data['id'], data['name'], data['address'],
                                data['email'], data['password'])

        return customer.__dict__

def get_customers_by_email(email):
    """Use query to get customer by email"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'],
                                row['email'] , row['password'])
            customers.append(customer.__dict__)

    return customers

def create_customer(customer):
    """Function to add customer via POST request"""
    # Get the id value of the last customer in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the customer dictionary
    customer["id"] = new_id

    # Add the customer dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer

def delete_customer(id):
    """Delete customer from database"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM CUSTOMER
        WHERE id = ?
        """, (id, ))
        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        result = False
    else:
        # Forces 204 response by main module
        result = True

    return result

def update_customer(id, new_customer):
    """Make an update to the customer row"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE CUSTOMER
            SET
                name = ?,
                address = ?,
                email = ?,
                password = ?
        WHERE id = ?
        """, (new_customer['name'], new_customer['address'],
              new_customer['email'], new_customer['password'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        result = False
    else:
        # Forces 204 response by main module
        result = True

    return result
