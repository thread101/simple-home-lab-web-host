
def critical(func):
    def wrapper(*args, **kwags):
        try:
            result = func(*args, **kwags)
        except Exception as e:
            result = e

        return result
    
    return wrapper
