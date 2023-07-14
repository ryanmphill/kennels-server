import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals
from views import get_single_animal
from views import create_animal
from views import delete_animal
from views import update_animal
from views import get_all_locations
from views import get_single_location
from views import create_location
from views import delete_location
from views import update_location
from views import get_all_employees
from views import get_single_employee
from views import create_employee
from views import delete_employee
from views import update_employee
from views import get_all_customers
from views import get_single_customer
from views import create_customer
from views import update_customer

# Define a Dictionary to hold a reference to the functions needed
method_mapper = {
    "animals": {
        "single": get_single_animal,
        "all": get_all_animals
    },
    "locations": {
        "single": get_single_location,
        "all": get_all_locations
    },
    "employees": {
        "single": get_single_employee,
        "all": get_all_employees
    },
    "customers": {
        "single": get_single_customer,
        "all": get_all_customers
    }
}
# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function

    # Here's a method that takes the path of the request as an input.
    # It returns a tuple with the resource and id
    def parse_url(self, path):
        """Split the path into the resource and the id"""
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    # Method to handle getting resources
    def get_all_or_single(self, resource, id):
        """Either get all of resource or single item"""
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = f'# {id} in {resource} not found'
        else:
            if resource in ["animals", "customers", "employees", "locations"]:
                self._set_headers(200)
                response = method_mapper[resource]["all"]()
            else:
                self._set_headers(404)
                response = f'{resource} does not exist in database'

        return response

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        response = None  # Default response
        # Your new console.log() that outputs to the terminal
        print(self.path)
        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)
        # Try to get requested resource or dictionary and return response
        response = self.get_all_or_single(resource, id)
        # Send a JSON formatted string as a response
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handle POST requests made to server"""

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, _) = self.parse_url(self.path)

        # Initialize new item to post
        response = None

        # Define function that finds any missing keys on the post body
        def find_missing_keys(post_dictionary, list_of_keys):
            message = []
            for key in list_of_keys:
                if key not in post_dictionary:
                    message.append({ "message": f"{key} is required" })
            if len(post_dictionary) > len(list_of_keys):
                message.append({ "message": "Looks like there are some unecessary keys" })
            return message

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            required_keys = ["name", "species", "locationId", "customerId", "status"]
            error_messages = find_missing_keys(post_body, required_keys)
            if len(error_messages) == 0:
                response = create_animal(post_body)
                self._set_headers(201)
            else:
                response = error_messages
                self._set_headers(400)
        # Add a new location to the list
        if resource == "locations":
            required_keys = ["name", "address"]
            error_messages = find_missing_keys(post_body, required_keys)
            if len(error_messages) == 0:
                response = create_location(post_body)
                self._set_headers(201)
            else:
                response = error_messages
                self._set_headers(400)

        # Add a new employee to the list
        if resource == "employees":
            required_keys = ["name"]
            error_messages = find_missing_keys(post_body, required_keys)
            if len(error_messages) == 0:
                response = create_employee(post_body)
                self._set_headers(201)
            else:
                response = error_messages
                self._set_headers(400)

        # Add new customer upon registration
        if resource == "customers":
            required_keys = ["fullName", "email"]
            error_messages = find_missing_keys(post_body, required_keys)
            if len(error_messages) == 0:
                response = create_customer(post_body)
                self._set_headers(201)
            else:
                response = error_messages
                self._set_headers(400)

        # Encode the new item and send in response
        self.wfile.write(json.dumps(response).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handle put requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Update a single animal in the list
        if resource == "animals":
            update_animal(id, post_body)

        # Update Location
        if resource == "locations":
            update_location(id, post_body)

        # Update employee
        if resource == "employees":
            update_employee(id, post_body)

        # Update customer
        if resource == "customers":
            update_customer(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle a DELETE request"""
        response = ""

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            animal_deleted = delete_animal(id)
            if animal_deleted is True:
                self._set_headers(204)
            else:
                self._set_headers(404)
                message = {"message": f"Animal {id} not found"}
                response = json.dumps(message)
        # Delete a location
        if resource == "locations":
            location_deleted = delete_location(id)
            if location_deleted is True:
                self._set_headers(204)
            else:
                self._set_headers(404)
                message = {"message": f"Location {id} not found"}
                response = json.dumps(message)

        # Delete an employee
        if resource == "employees":
            employee_deleted = delete_employee(id)
            if employee_deleted is True:
                self._set_headers(204)
            else:
                self._set_headers(404)
                message = {"message": f"Employee {id} not found"}
                response = json.dumps(message)

        # Delete customer
        if resource == "customers":
            message = {"message": "Deleting customers requires contacting company directly"}
            response = json.dumps(message)
            self._set_headers(405)

        if resource not in ["customers", "employees", "animals", "locations"]:
            self._set_headers(404)
            message = {"message": "Cannot find resource"}
            response = json.dumps(message)

        # Encode the new animal and send in response
        self.wfile.write(response.encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
