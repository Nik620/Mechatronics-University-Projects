==============================================================================
COMPLEX NUMBERS (VERSION 3.1.0)
===

The following documentation is to be used to support the operation of:
ComplexNumbers.exe

The software ComplexNumbers.exe is intended to manipulate complex numbers in
cartesian form (addition, subtraction, and multiplication) and in 2x2 matrix
multiplications. Additional conversions to polar form are also available.

Running the software will run through several hardcoded matrix and complex
number operations and print the results.

==============================================================================

Version: 	3.1.0
Release Notes:	Updates to update absolute values, add features for exponents,
add greater than and less than functions
Released: 	2024-11-20

Created by Nik Paulic. ==============================================================================

# CONTENTS

1. Requirements
2. Installation
3. Getting Started
4. How to Use

4.1 Running Executable

4.2 ComplexNumber

4.3 ComplexMatrix

5. Acknowledgements

==============================================================================

1. Requirements
   ===============

This software was designed to be run with Windows 7, 8, 10, and 11 as an
x-64 operating system.

The software uses the requirements of:
Python version 3.10 or later
numpy version 1.26.4 or later

Ensure that the files are extracted from the .zip file prior to execution.



2. Installation
   ===============

Unzip the folder to ensure all of the files are available.



3. Getting Started
   ==================

Relocate the file as desired, double-click to launch the application. If
desired to use the code as a library, ensure that the proper steps are taken
to import the file into the new code.



4. How to use
   ===============

When importing ComplexNumbers.exe as a library, the file must consider that
the executable uses two classes: ComplexNumber and ComplexMatrix.

Testing may be performed with test\_matrix\_operations() and debugging\_mode().



# 4.1 Running Executable

When operating ComplexNumbers.exe, ensure that the instructions are properly
followed. The program will run to input values into two matrices, and then
operate based on vector multiplication or matrix multiplication.

There is no need to compile the executable, and may be run per section 3. To
run the file, either follow section 3 or run it through a command line
(navigate to the directory with the executable file and run).



# 4.2 ComplexNumber

To register a complex number (in cartesian form), you must call the
ComplexNumber as follows:

ComplexNumber(real\_number, imaginary\_number)

To see the contents of the ComplexNumber object, you can simply print
the object:

print(ComplexNumber(2,3))
----> '2+3i'

To get read-only properties of the complex number, the following calls are
permissible:

For example, complex\_1 is a custom inputs as follows:
complex\_1 = ComplexNumber(34.2, 3)

complex\_1.get\_real
----> 34.2

complex\_1.get\_imaginary
----> 3

complex\_1.get\_complex\_num
----> \[34.2, 3]

complex\_1.get\_complex\_str
----> '34.2+3i'

complex\_1.get\_phase
----> 0.09

complex\_1.get\_polar\_num
----> \[34.33, 0.09]

complex\_1.get\_polar\_str
----> '34.33cis(0.09)'

If looking for a random complex number generator, two options are available.
Use generator for a number within restricted bounds, or probability for a
value whose probability is always <= 1.

complex\_1 = ComplexNumber.probability()
----> 0.49+0.7i

complex\_2 = ComplexNumber.generator(1,10,2,10)
----> 5.19+6.45i

To call on complex addition, subtraction, multiplication, printing an
operation, or printing the polar coordinates, the following may be used to
either directly retrieve the new ComplexNumber product or print the product.

For example, complex\_1, complex\_2, and operation are custom inputs as follows:
complex\_1 = ComplexNumber(34.2, 3)
complex\_2 = ComplexNumber(-4, 2)
operation = "+"

complex\_1 + complex\_2
--print()--> 30.2+5i

complex\_1 - complex\_2
--print()--> 38.2+1i

complex\_1 \* complex\_2
--print()--> -142.8+56.4i

abs(complex\_1)
----> 34.33

complex\_1 \*\* 3
----> 39078.29+10499.76i

complex\_1 > complex\_2
----> True

complex\_1 < complex\_2
----> False

complex\_1.print\_operation\_results(complex\_2, operation)
----> The result of  34.2+3i + -4+2i  yields  30.2+5i

complex\_1.print\_polar\_coordinates()
----> The polar coordinates of  34.2+3i  is  34.33cis(0.09)



# 4.3 ComplexMatrix

To register a complex matrix, you must input a list of two lists that
contain two ComplexNumber objects, as follows:

ComplexMatrix(\[\[ComplexNumber(a, b), ComplexNumber(c, d)],
\[ComplexNumber(e, f), ComplexNumber(g, h)]])

It is also permissible to generate complex numbers in variables followed by
inputting into the ComplexMatrix class (and mix if necessary).

To see the contents of the ComplexMatrix object, you can simply print
the object:

print(\[\[ComplexNumber(1,1), ComplexNumber(2,0)],
\[ComplexNumber(0,0), ComplexNumber(2,5)]])
----> '\['1+1i', '2'], \['0', '2+5i']'

To get read-only properties of the complex matrix, the following calls are
permissible:

For example, the custom input of matrix\_1 will be used to demonstrate:
matrix\_1 = ComplexMatrix(\[\[ComplexNumber(1,1), ComplexNumber(2,0)],
\[ComplexNumber(0,0), ComplexNumber(2,5)]])

matrix\_1.matrix
----> a matrix of complex number objects \[\[obj,obj],\[obj,obj]]

matrix\_1.matrix\_num
----> (\['1+1i', '2'], \['0', '2+5i'])

matrix\_1.matrix\_size
----> \[2,2]

To call on matrix multiplication, the following may be used to either directly
retrieve the new ComplexMatrix product or to print the product.

For example, the custom input of matrix\_1 will be used to demonstrate:
matrix\_1 = ComplexMatrix(\[\[ComplexNumber(1,1), ComplexNumber(2,0)],
\[ComplexNumber(0,0), ComplexNumber(2,5)]])
matrix\_2 = ComplexMatrix(\[\[ComplexNumber(5,-5), ComplexNumber(0,-2)],
\[ComplexNumber(0,4.2), ComplexNumber(-11.1,0)]])

matrix\_3 = matrix\_1 \* matrix\_2
--print()--> (\['10.0+8.4i', '-20.2-2.0i'], \['-21.0+8.4i', '-22.2-55.5i'])

Finally, to build a set of custom matrices with guidance, simply use:
ComplexMatrix.operation\_menu()

This will allow the user to input a custom matrix of any size to multiply
with another matrix of any size, pending whether or not the matrices can be
multiplied together.



5. Acknowledgements
   ===================

Thank you to numpy for the use of its libraries and chatGTP for supporting
sections of this software where applicable.



==============================================================================
End

