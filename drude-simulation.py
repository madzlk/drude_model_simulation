import pygame
import random
import math

#slider do zmiany stałych w czasie rzeczywistym, maibi python_widget
#https://pygamewidgets.readthedocs.io/en/stable/widgets/slider/#slider

# SYMULACJA DLA JEDNEGO ELEKTRONU

#    https://physics.iisc.ac.in/~aveek_bid/wp-content/uploads/2019/07/Lecture-1-Drude-model.pdf
#    Basic assumption of Drude model:
#
# 1. Between collisions electrons move in straight line (in the absence of a any
#    electromagnetic field) - effect of electron-electron interaction is ignored (independent
#    electron approximation – reasonably valid) – effect of electron-ion in ignored
#    (independent-electron approximation; completely invalid).
#
# 2. Mean free time between collisions is TAU (probability of collision per unit time is 1/tau;
#    probability of having a collision in infinitesimal time interval dt is dt/tau is
#    independent of electron’s position or velocity (a good assumption).
#
# 3. Electrons achieve thermal equilibrium by collisions with lattice – they emerge after
#    collision at a random direction with speed appropriate to the temperature of the region
#    where collision happened – the hotter the region; the higher the speed of the emerging
#    electrons.

# stałe
WIDTH, HEIGHT = 800, 600
ELECTRON_MASS = 9.11e-31    # kg
ELECTRON_CHARGE = -1.6e-19  # C
MEAN_FREE_TIME = 1e-15      # sekundy, zabrane z tego pliku https://physics.iisc.ac.in/~aveek_bid/wp-content/uploads/2019/07/Lecture-1-Drude-model.pdf
TIME_STEP = 1e-13           # sekundy
ELECTRIC_FIELD = 10e5       # volt/metr
SCALE = 1e9                 # aby zmiany były widoczne w symulacji sklaujemy je, bo faktycznie są tini tajni
BOLTZAMAN = 1.38e-23        # stała bolec-mana
TEMPERATURE = 300           # w kelwinach


# nie mogłam znaleźć zakresu w jakim trzeba wylosować randomową prędkość, to mi powiedział CHATGPT:
# In the Drude model, when an electron undergoes a collision with the lattice, it loses its previous
# velocity memory and is assigned a new velocity that is appropriate for the temperature of the material.
# The thermal velocity is given by the equation:

# pierwiastek(3*stała boltzmana*temperatura w kelwinach/masa elektronu)

# This is typically the characteristic velocity that you would use for assigning new random velocities after a collision.

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

electron = {
    "position": [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)],
    "velocity": [0, 0], # pierwsza składowa pozioma, druga pionowa
}

thermal_velocity = math.sqrt(3*BOLTZAMAN*TEMPERATURE/ELECTRON_MASS)

running = True
while running:
    screen.fill((0, 0, 0))  # co klatka czyścimy ekran, bo inaczej zosałby obraz elektrony z poprzednije iteracji

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # an electron will have a velocity v = v0 - eEt/m
    electron["velocity"][0] += ELECTRON_CHARGE * ELECTRIC_FIELD * TIME_STEP / ELECTRON_MASS # dodajemy, a nie odejmujemy bo nas nie obchodzi kierunek
    electron["velocity"][1] += 0 # zakładamy, że siła elktryczna działa w poziomie, więc w pionie nic się nie zmienia

    electron["position"][0] += electron["velocity"][0] * TIME_STEP * SCALE
    electron["position"][1] += electron["velocity"][1] * TIME_STEP * SCALE

    # probability of having a collision in infinitesimal time interval dt is dt/tau
    if random.random() < TIME_STEP / MEAN_FREE_TIME:
        electron["velocity"] = [random.uniform(-thermal_velocity, thermal_velocity), random.uniform(-thermal_velocity, thermal_velocity)]

    # żeby eleektron nie uciekł z erkanu
    electron["position"][0] %= WIDTH
    electron["position"][1] %= HEIGHT

    pygame.draw.circle(screen, (0, 255, 255), (int(electron["position"][0]), int(electron["position"][1])), 5)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
