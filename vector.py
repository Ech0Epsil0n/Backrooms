# Alex Stambaugh
# ETGG 1803 Lab #5
# Finished March 11th 2022
# Outside Sources: Python Docs

## IMPORTS AND INITIALIZATIONS ##

## MAIN CODE ##
import math

def dot (vec_one, vec_two) :
    """Returns the dot product of two vectors of the same dimension."""

    # Checks for input validity.
    if not isinstance(vec_one, Vector) or not isinstance(vec_two, Vector) :
        print(vec_one)
        print(vec_two)

        raise TypeError("ERROR: Dot product only accepts vectors.")

    if len(vec_one.data) != len(vec_two.data) :
        raise TypeError("ERROR: Vectors must be of equivalent length.")

    # Adds the multiplied values from both vectors to new_list.
    return_int = 0
    i = 0

    while i < len(vec_one) :
        return_int += (vec_one[i] * vec_two[i])
        i += 1

    return return_int

def cross (v, w) :
    """Returns the cross product of 3D vectors v and w."""

    # Checks for input validity.
    if not isinstance(v, Vector3) or not isinstance(w, Vector3) :
        raise TypeError("ERROR: Cross Product only functions with three-dimensional vectors.")

    # Performs the cross-product operation.
    new_x = (v.y * w.z) - (w.y * v.z)
    new_y = (v.x * w.z) - (w.x * v.z)
    if new_y != 0 :
        new_y = -new_y
    new_z = (v.x * w.y) - (w.x * v.y)

    return Vector3(new_x, new_y, new_z)

def polar_to_Vector2 (pol_cord, negate=False) :
    """Returns a Vector2 from player-input polar coordinates. Has an additional parameter to negate y for
    Pygame."""

    # Checks for validity of input.
    if not isinstance(pol_cord, tuple) :
        raise TypeError("ERROR: Polar coordinate input must be in tuple format.")

    # Finds x and y values of vector.
    new_y = math.sin(pol_cord[1]) * pol_cord[0], 2
    new_x = math.cos(pol_cord[1]) * pol_cord[0], 2

    # Negates y, if necessary.
    if negate == True :
        new_y = -new_y

    return Vector2(new_x, new_y)

class Vector :
    def __init__ (self, *args) :
        """Takes a variable number of input values and creates a vector from them."""

        # Establishes baseline variables.
        self.data = []

        # Adds values to self.data list.
        for value in args :
            if isinstance(value, Vector) :
                continue

            if isinstance(value, int) or isinstance(value, float) or isinstance(value, list) :
                if not isinstance(value, list) or isinstance(value, Vector) :
                    self.data.append(float(value))

                if isinstance(value, list):
                    for item in value :
                        try :
                            if isinstance(item, Vector) == False :
                                self.data.append(float(item))

                            else :
                                for value in item :
                                    self.data.append(float(value))

                        except :
                            continue

            else :
                raise TypeError ("ERROR: Input must be ints/floats/lists.")

        # Establishes the length of Vector.
        self.dim = len(self.data)

        # Sets vector class.
        if self.dim == 2 :
            self.__class__ = Vector2

        elif self.dim == 3 :
            self.__class__ = Vector3

    def __str__ (self) :
        """Returns the values of Vector in the form of a string."""

        # Creates start point for return string.
        return_str = f"<Vector{len(self.data)}: "

        # Continually adds values and finalizes return string.
        i = 0

        while i < len(self.data) :
            if not i == len(self.data) - 1 :
                return_str += f"{self.data[i]}, "

            else :
                return_str += f"{self.data[i]}>"

            i += 1

        return return_str

    def __len__ (self) :
        """Returns the length of Vector in the form of an int."""

        return len(self.data)

    def __getitem__ (self, index) :
        """Gets a specific value from Vector using a user-input "index" value."""

        # Checks to make sure index is int.
        if not isinstance(index, int) :
            raise TypeError ("ERROR: Index value must be int.")

        # Attempts to pull a value from self.data.
        try :
            item = self.data[index]

        except IndexError :
            raise IndexError("ERROR: Index out of range.")

        # If successful, returns value.
        return item

    def __setitem__ (self, index, input) :
        """Gets a specific value from Vector using a user-input "index" value. Changes its value to user-input
        "input" value."""

        # Checks the validity of both index and input.
        if not isinstance(index, int) :
            raise TypeError ("ERROR: Index value must be int.")

        try :
            self.data[index]

        except IndexError :
            raise IndexError ("ERROR: Index value not valid.")

        if not isinstance(input, int) and not isinstance(input, float) :
            raise TypeError ("ERROR: Input value must be int/float.")

        # If valid, sets item.
        self.data[index] = float(input)

        return

    def __eq__ (self, other) :
        """Checks to see if Vector and a user-input "other" vector are equal."""

        # Tests to make sure that "other" is of vector class.
        if not isinstance(other, Vector) :
            raise TypeError ("ERROR: Input must be vector.")

        # If vector, compares both values and returns true/false.
        temp_bool = True

        # Checks for equivalent size.
        if self.dim == other.dim :
            # Compares each int in both data lists.
            for value in self.data :
                if not value == other.data[self.data.index(value)] :
                    temp_bool = False

        else :
            temp_bool = False

        # Finalizes operation.
        return temp_bool

    def __add__ (self, other) :
        """Adds Vector with a user-input "other" vector."""

        # Checks "other" type and raises error if not valid.
        if not isinstance(other, Vector) :
            raise TypeError ("ERROR: Input must be Vector.")

        # Checks to see Vector and "other" vector have equivalent length.
        if not self.dim == other.dim :
            raise ValueError ("ERROR: Vectors must be of equivalent length.")

        # If valid, commences operation.
        return_vector = self.copy()
        i = 0

        while i < len(self.data) :
            return_vector.data[i] += other.data[i]
            i += 1

        return return_vector

    def __sub__ (self, other) :
        """Subtracts Vector by user-input "other" vector."""

        # Checks to ensure that "other" vector is vector class.
        if not isinstance(other, Vector):
            raise TypeError("ERROR: Input must be Vector.")

        # Checks to ensure equivalent length.
        if not self.dim == other.dim:
            raise ValueError("ERROR: Vectors must be of equivalent length.")

        # If valid, commences operation.
        return (self + -other)

    def __mul__ (self, other) :
        """Multiplies Vector with a user-input "other" vector/int/float."""

        # Creates a copy of the self Vector to return.
        return_vector = self.copy()

        # Checks to ensure that input is valid.
        if not isinstance(other, Vector) and not isinstance(other, int) and not isinstance(other, float) :
            return NotImplemented

        ## RUNS IF INPUT IS VECTOR ##
        if isinstance(other, Vector) :
            # Checks to ensure equivalent length.
            if not self.dim == other.dim :
                raise ValueError ("ERROR: Vectors must be of equivalent length.")

            # If valid, commences operation.
            i = 0

            while i < len(self.data) :
                return_vector.data[i] *= other.data[i]
                i += 1


        ## RUNS IF INPUT IS INT/FLOAT ##
        if isinstance(other, int) or isinstance(other, float) :
            # Multiplies all values in Vector by input.
            i = 0

            while i < len(self.data) :
                return_vector.data[i] *= other
                i += 1

        return return_vector

    def __rmul__ (self, other) :
        return self * other

    def __truediv__ (self, other) :
        """Divides Vector by user-input "other" int/float."""

        # Creates a copy of self vector.
        return_vector = self.copy()

        # Tests for input validity.
        if not isinstance(other, int) and not isinstance(other, float) :
            raise TypeError ("ERROR: Input must be int/float.")

        # If valid, commneces operation.
        i = 0

        while i < len(self.data) :
            return_vector.data[i] /= other
            i += 1

        return return_vector

    def __neg__ (self) :
        """Returns a negative version of Vector."""

        return self * -1

    def pop (self, index) :
        """Removes a value from a vector."""

        # Checks for validity of input.
        if isinstance(index, int) == False or index > len(self.data) :
            raise IndexError("ERROR: Index value must be int less than length of Vector data.")

        self.data.pop(index)

        return

    def copy (self) :
        """Returns a deep copy of Vector."""

        # Creates an empty vector and assigns a Vector2/Vector3 class if applicable.
        temp_vector = Vector()

        if self.dim == 2 :
            temp_vector.__class__ = Vector2

        elif self.dim == 3 :
            temp_vector.__class__ = Vector3

        # Copies value attributes to empty vector.
        temp_vector.data = self.data[:]
        temp_vector.dim = self.dim

        return temp_vector

    def norm (self, p) :
        """Returns user-input "p" norm of Vector."""

        # Checks input validity.
        if not isinstance(p, int) :
            raise TypeError("ERROR: 'P' value must be int.")

        # Norm calculation.
        norm = 0
        for value in self.data :
            if value < 0 :
                value = -value

            norm += value ** p

        norm ** (1 / p)
        return norm

    def mag (self) :
        """Returns the magnitude of Vector."""

        # Square roots temp_value to return magnitude.
        return math.sqrt(self.norm(2))

    def mag_squared (self) :
        """Returns the magnitude of Vector squared."""

        # Square roots temp_value to return magnitude.
        return self.norm(2)

    def normalize (self) :
        """Returns a unit vector in the same direction of Vector."""

        return (self / self.mag())

    def is_zero (self) :
        """If Vector is a zero vector, returns True. If else, returns False."""

        # Loops through all values.
        temp_bool = True
        for value in self.data :
            if value != 0 :
                temp_bool = False

        return temp_bool

    def i (self) :
        """Returns a temp_vector vector class that contains all Vector items converted to integers."""

        # Loops through all values.
        int_list = []
        for value in self.data :
            int_list.append(int(value))

        return(Vector(int_list))

# Defines Vector2/Vector3 classes.
class Vector2 (Vector) :
    """Vector2. Inherits from Vector class."""

    # Creates Vector2.
    def __init__ (self, x, y) :
        super().__init__(x, y)

        self.x = self.data[0]
        self.y = self.data[1]

    ## DEFINES PROPERTIES ##
    @property
    def x(self) :
        return self.data[0]

    @x.setter
    def x(self, value):
        """Sets x value."""

        # Checks for validity.
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("ERROR: Value must be inputed.")

        # If valid, commences operation.
        self[0] = float(value)

    @property
    def y (self) :
        return self.data[1]

    @y.setter
    def y (self, value):
        """Sets y value."""

        # Checks for validity.
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("ERROR: Value must be inputed.")

        # If valid, commences operation.
        self[1] = float(value)

    def radians (self) :
        """Returns the theta angle of Vector in radians."""

        return(math.atan(self.y / self.x))

    def radians_inv (self) :
        """Returns the theta angle of Vector in radians."""

        return(math.atan(-(self.y) / self.x))

    def degrees (self) :
        """Returns the theta angle of Vector in degrees."""

        degrees = (self.radians() * 180) / math.pi
        return f"{(degrees, 2)} DEGREES"

    def degrees_inv (self) :
        """Returns the theta angle of Vector in degrees."""

        degrees = (self.radians_inv() * 180) / math.pi
        return f"{(degrees, 2)} DEGREES"

    def perpendicular (self) :
        """Returns Vector2 perpendicular to Vector."""

        temp_vec = Vector(self.x, self.y, 0)
        temp_vec = cross(temp_vec, Vector(0, 0, 1))

        return temp_vec


class Vector3 (Vector) :
    """Vector3. Inherits from Vector class."""

    # Creates Vector3.
    def __init__(self, x, y, z) :
        super().__init__(x, y, z)

    ## DEFINES PROPERTIES ##
    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, value):
        """Sets x value."""

        # Checks for validity.
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("ERROR: Value must be inputed.")

        # If valid, commences operation.
        self[0] = float(value)

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, value):
        """Sets y value."""

        # Checks for validity.
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("ERROR: Value must be inputed.")

        # If valid, commences operation.
        self[1] = float(value)

    @property
    def z (self) :
        return self.data[2]

    @z.setter
    def z (self, value) :
        """Sets z value."""

        # Checks for validity.
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("ERROR: Value must be inputed.")

        # If valid, commences operation.
        self[2] = float(value)
