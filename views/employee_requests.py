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
