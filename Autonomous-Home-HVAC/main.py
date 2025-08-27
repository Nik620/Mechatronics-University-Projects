"""***************************************************************************
Title:          Home Automation HVAC Controls System
File:           main.py
Release Notes:  N/A

Author:         Nik Paulic

Description:    The main application to call and run the GUI, Model, and the
                controller.
***************************************************************************"""

"""*********************Libraries******************************************"""
import controller


"""*********************Main Routine***************************************"""
if __name__ == "__main__":
    try:
        # Create the controller
        controller = controller.ThermostatController()
        
    except Exception as e:
        print(f"Critical error: {e}")
