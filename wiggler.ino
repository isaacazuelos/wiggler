// An Arduino sketch that takes your cursor on a random walk.

#include <Mouse.h>

void setup() { Mouse.begin(); }

void loop() {
  const int MAX = 10;

  auto x = random(-MAX, MAX);
  auto y = random(-MAX, MAX);

  Mouse.move(x, y, 0);
  delay(16);  // about once a frame at 60Hz
}
