"""***************************************************************************
Title:          Radioactive Atom
File:           RadAtom.py
Release Notes:  In development

Author:         Nik Paulic

Purpose:        This app creates classes to generate an atom, another atom
                that may or may not be radioactive, and a bottle/container
                for the atoms that consists of a mix of these atoms.
Description:    Using complex numbers, this software assigns probabilities to
                a container to determine the concentration of hazardous atoms
                within.
***************************************************************************"""

"""*********************Libraries******************************************"""
from ComplexNumbers import ComplexNumber, ComplexMatrix


"""*********************Classes********************************************"""
'========================================='
class Atom():
    """
    Initialization of an atom class
    """
    def __init__(self):
        """
        Initializes an atom that is not radioactive
        """
        self._radioactive = False
        
    
    @property
    def radioactivity(self):
        """
        Returns the radioactivity status of the atom
        """
        return self._radioactive


'========================================='
class SketchyAtom(Atom):
    """
    Initialization of an atom class
    """
    def __init__(self):
        """
        Initializes an atom that may be radioactive
        """
        super().__init__()
        self.__decay_probability = (abs(ComplexNumber.probability()))**2
    
    @property
    def radioactivity(self):
        """
        Returns the radioactivity status of the atom
        """
        if self.__decay_probability > 0.5:
            self._radioactive = True
        return self._radioactive
    

class Bottle():
    def __init__(self, num_atoms = 100):
        """
        Initializes the bottle properties based on user input of num of atoms
        """
        self.num_atoms = num_atoms 
        self.bottle = [] 
        self.probabilities = self.generate_probabilities()
    
    
    def bottle_contents(self):
        """
        Decodes the probabilities to generate atoms in the bottle
        """
        # Initializing the vial in the box
        bottle_probabilities = self.probabilities.matrix
        
        # Calculating whether or not an atom or sketchy atom is present
        for row in bottle_probabilities:
            for element in row:
                if (abs(element))**2 > 0.5: 
                    self.bottle.append(SketchyAtom())
                else:
                    self.bottle.append(Atom())
        
        return self.bottle
        
        
    def generate_probabilities(self):
        """
        Generates the probability matrix for the types of atoms in the bottle
        """
        column = []
        for i in range(1):
            row = []
            for j in range(self.num_atoms):
                row.append(ComplexNumber.probability())
            column.append(row)
        return ComplexMatrix(column)


"""*********************Main Routine***************************************"""
# Runs the main routine
if __name__ == "__main__":
    None