""" A mouse wiggler for the NeoKey Trinkey.

This has three modes, based on stoplight colours.

1. Red is off, where no mouse wiggling happens.
2. Yellow wiggles the mouse every 1 to 4 minutes at random.
3. Green wiggles the mouse constantly.

You can see the current mode by touching the capacitive 
button, and cycle modes with the big button.
"""

import time
import random
import board
import neopixel
import usb_hid
import touchio

from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Pull

# The three stoplight colours. We use these both for setting the
# light colour, and for tracking the mode we're currently in with
# the `current_mode` global.
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# How many times does the mouse move around when it wiggles.
MOVES_PER_WIGGLE = 5

# How far is the mouse allowed to move when it wiggles.
MAX_WIGGLE_DISTANCE = 15

# Time between wiggles when in yellow mode, in seconds.
MIN_DELAY = 1 * 60
MAX_DELAY = 4 * 60

# The neopixel rgb led.
PIXEL = neopixel.NeoPixel(board.NEOPIXEL, 1)

# The object which lets us behave like a mouse.
MOUSE = Mouse(usb_hid.devices)


def do_nothing():
    """ Does nothing. Used as the default action for buttons. """

    pass


class Button:
    """ A class for treating some input as a button with 4 distinct
    state callbacks which are called based on button state changes
    every time `tick` is called.

    1. `on_press` when the button goes from active to inactive.
    2. `on_held` when the button is stayed active.
    3. `on_release` when the button goes from active to inactive.
    4. `on_rest` when the button stayed inactive.

    Users will want to assign these callbacks useful values.

    Make sure `tick` isn't called too often, as there's no built-in
    switch [debounce][] here.

    [debounce]: https://learn.adafruit.com/make-it-switch/debouncing
    """

    def __init__(self, input, name):
        """ Create a new `Button`.

        - `input` should be an object with a `value` which indicates 
          if the input is actuated.
        - `name` is used to identify which button is in what state in
          the program's output.
        """

        self.input = input
        self.name = name
        self.previous = None

        self.on_press = do_nothing
        self.on_held = do_nothing
        self.on_release = do_nothing
        self.at_rest = do_nothing

    def is_active(self):
        """ A predicate for if the `input` we're modelling as a button
        currently actuated?
        """

        return self.input.value

    def tick(self):
        """ This method should be called in the main loop. It looks 
        at the `previous` state and if the button `is_active`, and 
        then calls the correct callbacks.

        This will return the result of any callback called.
        """

        current = self.is_active()

        if current and not self.previous:
            print("{} was pressed".format(self.name))
            result = self.on_press()
        elif current and self.previous:
            print("{} is held".format(self.name))
            result = self.on_held()
        elif not current and self.previous:
            print("{} was released".format(self.name))
            result = self.on_release()
        else:
            result = self.at_rest()

        # so previous is correctly tracked for next tick
        self.previous = current
        return result


def next_colour(c):
    """ Takes a colour and returns the next stoplight colour, in the
    following order: `RED`, `YELLOW`, `GREEN`.

    Will return `RED` as the next colour for unrecognized colours.
    """

    if c == RED:
        return YELLOW
    elif c == YELLOW:
        return GREEN
    else:
        return RED


def update_current_colour():
    """ Updates the `current_colour` to the `next_colour`. """

    global current_colour
    current_colour = next_colour(current_colour)


def set_led_to_current_colour():
    """ Set the led PIXEL to `current_colour`. """

    global current_colour
    PIXEL.fill(current_colour)


def wiggle(mouse):
    """ Wiggles the `mouse` around.

    Makes `MOVES_PER_WIGGLE` moves, going at most `MAX_WIGGLE_DISTANCE`
    in either direction horizontally and vertically.

    In testing, the wigging was annoying since it would jump the cursor
    away from the path I had it on, so there's an extra final move back 
    towards the original coordinates.
    """

    print("wiggle!")

    # This code doesn't seem to reliably work, but I can't figure out
    # why. It helps make the wiggles stay closer to the same point
    # though, so I'm leaving it in.
    dx = 0
    dy = 0

    for _ in range(MOVES_PER_WIGGLE):
        x = random.randint(-MAX_WIGGLE_DISTANCE, MAX_WIGGLE_DISTANCE)
        y = random.randint(-MAX_WIGGLE_DISTANCE, MAX_WIGGLE_DISTANCE)
        dx -= x
        dy -= y
        mouse.move(x=x, y=y)

    # Move the mouse back to the starting position.
    mouse.move(x=dx, y=dy)


def make_button():
    """ Make a `Button` to model the MX switch and set up our
    callbacks for lighting up the LED and cycling `current_colour`.
    """

    pin = DigitalInOut(board.SWITCH)
    pin.switch_to_input(pull=Pull.DOWN)

    button = Button(pin, "button")
    button.on_press = update_current_colour
    button.on_held = set_led_to_current_colour
    return button


def make_touch():
    """ Make a `Button` to model the touch sensor and set up the
    callback for showing `current_colour` on the LED.
    """

    touch = Button(touchio.TouchIn(board.TOUCH), "touch")
    touch.on_held = set_led_to_current_colour
    return touch


def after(scheduled_time, action=None, *args, **kwargs):
    """ Returns `True` if the current time is after the `scheduled_time`. 
    These arguments are in seconds.

    If an `action` is given, it will be called (with any extra arguments) 
    if it's passed the `scheduled_time` as well.
    """

    current_time = time.monotonic()

    if current_time >= scheduled_time:
        action(*args, **kwargs)
        return True
    else:
        return False


button = make_button()
touch = make_touch()

current_colour = RED
wiggle_time = time.monotonic()

while True:
    button.tick()
    touch.tick()

    if current_colour == GREEN:
        wiggle(MOUSE)
    elif current_colour == YELLOW:
        if after(wiggle_time, wiggle, MOUSE):
            # wiggle_time += random.randint(MIN_DELAY, MAX_DELAY)
            wiggle_time += 1
        else:
            wait = wiggle_time - time.monotonic()
            print("next wiggle in {} seconds".format(wait))
    else:
        # We don't do any wiggling if we're RED.
        pass

    # Make sure the light is turned off if nothing is pressed.
    if not button.is_active() and not touch.is_active():
        PIXEL.fill(0)

    # We need to sleep a bit to debounce the switches.
    time.sleep(1.0/60.0)
