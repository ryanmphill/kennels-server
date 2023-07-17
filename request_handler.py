import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import all, retrieve, create, update, delete

# Define a Dictionary to hold a reference to the required keys for each resource
required_keys = {
    "animals": ["name", "species", "locationId", "customerId", "status"],
    "locations": ["name", "address"],
    "employees": ["name"],
    "customers": ["fullName", "email"]
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
            response = retrieve(resource, id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = f'# {id} in {resource} not found'
        else:
            if resource in ["animals", "customers", "employees", "locations"]:
                self._set_headers(200)
                response = all(resource)
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

        # Add a new item to the list
        if resource in ["animals", "locations", "employees", "customers"]:
            error_messages = find_missing_keys(post_body, required_keys[resource])
            if len(error_messages) == 0:
                response = create(resource, post_body)
                self._set_headers(201)
            else:
                response = error_messages
                self._set_headers(400)
        else:
            response = {"message": f"the resource '{resource}' was not found"}
            self._set_headers(404)

        # Encode the new item and send in response
        self.wfile.write(json.dumps(response).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handle put requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Set default empty response
        response = ""

        # Update a single item in the list
        if resource in ["animals", "locations", "employees", "customers"]:
            update(resource, id, post_body)
            self._set_headers(204)
        else:
            response = json.dumps({"message": f"Resource '{resource}' not found"})
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write(response.encode())

    def do_DELETE(self):
        """Handle a DELETE request"""
        response = ""

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single item from the list
        if resource in ["animals", "locations", "employees"]:
            item_deleted = delete(resource, id)
            if item_deleted is True:
                self._set_headers(204)
            else:
                self._set_headers(404)
                message = {"message": f"Item #{id} in '{resource}' not found"}
                response = json.dumps(message)
        elif resource == "customers":
            message = {"message": "Deleting customers requires contacting company directly"}
            response = json.dumps(message)
            self._set_headers(405)
        else:
            response = json.dumps({"message": f"Resource '{resource}' not found"})
            self._set_headers(404)

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
