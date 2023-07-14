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

def delete_location(id):
    """Delete location from list"""
    # Initial -1 value for location index, in case one isn't found
    location_index = -1

    # Set a value to return that is not None if delete is successful
    item_deleted = False

    # Iterate the LOCATIONS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the location was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)
        item_deleted = True

    # Return if the dictionary was successfully deleted
    return item_deleted

def update_location(id, new_location):
    """Update an location in the list"""
    # Iterate the LOCATIONS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Update the value.
            LOCATIONS[index] = new_location
            break
