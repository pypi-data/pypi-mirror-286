import logging

def error_handler(func):
    """
    API error handler. 
    Decorator object for simplifying code
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err: # pylint disable=broad-exception-caught
            logging.info(f"Houston, we have a problem: \n\n {err} \n\n") # pylint disable=broad-exception-caught
            return None # pylint disable=broad-exception-caught
    return wrapper # pylint disable=broad-exception-caught
