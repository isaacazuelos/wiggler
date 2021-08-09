# Wiggler

Using an Arduino to take your cursor on a [random walk.](walk) Should work on
anything that supports Arduino's `Mouse.h` library.

I had originally tried to make this work on a [2% Milk][milk] board with some
better controls. For reasons I couldn't figure out, the pro micro clone I had
didn't work with `Mouse.h` for some reason. You can see this attempt's code in
the `milk` directory.

I also tried to get this working on an STM32 [blackpill][] with other features
too, but some poking around with a multimeter makes it look like my knockoff's
user-programmable button is not connected correctly.

[walk]: https://en.wikipedia.org/wiki/Random_walk
[milk]: https://github.com/Spaceman/SpaceboardsHardware/tree/master/Keyboards/2%25%20Milk
[blackpill]: https://github.com/WeActTC/MiniSTM32F4x1

## License

This project is under the [MIT][] license. At least to the extent it makes sense
to release 12 lines of code.

[MIT]: https://choosealicense.com/licenses/mit
