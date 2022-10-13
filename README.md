# DEM_PFC2D_models
General code for DEM models using Particle Flow Code (PFC2D) v7.00. These models are part of the "Geomechanical modeling of ground surface deformation associated with thrust and reverse fault earthquakes: a discrete element approach" project. 

README.txt
Each set of project files contains everything requried to reproduce a model in Particle Flow Code (PFC2D) version 7.00.152 or sooner. 
The fish functions file defines each of the fish commands required for a model (e.g., defing the boundary conditions, generating pregrowth layers, making a fault, running the deformation sequence). 
The parameter_def file contains each of the numerical parameters that are modified for each of the trials (e.g., model width, particle radii, cohesion and tensile strength of contact bonds, etc). 
The run file calls each of the parameters and fish functions in the order required for a full generation of sediment and deformation sequence. 
The .sav files are saved states of undeformed (unbounded/unbonded) sediment as well as the last deformation stage (used in figures). These are large files and may take a few minutes to load properly. The unbonded.sav files can be used in place of regenerating sediment. The contact bond strengths can be modified directly from the unbonded.sav or homogeneous_bonded.sav files. 
For the general D5 model code, there is a python script attached (homogenous.py) that will automate a series of trials of varying cohesion and tensile strength of the contact bonds, fault dip angles, and fault seed lengths for a given sediment assemblage (unbonded.sav). This code will call the parameters and fish functions directly rather than iterating through the run file. 
