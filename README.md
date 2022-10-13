# DEM_PFC2D_models
General code for DEM models using Particle Flow Code (PFC2D) v7.00. These models are part of the "Geomechanical modeling of ground surface deformation associated with thrust and reverse fault earthquakes: A discrete element approach" project. 

You will need to download PFC2D v7.0 or later to open these files and obtain an Itasca license for the software to run models with > 1000 particles. 

# README.txt
Each set of project files contains everything required to reproduce a model in Particle Flow Code (PFC2D) version 7.00.152 or later. 
The main project file (D5.prj) will open the required data files attached and contain a series of plots to visualize the model (generally the particles and contact bonds) in PFC2D. The models can be run from the command line or iPython console. 
The fish functions file defines each of the fish commands required for a model (e.g., defining the boundary conditions, generating pregrowth layers, making a fault, running the deformation sequence). 
The parameter_def file contains each of the numerical parameters that are modified for each of the trials (e.g., model width, particle radii, cohesion and tensile strength of contact bonds, etc). 
The run file calls each of the parameters and fish functions in the order required for a full generation of sediment and deformation sequence. Sediment will need to be generated first as an unbonded.sav file. This can be done using the run file and calling each of the fish functions. 
There is a python script attached (homogenous.py) that will automate a series of trials of varying cohesion and tensile strength of the contact bonds, fault dip angles, and fault seed lengths for a given sediment assemblage (unbonded.sav). This code will call the parameters and fish functions directly rather than iterating the trials individually through the run file. 
