"""
Dynamic Simulation Script: Load Increase on Load 39
Monitors frequency on Bus 16 and exports results to CSV

Project: 39 Bus New England System - 2
Study Case: Study Cases 1. Power Flow
"""

# ============================================================================
# STEP 1: Access PowerFactory
# ============================================================================
import os
os.environ["PATH"] = r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2" + os.environ["PATH"]

import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9")

# Import powerfactory
import powerfactory as pf
app = pf.GetApplication()  # Get the application

# ============================================================================
# STEP 2: Access and activate project
# ============================================================================
user = app.GetCurrentUser()
project = app.ActivateProject("39 Bus New England System - 2")  # Activate the desired project
prj = app.GetActiveProject()

print(f"Project activated: {prj.loc_name}")

# ============================================================================
# STEP 2.5: Activate study case (if needed)
# ============================================================================
# Try to activate the study case "Study Cases 1. Power Flow"
try:
    study_cases = prj.GetContents('*.IntCase')
    for sc in study_cases:
        if '1. Power Flow' in sc.loc_name or 'Power Flow' in sc.loc_name:
            sc.Activate()
            print(f"Study case activated: {sc.loc_name}")
            break
except:
    print("Note: Using default/active study case")

# ============================================================================
# STEP 3: Get all relevant objects (buses, loads)
# ============================================================================
# Create bus dictionary
buses = app.GetCalcRelevantObjects('*.ElmTerm')
bus_dict = {}
for bus in buses:
    bus_dict[bus.loc_name] = bus

# Create load dictionary
loads = app.GetCalcRelevantObjects('*.ElmLod')
load_dict = {}
for load in loads:
    load_dict[load.loc_name] = load

print(f"Found {len(bus_dict)} buses and {len(load_dict)} loads")

# ============================================================================
# STEP 4: Find Load 39 and Bus 16
# ============================================================================
# Find Load 39
if 'Load 39' not in load_dict:
    raise Exception("Could not find Load 39. Available loads: " + str(list(load_dict.keys())))
load_39 = load_dict['Load 39']
print(f"Found Load 39: {load_39.loc_name}")

# Find Bus 16
if 'Bus 16' not in bus_dict:
    raise Exception("Could not find Bus 16. Available buses: " + str(list(bus_dict.keys())))
bus_16 = bus_dict['Bus 16']
print(f"Found Bus 16: {bus_16.loc_name}")

# ============================================================================
# STEP 5: Get initial load value (to calculate increase)
# ============================================================================
initial_load_p = load_39.GetAttribute('plini')  # Initial active power in MW
print(f"Initial Load 39: P = {initial_load_p:.4f} MW")

# Define load increase (27.82% increase)
load_increase_factor = 1.2782  # 27.82% increase
new_load_p = initial_load_p * load_increase_factor
print(f"New Load 39 after increase: P = {new_load_p:.4f} MW")

# ============================================================================
# STEP 6: Create load increase event (EvtParam)
# ============================================================================
event_folder = app.GetFromStudyCase('IntEvt')
event_name = 'Load Increase Event 39'

# Create parameter event for load increase (active power)
event_folder.CreateObject('EvtLod', event_name + '_P')
load_event_p = event_folder.GetContents()[0]
load_event_p.time = 0.5  # Time of the event (0.5 second)
load_event_p.p_target = load_39  # Target is Load 39
load_event_p.iopt_type = 0 # type of load increase
load_event_p.dP = 27.82  # New active power value


# ============================================================================
# STEP 7: Reset calculation and set up results monitoring
# ============================================================================
app.ResetCalculation()

# Get results file and add frequency variable for Bus 16
elmres = app.GetFromStudyCase('All calculations.ElmRes')
elmres.Clear()
elmres.AddVariable(bus_16, 'm:fehz')  # Add frequency variable (m:fehz is frequency in Hz)

print("Added frequency monitoring for Bus 16")

# ============================================================================
# STEP 8: Set initial conditions
# ============================================================================
ini = app.GetFromStudyCase('ComInc')
ini.Execute()
print("Initial conditions calculated")

# ============================================================================
# STEP 9: Run dynamic simulation
# ============================================================================
sim = app.GetFromStudyCase('ComSim')
sim.tstop = 60.0  # Simulation time: 10 seconds
sim.Execute()
print(f"Dynamic simulation completed (t = 0 to {sim.tstop} s)")

# ============================================================================
# STEP 10: Export results directly to CSV
# ============================================================================

comres = app.GetFromStudyCase('ComRes')
comres.iopt_csel = 0
comres.iopt_locn = 1
comres.ciopt_head = 1
comres.pResult = elmres
comres.ipt_exp = 6  # 6 is for CSV file
comres.f_name = r'C:\Users\VM-PF\Documents\01 - Scripting Dynamic Simulation\src_code\frequency_bus16_results.csv'
comres.Execute()
print(f"Results exported to CSV: frequency_bus16_results.csv")

# ============================================================================
# STEP 13: Clean up
# ============================================================================
# Reset calculation
app.ResetCalculation()

# Delete the events
load_event_p.Delete()
print("Events deleted and calculation reset")

print("\n=== Simulation completed successfully ===")
print(f"CSV file saved at: frequency_bus16_results.csv")

