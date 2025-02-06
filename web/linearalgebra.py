"""
Vector and Matrix calculator
Alexandre Cornu
Contains the classes for Vector and Matrix
History:
Nov 8, 2024: Added the __init__(), components() setter and getter, magnitude, __add__(), __sub__(), __mul__(), dotProduct(), and isSameDimension() methods
Nov 11, 2024: Added the Op() class. Removed the dotProduct() method from the Vector class and added it to the Op class. Added cross_product() method to Op. Added __str__() magic method to Vector
Nov 14, 2024: Added the angle_betwen_vectors() method
Nov 15, 2024: Added the __init__() method, validateMatrix() method, multiply() method
Nov 16, 2024: Modified the __init() method to assign the Matrix class a list of Vector objects and added the from_2d_list() method. Added the __str__() magic method for Matrix class
Nov 25, 2024: Added the give_2d_list() method to the Matrix class
Dec 30, 2024: Modified the entire code's methods (except for give_2d_list() and from_2d_list()) such that they are in camel case instead of using underscores. Also modified the from_2d_list() method to properly create a matrix from a 2d list of floats/ints
Dec 31, 2024: Finished the determinant() method. Modified the __str__() magic method for the Matrix class. Added the hadamardProduct() method.
Jan 1, 2025: Added the trace() method. Modified the methods of the Op class to all be static methods instead of class methods. Added the __add__(), __sub__(), and scalarMultiply() methods to the Matrix class. Renamed multiply() to matrixMultiply(). Fixed a bug in matrixMultiply()
Jan 2, 2025: Added the transpose() method. Fixed the hadamardProduct() method to now work with vectors.
Jan 11, 2025: Added the inverseMatrix() and __pow__() methods to the Matrix class
Jane 12, 2025: Fixed matrixMultiply() to work with different types of non-square matrices.
"""
import math

class Vector():
  """
  Creates a vector object in any dimension
  Attributes:
    _components (list[float]): A list containing n amount of components of an n-dimentional vector
  """
  def __init__(self, components):
    """
    Assigns values to the vector object
    Args:
      components (list[float]): A list that contains the components of the vector
    """
    self.components = components

  @property
  def components(self):
    return self._components
  
  @components.setter
  def components(self, new_comps):
    """
    Validates the components list before it is set
    Args:
      new_comp (list): A list of variable length that contains the components of the vector
    """
    for comp in new_comps:
      if isinstance(comp, int) == False and isinstance(comp, float) == False:
        raise TypeError("Components list must contain either floats or ints")
    self._components = new_comps

  def magnitude(self):
    """
    Calculates the magnitude of the vector
    Returns:
      math.sqrt(squared_sum) (float): The magnitude of the vector
    """
    squared_sum = 0
    for comp in self.components:
      squared_sum += comp**2
    return math.sqrt(squared_sum)
  
  def __add__(self, other_vector):
    """
    Operation for vector addition
    Args:
      other_vector (Vector): The addend of the operation
    Returns:
      resultant (Vector): The resultant vector of the addition
    """
    resultant_components = []
    # Validates that other_vector is a Vector object
    if self.__class__.isSameDimension(self, other_vector):
      for index, comp in enumerate(other_vector.components):
        resultant_components.append(self.components[index]+comp)
    else:
      raise Exception("__add__ method cannot add vectors with different dimensions")
    resultant = Vector(resultant_components)
    return resultant

  def __mul__(self, scalar):
    """
    Magic method for scalar multiplication
    Args:
      scalar (int or float): A scalar value that is multiplied with the vector
    Returns:
      resultant (Vector): The resultant vector of the multiplication
    """
    resultant_components = []
    if isinstance(scalar, int) or isinstance(scalar, float):
      for comp in self.components:
        resultant_components.append(comp*scalar)
    else:
      raise TypeError("Scalar multiplication for a Vector object only works when given an integer or float")
    resultant = Vector(resultant_components)
    return resultant

  def __sub__(self, other_vector):
    """
    Operation for vector subtraction
    Args:
      other_vector (Vector): The subtrahend of the subtraction
    Returns:
      resultant (Vector): The resultant vector of the subtraction
    """
    if self.__class__.isSameDimension(self, other_vector):
      subtrahend = other_vector*-1
      resultant = self + subtrahend # It is doing addition because Vector - Vector is the same Vector + (-Vector))
    else:
      raise Exception("__sub__() method cannot subtract vectors with different dimensions")
    return resultant

  def __str__(self):
    return f"{self.components}"

  @staticmethod
  def isSameDimension(v1, v2):
    """
    Checks if two vectors have the same dimension
    Also validates if the two passed values are Vector objects
    Args:
      v1 (Vector): A vector being compared
      v2 (Vector): A vector being compared
    Returns:
      same_dimension (bool): True if the length of the component lists are equivalent. False if the lengths do not match
    """
    if isinstance(v1, Vector) == False or isinstance(v2, Vector) == False:
      raise Exception("Cannot compare the dimensions of an object that is not a vector")
    else:
      same_dimension = len(v1.components) == len(v2.components)
    return same_dimension


class Matrix():
  """
  Creates a matrix of any dimension
  Example of how it looks:
  [[Vector],[Vector],[Vector]]
  Attributes:
    vector_list (list[Vector]): This 2d list contains the elements present in the matrix
    square (bool): True if the matrix has equal length for its rows and collumns
  """

  def __init__(self, vector_list):
    """
    Assigns values to the Matrix object
    Args:
      vector_list (list[Vector]): A list of vectors with equal dimensions
    """
    self.validateMatrix(vector_list)
    self.vector_list = vector_list
    # This can use the first vector of vector_list because the vectors have already been validated to be of equal dimensions
    self.square = len(vector_list) == len(vector_list[0].components)
    
  
  @staticmethod
  def validateMatrix(vector_list):
    """
    Validates the given list of elements to ensure that they are only made up of ints or floats
    Raises an error if the given 2d list is not valid
    Args:
      vector_list (list[Vector]): A list of vectors with equal dimensions
    """
    if not isinstance(vector_list, list):
      raise TypeError(f"{type(vector_list)} type argument is not valid for instantiating a Matrix object")

    for vector in vector_list:
      if not isinstance(vector, Vector):
        raise TypeError("Matrix class requires a list of Vector object to be instantiated")
    
    # Multiple for loops have to be used since this validation below requires that all of the elements in vector_list have been validated to be Vectors
    comparison_vector = vector_list[0]
    for vector in vector_list:
      if not Vector.isSameDimension(comparison_vector,vector):
        raise Exception("All vectors in the list must have equal dimensions")
  
  @classmethod
  def from_2d_list(cls,elements):
    """
    Creates a matrix object from a list of vectors
    Args:
      elements (list[list[float]]): A 2d list containing the elements present in the matrix
    Returns:
      cls(vector_list) (Matrix): A matrix object made from a 2d list of vector components
    """

    if not isinstance(elements, list):
      raise TypeError("Matrix class requires a 2d list of ints or floats to be passed as an argument")
    
    collumn_length = len(elements[0])

    for sublist in elements:
      if len(sublist) != collumn_length: # Verifies that the matrix has consistent lengths
        raise Exception("The sublists in the provided argument must have equal lengths")
      for component in sublist:
        if not isinstance(component, int) and not isinstance(component, float):
          raise TypeError("The elements in the 2d list must be either an int or a float")
    
    vector_list = []
    for col in range(0,len(elements[0])):
      sublist = []
      for row in range(0,len(elements)):
        sublist.append(elements[row][col])
      vector_list.append(Vector(sublist))

    return cls(vector_list)

  def give_2d_list(self):
    """
    Returns a 2d list of the matrix's components
    Return:
      components_list (list[list[int or float]])
    """
    components_list = []
    for row in range(0,len(self.vector_list[0].components)):
      sublist = []
      for collumn in range(0,len(self.vector_list)):
        sublist.append(self.vector_list[collumn].components[row])
      components_list.append(sublist)
    
    return components_list
  
  def __add__(self, mat):
    """
    This functions adds a matrix to another matrix of the same dimension
    Args:
      mat (Matrix): A matrix of the same dimension
    Returns:
      Matrix(result): The sum of both matrices
    """
    if not isinstance(mat, Matrix):
      raise TypeError(f"Cannot add a {type(mat)} to a Matrix")
    elif len(mat.vector_list) != len(self.vector_list) or len(mat.vector_list[0].components) != len(self.vector_list[0].components):
      raise Exception("Cannot add two matrices with different dimensions")
    
    result = []

    for i in range(0,len(mat.vector_list)):
      result.append(self.vector_list[i] + mat.vector_list[i])
    
    return Matrix(result)
  
  def __sub__(self, mat):
    """
    This functions subtracts a matrix from another matrix of the same dimension
    Args:
      mat (Matrix): A matrix of the same dimension
    Returns:
      Matrix(result): The difference of both matrices
    """
    if not isinstance(mat, Matrix):
      raise TypeError(f"Cannot subtract a {type(mat)} from a Matrix")
    elif len(mat.vector_list) != len(self.vector_list) or len(mat.vector_list[0].components) != len(self.vector_list[0].components):
      raise Exception("Cannot subtract two matrices with different dimensions")
    
    result = []

    for i in range(0,len(mat.vector_list)):
      result.append(self.vector_list[i] - mat.vector_list[i])
    
    return Matrix(result)

  def scalarMultiply(self, scalar):
    """
    This functions mutliplies the matrix with a scalar (number)
    Args:
      scalar (int or float): The number that is multiplying the matrix
    Returns:
      Matrix(result): The matrix that is a product of the scalar multiplication
    """
    if not isinstance(scalar, int) and not isinstance(scalar, float):
      raise TypeError(f"Cannot multiply a matrix with {type(scalar)}")
    
    result = []
    for i in range(0,len(self.vector_list)):
      result.append(self.vector_list[i] * scalar)
    
    return Matrix(result)

  def transpose(self):
    """
    Creates a transposed matrix
    Returns:
      transposed_matrix (Matrix): A transposed matrix
    """
    # Note that this function relies on the way that I implemented the Matrix class (in terms of it being a list of vectors and how the give_2d_list() method returns the matrix as a 2d list in a different format from the vectors) so if I modify the way that the __init__() works, then I have to modify this method
    temp_list = self.give_2d_list()
    transposed_vector_list = []
    for sublist in temp_list:
      transposed_vector_list.append(Vector(sublist))
    
    transposed_matrix = Matrix(transposed_vector_list)

    return transposed_matrix

  def matrixMultiply(self, other_matrix):
    """
    This is the function for matrix-vector/matrix-matrix multiplication
    Args:
      other_matrix (Matrix or Vector): The vector/matrix who is being transformed by the calling matrix
    Returns:
      transformed_matrix (Matrix or Vector): The resulting tranformation/vector after being transformed by the calling matrix
    """
    
    if (not isinstance(other_matrix,Matrix)) and (not isinstance(other_matrix,Vector)):
      raise TypeError(f"matrixMultiply() can only multiply matrices wih other matrices or vectors, not {type(other_matrix)} objects")
    elif isinstance(other_matrix, Vector):
      if len(self.vector_list) != len(other_matrix.components):
        raise Exception("Cannot multiply matrices of incompatible dimensions")
    elif isinstance(other_matrix, Matrix):
      if len(self.vector_list) != len(other_matrix.vector_list[0].components):
        raise Exception("Cannot multiply matrices of incompatible dimensions")

    if isinstance(other_matrix, Vector):
      other_matrix_vectors = [other_matrix] # Turns it into a 2d list due to how the algorithm works for matrix multiplication
    else:
      other_matrix_vectors = other_matrix.vector_list

    transformed_matrix_list = []

    for vector in other_matrix_vectors:
      transformed_vector = Vector([0]*len(self.vector_list[0].components)) # Creates the zero vector
      for index, comp in enumerate(vector.components):
        # (Note to self) This calculation could be a bit cleaner if you made __iadd__() for the Vector class
        transformed_vector = transformed_vector + self.vector_list[index]*comp
      transformed_matrix_list.append(transformed_vector)
    
    if len(transformed_matrix_list) == 1:
      transformed_matrix = transformed_matrix_list[0]
    else:
      transformed_matrix = Matrix(transformed_matrix_list)

    return transformed_matrix
  
  def inverseMatrix(self):
    """
    Returns the inverse matrix of the calling object
    """

    if not self.square:
      raise Exception("Only square matrices can be exponentiated")

    identity_matrix_list = []
    for i in range(0,len(self.vector_list)):
      sublist = []
      for j in range(0,len(self.vector_list[0].components)):
        if i == j:
          sublist.append(1)
        else:
          sublist.append(0)
      identity_matrix_list.append(sublist)

    # Below is the code for creating the augmented matrix

    temp_list = self.vector_list.copy()
    for sublist in identity_matrix_list:
      temp_list.append(Vector(sublist))

    temp_matrix = Matrix(temp_list)
    temp_matrix = Op.reducedRowEchelonForm(temp_matrix)
    midpoint = math.floor((len(temp_matrix.vector_list)-1)/2)
    inverse_matrix_list = temp_matrix.vector_list[midpoint+1:] # The +1 is there because (by default), the starting index in inclusive for list slicing. Therefore, I needed to add 1 to make it exclusive.
    
    return Matrix(inverse_matrix_list)
  
  def __pow__(self, exponent):
    """
    Raises a matrix to any power
    Args:
      exponent (int): An integer value
    Returns:
      exponentiated_matrix (Matrix): The power of the exponentiation
    """
    if not self.square:
      raise Exception("Only square matrices can be exponentiated")
    elif not isinstance(exponent,int):
      raise TypeError("Matrix object can only be raised the power of an integer")
    
    # Inverts the matrix if the exponent is negative
    if exponent < 0:
      temp_matrix = self.inverseMatrix()
    else:
      temp_matrix = self

    original_matrix = Matrix(temp_matrix.vector_list.copy())
    exponentiated_matrix = Matrix(temp_matrix.vector_list.copy())
    for i in range(0,abs(exponent)-1):
      exponentiated_matrix = exponentiated_matrix.matrixMultiply(original_matrix)
    
    return exponentiated_matrix

  def __str__(self):
    """
    Returns a list of the components of the vectors in the Matrix object
    """
    printable_list = str(self.give_2d_list())
    return printable_list

class Op():
  """
  This class will be used to perform more complex operations on vectors and matrices
  """

  @staticmethod
  def dotProduct(v1, v2):
    """
    Operation for the dot product of two vectors
    Args:
      v1 (Vector): An operand in the dot product
      v2 (Vector): The other operand in the dot product
    Returns:
      scalar (int or float): The scalar that is outputed from the dot product
    """
    if Vector.isSameDimension(v1, v2):
      scalar = 0
      # The arrangement of v1 and v2 in this calculation does not matter because dot product is commutative
      for index, comp in enumerate(v2.components):
        scalar += v1.components[index]*comp
    else:
      raise Exception("Cannot evaluate the dot product of two vectors with different dimesions")
    return scalar

  @staticmethod
  def crossProduct(v1, v2):
    """
    Operation for the cross product of two vectors
    Args:
      v1 (Vector): The first operand in the cross product
      v2 (Vector): The second operand in the dot product
    Returns:
      v3 (Vector): The cross product of v1 & v2 (a Vector orthogonal to v1 & v2 whose magnitude is equal to the magnitude of v1 & v2's determinant)
    """
    # Note, even though the method is validating that the two vectors are exclusively in 3d, it is possible to have a cross product in 7d if you treat the vectors like octonions (but I have yet to learn enough about this subject to give compute a 7d cross product)

    if len(v1.components) == 3 and len(v2.components) == 3:
      x_comp = (v1.components[1]*v2.components[2]) - (v1.components[2]*v2.components[1])
      y_comp = (v1.components[2]*v2.components[0]) - (v1.components[0]*v2.components[2])
      z_comp = (v1.components[0]*v2.components[1]) - (v1.components[1]*v2.components[0])
      v3 = Vector([x_comp,y_comp,z_comp])
    else:
      raise Exception("Cross product can only be used for vectors exclusively in 3d")

    return v3
  
  @staticmethod
  def angleBetweenVectors(v1, v2):
    """
    Finds the angle between to given vecters using the dot product
    Args:
      v1 (Vector): The first vector
      v2 (Vector): The second vector
    Returns:
      angle (float): The angle between the two vectors (in degrees)
    """
    if Vector.isSameDimension(v1, v2):
      if v1.magnitude() == 0 or v2.magnitude() == 0:
        raise ValueError("Cannot find the angle between two vectors if one of them is the zero vector")
      numerator = cls.dotProduct(v1,v2)
      denominator = v1.magnitude()*v2.magnitude()
      
      angle = math.acos(numerator/denominator)
      # converts to degrees
      angle = round(angle*(360/math.tau), 2)
    else:
      raise Exception("Cannot evaluate the angle between two vectors with different dimesions")
    return angle

  @staticmethod
  def hadamardProduct(mat1, mat2):
    """
    Computes the hadamard product of two matrices/vectors
    Args:
      mat1 (Matrix or Vector): The first matrix/vector
      mat2 (Matrix or Vector): The second matrix/vector
    Returns:
      result (Matrix or Vector): The hadamard product of both vectors/matrices
    """
    # This is the simplest thing to calculate (just multiply the components)
    
    if isinstance(mat1,Vector) and isinstance(mat2,Vector):
      if not Vector.isSameDimension(mat1,mat2):
        raise Exception("Cannot evaluate the hadamard product of two vectors with different dimensions")
      result = []
      for i in range(0,len(mat1.components)):
        result.append(mat1.components[i] * mat2.components[i])
      result = Vector(result)
    elif isinstance(mat1,Matrix) and isinstance(mat2,Matrix):
      if (len(mat1.vector_list) != len(mat2.vector_list)) or (len(mat1.vector_list[0].components) != len(mat2.vector_list[0].components)):
        raise Exception("Cannot evaluate the hadamard product of two matrices with different dimensions")
      mat1 = mat1.give_2d_list()
      mat2 = mat2.give_2d_list()
      result = []
      for row in range(0,len(mat1)):
        sublist = []
        for col in range(0,len(mat1[0])):
          sublist.append(mat1[row][col]*mat2[row][col])
        result.append(sublist)
      result = Matrix.from_2d_list(result)
    else:
      raise TypeError("Hadamard product can only be evaluated for 2 vectors or 2 matrices")

    return result

  @staticmethod
  def trace(mat):
    """
    Computes the trace of the matrix (trace is the sum of the matrix's diagonals)
    Args:
      mat (Matrix): A square matrix
    Returns:
      result (float or int): The sum of the matrix's diagonals
    """

    if not isinstance(mat,Matrix):
      raise TypeError(f"Cannot evaluate the trace of a {type(mat)} object")
    elif not mat.square:
      raise Exception("Cannot evaluate the trace of a non-square matrix")

    mat = mat.give_2d_list()

    result = 0
    for i in range(0,len(mat)):
      result += mat[i][i]
    
    return result

  @staticmethod
  def reducedRowEchelonForm(mat):
    """
    Converts a matrix into reduced row echelon form
    Args:
      mat (Matrix): A matrix of any dimension
    Returns:
      rref_matrix (Matrix): The same matrix in reduced row echelon form
    """

    if not isinstance(mat,Matrix):
      raise TypeError(f"Cannot convert a {type(mat)} object into reduced row echelon form")

    # BTW this code below has multiple return statements so maybe later I should modify it to only have one return statement

    num_rows = len(mat.vector_list[0].components)
    num_cols = len(mat.vector_list)
    mat = mat.give_2d_list() # Redefines the mat variable as a 2d list of floats/ints
    lead = 0
    for r in range(0,num_rows):
      if num_cols <= lead:
        return # The matrix cannot be put into rref
      i = r
      while mat[i][lead] == 0:
        i += 1
        if num_rows == i:
          i = r
          lead += 1
          if num_cols == lead: # This occurs if an entire column (that has a pivot point) in the matrix is full of zeroes
            # The two cases where this exception will occur is if:
            # 1. There is an infinite solution (common line of intersection in 3d as an example)
            # 2. There are no common points of intersection
            raise Exception("Matrix cannot be put into reduced row echelon form")
      mat[i], mat[r] = mat[r], mat[i]
      value = mat[r][lead]
      for j in range(0,num_cols):
        mat[r][j] /= value
      for i in range(0,num_rows):
        if i == r:
          continue
        value = mat[i][lead]
        for j in range(0,num_cols):
          mat[i][j] -= value * mat[r][j]
      lead += 1
    
    # I put the for loop below to convert any -0.0 into 0.0
    for row in range(0,len(mat)):
      for col in range(0,row):
        if mat[row][col] == -0.0:
          mat[row][col] = 0.0

    rref_matrix = Matrix.from_2d_list(mat)

    return rref_matrix

  @staticmethod
  def determinant(mat):
    """
    Computes the determinant of a provided matrix
    Args:
      mat (Matrix): A square matrix
    Returns:
      det (float): The signed volume of the polytope formed by the matrix's vectors
    """
    if not isinstance(mat,Matrix):
      raise TypeError(f"Cannot evaluate the determinant of a {type(mat)} object")
    elif not mat.square:
      raise Exception("Cannot evaluate the determinant of a non-square matrix")
    
    # Code below converts the matrix into row echelon form (not reduced)

    mat = mat.give_2d_list() # mat will be converted into an upper triangular matrix
    multiplication_list = [] # This is a list that records all of the coefficients used to multiply the rows
    # Each sublist in multiplication_list represents the coefficients used in the subtraction of each row in each collumn

    for col in range(0,len(mat[0])):
      multiplication_sublist = []
      for row in range(0,len(mat)):
        pivot = mat[col][col]
        current_value = mat[row][col]
        i = 0
        while mat[col][col] == 0: # If the pivot value is 0, the program checks every row below to see if there exists one that has a none zero value in the same collumn
          if mat[i][col] != 0:
            # This adds a row to the pivot row to get rid of the zero in the pivot element
            for j in range(0,len(mat)):
              mat[col][j] += mat[i][j]
            # There is no break used here because the pivot is modified
          elif i == len(mat)-1:
            # This means that all the values in the collumn are zero
            # If this occurs, the determinant is simply zero
            return 0
          i += 1
        if row <= col:
          continue
        # These variables have to be defined here because the code above might have modified the matrix
        pivot = mat[col][col]
        current_value = mat[row][col]
        coefficient = current_value / pivot
        multiplication_sublist.append(coefficient)
        # subtracts one row from another
        for i in range(0,len(mat)):
          mat[row][i] -= coefficient * mat[col][i]
      multiplication_list.append(multiplication_sublist)

    # Below is the code for creating the lower triangular matrix (technically this is not needed because its determinant will always be 1 but I think it is cool)
    lower_triangular_matrix = []
    for row in range(0,len(mat)):
      sublist = []
      for col in range(0,len(mat[0])):
        if col == row:
          sublist.append(1)
        elif col > row:
          sublist.append(0)
        elif col < row and col != len(mat)-1:
          sublist.append(multiplication_list[col][row-(col+1)]) # The row-(col+1) is done to make sure it gets the right element from multiplication list
      lower_triangular_matrix.append(sublist)

    # Now both the upper and lower triangular matrices have been made.
    # All that is left is to compute their determinants and multiply them
    # The determinant of a triangular matrix is computed by multiplying the diagonal elements

    lower_determinant = 1 # This will still technically be 1 after the multiplication
    for i in range(0,len(lower_triangular_matrix)):
      lower_determinant *= lower_triangular_matrix[i][i]
    
    upper_determinant = 1 # Set to 1 b/c it is the multiplicative identity
    for i in range(0,len(mat)):
      upper_determinant *= mat[i][i]

    det = lower_determinant * upper_determinant

    return det

    
# ---------------------------
# Below is the main.py code
# ---------------------------

my_list1 = [
  [0],
  [0],
]
my_list2 = [
  [1,0,-2,0],
  [5,2,-1,0],
  [2,0,-4,1]
]
my_list3 = [
  [1,0,1,0],
  [2,0,-3,0],
  [4,0,-1,0]
]

M1 = Matrix.from_2d_list(my_list1)
M2 = Matrix.from_2d_list(my_list2)
M3 = Matrix.from_2d_list(my_list3)

v1 = Vector([1,2,3])

print(Op.reducedRowEchelonForm(M2))
