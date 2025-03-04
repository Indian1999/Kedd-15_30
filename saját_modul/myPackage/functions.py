def add(x,y):
    return x+y

def average(x,y):
    return add(x,y) / 2

def power(x:float, y:float) -> float:
    """This function raises the float x to the power of y and returns the result."""
    return float(x ** y)

def matrix_generator(n:int, m:int) -> list[list[int]]:
    """
    Creates an n*m matrix filled with 0s.
    
    Args:
        n (int): The number of rows.
        m (int): The number of columns.
        
    Returns:
        list[list[int]]: An n x m matrix filled with 0s.
        
    Example:
        >>> matrix_generator(2, 3)
        [[0,0,0], [0,0,0]]
    """
    return [[0 for j in range(m)] for i in range(n)]