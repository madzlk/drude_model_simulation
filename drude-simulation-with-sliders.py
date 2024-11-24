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
def setElectricField(s):
    w2.text = '{:1.2f}'.format(s.value)
sl2 = slider(min=-1, max=1, value=0.5, length=220, bind=setElectricField, left=50)
w2 = wtext(text='{:1.2f}'.format(sl2.value))
scene.append_to_caption(' volt/meter\n')

scene.append_to_caption("\n")
scene.append_to_caption("Scattering time: ")
def setScatteringTime(s):
    w3.text = '{:1.2f}'.format(s.value)
sl3 = slider(min=0.1, max=2, value=0.1, length=220, bind=setScatteringTime, left=50)
w3 = wtext(text='{:1.2f}'.format(sl3.value))
scene.append_to_caption(' s\n')

scene.append_to_caption(
    "<p style=' font-size: 16px; color: gray;'>"
    "This simulation demonstrates the motion of an electron under the influence of an electric field\n"
    "with regard to drude model"
)

xvst = gcurve(color=color.green, label="Average X Position vs Time")
yvst = gcurve(color=color.red, label="Average Y Position vs Time")
zvst = gcurve(color=color.black)

# ──────────────────────────────────────────────────────────────────────────────
# PARSING COMMAND LINE ARGUMENTS
# ──────────────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Drude Model Simulation with adjustable number of electrons.")
parser.add_argument('--num-electrons', type=int, default=30,
                    help="Number of electrons to simulate (default: 30).")
parser.add_argument('--metal', action='store_true', default=False,
                    help="If specified, electrons are spawned inside a metal.")
parser.add_argument('--infinite-metal', action='store_true', default=False,
                    help="If specified, electrons are spawned inside a metal that behaves like an infinite pool (no boundaries).")
args = parser.parse_args()

num_electrons = args.num_electrons
is_metal = args.metal  # this will be True if '--metal' is passed, False otherwise
is_infinite_metal = args.infinite_metal  # this will be True if '--infinite-metal' is passed

if num_electrons <= 0:
    print("Invalid number of electrons. Using default value of 30.")
    num_electrons = 30

print(f"Simulating with {num_electrons} electrons.")
if is_metal:
    if is_infinite_metal:
        print("Electrons will be spawned inside an infinite metal (no boundaries).")
    else:
        print("Electrons will be spawned inside a finite metal.")
else:
    print("Electrons will be in an infinite pool.")

# ──────────────────────────────────────────────────────────────────────────────
# WIRE
# ──────────────────────────────────────────────────────────────────────────────

class metal:
    def __init__(self, position, length, width):
        self.size = vector(length, width, width)
        self.body = box(size=self.size, pos = position, opacity = 0.3)

        self.top = position.y + 0.5*self.body.size.y
        self.bottom = position.y - 0.5*self.body.size.y

        self.left = position.x - 0.5*self.body.size.x
        self.right = position.x + 0.5*self.body.size.x


# ──────────────────────────────────────────────────────────────────────────────
# ELECTRON BEHAVIOUR DRIVEN BY DRUDE MODEL
# ──────────────────────────────────────────────────────────────────────────────


class electron:
    def __init__(self, position):
        self.body = sphere(pos=position, radius=0.05, color=color.blue, make_trail=False if is_infinite_metal or is_metal else True, retain=100)
        self.speed = 1
        self.velocity = vector(0.1, 0,0)


def move_electrons(electrons):
    avg_position = vector(0,0,0)

    for electron in electrons:
        should_scatter = uniform(0,1) < TIME_STEP/scattering_time
        if should_scatter:
            angle = uniform(0,  2 * math.pi)
            electron.velocity = electron.speed * vector(cos(angle), sin(angle), 0)
        else:
            # here we apply electric field without calculating acceleration
            # real equation for acceleration would be
            # acceleration = ELECTRON_CHARGE * electric_field / ELECTRON_MASS
            electron.velocity += vector(electric_field, 0, 0) * TIME_STEP

        if is_metal or is_infinite_metal:
            electron_position = electron.body.pos
            if electron_position.x > metal_chunk.right and electron.velocity.x >0:
                if is_infinite_metal:
                    electron.body.pos.x = metal_chunk.left
                else:
                    electron.velocity.x *= -1
            if electron_position.x < metal_chunk.left  and electron.velocity.x <0:
                if is_infinite_metal:
                    electron.body.pos.x = metal_chunk.right
                else:
                    electron.velocity.x *= -1
            if electron_position.y > metal_chunk.top  and electron.velocity.y >0:
                electron.velocity.y *= -1

            if electron_position.y < metal_chunk.bottom  and electron.velocity.y <0:
                electron.velocity.y *= -1


        electron.body.pos += electron.velocity * TIME_STEP
        avg_position += electron.body.pos

    avg_position /= len(electrons)
    return avg_position

# ──────────────────────────────────────────────────────────────────────────────
# ELECTRONS INITIALIZATION
# ──────────────────────────────────────────────────────────────────────────────

if is_metal or is_infinite_metal:
    metal_chunk = metal(vector(0,0,0), 10, 1)
    electric_field_magnitude_arrow = arrow(pos=vec(0, 0, 0), axis=vec(1, 0, 0), color=color.red)

electrons = [electron(vector(0,0,0)) for _ in range(num_electrons)]


# ──────────────────────────────────────────────────────────────────────────────
# SIMULATION LOOP
# ──────────────────────────────────────────────────────────────────────────────

TIME_STEP = 0.01
t = 0

def wait_for_input():
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            global stop_simulation
            stop_simulation = True
            print("Received 'q', stopping simulation.")

stop_simulation = False
input_thread = threading.Thread(target=wait_for_input)
input_thread.daemon = True
input_thread.start()

while True:
    rate(500)

    scattering_time = sl3.value
    electric_field = sl2.value

    electric_field_magnitude_arrow.axis.x = electric_field
    avg_position = move_electrons(electrons)

    if stop_simulation:
        print("Simulation terminated.")
        break

    t += TIME_STEP


    xvst.plot(pos=(t, avg_position.x))
    yvst.plot(pos=(t, avg_position.y))

    # the Z value is used like a marker, it will always be a 0
    zvst.plot(pos=(t, avg_position.z))
