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


def get_single_customer(requested_id):
    """Use the id to get a single customer"""

    #Set the requested customer to None by default
    requested_customer = None

    #Iterate through the customer and find the requested customer
    for customer in CUSTOMERS:
        if customer["id"] == requested_id:
            requested_customer = customer

    return requested_customer

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
    """Delete customer from list"""
    # Initial -1 value for customer index, in case one isn't found
    customer_index = -1

    # Iterate the CUSTOMERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Store the current index.
            customer_index = index

    # If the customer was found, use pop(int) to remove it from list
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
    """Update an customer in the list"""
    # Iterate the CUSTOMERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Update the value.
            CUSTOMERS[index] = new_customer
            break
