CUSTOMERS = [
    {
        "id": 1,
        "name": "Ryan Tanay"
    },
    {
        "id": 2,
        "name": "Debra Deberson"
    },
    {
        "id": 3,
        "name": "Lawny Lawnmire"
    },
    {
        "id": 4,
        "name": "Hugh Hughbert"
    }
]

def get_all_customers():
    """Get all of the customers"""
    return CUSTOMERS

def get_single_customer(requested_id):
    """Use the id to get a single customer"""

    #Set the requested customer to None by default
    requested_customer = None

    #Iterate through the customers and find the requested customer
    for customer in CUSTOMERS:
        if customer["id"] == requested_id:
            requested_customer = customer
    
    return requested_customer
