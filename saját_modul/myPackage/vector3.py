class Vector3:
    """
    Implements a basic Vector3 class.
    """
    def __init__(self, x:float = 0, y:float = 0, z:float = 0) -> None:
        """
        Creates a Vector3 object, with default values of 0 if the arguments are not given.
        
        Args:
            x (float): The value of the x coordinate.
            y (float): The value of the y coordinate.
            z (float): The value of the z coordinate.
            
        Example:
            >>> v = Vector3(5,4,3)
        """
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def distance(v1:"Vector3", v2:"Vector3") -> float:
        """
        Returns the distance between to 3D points as a float value.
        """
        return ((v1.x-v2.x)**2 + (v1.y-v2.y)**2 + (v1.z-v2.z)**2)**(1/2)