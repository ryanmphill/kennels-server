LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    """Get all of the locations"""
    return LOCATIONS

def get_single_location(requested_id):
    """Use the id to get a single location"""

    #Set the requested location to None by default
    requested_location = None

    #Iterate through the locations and find the requested location
    for location in LOCATIONS:
        if location["id"] == requested_id:
            requested_location = location
    return requested_location


def create_location(location):
    """Function to add location via POST request"""
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the location dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location
