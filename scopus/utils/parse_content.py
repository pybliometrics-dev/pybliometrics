def listify(element):
    """Helper function to turn an element into a list if it isn't a list yet.
    """
    if isinstance(element, list):
        return element
    else:
        return [element]
