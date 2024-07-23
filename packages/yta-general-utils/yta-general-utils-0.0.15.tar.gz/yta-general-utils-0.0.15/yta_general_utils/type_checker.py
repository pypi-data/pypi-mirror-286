def variable_is_type(variable, type):
    """
    Checks if the type of the provided 'variable' is the also provided
    'type', returning True if yes or False if not.
    """
    # TODO: Maybe let this accept array of types to check 
    # if one of them (?)
    if isinstance(variable, type):
        return True
    
    return False