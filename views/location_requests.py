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

