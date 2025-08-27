"""***************************************************************************
Title:          Rocket Landing Control Simulation
File:           RocketLanding.py
Release Notes:  Initial Release

Author:         Nik Paulic

Description:    This app simulates a rocket landing based on trajectory and
                control data.
***************************************************************************"""

"""*********************Libraries******************************************"""
# Import necessary libraries
from vpython import *
import pandas as pd
import time

"""*********************Global**********************************************"""
data_file = 'StateFeedback3D.csv'
scale = 2
t_factor = 20

"""*********************Functions*******************************************"""
'========================================='
# Load trajectory data (replace 'trajectory.csv' with actual file)
def load_trajectory(file_path):
    data = pd.read_csv(file_path)
    return data['x'], data['y'], data['z'], data['Pitch (deg)'], data['Yaw (deg)'], data['Thrust Pitch Angle (deg)'], data['Thrust Yaw Angle (deg)'], data['Thrust (N)']

'========================================='
def animate_rocket(camera = False):
    
    rocket.axis = vector(1, 0, 0)  # Reset orientation to default
    rocket.up = vector(0, 1, 0)    # Reset "up" vector

    arrow_length = 2 * scale # Adjust scale if needed
    nzl = 2 * scale # Nozzle length
    arrow_offset_magnitude = rocket.length/2 + nzl + arrow_length/2 # Distance "below"

    # Initialize arrow's initial orientation
    arrow.axis = vector(1, 0, 0) * arrow_length # Start along +x
        
    for i in range(len(x)):
        # Adjust camera
        rate(20)  # Controls animation speed
        if camera: 
            # Adjust distance
            scene.camera.pos = vector(rocket.pos.x+10, rocket.pos.y + 10, rocket.pos.z + 30)  
            # Adjust camera position
            scene.camera.axis = rocket.pos - scene.camera.pos
        else: 
            # Adjust distance
            scene.camera.pos = vector(rocket.pos.x, rocket.pos.y, rocket.pos.z + 100)
            # Adjust camera position
            scene.camera.axis = rocket.pos - scene.camera.pos

        # Rocket Position
        rocket.pos = vector(x[i], y[i] + floor_pos + rocket.length * 2, z[i])

        # Rocket Rotation
        rocket_rotation_z = radians(thetaX[i])
        rocket_rotation_y = radians(thetaY[i])
        
        #arrow.axis = cross(rocket.axis.norm() * (thrust[i] / t_factor),vector(0,0,1))
        if i > 0:
            delta_rotation_z = radians(thetaX[i]) - radians(thetaX[i-1])
            delta_rotation_y = radians(thetaY[i]) - radians(thetaY[i-1])
            arrow.rotate(angle=delta_rotation_z, axis=vector(0, 0, 1))
            arrow.rotate(angle=delta_rotation_y, axis=vector(1, 0, 0))
            # Apply rocket rotation
            rocket.rotate(angle=radians(thetaX[i]) - radians(thetaX[i-1]), axis=vector(0, 0, 1))
            rocket.rotate(angle=radians(thetaY[i]) - radians(thetaY[i-1]), axis=vector(1, 0, 0))
                    
        elif i == 0:
            # Set initial arrow orientation to match initial rocket orientation
            arrow.axis = cross(rocket.axis.norm() * arrow_length,vector(0,0,1))
        
        # Arrow Position (Place it "below" the rocket along its local -y axis)
        arrow.pos = rocket.pos - rocket.up.norm() * arrow_offset_magnitude
        
        # Arrow Rotation
        if i == 0:
            arrow.rotate(angle=radians(alphaX[i]), axis=vector(0, 0, 1))   
            arrow.rotate(angle=radians(alphaY[i]), axis=vector(1, 0, 0))
        elif i > 0:
            arrow.rotate(angle=radians(alphaX[i])-radians(alphaX[i-1]), axis=vector(0, 0, 1))   
            arrow.rotate(angle=radians(alphaY[i])-radians(alphaY[i-1]), axis=vector(1, 0, 0))
        
        # Arrow Magnitude
        current_direction = arrow.axis.norm()
        new_magnitude = thrust[i] / t_factor
        if new_magnitude == 0:
            new_magnitude = 0.01
        arrow.axis = current_direction * new_magnitude

'========================================='
# Initiate simulation
def simulate(evt):
    # Load trajectory data and animate rocket
    start_text.visible = False
    animate_rocket()
    animate_rocket(True)

"""*********************Main Routine***************************************"""
# Runs the main routine
if __name__ == "__main__":
    # Import Data
    x, z, y, thetaX, thetaY, alphaX, alphaY, thrust = load_trajectory(data_file) #Note y and z are swapped
    
    # Initialize 3D scene
    scene = canvas(title="Rocket Landing Simulation", width=500, height=500)
    start_text = text(text="Rocket Landing Control", pos=vector(-70, 35, 0), height=10, color=color.white)
        
    # Create ground (lower platform)
    floor_pos = -50 # floor offset
    floor_thk = 0.2
    ground = box(pos=vector(0, floor_pos, 0), size=vector(10, floor_thk, 10), color=color.gray(0.5))
    earth = box(pos=vector(0, floor_pos-floor_thk, 0), size=vector(250, floor_thk, 250), color=color.green)
    
    # Create rocket body
    bcl = 5 * scale
    bcr = 0.6 * scale
    body = cylinder(pos=vector(0, 1, 0), axis=vector(0, bcl, 0), radius=bcr, color=color.white)
    
    # Add nosecone to the rocket
    ncl = 1.52 * 2 * scale
    nosecone = ellipsoid(pos=vec(0, 0, 0), length=bcr*2, height=ncl, width=bcr*2, color=color.cyan)
    
    # Fin Settings
    fbh = .44 * scale # fin height
    fbl = 1.02 * scale # fin length
    fbw = 0.03 * scale # fin depth
    fbd = sqrt(2*fbh*fbh) # diagonal length
    fbt = fbl-fbh # non-slant part
    
    # fin 1
    fin1a = box(pos=vector(0, 0, 0), size=vector(fbd, fbd, fbw), color=color.cyan)
    fin1a.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin1b = box(pos=vector(0, 0, 0), size=vector(fbd/2, fbd/2, fbw), color=color.cyan)
    fin1b.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin1c = box(pos=vector(0, 0, 0), size=vector(fbh, fbt, fbw), color=color.cyan)
    
    # fin 2
    fin2a = box(pos=vector(0, 0, 0), size=vector(fbd, fbd, fbw), color=color.cyan)
    fin2a.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin2b = box(pos=vector(0, 0, 0), size=vector(fbd/2, fbd/2, fbw), color=color.cyan)
    fin2b.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin2c = box(pos=vector(0, 0, 0), size=vector(fbh, fbt, fbw), color=color.cyan)
    
    # fin 3
    fin3a = box(pos=vector(0, 0, 0), size=vector(fbd, fbd, fbw), color=color.cyan)
    fin3a.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin3a.rotate(angle=radians(90), axis=vector(0, 1, 0))
    fin3b = box(pos=vector(0, 0, 0), size=vector(fbd/2, fbd/2, fbw), color=color.cyan)
    fin3b.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin3b.rotate(angle=radians(90), axis=vector(0, 1, 0))
    fin3c = box(pos=vector(0, 0, 0), size=vector(fbh, fbt, fbw), color=color.cyan)
    fin3c.rotate(angle=radians(90), axis=vector(0, 1, 0))
    
    # fin 4
    fin4a = box(pos=vector(0, 0, 0), size=vector(fbd, fbd, fbw), color=color.cyan)
    fin4a.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin4a.rotate(angle=radians(90), axis=vector(0, 1, 0))
    fin4b = box(pos=vector(0, 0, 0), size=vector(fbd/2, fbd/2, fbw), color=color.cyan)
    fin4b.rotate(angle=radians(45), axis=vector(0, 0, 1))
    fin4b.rotate(angle=radians(90), axis=vector(0, 1, 0))
    fin4c = box(pos=vector(0, 0, 0), size=vector(fbh, fbt, fbw), color=color.cyan)
    fin4c.rotate(angle=radians(90), axis=vector(0, 1, 0))
    
    # Rocket Assembly
    hidden = ellipsoid(pos=body.pos+vec(0, scale*8, 0), length=bcr/8, height=bcr/8, width=bcr/8, color=color.black)
    nosecone.pos = body.pos + body.axis  # Adjust based on the body
    fin1a.pos = body.pos + vector(bcr, fbl-fbh, 0)
    fin1b.pos = body.pos + vector(bcr+fbh/2, 0, 0)
    fin1c.pos = body.pos + vector(bcr+fbh/2, fbt/2, 0)
    fin2a.pos = body.pos + vector(-bcr, fbl-fbh, 0)
    fin2b.pos = body.pos + vector(-bcr-fbh/2, 0, 0)
    fin2c.pos = body.pos + vector(-bcr-fbh/2, fbt/2, 0)
    fin3a.pos = body.pos + vector(0, fbl-fbh, -bcr)
    fin3b.pos = body.pos + vector(0, 0, -bcr-fbh/2)
    fin3c.pos = body.pos + vector(0, fbt/2, -bcr-fbh/2)
    fin4a.pos = body.pos + vector(0, fbl-fbh, bcr)
    fin4b.pos = body.pos + vector(0, 0, bcr+fbh/2)
    fin4c.pos = body.pos + vector(0, fbt/2, bcr+fbh/2)
    rocket_body = compound([body, nosecone, fin1a, fin1b, fin1c, fin2a, fin2b, fin2c, 
                            fin3a, fin3b, fin3c, fin4a, fin4b, fin4c])
    rocket = compound([rocket_body, hidden])
    cg_offset = -rocket.length/2 + 2.52
    
    # Thrust
    nzl = 2 * scale
    arrow = arrow(pos=vector(0,0,0), axis=vec(0, -nzl, 0), shaftwidth=1, color=color.orange)
    
    # Start Scene
    scene.bind("click", simulate)