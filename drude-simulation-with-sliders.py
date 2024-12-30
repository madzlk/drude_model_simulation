import argparse
import sys
from vpython import *
from random import uniform
import math
import threading

# ──────────────────────────────────────────────────────────────────────────────
# UI AND SLIDERS
# ──────────────────────────────────────────────────────────────────────────────

scene.title = "<h1>Drude Model Simulation</h1>"
scene.append_to_caption("\n")
scene.append_to_caption("<b>Simulation Controls:</b>\n")
scene.append_to_caption("\n\n\n")

scene.append_to_caption("Electric field: ")
def update_electric_field(slider):
    electric_field_display.text = '{:1.2f}'.format(slider.value)

electric_field_slider = slider(min=-1, max=1, value=0.5, length=220, bind=update_electric_field, left=50)
electric_field_display = wtext(text='{:1.2f}'.format(electric_field_slider.value))
scene.append_to_caption(' volt/meter\n')

scene.append_to_caption("\n")
scene.append_to_caption("Scattering time: ")
def update_scattering_time(slider):
    scattering_time_display.text = '{:1.2f}'.format(slider.value)

scattering_time_slider = slider(min=0.1, max=2, value=0.1, length=220, bind=update_scattering_time, left=50)
scattering_time_display = wtext(text='{:1.2f}'.format(scattering_time_slider.value))
scene.append_to_caption(' s\n')

scene.append_to_caption(
    "<p style=' font-size: 16px; color: gray;'>"
    "This simulation demonstrates the motion of an electron under the influence of an electric field\n"
    "based on the Drude model."
)

# Graphs for visualization
x_position_plot = gcurve(color=color.green, label="Average X Position vs Time")
y_position_plot = gcurve(color=color.red, label="Average Y Position vs Time")
z_marker_plot = gcurve(color=color.black, label="Z Marker (Always 0)")

# ──────────────────────────────────────────────────────────────────────────────
# PARSING COMMAND LINE ARGUMENTS
# ──────────────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Drude Model Simulation with adjustable parameters.")
parser.add_argument('--num-electrons', type=int, default=30, help="Number of electrons to simulate (default: 30).")
parser.add_argument('--metal', action='store_true', help="Simulate electrons within a metal.")
parser.add_argument('--infinite-metal', action='store_true', help="Simulate within an infinite metal (no boundaries).")
args = parser.parse_args()

num_electrons = max(args.num_electrons, 1)  # Ensure at least 1 electron
simulate_in_metal = args.metal
simulate_in_infinite_metal = args.infinite_metal

print(f"Simulating with {num_electrons} electrons.")
if simulate_in_metal:
    metal_description = "infinite" if simulate_in_infinite_metal else "finite"
    print(f"Electrons will be simulated inside a {metal_description} metal.")
else:
    print("Electrons will be simulated in an open environment.")

# ──────────────────────────────────────────────────────────────────────────────
# METAL CLASS
# ──────────────────────────────────────────────────────────────────────────────

class Metal:
    """Represents a metal block with boundaries for electron interactions."""
    def __init__(self, position, length, width):
        self.size = vector(length, width, width)
        self.body = box(size=self.size, pos=position, opacity=0.3)

        self.top = position.y + 0.5 * self.body.size.y
        self.bottom = position.y - 0.5 * self.body.size.y
        self.left = position.x - 0.5 * self.body.size.x
        self.right = position.x + 0.5 * self.body.size.x

# ──────────────────────────────────────────────────────────────────────────────
# ELECTRON CLASS
# ──────────────────────────────────────────────────────────────────────────────

class Electron:
    """Represents an individual electron with position and velocity."""
    def __init__(self, position):
        self.body = sphere(
            pos=position, radius=0.05, color=color.blue,
            make_trail=not (simulate_in_metal or simulate_in_infinite_metal), retain=100
        )
        self.speed = 1
        self.velocity = vector(0.1, 0, 0)

# ──────────────────────────────────────────────────────────────────────────────
# ELECTRON MOTION LOGIC
# ──────────────────────────────────────────────────────────────────────────────

def move_electrons(electron_list):
    """Updates the position and velocity of all electrons based on the Drude model."""
    average_position = vector(0, 0, 0)

    for electron in electron_list:
        # Determine if the electron should scatter
        if uniform(0, 1) < TIME_STEP / scattering_time:
            angle = uniform(0, 2 * math.pi)
            electron.velocity = electron.speed * vector(cos(angle), sin(angle), 0)
        else:
            electron.velocity += vector(electric_field, 0, 0) * TIME_STEP

        # Handle boundary conditions if in metal
        if simulate_in_metal or simulate_in_infinite_metal:
            position = electron.body.pos
            if position.x > metal_chunk.right and electron.velocity.x > 0:
                if simulate_in_infinite_metal:
                    electron.body.pos.x = metal_chunk.left
                else:
                    electron.velocity.x *= -1
            if position.x < metal_chunk.left and electron.velocity.x < 0:
                if simulate_in_infinite_metal:
                    electron.body.pos.x = metal_chunk.right
                else:
                    electron.velocity.x *= -1
            if position.y > metal_chunk.top and electron.velocity.y > 0:
                electron.velocity.y *= -1
            if position.y < metal_chunk.bottom and electron.velocity.y < 0:
                electron.velocity.y *= -1

        electron.body.pos += electron.velocity * TIME_STEP
        average_position += electron.body.pos

    return average_position / len(electron_list)

# ──────────────────────────────────────────────────────────────────────────────
# SIMULATION INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────

if simulate_in_metal or simulate_in_infinite_metal:
    metal_chunk = Metal(vector(0, 0, 0), 10, 1)
    electric_field_arrow = arrow(pos=vector(0, 0, 0), axis=vector(1, 0, 0), color=color.red)

electron_list = [Electron(vector(0, 0, 0)) for _ in range(num_electrons)]

# ──────────────────────────────────────────────────────────────────────────────
# SIMULATION LOOP
# ──────────────────────────────────────────────────────────────────────────────

TIME_STEP = 0.01
t = 0

def monitor_user_input():
    """Monitors user input to allow for simulation termination."""
    while True:
        if input().strip().lower() == 'q':
            global stop_simulation
            stop_simulation = True
            print("Received 'q'. Stopping simulation.")
            break

stop_simulation = False
input_thread = threading.Thread(target=monitor_user_input, daemon=True)
input_thread.start()

while not stop_simulation:
    rate(500)

    scattering_time = scattering_time_slider.value
    electric_field = electric_field_slider.value

    if simulate_in_metal or simulate_in_infinite_metal:
        electric_field_arrow.axis.x = electric_field

    avg_position = move_electrons(electron_list)

    t += TIME_STEP
    x_position_plot.plot(pos=(t, avg_position.x))
    y_position_plot.plot(pos=(t, avg_position.y))
    z_marker_plot.plot(pos=(t, avg_position.z))

print("Simulation terminated.")
