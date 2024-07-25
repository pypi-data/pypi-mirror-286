from __future__ import annotations
from typing import Optional, Tuple


class Vector:
    def __init__(
            self,
            v:Optional[Tuple[int, float]]=None,
        ) -> None:
        self.v=v
        
    def mul_k(self,k) -> Vector:
        """
        Multiply the vector by a scalar value.
        """
        return Vector(tuple(map(lambda x: x*k, self.v)))
    
    @staticmethod
    def dot(v1:Tuple[int, float], v2:Tuple[int, float]) -> int | float:
        """
        Calculates the dot product of two vectors.
        """
        return sum([x*y for x,y in zip(v1, v2)])
    
    @staticmethod
    def cross(v1:Tuple[int, float], v2:Tuple[int, float]) -> int | float:
        """
        Calculates the cross product of two vectors.
        """
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v1[2],
            v1[0] * v2[1] - v2[1] * v2[0]
        ]
        
    @property
    def magnitude(self) -> int | float:
        """
        Calculates the magnitude of the vector.
        """
        return sum(x**2 for x in self.v)**0.5
    
    @property
    def unit_vector(self) -> int | float:
        """
        Calculates the unit vector of the vector.
        """ 
        return self / self.magnitude
    
    @staticmethod
    def projection(v1:Tuple[int, float], v2:Tuple[int, float]) -> Vector:
        """
        Calculates the projection of v1 onto v2.
        """
        return Vector(tuple(map(lambda x: x *(Vector.dot(v1, v2) / Vector.dot(v2,v2)), v2)))
    
    @staticmethod
    def area(v1:Tuple[int, float],v2:Tuple[int, float]) -> int | float:
        """
        Calculates the area of the triangle formed by v1 and v2.
        """
        return Vector(Vector.cross(v1, v2)).magnitude()
    
    @staticmethod
    def triangle(v1:Tuple[int, float],v2:Tuple[int, float]):
        """
        Calculates the area of the triangle formed by v1 and v2.
        """
        return (Vector.area(v1,v2))
    
    @staticmethod
    def angle(v1:Tuple[int, float],v2:Tuple[int, float]):
        """
        Calculates the angle between v1 and v2.
        """
        return Vector.dot(v1, v2) / (Vector(v1).magnitude * Vector(v2).magnitude())

    def __add__(self, other) -> Vector:
        return Vector(tuple(x+y for x,y in zip(self.v, other.v)))
    
    def __sub__(self, other) -> Vector:
        return Vector(tuple(x-y for x,y in zip(self.v, other.v)))
    
    def __mul__(self, other) -> Vector:
        return Vector(tuple(x*y for x,y in zip(self.v, other.v)))

    def __truediv__(self, other) -> Vector:
        return Vector(tuple(x/y for x,y in zip(self.v, other.v)))  
    
    def __repr__(self):
        return f"Vector({self.v}"
    
    def __iter__(self):
        return iter(self.v)