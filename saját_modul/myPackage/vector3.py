class Vector3:
    """
    Implements a basic Vector3 class.
    """
    zero = None
    """ A vector representing (0,0,0), the origin."""
    one = None
    """ A vector representing (1,1,1)."""
    right = None
    """ A vector representing (1,0,0)."""
    left = None
    """ A vector representing (-1,0,0)."""
    up = None
    """ A vector representing (0,1,0)."""
    down = None
    """ A vector representing (0,-1,0)."""
    forward = None
    """ A vector representing (0,0,1)."""
    backward = None
    """ A vector representing (0,0,-1)."""
    
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
    
    @staticmethod
    def distance(v1:"Vector3", v2:"Vector3") -> float:
        """
        Returns the distance between to 3D points as a float value.
        """
        return ((v1.x-v2.x)**2 + (v1.y-v2.y)**2 + (v1.z-v2.z)**2)**(1/2)
    
    def length(self) -> float:
        """Returns the length of the Vector3 object"""
        return ((self.x)**2 + (self.y)**2 + (self.z)**2)**(1/2)
    
Vector3.zero = Vector3(0,0,0)
Vector3.one = Vector3(1,1,1)
Vector3.right = Vector3(1,0,0)
Vector3.left = Vector3(-1,0,0)
Vector3.up = Vector3(0,1,0)
Vector3.down = Vector3(0,-1,0)
Vector3.forward = Vector3(0,0,1)
Vector3.backward = Vector3(0,0,-1)