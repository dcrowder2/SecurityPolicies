# Dakota Crowder
# Lorenzo Griego
# CSCE A465 Computer and Network Security
# Assignment 1

# This class holds the connections of the user objects and the program objects
# as well as updates and pulls from a database to store the connections
class Group:
    # A private variable to hold the different structures that hold group membership
    # Initially empty, will get loaded in from the database
    __dictionary = {
        "SuperAdmin" : [],
        "Admin" : [],
        "SystemEngineer" : [],
        "User" : []
    }

    # This will load in from the database for use in the program
    def load_groups():
        # TODO: figure out database engine, then integration with python
        # Defualt return of true to signafy that the database has been properly loaded
        return True

    # This will write to the database the current groups
    def write_groups():
        # TODO: Again the database engine, but also maybe a system that makes sure
        # to only write when something changes, but I don't know if that is within
        # our scope
        return True

    # Will return a list of the super admins, provided the correct key
    def get_super_admin(key):
        # Defualt return of nothing, because it should require a key to get
        # the list of super admins
        return None

    # Will return a list of the admins, provided the correct key
    def get_admin(key):
        # Same as with super admins, you should not be able to get the list
        # without a key
        return None

    def get_system_engineer(key):
        
        return None

    def get_user(key):

        return None
