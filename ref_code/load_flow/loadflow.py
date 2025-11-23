# Access PowerFactory
import os
os.environ["PATH"] = r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2" + os.environ["PATH"]

import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9")

# Import powerfactory
import powerfactory as pf
app=pf.GetApplication() # Get the application

# Access and activate project
user = app.GetCurrentUser()
project = app.ActivateProject("Nine-bus System") # Activate the desired project
prj = app.GetActiveProject()

# app.Show() # (optional)



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

# Get generators (synchronous generators)
generators = app.GetCalcRelevantObjects('*.ElmSym')

# Get lines
lines = app.GetCalcRelevantObjects('*.ElmLne')

# Run loadflow
ldf = app.GetFromStudyCase('ComLdf')
ldf.Execute()

# Import libraries for visualization
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configure seaborn style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Collect bus data (voltages and angles)
bus_data = []
for bus in buses:
    voltage = bus.GetAttribute('m:u')  # Voltage in p.u.
    angle = bus.GetAttribute('m:phiu')  # Voltage angle in degrees
    active_power = bus.GetAttribute('m:Pflow')  # Active power flow in MW
    reactive_power = bus.GetAttribute('m:Qflow')  # Reactive power flow in Mvar
    bus_data.append({
        'Bus': bus.loc_name,
        'Voltage (p.u.)': voltage,
        'Angle (deg)': angle,
        'Active Power Flow (MW)': active_power,
        'Reactive Power Flow (Mvar)': reactive_power
    })

# Collect load data
load_data = []
for load in loads:
    active_power = load.GetAttribute('m:P:bus1')  # Active power in MW
    reactive_power = load.GetAttribute('m:Q:bus1')  # Reactive power in Mvar
    power_factor = load.GetAttribute('m:cosphi')  # Power factor
    load_data.append({
        'Load': load.loc_name,
        'Active Power (MW)': active_power,
        'Reactive Power (Mvar)': reactive_power,
        'Power Factor': power_factor
    })

# Collect generator data
gen_data = []
for gen in generators:
    try:
        active_power = gen.GetAttribute('m:P:bus1')  # Active power in MW
        reactive_power = gen.GetAttribute('m:Q:bus1')  # Reactive power in Mvar
        # Only add if values are not None
        if active_power is not None and reactive_power is not None:
            gen_data.append({
                'Generator': gen.loc_name,
                'Active Power (MW)': active_power,
                'Reactive Power (Mvar)': reactive_power
            })
    except Exception as e:
        print(f"Error getting generator data for {gen.loc_name}: {e}")

# Collect line data
line_data = []
for line in lines:
    p_from = line.GetAttribute('m:P:bus1')  # Active power from bus in MW
    q_from = line.GetAttribute('m:Q:bus1')  # Reactive power from bus in Mvar
    line_data.append({
        'Line': line.loc_name,
        'Active Power (MW)': p_from,
        'Reactive Power (Mvar)': q_from
    })

# Create DataFrames
df_buses = pd.DataFrame(bus_data)
df_loads = pd.DataFrame(load_data)
df_generators = pd.DataFrame(gen_data)
df_lines = pd.DataFrame(line_data)

# Ensure DataFrames have correct columns even if empty
if df_loads.empty:
    df_loads = pd.DataFrame(columns=['Load', 'Active Power (MW)', 'Reactive Power (Mvar)', 'Power Factor'])
if df_generators.empty:
    df_generators = pd.DataFrame(columns=['Generator', 'Active Power (MW)', 'Reactive Power (Mvar)'])
if df_lines.empty:
    df_lines = pd.DataFrame(columns=['Line', 'Active Power (MW)', 'Reactive Power (Mvar)'])

# Print data to console
print("\n=== Bus Results ===")
for bus in buses:
    voltage = bus.GetAttribute('m:u')
    print(f"Voltage of bus {bus.loc_name}: {voltage:.4f} p.u.")

print("\n=== Load Results ===")
if loads:
    for load in loads:
        power = load.GetAttribute('m:P:bus1')
        print(f"Power of load {load.loc_name}: {power:.4f} MW")
else:
    print("No loads found")

print("\n=== Generator Results ===")
if generators:
    for gen in generators:
        try:
            active_power = gen.GetAttribute('m:P:bus1')
            reactive_power = gen.GetAttribute('m:Q:bus1')
            print(f"Generator {gen.loc_name}: P={active_power:.4f} MW, Q={reactive_power:.4f} MVar")
        except Exception as e:
            print(f"Error getting generator data for {gen.loc_name}: {e}")
else:
    print("No generators found")

# Create visualizations
fig = plt.figure(figsize=(14, 8))

# Graph 1: Bus voltages (substations)
ax1 = plt.subplot(2, 3, 1)
sns.barplot(data=df_buses, x='Bus', y='Voltage (p.u.)', ax=ax1)
ax1.axhline(y=1.0, color='r', linestyle='--', linewidth=2, label='Nominal voltage (1.0 p.u.)')
ax1.set_title('Bus Voltages (Substations)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Bus', fontsize=9)
ax1.set_ylabel('Voltage (p.u.)', fontsize=9)
ax1.tick_params(axis='x', rotation=45, labelsize=8)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Graph 2: Bus voltage angles
ax2 = plt.subplot(2, 3, 2)
sns.barplot(data=df_buses, x='Bus', y='Angle (deg)', hue='Bus', ax=ax2, palette='coolwarm', legend=False)
ax2.set_title('Bus Voltage Angles', fontsize=11, fontweight='bold')
ax2.set_xlabel('Bus', fontsize=9)
ax2.set_ylabel('Angle (degrees)', fontsize=9)
ax2.tick_params(axis='x', rotation=45, labelsize=8)
ax2.grid(True, alpha=0.3)

# Graph 3: Bus active power flow
ax3 = plt.subplot(2, 3, 3)
sns.barplot(data=df_buses, x='Bus', y='Active Power Flow (MW)', hue='Bus', ax=ax3, palette='viridis', legend=False)
ax3.set_title('Bus Active Power Flow', fontsize=11, fontweight='bold')
ax3.set_xlabel('Bus', fontsize=9)
ax3.set_ylabel('Active Power Flow (MW)', fontsize=9)
ax3.tick_params(axis='x', rotation=45, labelsize=8)
ax3.grid(True, alpha=0.3)

# Graph 4: Bus reactive power flow
ax4 = plt.subplot(2, 3, 4)
sns.barplot(data=df_buses, x='Bus', y='Reactive Power Flow (Mvar)', hue='Bus', ax=ax4, palette='plasma', legend=False)
ax4.set_title('Bus Reactive Power Flow', fontsize=11, fontweight='bold')
ax4.set_xlabel('Bus', fontsize=9)
ax4.set_ylabel('Reactive Power Flow (Mvar)', fontsize=9)
ax4.tick_params(axis='x', rotation=45, labelsize=8)
ax4.grid(True, alpha=0.3)

# Graph 5: Generator power
ax5 = plt.subplot(2, 3, 5)
if not df_generators.empty:
    x_pos = np.arange(len(df_generators))
    width = 0.35
    ax5.bar(x_pos - width/2, df_generators['Active Power (MW)'], width, label='Active (MW)', alpha=0.8, color='green')
    ax5.bar(x_pos + width/2, df_generators['Reactive Power (Mvar)'], width, label='Reactive (Mvar)', alpha=0.8, color='orange')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(df_generators['Generator'], rotation=45, ha='right', fontsize=8)
    ax5.legend(fontsize=8)
else:
    ax5.text(0.5, 0.5, 'No generators found', ha='center', va='center', transform=ax5.transAxes)
ax5.set_title('Generator Power', fontsize=11, fontweight='bold')
ax5.set_xlabel('Generator', fontsize=9)
ax5.set_ylabel('Power (MW/Mvar)', fontsize=9)
ax5.grid(True, alpha=0.3, axis='y')

# Graph 6: Load power (if available) or Line power
ax6 = plt.subplot(2, 3, 6)
if not df_loads.empty:
    x_pos = np.arange(len(df_loads))
    width = 0.35
    ax6.bar(x_pos - width/2, df_loads['Active Power (MW)'], width, label='Active (MW)', alpha=0.8, color='blue')
    ax6.bar(x_pos + width/2, df_loads['Reactive Power (Mvar)'], width, label='Reactive (Mvar)', alpha=0.8, color='red')
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(df_loads['Load'], rotation=45, ha='right', fontsize=8)
    ax6.legend(fontsize=8)
    ax6.set_title('Load Power', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Power (MW/Mvar)', fontsize=9)
elif not df_lines.empty:
    # Show top 10 lines by power if there are many
    df_lines_sorted = df_lines.nlargest(min(10, len(df_lines)), 'Active Power (MW)')
    x_pos = np.arange(len(df_lines_sorted))
    width = 0.35
    ax6.bar(x_pos - width/2, df_lines_sorted['Active Power (MW)'], width, label='Active (MW)', alpha=0.8, color='purple')
    ax6.bar(x_pos + width/2, df_lines_sorted['Reactive Power (Mvar)'], width, label='Reactive (Mvar)', alpha=0.8, color='cyan')
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(df_lines_sorted['Line'], rotation=45, ha='right', fontsize=7)
    ax6.legend(fontsize=8)
    ax6.set_title('Line Power Flow (Top 10)', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Power (MW/Mvar)', fontsize=9)
else:
    ax6.text(0.5, 0.5, 'No load/line data found', ha='center', va='center', transform=ax6.transAxes)
ax6.set_xlabel('Element', fontsize=9)
ax6.tick_params(axis='x', rotation=45)
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('loadflow_results.png', dpi=300, bbox_inches='tight')
print("\n=== Graphs saved to 'loadflow_results.png' ===")
plt.show()
