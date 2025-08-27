"""***************************************************************************
Title:          Complex Numbers
File:           ComplexNumbers.py
Version:        3.1.0
Release Notes:  Revised the absolute value of complex number to an overloaded
                function instead of a property. Added additional feature to
                take a complex number to an exponent, as well as to compare 
                greater than or less than. Also added a random complex number
                generator.

Author:         Nik Paulic

Purpose:        Generates complex numbers, creates matrices, and multiplies
                matrices (in addition to complex number addition and 
                multiplication).
Description:    This file is used to support the user in complex number matrix
                multiplication. It also has the capacity to convert a set of
                values to a complex number, add/subract, and multiply them.
***************************************************************************"""
"""*********************Libraries******************************************"""
import math
import gc
import random


"""*********************Functions******************************************"""
'========================================='
def debugging_mode():
    """
    Runs debugging mode with a viewer for the garbage collection
    
    Note: Some assistance from chatGTP
    """
    print("Debug mode active")
    complex_A = ComplexNumber(1, -3, debug=True)
    complex_B = ComplexNumber(0, 4, debug=True)
    print(complex_A)
    print(complex_B)

    # Performing some operations
    complex_A.print_operation_results(complex_B, "+")
    complex_B.print_operation_results(complex_A, "-")
    complex_A.print_operation_results(complex_B, "*")
    complex_A.print_polar_coordinates()

    # Cleaning memory
    print("Deleting objects")
    del complex_A
    del complex_B
    
    # Garbage collection
    print("It's garbage collection time!")
    gc.collect()
    print("Garbage collection complete")


def test_matrix_operations():
    """
    Runs several matrix operations to test file
    """
    matrix_A = ComplexMatrix([[ComplexNumber(1,1), ComplexNumber(2,0)], 
                              [ComplexNumber(0,0), ComplexNumber(2,5)]])
    matrix_B = ComplexMatrix([[ComplexNumber(5,-5), ComplexNumber(0,-2)], 
                              [ComplexNumber(0,4.2), ComplexNumber(-11.1,0)]])
    matrix_A.print_matrix_multiplication(matrix_B, 'v')
    matrix_A.print_matrix_multiplication(matrix_B, 'm')


"""*********************Classes********************************************"""
'========================================='
class ComplexNumber:
    """
    Creates a complex number and manipulates it with operators
    """
    def __init__(self, real_number, imaginary_number, debug = False):
        """
        Creates the real and imaginary parts of the class
        
        Arguments: Number input to represent the real component (float)
                   Number input for the imaginary component (float)
        """
        self.__debug = debug
        try:
            if (isinstance(real_number, (int, float)) and 
                isinstance(imaginary_number, (int, float))):
                self.__real_number = round(real_number, 2)
                self.__imaginary_number = round(imaginary_number, 2)
            else:
                raise TypeError
        except:
            print(real_number, " ", imaginary_number)
            print("E01: The inputs must be a ComplexNumber as [a, b].\n")
            return None  
        
        
    def __del__(self):
        """ 
        Destructor that prints a debug message when instance is destroyed
        
        Note: Some support with chatGTP
        """
        if hasattr(self, '__debug') and self.__debug == True:
            print(self.complex_str, " is being destroyed.")
            
            
    def __str__(self):
        """
        Returns: The complex number (string)
        Note: The function is made with chatGTP
        """
        complex_number = self.complex_str
        return complex_number
    
    
    def __add__(self, number):
        """
        Adds two complex numbers together
        
        Arguments: Two complex numbers (ComplexNumber)
        Returns: An added complex number (ComplexNumber)
        """
        if ComplexNumber._complex_checker(number):
            realPart = (self.real + number.real)
            imaginaryPart = (self.imaginary + number.imaginary)
            return ComplexNumber(realPart, imaginaryPart)
        else:
            # Returns for failure to comply with __complex_checker
            return None
    

    def __sub__(self, number):
        """
        Subtracts two complex numbers together
        
        Arguments: Two complex numbers (ComplexNumber)
        Returns: A subtracted complex number (ComplexNumber)
        """
        if ComplexNumber._complex_checker(number):
            realPart = (self.real - number.real)
            imaginaryPart = (self.imaginary - number.imaginary)
            return ComplexNumber(realPart, imaginaryPart)
        else:
            # Returns for failure to comply with __complex_checker
            return None
    

    def __mul__(self, number):
        """
        Multiplies two complex numbers together
        
        Arguments: Two complex numbers (ComplexNumber)     
        Returns: A multiplied complex number (ComplexNumber)
        """
        if ComplexNumber._complex_checker(number):
            realPart = (self.real * number.real - 
                        self.imaginary * number.imaginary)
            imaginaryPart = (self.real * number.imaginary + 
                             self.imaginary * number.real)
            return ComplexNumber(realPart, imaginaryPart)
        else:
            # Returns for failure to comply with __complex_checker
            return None
        
        
    def __abs__(self):
        """
        Creates the absolute value of a complex number.
        """
        absolute_val = math.sqrt((self.real)**2 + (self.imaginary)**2)
        return absolute_val
        
    
    def __pow__(self, exponent):
        """
        Runs the exponent/power operation on a number, exponent must be an int
        """
        try:
            if isinstance(exponent, int) and exponent >= 0:
                power = self
                exponent -= 1
                while exponent != 0:
                    power = power * self
                    exponent -= 1
                return power
            else:
                raise TypeError
        except:
            print(exponent)
            print("E15: The input must be an integer > 0, ex. 3\n")
            return False 
        
    
    def __gt__(self, number):
        """
        Performs a greater than operation for a complex number.
        """
        if ComplexNumber._complex_checker(number):
            value_1 = abs(self)
            value_2 = abs(number)
            if value_1.real > value_2.real:
                return True
            else:
                return False
        else:
            # Returns for failure to comply with __complex_checker
            return None
        
    
    def __lt__(self, number):
        """
        Performs a greaterthan operation for a complex number.
        """
        if ComplexNumber._complex_checker(number):
            value_1 = abs(self)
            value_2 = abs(number)
            if value_1.real < value_2.real:
                return True
            else:
                return False
        else:
            # Returns for failure to comply with __complex_checker
            return None
        
        
    @property
    def real(self):
        """
        Returns: The real number (float)
        """
        return self.__real_number 
    
    
    @property
    def imaginary(self): 
        """
        Returns: The imaginary number (float)
        """
        return self.__imaginary_number 
    
    
    @property
    def complex_num(self):
        """
        Returns: The complex number (list of floats)
        """
        return [self.__real_number, self.__imaginary_number]
    
    
    @property
    def complex_str(self):
        """
        Returns: The complex number (string)
        Note: The function is made partially with chatGTP
        """
        # real > or < 0, imaginary > 0
        if ((self.__real_number > 0 or self.__real_number < 0) 
            and self.__imaginary_number > 0): 
            complex_number = (str(self.__real_number) + "+" + 
                              str(self.__imaginary_number) + "i")
        
        # real > or < 0, imaginary < 0
        elif ((self.__real_number > 0 or self.__real_number < 0) 
            and self.__imaginary_number < 0): 
            complex_number = (str(self.__real_number) +  
                              str(self.__imaginary_number) + "i")
        
        # real > or < 0, imaginary = 0
        elif ((self.__real_number > 0 or self.__real_number < 0) 
              and self.__imaginary_number == 0):
            complex_number = str(self.__real_number)
            
        # real = 0, imaginary > or < 0
        elif self.__real_number == 0 and (self.__imaginary_number > 0 
                                          or self.__imaginary_number < 0):
            complex_number = str(self.__imaginary_number) + "i"
        
        # real and imaginary = 0
        else:
            complex_number = str(self.__real_number)
            
        return complex_number 
    
    
    @property
    def phase(self):
        """
        Returns: The phase of the complex number (float)
        """
        return round(math.atan2(self.__imaginary_number, 
                                self.__real_number), 2)
    
    
    @property
    def polar_num(self):
        """
        Returns: The phase of the complex number (list of floats)
        """
        return [self.absolute_value, self.phase]
    
    
    @property
    def polar_str(self):
        """
        Returns: The phase of the complex number (string)
        """
        polar = (str(self.absolute_value) + "cis(" + 
                 str(self.phase) + ")")
        return polar
    
    
    @staticmethod
    def _complex_checker(number):
        """
        Checks whether or not the input is a ComplexNumber object
        
        Argument: A complex number (ComplexNumber)
        Returns: True if a ComplexNumber object or returns to user to retry
        """
        try:
            if isinstance(number, ComplexNumber):
                return True
            else:
                raise TypeError
        except:
            print(number)
            print("E02: The input is not a ComplexNumber\n")
            return False 
        
        
    @staticmethod
    def generator(lower_real, upper_real, lower_imaginary, upper_imaginary):
        """
        Returns a random complex number
        
        Argument: the lower/upper bounds of a real/imaginary numbers
        Returns: A complex number
        """
        try:
            real = random.uniform(lower_real, upper_real)
            imaginary = random.uniform(lower_imaginary, upper_imaginary)
            return ComplexNumber(real, imaginary)
        except:
            print("E16: The inputs must be in order of 1) lower bound of ",
                  "real num, 2) upper bound of real num, 3) lower bound of ",
                  "imaginary num, and 4) upper bound of imaginary num. ",
                  "For example, generator(2,5,3,7)")
            return None
        
    
    @staticmethod
    def probability():
        """
        Returns a random complex number whose square of absolute val is <= 1
        """
        real = random.random()
        imaginary = random.random()
        while (real ** 2 + imaginary ** 2) > 1:
            real = random.random()
            imaginary = random.random()
        return ComplexNumber(real, imaginary)
        
        
    def print_operation_results(self, number, operation):
        """
        Prints & returns the complex addition, subtraction, or multiplication
        
        Arguments: Two complex numbers (ComplexNumber)
                   An input of the operation "+", "-", or "*" (string)
        Returns: An operated new complex number (ComplexNumber)
        Note: Idea for enumerator heavily supported by chatGTP
        """
        operation = operation.lower()
        operations = {
            "+": self + number,
            "-": self - number,
            "*": self * number
            }
        
        try:
            if operation in operations:
                print("The result of ", self, operation, number, " yields ",
                      operations[operation], "\n")
                return operations[operation]
            else:
                raise TypeError 
        except:
            print(operation)
            print("E03: The operator needs to be one of: \n",
                  "+, -, or * (in parenthesis).\n")
            return None
    
    
    def print_polar_coordinates(self):
        """
        Prints and returns the polar coordinates
        
        Arguments: A complex number (ComplexNumber)
        Returns: The resulting polar coordinates from complex_str (string)
        """
        polar = self.polar_str
        print("The polar coordinates of ", self.complex_str, " is ",
              polar, "\n")
        return polar

 
'========================================='
class ComplexMatrix(ComplexNumber):
    """
    Creates a class for complex number matrices with matrix multiplication
    and element-wise products (vectors).
    """
    def __init__(self, matrix):
        """
        Initializes the 2x2 matrix with complex number elements.
        
        Arguments: A matrix in the format of list of lists
        """
        try:
            if isinstance(matrix, list):
                row_length = len(matrix[0])
                for row in matrix:
                    if not(isinstance(row, list)):
                        raise ValueError
                    if len(row) != row_length:
                        raise ValueError
                    for element in row:
                        if not(element, ComplexNumber):
                            raise TypeError
                self.__matrix = matrix
            else:
                raise ValueError
        except ValueError:
            print("E05: The input must be a vector or matrix in a list of ",
                  "list format, ie. [[1, 2, 3]] or [[1],[2],[3]]. Rows must",
                  " be of equal length if multiple rows input.")
            return None
        except TypeError:
            print("E04: All elements must be instances of ComplexNumber")
            return None
        except:
            print("E07: Error with initialization")
            return None
    
    
    def __str__(self):
        """
        Returns: The complex matrix (string)
        """
        return str(self.matrix_num)
    
    
    def __mul__(self, matrix):
        """
        Multiplies matrices or vectors and returns the products.
        
        Arguments: Two compatable matrices or vectors (ComplexMatrix)
        Returns: The product matrix or vector (ComplexMatrix).
        Notes: The matrix multiplication simplified with ChatGTP
        """
        try:
            # Check for class type
            if not(self.__complex_matrix_checker(matrix)):
                raise TypeError
                
            # Check for multiplication size compatability
            matrix_1_size = self.matrix_size
            matrix_2_size = matrix.matrix_size
            # Matrix Multiplication
            if (matrix_1_size[1] == matrix_2_size[0]):
                # Initialize the result matrix with zeros 
                result = ([[ComplexNumber(0, 0) for _ in 
                            range(matrix_2_size[1])] for _ in 
                           range(matrix_1_size[0])])
                # Perform matrix multiplication 
                matrix1 = self.matrix
                matrix2 = matrix.matrix
                for i in range(matrix_1_size[0]): 
                    for j in range(matrix_2_size[1]): 
                        for k in range(matrix_2_size[0]): 
                            result[i][j] += matrix1[i][k] * matrix2[k][j]
                return ComplexMatrix(result)
            
            else:
                raise ValueError
        except TypeError: 
            print("E08: Both entries must be ComplexMatrix values") 
            return None 
        except ValueError: 
            print("E10: These matrices are not compatible to multiply.") 
            return None 
        except Exception as e: 
            print(f"Unexpected error: {e}") 
            return None
        
        
    @property
    def matrix(self):
        """
        Returns: The complex matrix to prevent name mangling (ComplexMatrix)
        """
        return self.__matrix
    
    
    @property
    def matrix_num(self):
        """
        Returns: The complex matrix (Matrix of ComplexNumbers)
        """
        matrix_num = []
        for row in self.__matrix: 
            row_content = []
            for element in row:
                row_content.append(element.complex_str)
            matrix_num.append(row_content)
        return matrix_num
    
    @property
    def matrix_size(self):
        """
        Returns: A list of the matrix size as rows and columns
        """
        columns = 0
        rows = 0
        for row in self.__matrix:
            if rows == 0:
                for element in row:
                    columns += 1
            rows += 1
        return [rows, columns]
    
    
    @staticmethod
    def __complex_matrix_checker(matrix):
        """
        Checks for whether or not the matrix is 2x2 and uses ComplexNumber
        
        Arguments: A matrix (ComplexMatrix)
        Returns: True or returns to user to try again (Bool)
        Note: The function is heavily supported with chatGTP
        """ 
        try:
            if isinstance(matrix, ComplexMatrix):
                return True
            else:
                raise TypeError
        except:
            print(matrix)
            print("E09: The input is not a ComplexMatrix.")
            return False
    
    
    @staticmethod
    def operation_menu():
        """
        Runs a menu for the user to perform either a matrix or vector product
        
        Arguments: The operation for the menu be cast by the user between 'm' 
                   for matrix multiplication, 'v' for vector multiplication, 
                   and 'e' to exit. Once these are cast, the inputs will 
                   request elements for 2 ComplexMatrix objects.
        Note: Some support with chatGTP
        """        
        # Matrix Building
        while True:
            if not ComplexMatrix.__run_class():
                break
            try:
                print("Enter the dimensions of matrix/vector 1: ")
                mat_1_size = []
                mat_1_size.append(int(input("No. rows: ")))
                mat_1_size.append(int(input("No. columns: ")))
                print("Enter the dimensions of matrix/vector 2: ")
                mat_2_size = []
                mat_2_size.append(int(input("No. rows: ")))
                mat_2_size.append(int(input("No. columns: ")))
                if (mat_1_size[0] <= 0 or mat_1_size[0] <= 0 or 
                    mat_2_size[1] <= 0 or mat_2_size[1] <= 0): 
                    raise ValueError
                print("\nBuilding matrix 1")
                matrix_1 = ComplexMatrix.__matrix_builder(mat_1_size)
                print("\nBuilding matrix 2")
                matrix_2 = ComplexMatrix.__matrix_builder(mat_2_size)
                result = matrix_1 * matrix_2
                print(matrix_1, " multiplied by ", matrix_2, " yields \n",
                      result, "\n")
            except UnboundLocalError:
                print("E14: Unexpected error")
            except:
                print("E12: Please enter an int > 0 for the entry") 
            
    
    @staticmethod
    def __matrix_builder(matrix_size):
        """
        Builds a matrix for the user
        
        Arguments: The size of matrix in form [rows, columns]
        """
        while True:
            try:
                matrix = []
                for row in range(matrix_size[0]):
                    columns = []
                    print("\nrow ", row + 1)
                    for element in range(matrix_size[1]):
                        real = float(input("real part: "))
                        imaginary = float(input("imaginary part: "))
                        columns.append(ComplexNumber(real, imaginary))
                    matrix.append(columns)     
                return ComplexMatrix(matrix)
            except:
                print("E13: please input a number")
    
    
    @staticmethod
    def __run_class():
        while True:
            try:
                print("Welcome to ComplexNumbers")
                operation_type = input("What operation do you need?\n"
                                       "'m' for matrix multiplication\n"
                                       "'e' to exit the program:\n")
                if operation_type == 'm' or operation_type == 'e': break
                else: raise ValueError("Invalid operation type.")
            except:
                print("E11: Please write either 'm' or 'e'\n")
        if operation_type == 'e': return False
        elif operation_type == 'm': return True
        
     
"""*********************Main Routine***************************************"""
# Runs the main routine
if __name__ == "__main__":

    ComplexMatrix.operation_menu()
