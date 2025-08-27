"""***************************************************************************
Title:          Quantum Cat
File:           QuantumCat.py
Release Notes:  In development

Author:         Nik Paulic

Purpose:        This app creates a cat object, whose state is dictated by
                whether the input material is hazardous to the cat.
Description:    In creation of the cat object, the object can change its state
                based on a user input.
***************************************************************************"""

"""*********************Libraries******************************************"""
import RadAtom


"""*********************Classes********************************************"""
'========================================='
class Cat():
    """
    Initializes a cat class
    """
    def __init__(self, alive = True):
        """
        Initializes the state of the cat as alive or not
        """
        self.__alive = alive
    
    
    def alive(self, radioactive):
        """
        Based on an atom's state, determines if the cat is alive or not
        """
        if radioactive:
            self.__alive = False
        return self.__alive


"""*********************Main Routine***************************************"""
# Runs the main routine
if __name__ == "__main__":
    None