DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 4,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 2,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }
    ],
    "customers": [
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
    ],
    "employees": [
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
    ],
    "locations": [
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
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, resource_id):
    """For GET requests to a single resource"""
    #Set the requested customer to None by default
    requested_item = None

    #Iterate through the customer and find the requested customer
    for single_item in DATABASE[resource]:
        if single_item["id"] == resource_id:
            requested_item = single_item
            # Expand customers and locations if resource is animals
            if resource == "animals":
                # Get the location and customer that correspond to the foreign keys
                animal_location = retrieve("locations", single_item["locationId"])
                animal_customer = retrieve("customers", single_item["customerId"])
                # Add the foreign dictionaries to the requested animal dictionary
                requested_item["location"] = animal_location
                requested_item["customer"] = animal_customer
                # Delete the foreign keys since they are no longer needed
                del requested_item["locationId"]
                del requested_item["customerId"]
                break

    return requested_item


def create(resource, new_post_item):
    """For POST requests to a collection"""
    # Get the id value of the last item in the list
    max_id = DATABASE[resource][-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the dictionary
    new_post_item["id"] = new_id

    # Add the animal dictionary to the list
    DATABASE[resource].append(new_post_item)

    # Return the dictionary with `id` property added
    return new_post_item


def update(resource, resource_id, updated_item):
    """For PUT requests to a single resource"""
    # Iterate the resource list, but use enumerate() so that
    # you can access the index value of each item.
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == resource_id:
            # Found the item to update. Update the value.
            DATABASE[resource][index] = updated_item
            break



def delete(resource, resource_id):
    """For DELETE requests to a single resource"""
    # Initial -1 value for animal index, in case one isn't found
    resource_index = -1

    # Set a value to return that is not None if delete is successful
    item_deleted = False

    # Iterate the resource list, but use enumerate() so that you
    # can access the index value of each item
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == resource_id:
            # Found the animal. Store the current index.
            resource_index = index
            break

    # If the animal was found, use pop(int) to remove it from list
    if resource_index >= 0:
        DATABASE[resource].pop(resource_index)
        item_deleted = True

    # Return if the dictionary was successfully deleted
    return item_deleted
