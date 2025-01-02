import argparse
from vpython import *
from random import uniform
import math
import threading
import random
import time

# ──────────────────────────────────────────────────────────────────────────────
# PHYSICAL CONSTANTS AND PARAMETERS
# ──────────────────────────────────────────────────────────────────────────────
ELECTRON_CHARGE = -1.60217662e-19   # C
ELECTRON_MASS   = 9.10938356e-31    # kg
BOLTZMANN_CONST = 1.380649e-23      # J/K
TEMPERATURE     = 300               # K
TIME_STEP       = 1e-14             # s


VISUAL_SCALE = 1e10
SCATTERING_TIME_SCALE = 1e-14
ELECTRIC_FIELD_SCALE = 1e6

# ──────────────────────────────────────────────────────────────────────────────
# UI AND SLIDERS
# ──────────────────────────────────────────────────────────────────────────────

scene.title = "<h1>Drude Model Simulation</h1>"

scene.append_to_caption("\n<b>Drift velocity: </b>")
drift_velocity_display = wtext(text='0')

def update_drift_velocity(new_velocity):
    drift_velocity_display.text = '{:.2e}'.format(new_velocity)

scene.append_to_caption("\n<hr />")

scene.append_to_caption("\n<b>Simulation Controls:</b>\n\n\n")

scene.append_to_caption("Electric field: ")
def update_electric_field(slider):
    electric_field_display.text = '{:1.4g}'.format(slider.value)

    # Recalculate theoretical drift velocity
    drift_velocity = calculate_drift_velocity(
        slider.value * ELECTRIC_FIELD_SCALE, scattering_time
    )
    update_drift_velocity(drift_velocity)

# Increase the range drastically for better visibility
electric_field_slider = slider(min=-1, max=1, value=0, length=500, bind=update_electric_field, left=50)
electric_field_display = wtext(text='{:1.4g}'.format(electric_field_slider.value))
scene.append_to_caption(' V/m * 10^6\n\n')

scene.append_to_caption("Scattering time: ")
def update_scattering_time(slider):
    scattering_time_display.text = '{:1.4g}'.format(slider.value)

    # Recalculate theoretical drift velocity
    drift_velocity = calculate_drift_velocity(
        electric_field, slider.value * SCATTERING_TIME_SCALE
    )
    update_drift_velocity(drift_velocity)


scattering_time_slider = slider(min=0.01 , max=21, value=2, length=220, bind=update_scattering_time, left=50)
scattering_time_display = wtext(text='{:1.4g}'.format(scattering_time_slider.value))
scene.append_to_caption(' s * 10^-14\n\n\n')

def reset_animation():
    global electrons, avg_position, stop_simulation, t
    stop_simulation = True
    time.sleep(0.2)
    t = 0
    x_position_plot.delete()
    y_position_plot.delete()
    z_marker_plot.delete()

    avg_position = vector(0, 0, 0)
    # scene.camera.pos = vector(0, 0, 0)
    # scene.camera.axis = vector(0, -1, -2)

    # Clear trails
    for electron in electrons:
        electron.body.clear_trail()  # Clears the existing trail
        electron.body.make_trail = False  # Disable trail temporarily

    # Reinitialize electrons
    electrons.clear()
    electrons = [Electron(vector(0, 0, 0)) for _ in range(num_electrons)]

    stop_simulation = False

reset_button = button(bind=reset_animation, text="Reset")


scene.append_to_caption(
    "<p style='font-size: 16px; color: gray;'>"
    "Demonstration of the Drude model with scaled positions for visibility."
    "</p>"
)

# Graphs for visualization
x_position_plot = gcurve(color=color.green, label="Average X Position vs Time")
y_position_plot = gcurve(color=color.red, label="Average Y Position vs Time")
z_marker_plot   = gcurve(color=color.black, label="Z Marker")


# ──────────────────────────────────────────────────────────────────────────────
# PARSING COMMAND LINE ARGUMENTS
# ──────────────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Drude Model Simulation with adjustable parameters.")
parser.add_argument('--num-electrons', type=int, default=30, help="Number of electrons to simulate.")
args = parser.parse_args()

num_electrons = max(args.num_electrons, 1)

# ──────────────────────────────────────────────────────────────────────────────
# HELPER: THERMAL VELOCITY
# ──────────────────────────────────────────────────────────────────────────────

def random_thermal_velocity(temp=TEMPERATURE):
    sigma = math.sqrt(BOLTZMANN_CONST * temp / ELECTRON_MASS)
    vx = random.gauss(0, sigma)
    vy = random.gauss(0, sigma)
    return vector(vx, vy, 0)

# ──────────────────────────────────────────────────────────────────────────────
# ELECTRON CLASS
# ──────────────────────────────────────────────────────────────────────────────

class Electron:
    """Represents an electron with position and velocity."""
    def __init__(self, position):
        # We'll store physical_position separately from the visual representation
        self.physical_position = position
        self.body = sphere(
            pos=position * VISUAL_SCALE,
            radius=0.05,
            color=color.blue,
            make_trail=True,
            retain=100
        )
        self.velocity = random_thermal_velocity()

# ──────────────────────────────────────────────────────────────────────────────
# ELECTRON MOTION
# ──────────────────────────────────────────────────────────────────────────────

def move_electrons(electrons):
    average_position = vector(0, 0, 0)

    for electron in electrons:
        if uniform(0, 1) < TIME_STEP / scattering_time:
            # Resample thermal velocity
            electron.velocity = random_thermal_velocity()
        else:
            # a = (q * E) / m
            acceleration = (ELECTRON_CHARGE * vector(electric_field, 0, 0)) / ELECTRON_MASS
            electron.velocity += acceleration * TIME_STEP

        electron.physical_position += electron.velocity * TIME_STEP

        # Update the visual position
        electron.body.pos = electron.physical_position * VISUAL_SCALE
        average_position += electron.physical_position

    return average_position / len(electrons)


def calculate_drift_velocity(electric_field, tau):
    return (ELECTRON_CHARGE * electric_field * tau) / ELECTRON_MASS

# ──────────────────────────────────────────────────────────────────────────────
# CREATE ELECTRONS
# ──────────────────────────────────────────────────────────────────────────────

electrons = [Electron(vector(0, 0, 0)) for _ in range(num_electrons)]

t = 0

# ──────────────────────────────────────────────────────────────────────────────
# THREAD TO MONITOR USER INPUT FOR EXIT
# ──────────────────────────────────────────────────────────────────────────────

def monitor_user_input():
    while True:
        if input().strip().lower() == 'q':
            global stop_simulation, exit_program
            stop_simulation = True
            exit_program = True
            print("Received 'q'. Stopping simulation.")
            break

stop_simulation = False
exit_program = False
input_thread = threading.Thread(target=monitor_user_input, daemon=True)
input_thread.start()

# ──────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────────────────────────────────────

while not exit_program:
    rate(5000)
    while not stop_simulation:
        scattering_time = scattering_time_slider.value * SCATTERING_TIME_SCALE
        electric_field  = electric_field_slider.value * ELECTRIC_FIELD_SCALE

        avg_position = move_electrons(electrons)
        t += TIME_STEP

        # Plot the average (unscaled) position
        x_position_plot.plot(pos=(t, avg_position.x))
        y_position_plot.plot(pos=(t, avg_position.y))
        z_marker_plot.plot(pos=(t, avg_position.z))
