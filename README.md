Drude Model Simulation
================================

This project provides simulation of electron dynamics within an applied electric field, grounded in the theoretical framework of the Drude model.

## Features

* **Dynamic Simulation**: Real-time visualization of electron trajectories and statistical behavior under varying physical conditions.
* **Configurable Parameters**: Interactive sliders enable fine-tuned control over the electric field intensity and scattering timescale.
* **Comprehensive Graphical Output**: Generates plots illustrating the temporal evolution of average electron positions in both the x and y dimensions.
* **Command-Line Flexibility**: Supports argument-based customization, including the number of simulated electrons and the environmental constraints.

## Requirements

### Python Version
Python 3.x

### Dependencies

* `vpython`
* Standard libraries: `math`, `argparse`, `threading`

### Installation

Install the necessary Python dependencies with:

pip install vpython

## Usage

### Executing the Simulation

Run the script using the following command:

python drude_model_sim.py

### Command-Line Configuration

* `--num-electrons`: Defines the quantity of electrons to simulate (default: 30).

Example usage:

python drude_model_sim.py --num-electrons 50

### Interactive Controls

* **Electric Field Strength**: Adjustable in volts per meter via slider.
* **Scattering Time**: Modifiable timescale for electron scattering events, expressed in seconds.

The parameters can be dynamically altered through the user interface during runtime.

## Simulation Control

To terminate the simulation gracefully, input `q` into the terminal. Eventually just close the localhost site, the experience is hosted on.

## Outputs

Observe electrons responding to the combined influence of electric fields and scattering processes. Monitor plots of positional averages over time. Displays real-time updates regarding simulation parameters and settings.
