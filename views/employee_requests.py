EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    },
    {
        "id": 2,
        "name": "Dan Daniels"
    },
    {
        "id": 3,
        "name": "Johnny Johnson"
    }
]


def get_all_employees():
    """Get all of the employees"""
    return EMPLOYEES

def get_single_employee(requested_id):
    """Use the id to get a single employee"""

    #Set the requested employee to None by default
    requested_employee = None

    #Iterate through the employees and find the requested employee
    for employee in EMPLOYEES:
        if employee["id"] == requested_id:
            requested_employee = employee

    return requested_employee

def create_employee(employee):
    """Function to add employee via POST request"""
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee
