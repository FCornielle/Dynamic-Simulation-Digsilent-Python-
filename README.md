# Power System Stability Simulation with DIgSILENT PowerFactory + Python

A structured collection of Python scripts and Jupyter notebooks that automate **power system stability studies** in DIgSILENT PowerFactory, using the IEEE 39-bus New England system as the test case. Each study compares a **Base Case** against a **New Generation Case** to quantify the impact of adding new generation to the grid.

## Studies included

| # | Study | What it answers |
|---|---|---|
| 1.1 | Dispatch & load flow | How do power flows and bus voltages change with the new generation? |
| 1.2 | Voltage profile | How much do voltage levels deviate across the system? |
| 1.3 | N-1 contingency | Is the system secure under single contingencies? |
| 1.4 | Short circuit | How are fault levels affected? |
| 2.1 | Eigenvalue analysis | What happens to oscillatory modes and damping ratios? |
| 2.2 | Small-signal perturbation | How does the system respond to small disturbances? |
| 3 | Transient stability | Does the system survive a three-phase fault and its clearing? |
| 4 | Voltage stability | How does voltage recover after a single-phase fault with auto-reclosing? |
| 5 | Frequency stability | RoCoF, frequency nadir and generator speed after generation loss |

Every script exports its results to CSV and then builds both static plots (matplotlib/seaborn, PNG) and interactive plots (Bokeh, HTML), including side-by-side Base vs. New Generation comparisons.

## Repository layout

```
src_code/     Notebooks and scripts, one folder per study (see src_code/README.md)
ref_code/     Reference PowerFactory automation scripts (load flow, dynamic simulation)
ref_doc/      Background papers on power system stability with high renewable penetration
```

## Requirements

- DIgSILENT PowerFactory 2021 SP2 with the Python API enabled
- Python 3.9
- `matplotlib`, `pandas`, `numpy`, `openpyxl`, `seaborn`, `bokeh`

```bash
pip install matplotlib pandas numpy openpyxl seaborn bokeh
```

## Usage

Open PowerFactory with the project *39 Bus New England System - 2* loaded, then run any study directly:

```bash
python src_code/01_steady_state_simulations/1.1_dispatch_load_flow_analysis/dispatch_load_flow_analysis.py
```

Outputs (CSV, PNG, HTML) are written next to the script that produced them. Sections marked `NOTE:` are the ones to adjust for a different network.

See [`src_code/README.md`](src_code/README.md) for the detailed description of each study.
