
class vector:
    def __init__(self, x, y, z ,a):
        self.x = x
        self.y = y
        self.z = z    
        self.a=a
        self.s=str(self.x)+str(self.y)+str(self.z)+str(self.a) #string representation of the vector
    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z,self.a+other.a)
    def __mul__(self, scalar):#scalar is a number
        return vector(self.x * scalar, self.y * scalar, self.z * scalar,self.a*scalar)
    def __str__(self):
        return f"vector({self.x}, {self.y}, {self.z},{self.a})"    
    def __len__(self):  # len() must return int
          # return len(str(self.x)) + len(str(self.y)) + len(str(self.z))+len(str(self.a))
          #this method counts the number of digits in the vector components
          # return len(str(self.x)) + len(str(self.y)) + len(str(self.z))+len(str(self.a))
          #this method counts the number of non-space characters in the string
          return len(self.s)
    
v1 = vector(2, 3,0,1)
v2 = vector(4, 5, 6,2)
v = vector(1, 2, 3,4)

print(f"len(v1) = {len(v1)}")     # Proper length





#other part


 import math
class vector:
    def __init__(self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z)

    # def __sub__(self, other):
    #     return vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):#scalar is a number
        return vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __str__(self):
        return f"vector({self.x}x+ {self.y}y+ {self.z}z)"
    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z) 

    # def __truediv__(self, scalar):
    #     return vector(self.x / scalar, self.y / scalar, self.z / scalar)

    # def __repr__(self):
    #     return f"vector({self.x}, {self.y}, {self.z})"
    def __abs__(self):  # magnitude of vector
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __len__(self):  # len() must return int
        return int(abs(self))

v1 = vector(2, 3, 4)
v2 = vector(4, 5, 6)
v = vector(1, 2, 3)
v4 = v1 * v2.x  # This will print the x component of the resulting vector
v5 = v1 * v2.y  # This will print the y component of the resulting vector
v6 = v1 * v2.z  # This will print the z component of the resulting vector
v7 = v1.__add__(v2).__add__(v)

print(v4)  # Output: vector(6, 9, 12)
print(v5)  # Output: vector(10, 15, 20)
print(v6)  # Output: vector(16, 24, 32)
print("")
print(v7)  # Output: vector(6, 8, 10)
print(v7.x, v7.y, v7.z)  # Output: 6 8 10
print(f"\nabs(v1) = {abs(v1)}")   # Proper magnitude
print(f"len(v1) = {len(v1)}")     # Proper length

