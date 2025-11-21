# Acceder a PowerFactory
import os
os.environ["PATH"] = r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2" + os.environ["PATH"]

import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9")

#importar powerfactory
import powerfactory as pf #comentarios
app=pf.GetApplication() #obtneer la app

#acceder al proyecto y activar
user = app.GetCurrentUser()
project = app.ActivateProject("Nine-bus System") #activar el proyecto que quiero
prj = app.GetActiveProject()

# app.Show() #(optativo)

# create bus dictionary
buses = app.GetCalcRelevantObjects('*.ElmTerm')
bus_dict = {}
for bus in buses:
    bus_dict[bus.loc_name] = bus

# create generator dictionary
generators = app.GetCalcRelevantObjects('*.ElmSym')
generator_dict = {}
for generator in generators:
    generator_dict[generator.loc_name] = generator

# create line dictionary
lines = app.GetCalcRelevantObjects('*.ElmLne')
line_dict = {}
for line in lines:
    line_dict[line.loc_name] = line

# events name variables
shc_name = 'short circuit event'
switch_name = 'switch event'    

# Create events
shc_folder = app.GetFromStudyCase('IntEvt')
shc_folder.CreateObject('EvtShc', shc_name) # create short circuit event
shc_folder.CreateObject('EvtSwitch', switch_name) # create switch event

# Read events
events = shc_folder.GetContents()
shc_event = events[0]
switch_event = events[1]


# Set short circuit event parameters
shc_event.time = 1 # time of the event
shc_event.i_shc = 0 # type of short circuit
shc_event.p_target = bus_dict['Bus 8']


# Set switch event parameters
switch_event.time = 1.4 # time of the event
switch_event.i_switch = 0 # type of switch
switch_event.p_target = line_dict['Line 7-8']

# Reset calculation
app.ResetCalculation()

# Read and modify file results
elmres = app.GetFromStudyCase('All calculations.ElmRes')
elmres.Clear()
elmres.AddVariable(generator_dict['G2'], 's:xspeed')


# Initial conditions
ini = app.GetFromStudyCase('ComInc')
ini.Execute()

# Dynamic simulation
sim = app.GetFromStudyCase('ComSim')
sim.tstop = 15
sim.Execute()

# call comres to export results
comres = app.GetFromStudyCase('ComRes')
comres.iopt_csel = 0
comres.iopt_tsel = 0
comres.iopt_locn = 2
comres.ciopt_head = 1
comres.pResult = elmres # from it's going to export from results files
comres.ipt_exp = 4 # 4 is for text file
comres.f_name = r'C:\Users\VM-PF\Documents\01 - Scripting Dynamic Simulation\results.txt'
comres.Execute()

# Reset calculation
app.ResetCalculation()

# Delete events
shc_event.Delete()
switch_event.Delete()

# Plot results
import numpy as np
import matplotlib.pyplot as plt
my_arr = np.genfromtxt(r'C:\Users\VM-PF\Documents\01 - Scripting Dynamic Simulation\results.txt', skip_header=2, filling_values=999999999)
plt.plot(my_arr[:, 0], my_arr[:, 1])
plt.xlabel('Time (s)')
plt.ylabel('Speed (p.u.)')
plt.title('Speed vs Time')
plt.grid(True)
plt.show()
