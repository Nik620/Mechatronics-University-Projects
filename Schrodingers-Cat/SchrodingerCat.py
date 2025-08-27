"""***************************************************************************
Title:          Schrodinger's Cat
File:           SchrodingerCat.py
Release Notes:  In development

Author:         Nik Paulic

Purpose:        This program creates a simulation of the Schrodinger's cat
                experiment - in which a cat and a vial/bottle of hazardous
                material are placed in a box together. Once opened, we 
                determine whether or not the cat is alive or dead depending on
                the state of the vial.
Description:    In compilation of the programs QuantumCat and RadAtom, we can
                use the objects created with those software to create a GUI
                in this simulation.
***************************************************************************"""

"""*********************Libraries******************************************"""
import sys
import QuantumCat
import RadAtom
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QGridLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

"""*********************Functions******************************************"""
'========================================='
def experiment():
    """
    Runs the GUI
    """
    app = QApplication(sys.argv)
    window = Gui()
    window.show()
    sys.exit(app.exec_())
    

"""*********************Classes********************************************"""
'========================================='
class Box():
    """
    Initializes the box class
    """
    def __init__(self, bottle = RadAtom.Bottle()):
        """
        Within the box, a cat and bottle of a substance are initialized
        """
        self.cat = QuantumCat.Cat()
        self.bottle = bottle.bottle_contents()
        
        
    def open_box(self):
        """
        Returns the state of the cat when box is opened based on the bottle
        """
        # Calculate the vial hazard
        bottle_hazard = 0
        bottle_size = len(self.bottle)
        for atom in self.bottle:
            if atom.radioactivity:
                bottle_hazard += 1
        hazard_concentration = bottle_hazard / bottle_size
                
        # Lethal dose is 27 radioactive atoms of 100
        return self.cat.alive(hazard_concentration >= .27)  
        
        
'========================================='
class Gui(QMainWindow):
    """
    Initializes and runs a GUI calling on PyQt5 library
    
    Arguments: A Box object
    """
    def __init__(self, box = Box()):
        """
        Generates the main GUI and initializes the box, button, and title
        """
        super().__init__()
        
        # Initializing window
        self.setWindowTitle("Schrodinger's Cat")
        self.resize(1000,600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setStyleSheet('background-color: white;')
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        
        # Button
        self.button = QPushButton("Open Box", central_widget)
        self.button.clicked.connect(self.opened_box)
        self.button.setFixedSize(80, 40)
        self.button.move(450, 550) 
        
        # Title
        title = QLabel("Schrodinger's Cat Experiment", self)
        title.setFixedSize(550, 60)
        title.setFont(QFont("Aptos", 20))
        title.move(250, 10) 
        
        # Box Initialization
        self.box = box
        self.box_image = QLabel(self)
        self.box_pixmap = QPixmap("closed_box.png")
        self.box_resize = self.box_pixmap.scaled(570, 445, Qt.KeepAspectRatio)
        self.box_image.setPixmap(self.box_resize)
        self.box_image.setFixedSize(self.box_resize.size())
        self.box_image.setAttribute(Qt.WA_TranslucentBackground, True)
        self.box_image.move(150,80)
        
        # Add feature to provide instructions on how to operate the GUI

    
    def opened_box(self):
        """
        Updates the images to illustrate the box with the inner contents
        """
        self.button.hide()
        self.box_pixmap = QPixmap("open_box.png")
        self.box_resize = self.box_pixmap.scaled(570, 445, Qt.KeepAspectRatio) 
        self.box_image.setPixmap(self.box_resize)
        
        if self.box.open_box():
            cat_pixmap = QPixmap("cat_alive.png")
            atom_pixmap = QPixmap("stable_atom.png")
        else:
            cat_pixmap = QPixmap("cat_dead.png")
            atom_pixmap = QPixmap("radioactive_atom.png")
        
        # Cat Image
        cat_image = QLabel(self)
        cat_resized = cat_pixmap.scaled(180, 230, Qt.KeepAspectRatio)
        cat_image.setPixmap(cat_resized)
        cat_image.setFixedSize(cat_resized.size())
        cat_image.setAttribute(Qt.WA_TranslucentBackground, True)
        cat_image.move(280,250)
        cat_image.show()
        
        # Atom Image
        atom_image = QLabel(self)
        atom_resized = atom_pixmap.scaled(70, 150, Qt.KeepAspectRatio)
        atom_image.setPixmap(atom_resized)
        atom_image.setFixedSize(atom_resized.size())
        atom_image.setAttribute(Qt.WA_TranslucentBackground, True)
        atom_image.move(460,300)
        atom_image.show()
        
        # Call for feature to reset gui
        
        
    def restore_gui(self):
        """
        Method to restore the session for a new experiment
        """
        return None
        

"""*********************Main Routine***************************************"""
# Runs the main routine
if __name__ == "__main__":
    experiment()