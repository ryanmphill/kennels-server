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
    """Get all of the customer"""
    return CUSTOMERS

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
