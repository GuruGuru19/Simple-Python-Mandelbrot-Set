import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

AVG_TIME_PER_STEP = 1.70924E-08

EXPLOR_MODE = False

PIXELS = 500  # img size
MAX_ITER = 1500
ZOOM = 5  # zooming multiplier


# starting position
start_X = -4.621603e-1
start_Y = -5.823998e-1
start_R = 2.633507e-9

# Create a figure and a subplot
fig, ax = plt.subplots()

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)


# returns current time in ms
def timeNow():
    # Get the current time in seconds
    seconds = datetime.now().timestamp()

    # Convert the time to milliseconds
    milliseconds = int(seconds * 1000)

    return milliseconds


def mandelbrotSet(complex_numbers, max_iter):
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
    # number of steps
    steps_count = PIXELS * PIXELS * MAX_ITER
    # prints estimated time in s, h and number of steps
    print(f"estimated time {steps_count * AVG_TIME_PER_STEP}s or {(steps_count * AVG_TIME_PER_STEP) / 3600}h (steps: {steps_count})")

    # saves time at start
    all_start_time = timeNow()

    y *= -1
    # makes the x and y values matrices
    x_values, y_values = np.mgrid[y - r:y + r:PIXELS * 1j, x - r:x + r:PIXELS * 1j]

    # make a matrix of complex numbers (every cell represent a pixel)
    complex_numbers = x_values * 1j + y_values

    # calculation
    output = mandelbrotSet(complex_numbers, MAX_ITER)

    # how long it all took
    dt = timeNow() - all_start_time
    # printing time in ms and s and h
    print(f"time took: {dt}ms or {dt / 1000}s or {dt / (1000 * 60 * 60)}h")
    # printing average time per iteration
    print(f"avg time per iter: {(dt / MAX_ITER) / 1000}s")
    # printing the starting values
    print(f"X: {x}, Y: {y}, R: {r}")

    return output


# Define a function to be called when the mouse is clicked
def onclick(event):

    # Get the x and y coordinates of the click
    xp = event.xdata - PIXELS/2
    yp = event.ydata - PIXELS/2
    yp *= -1

    # distance per pixel
    resolution = 2 * onclick.R/PIXELS

    # translate the pixels to real values
    xv = onclick.X + xp * resolution
    yv = onclick.Y + yp * resolution

    # Only handle right clicks
    if event.button == 3:
        print(f'Right clicked at x={xv}, y={yv}')
        onclick.R *= ZOOM  # zoom out

    # Only handle middle clicks
    if event.button == 2:
        print(f'Middle clicked  at x={xv}, y={yv}')

    # Only handle left clicks
    if event.button == 1:
        print(f'Left clicked  at x={xv}, y={yv}')
        onclick.R /= ZOOM  # zoom in

    #  zoom in or out
    if event.button == 1 or event.button == 3:
        #  makes new pixels
        newC = plot(xv, yv, onclick.R)

        # updates values
        onclick.X = xv
        onclick.Y = yv

        #  show on screen
        plt.cla()
        plt.imshow(newC)
        fig.canvas.draw()

onclick.R = start_R
onclick.X = start_X
onclick.Y = start_Y


def animate(i):
    if animate.zoom <= start_R:
        return
    animate.zoom /= ZOOM
    c = plot(start_X, start_Y, animate.zoom)
    plt.cla()
    plt.imshow(c)
    fig.canvas.draw()



animate.zoom = 4

c = plot(start_X, start_Y, 3)

# Plot something on the subplot
plt.imshow(c)

if EXPLOR_MODE:
    # Connect the onclick function to the mouse click event
    fig.canvas.mpl_connect('button_press_event', onclick)
else:
    ani = FuncAnimation(fig, animate, interval=1)
# Show the plot
plt.tight_layout()
plt.show()
