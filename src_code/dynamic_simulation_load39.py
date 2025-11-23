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
loads = app.GetCalcRelevantObjects('*.ElmLoad')
load_dict = {}
for load in loads:
    load_dict[load.loc_name] = load

print(f"Found {len(bus_dict)} buses and {len(load_dict)} loads")

# ============================================================================
# STEP 4: Find Load 39 and Bus 16
# ============================================================================
# Find Load 39
if 'Load 39' in load_dict:
    load_39 = load_dict['Load 39']
    print(f"Found Load 39: {load_39.loc_name}")
else:
    # Try alternative naming (could be "Load39" or "39" or similar)
    load_39 = None
    for load_name, load_obj in load_dict.items():
        if '39' in load_name:
            load_39 = load_obj
            print(f"Found load with 39 in name: {load_name}")
            break
    if load_39 is None:
        raise Exception("Could not find Load 39. Available loads: " + str(list(load_dict.keys())))

# Find Bus 16
if 'Bus 16' in bus_dict:
    bus_16 = bus_dict['Bus 16']
    print(f"Found Bus 16: {bus_16.loc_name}")
else:
    # Try alternative naming
    bus_16 = None
    for bus_name, bus_obj in bus_dict.items():
        if '16' in bus_name or bus_name == '16':
            bus_16 = bus_obj
            print(f"Found bus with 16 in name: {bus_name}")
            break
    if bus_16 is None:
        raise Exception("Could not find Bus 16. Available buses: " + str(list(bus_dict.keys())))

# ============================================================================
# STEP 5: Get initial load value (to calculate increase)
# ============================================================================
initial_load_p = load_39.GetAttribute('m:P:bus1')  # Initial active power in MW
initial_load_q = load_39.GetAttribute('m:Q:bus1')  # Initial reactive power in Mvar
print(f"Initial Load 39: P = {initial_load_p:.4f} MW, Q = {initial_load_q:.4f} Mvar")

# Define load increase (e.g., 20% increase)
load_increase_factor = 1.2  # 20% increase
new_load_p = initial_load_p * load_increase_factor
new_load_q = initial_load_q * load_increase_factor
print(f"New Load 39 after increase: P = {new_load_p:.4f} MW, Q = {new_load_q:.4f} Mvar")

# ============================================================================
# STEP 6: Create load increase event (EvtParam)
# ============================================================================
event_folder = app.GetFromStudyCase('IntEvt')
event_name = 'Load Increase Event 39'

# Create parameter event for load increase (active power)
load_event_p = event_folder.CreateObject('EvtParam', event_name + '_P')
if load_event_p is None:
    raise Exception("Could not create load increase event for active power")

# Set event parameters for active power
load_event_p.time = 1.0  # Time of the event (1 second)
load_event_p.p_target = load_39  # Target is Load 39
load_event_p.var_name = 'plini'  # Parameter name for active power load
load_event_p.var_value = new_load_p  # New active power value

# Create parameter event for reactive power (optional, to maintain power factor)
load_event_q = None
try:
    load_event_q = event_folder.CreateObject('EvtParam', event_name + '_Q')
    if load_event_q is not None:
        load_event_q.time = 1.0  # Same time as active power
        load_event_q.p_target = load_39
        load_event_q.var_name = 'qlini'  # Parameter name for reactive power load
        load_event_q.var_value = new_load_q  # New reactive power value
        print(f"Created load increase events at t = {load_event_p.time} s (P and Q)")
    else:
        print(f"Created load increase event at t = {load_event_p.time} s (P only)")
except:
    print(f"Created load increase event at t = {load_event_p.time} s (P only, Q event failed)")

# ============================================================================
# STEP 7: Reset calculation and set up results monitoring
# ============================================================================
app.ResetCalculation()

# Get results file and add frequency variable for Bus 16
elmres = app.GetFromStudyCase('All calculations.ElmRes')
elmres.Clear()
elmres.AddVariable(bus_16, 'm:f')  # Add frequency variable (m:f is frequency in Hz)

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
sim.tstop = 10.0  # Simulation time: 10 seconds
sim.Execute()
print(f"Dynamic simulation completed (t = 0 to {sim.tstop} s)")

# ============================================================================
# STEP 10: Export results to text file first
# ============================================================================
workspace_path = r"C:\Users\VM-PF\Documents\01 - Scripting Dynamic Simulation"
results_txt = os.path.join(workspace_path, "temp_results.txt")

comres = app.GetFromStudyCase('ComRes')
comres.iopt_csel = 0
comres.iopt_tsel = 0
comres.iopt_locn = 2
comres.ciopt_head = 1
comres.pResult = elmres
comres.ipt_exp = 4  # 4 is for text file
comres.f_name = results_txt
comres.Execute()
print(f"Results exported to text file: {results_txt}")

# ============================================================================
# STEP 11: Read text file and convert to CSV
# ============================================================================
import numpy as np
import pandas as pd

# Read the text file (skip first 2 header lines)
data = np.genfromtxt(results_txt, skip_header=2, filling_values=0.0)

# Create DataFrame
df_results = pd.DataFrame(data, columns=['Time (s)', 'Frequency (Hz)'])

# ============================================================================
# STEP 12: Export to CSV
# ============================================================================
csv_output = os.path.join(workspace_path, "src_code", "frequency_bus16_results.csv")
df_results.to_csv(csv_output, index=False)
print(f"Results exported to CSV: {csv_output}")
print(f"\nResults summary:")
print(f"  - Number of data points: {len(df_results)}")
print(f"  - Time range: {df_results['Time (s)'].min():.3f} to {df_results['Time (s)'].max():.3f} s")
print(f"  - Frequency range: {df_results['Frequency (Hz)'].min():.4f} to {df_results['Frequency (Hz)'].max():.4f} Hz")

# ============================================================================
# STEP 13: Clean up
# ============================================================================
# Reset calculation
app.ResetCalculation()

# Delete the events
load_event_p.Delete()
if load_event_q is not None:
    load_event_q.Delete()
print("Events deleted and calculation reset")

# Optionally delete temporary text file
if os.path.exists(results_txt):
    os.remove(results_txt)
    print("Temporary text file removed")

print("\n=== Simulation completed successfully ===")
print(f"CSV file saved at: {csv_output}")

