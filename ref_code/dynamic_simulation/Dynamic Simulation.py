# Access PowerFactory
import os
os.environ["PATH"] = r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2" + os.environ["PATH"]

import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9")

# Import powerfactory
import powerfactory as pf # import the powerfactory module
app=pf.GetApplication() #obtain the application

# Access the project and activate it
user = app.GetCurrentUser()
project = app.ActivateProject("Nine-bus System") # activate the project that I want
prj = app.GetActiveProject()

# app.Show() #(optional)

# Create bus dictionary
buses = app.GetCalcRelevantObjects('*.ElmTerm')
bus_dict = {}
for bus in buses:
    bus_dict[bus.loc_name] = bus

# Create generator dictionary
generators = app.GetCalcRelevantObjects('*.ElmSym')
generator_dict = {}
for generator in generators:
    generator_dict[generator.loc_name] = generator

# Create line dictionary
lines = app.GetCalcRelevantObjects('*.ElmLne')
line_dict = {}
for line in lines:
    line_dict[line.loc_name] = line

# Events name variables
shc_name = 'short circuit event'
switch_name = 'switch event'    

# Create events (short circuit event and switch event)
shc_folder = app.GetFromStudyCase('IntEvt')
shc_folder.CreateObject('EvtShc', shc_name) # create short circuit event
shc_folder.CreateObject('EvtSwitch', switch_name) # create switch event

# Read events (short circuit event and switch event)
events = shc_folder.GetContents()
shc_event = events[0]
switch_event = events[1]


# Set short circuit event parameters (time of the event and type of short circuit)
shc_event.time = 1 # time of the event
shc_event.i_shc = 0 # type of short circuit
shc_event.p_target = bus_dict['Bus 8']


# Set switch event parameters (time of the event and type of switch)
switch_event.time = 1.4 # time of the event
switch_event.i_switch = 0 # type of switch
switch_event.p_target = line_dict['Line 7-8']

# Reset calculation (to clear the previous calculation)
app.ResetCalculation()

# Read and modify file results (to add the variable to the results file)
elmres = app.GetFromStudyCase('All calculations.ElmRes')
elmres.Clear()
elmres.AddVariable(generator_dict['G2'], 's:xspeed')


# Initial conditions (to set the initial conditions)    
ini = app.GetFromStudyCase('ComInc')
ini.Execute()

# Dynamic simulation (to run the dynamic simulation)
sim = app.GetFromStudyCase('ComSim')
sim.tstop = 10
sim.Execute()

# call comres to export results (to export the results to a text file)
comres = app.GetFromStudyCase('ComRes')
comres.iopt_csel = 0
comres.iopt_tsel = 0
comres.iopt_locn = 2
comres.ciopt_head = 1
comres.pResult = elmres # from it's going to export from results files
comres.ipt_exp = 4 # 4 is for text file
comres.f_name = r'C:\Users\VM-PF\Documents\01 - Scripting Dynamic Simulation\results.txt'
comres.Execute()

# Reset calculation (to clear the previous calculation)
app.ResetCalculation()

# Delete events (to delete the events)
shc_event.Delete()
switch_event.Delete()

# Plot results (to plot the results) 
import numpy as np
import matplotlib.pyplot as plt
my_arr = np.genfromtxt(r'C:\Users\VM-PF\Documents\01 - Scripting Dynamic Simulation\ref_code\dynamic_simulation\results.txt', skip_header=2, filling_values=999999999)
plt.plot(my_arr[:, 0], my_arr[:, 1])
plt.xlabel('Time (s)')
plt.ylabel('Speed (p.u.)')
plt.title('Speed vs Time')
plt.grid(True)
plt.show()
