import sqlite3
from models import Employee, Location

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
    """Get all the employees"""
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
            a.location_id,
            l.name location_name,
            l.address location_address
        FROM EMPLOYEE a
        JOIN Location l
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # class above.
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'])

            # Create a Location instance from the current row to expand employees location
            location = Location(row['location_id'], row['location_name'], row['location_address'])

            # Add the dictionary representation of the location to the employee
            employee.location = location.__dict__
            employees.append(employee.__dict__)

            #############################################
            # Delete the keys that are no longer needed
            # del employee.location_id
            #############################################

    return employees


def get_single_employee(id):
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
            a.location_id,
            l.name location_name,
            l.address location_address
        FROM EMPLOYEE a
        JOIN Location l
            ON l.id = a.location_id
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], data['address'],
                                data['location_id'])

        # Create a Location instance from the current row to expand employees location
        location = Location(data['location_id'], data['location_name'], data['location_address'])

        # Add the dictionary representation of the location to the employee
        employee.location = location.__dict__

        return employee.__dict__

def get_employees_by_location(location):
    """Use query to get employee by location"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.address,
            a.location_id
        from EMPLOYEE a
        WHERE a.location_id = ?
        """, ( location, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'])
            employees.append(employee.__dict__)

    return employees

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

def delete_employee(id):
    """Delete employee from database"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM EMPLOYEE
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

def update_employee(id, new_employee):
    """Make an update to the employee row"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE EMPLOYEE
            SET
                name = ?,
                address = ?,
                location_id = ?
        WHERE id = ?
        """, (new_employee['name'], new_employee['address'],
              new_employee['locationId'], id, ))

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
