# Power System Simulation Scripts

This directory contains organized Python scripts for comprehensive power system stability analysis using DIgSILENT PowerFactory.

## Project Structure

```
src_code/
├── 01_steady_state_simulations/
│   ├── 1.1_dispatch_load_flow_analysis/
│   │   └── dispatch_load_flow_analysis.py
│   ├── 1.2_voltage_profile_analysis/
│   │   └── voltage_profile_analysis.py
│   ├── 1.3_n1_contingency_analysis/
│   │   └── n1_contingency_analysis.py
│   └── 1.4_short_circuit_analysis/
│       └── short_circuit_analysis.py
├── 02_small_signal_stability/
│   ├── 2.1_eigenvalue_based/
│   │   └── eigenvalue_analysis.py
│   └── 2.2_perturbation_response/
│       └── small_signal_perturbation.py
├── 03_transient_stability/
│   └── transient_stability_analysis.py
├── 04_voltage_stability/
│   └── voltage_stability_analysis.py
├── 05_frequency_stability/
│   └── frequency_stability_analysis.py
└── dynamic_simulation_load39.py (existing script)
```

## Analysis Types

### 1. Steady-State Simulations

#### 1.1 Dispatch and Load Flow Analysis
- **Script**: `dispatch_load_flow_analysis.py`
- **Objective**: Evaluate the impact of new generation on system operation and power flows
- **Outputs**: 
  - Bus voltage magnitudes and angles
  - Active and reactive power flows
  - Generator power outputs
  - CSV files with results

#### 1.2 Voltage Profile Analysis
- **Script**: `voltage_profile_analysis.py`
- **Objective**: Assess voltage level variations caused by new generation integration
- **Outputs**:
  - Radar plot of bus voltages
  - Voltage deviation comparison between cases
  - CSV files with voltage profiles

#### 1.3 N-1 Contingency Analysis
- **Script**: `n1_contingency_analysis.py`
- **Objective**: Analyze system security under single contingencies
- **Outputs**:
  - Contingency result matrices
  - Violation and severity analysis
  - Comparative analysis between scenarios

#### 1.4 Short-Circuit Analysis
- **Script**: `short_circuit_analysis.py`
- **Objective**: Evaluate the influence of new generation on fault levels
- **Outputs**:
  - Short-circuit current and power values
  - Comparative plots and tables
  - CSV files with fault level data

### 2. Small-Signal Stability Analysis

#### 2.1 Eigenvalue-Based Small-Signal Stability
- **Script**: `eigenvalue_analysis.py`
- **Objective**: Determine the impact of new generation on system oscillatory modes
- **Outputs**:
  - Eigenvalue plots
  - Damping ratio comparison
  - CSV files with eigenvalue data

#### 2.2 Small-Signal Perturbation Response
- **Script**: `small_signal_perturbation.py`
- **Objective**: Assess dynamic response to small disturbances
- **Outputs**:
  - Generator speed vs. time plots
  - Scenario comparison
  - CSV files with response data

### 3. Transient Stability Analysis
- **Script**: `transient_stability_analysis.py`
- **Objective**: Evaluate system stability under large disturbances
- **Methodology**: Apply a three-phase fault at a selected substation and clear after defined clearing time
- **Outputs**:
  - Bus voltage vs. time
  - Generator speed vs. time
  - Generator rotor angle vs. time
  - Stability comparison between cases

### 4. Voltage Stability Analysis
- **Script**: `voltage_stability_analysis.py`
- **Objective**: Analyze voltage recovery and reactive power support during faults
- **Methodology**: Apply a single-phase fault followed by successful auto-reclosing
- **Outputs**:
  - Reactive power vs. time
  - Voltage recovery curves
  - Comparative analysis

### 5. Frequency Stability Analysis
- **Script**: `frequency_stability_analysis.py`
- **Objective**: Assess frequency behavior following generation loss
- **Key Metrics**:
  - System frequency
  - Rate of Change of Frequency (RoCoF)
  - Frequency nadir
  - Generator speed response
- **Outputs**:
  - Frequency and RoCoF plots
  - Generator speed vs. time
  - Comparative performance indicators

### Visualization Features

All scripts now include comprehensive visualization capabilities:
- **Static Plots**: High-quality PNG plots using matplotlib and seaborn
- **Interactive Plots**: Interactive HTML plots using Bokeh
- **Automatic CSV Loading**: Scripts automatically load exported CSV data for visualization
- **Comparison Plots**: Side-by-side comparison of Base Case vs New Generation Case
- **Multiple Plot Types**: Bar charts, line plots, scatter plots, histograms, radar plots, etc.

## Common Configuration

All scripts use the following common settings:
- **Project**: "39 Bus New England System - 2"
- **Study Case**: "Study Cases 1. Power Flow"
- **PowerFactory Version**: 2021 SP2
- **Python Version**: 3.9

## Prerequisites

1. **DIgSILENT PowerFactory 2021 SP2** installed
2. **Python 3.9** with PowerFactory Python API
3. **Optional packages** (for plotting and data processing):
   - `matplotlib` - For creating plots
   - `pandas` - For data manipulation
   - `numpy` - For numerical calculations
   - `openpyxl` - For Excel file creation

Install optional packages:
```bash
pip install matplotlib pandas numpy openpyxl
```

## Usage

1. **Run individual analysis scripts**:
   ```bash
   python src_code/01_steady_state_simulations/1.1_dispatch_load_flow_analysis/dispatch_load_flow_analysis.py
   ```

2. **Each script automatically**:
   - Exports results to CSV files
   - Loads the CSV data
   - Creates static plots (PNG format)
   - Creates interactive plots (HTML format using Bokeh)

3. **Run all analyses** (execute each script in sequence)

## Output Structure

Each analysis script creates in its respective folder:
- **CSV files**: Numerical results for Base Case and New Generation Case
- **Static plots (PNG)**: High-resolution plots for presentations and reports
- **Interactive plots (HTML)**: Interactive Bokeh plots for detailed exploration
- **Comparison files**: Side-by-side comparison data and visualizations

All outputs are saved in the same directory as the script for easy access.

## Notes

- All scripts follow the same structure as `dynamic_simulation_load39.py`
- Scripts are designed to work with both Base Case and New Generation Case scenarios
- Modify sections marked with "NOTE:" to customize for your specific system configuration
- Ensure PowerFactory is running and the project is accessible before executing scripts

## Course Development

This structure is designed for:
- GitHub repository organization
- Udemy course development
- Step-by-step learning progression
- Easy navigation and understanding

Each script includes:
- Clear objective statements
- Step-by-step comments
- Error handling
- Result export capabilities
- Comparison between scenarios

