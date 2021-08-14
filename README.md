# Wiggler

Use a [Adafruit NeoKey Trinkey][neokey] to wiggle the mouse periodically _for
reasons_.

This has three modes, based on stoplight colours.

1. Red is off, where no mouse wiggling happens.
2. Yellow wiggles the mouse every 1 to 4 minutes at random.
3. Green wiggles the mouse constantly.

You can see the current mode by touching the capacitive button, and cycle modes
with the big button.

[neokey]: https://www.adafruit.com/product/5020

## Installation

You'll need to set up CircuitPython on the Trinkey. Get the [`.uf2` file][uf2].
Double tap the reset button so it mounts as `TRINKEYBOOT` and drag the file onto
that drive to install it. It should reboot as and mount with a new name. Copy
the `code.py` file onto the drive and it should start running the code.

You can see the output of the script, and access a REPL, by connecting to the
serial console. [These instructions][serial] show you how to do that.

[uf2]: https://circuitpython.org/board/adafruit_neokey_trinkey_m0/

## Bugs

There's an issue where the wiggling doesn't always seem to return the cursor
back to _exactly_ where it started -- especially if it wiggles while your real
mouse if also giving inputs or changes modes. I can't find the culprit.

## License

This project is under the [MIT][] license. At least to the extent it makes sense
to release 12 lines of code.

[MIT]: https://choosealicense.com/licenses/mit
