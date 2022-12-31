import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

AVG_TIME_PER_STEP = 1.70924E-08;

EXPLOR_MODE = False

PIXELS = 500
MAX_ITER = 1000
ZOOM = 5

start_X = 0
start_Y = 0
start_R = 2

# Create a figure and a subplot
fig, ax = plt.subplots()

frame = np.zeros((PIXELS, PIXELS))


ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)




def timeNow():
    # Get the current time in seconds
    seconds = datetime.now().timestamp()

    # Convert the time to milliseconds
    milliseconds = int(seconds * 1000)

    return milliseconds


def mendelbrotSet(complex_numbers, max_iter):
    frame = np.zeros((PIXELS, PIXELS), dtype='int32')
    c = complex_numbers
    z = c
    n = 0
    lastp = -1
    start_time = timeNow()
    while n < max_iter:

        z = z ** 2 + c
        frame[np.abs(z) <= 2] += 1
        n += 1
        p = int(100 * (n / max_iter))
        if lastp != p:
            lastp = p;
            print(f"iter number: {n} out of {max_iter}. (%{p}) ({timeNow() - start_time}ms)")
            start_time = timeNow()
    return frame


def plot(x, y, r):
    steps_count = PIXELS * PIXELS * MAX_ITER
    print(f"estimated time {steps_count * AVG_TIME_PER_STEP}s or {(steps_count * AVG_TIME_PER_STEP) / 3600}h (steps: {steps_count})")
    all_start_time = timeNow()

    y *= -1
    x_values, y_values = np.mgrid[y - r:y + r:PIXELS * 1j, x - r:x + r:PIXELS * 1j]
    complex_numbers = x_values * 1j + y_values

    output = mendelbrotSet(complex_numbers, MAX_ITER)

    dt = timeNow() - all_start_time;
    print(f"time took: {dt}ms or {dt / 1000}s or {dt / (1000 * 60 * 60)}h")
    print(f"avg time per iter: {(dt / MAX_ITER) / 1000}s")

    return output


# Define a function to be called when the mouse is clicked
def onclick(event):

    # Get the x and y coordinates of the click
    xp = event.xdata - PIXELS/2
    yp = event.ydata - PIXELS/2
    yp *= -1

    # distance per pixel
    resolution = 2 * onclick.R/PIXELS

    xv = onclick.X + xp * resolution
    yv = onclick.Y + yp * resolution

    # Only handle right clicks
    if event.button == 3:
        print(f'Right clicked at x={xv}, y={yv}')
        onclick.R *= ZOOM

    if event.button == 2:
        print(f'Middle clicked  at x={xv}, y={yv}')

    # Only handle left clicks
    if event.button == 1:
        print(f'Left clicked  at x={xv}, y={yv}')
        onclick.R /= ZOOM

    if event.button == 1 or event.button == 3:
        newC = plot(xv, yv, onclick.R)
        onclick.X = xv
        onclick.Y = yv
        print(f"X: {xv}, Y: {yv}, R: {onclick.R}")

        plt.cla()
        plt.imshow(newC)
        fig.canvas.draw()

def animate(i):
    pass


onclick.R = start_R
onclick.X = start_X
onclick.Y = start_Y


c = plot(start_X, start_Y, start_R)

# Plot something on the subplot
plt.imshow(c)

if EXPLOR_MODE:
    # Connect the onclick function to the mouse click event
    fig.canvas.mpl_connect('button_press_event', onclick)

# Show the plot
plt.tight_layout()
plt.show()
