// An Arduino sketch to build a mouse wiggler out of a 2% Milk keyboard.
//
// I was never able to get the mouse movement to work, but everything else does
// what it should.

#include <Mouse.h>

// ## LEDs

const int LED = 17;
const bool LED_ON = HIGH;
const bool LED_OFF = LOW;

void set_rx_led(bool on) { digitalWrite(LED, on); }
void set_tx_led(bool on) { on ? TXLED1 : TXLED0; }

// ## Buttons

/// Buttons are mechanical devices, and the metal contacts often behave like
/// springs and "bounce" between on and off states when the switch is actuated.
///
/// While this isn't usually noticeable to humans, computers are fast enough to
/// read this bouncing.
///
/// This is the length of the delay we'll use between reading the switch's state
/// to detect an intentional change.
const int8_t DEBOUNCE_DELAY_MS = 16;  // About 1 frame at 60Hz.

const bool BUTTON_UP = HIGH;
const bool BUTTON_DOWN = LOW;
const uint8_t BUTTON_TOP = 4;
const uint8_t BUTTON_BOTTOM = 5;

/// Checks if the button went from down to up between successive calls,
/// indicating that the button was released.
///
/// This does not include any delay for debouncing.
bool top_was_released() {
  static auto previous = BUTTON_UP;

  auto current = digitalRead(BUTTON_TOP);
  auto was_released = (current == BUTTON_UP && previous == BUTTON_DOWN);

  previous = current;
  return was_released;
}

/// Like `top_was_released` but for the bottom button.
bool bottom_was_released() {
  static auto previous = BUTTON_UP;

  auto current = digitalRead(BUTTON_BOTTOM);
  auto was_released = (current == BUTTON_UP && previous == BUTTON_DOWN);

  previous = current;
  return was_released;
}

//  ## Wiggling

const int MAX_WIGGLE = 10;

/// Wiggle the mouse a random amount vertically and horizontally by at most
/// `MAX_WIGGLE`.
void wiggle() {
  auto x = random(-MAX_WIGGLE, MAX_WIGGLE);
  auto y = random(-MAX_WIGGLE, MAX_WIGGLE);
  Mouse.move(x, y, 0);
}

// ## Arduino functions

const uint32_t TWO_MINUTES_MS = 2L * 60L * 1000L;
const uint32_t ONE_SEC_MS = 1000L;

void setup() {
  pinMode(BUTTON_TOP, INPUT_PULLUP);
  pinMode(BUTTON_BOTTOM, INPUT_PULLUP);

  pinMode(LED, OUTPUT);
  set_rx_led(LED_OFF);
  set_tx_led(LED_OFF);

  Mouse.begin();
}

void loop() {
  static auto wiggle_enabled = false;
  static auto fast_mode = false;
  static uint32_t last_wiggled = 0;

  // Is it time to wiggle yet?
  uint32_t current = millis();
  uint32_t time_to_wait = fast_mode ? ONE_SEC_MS : TWO_MINUTES_MS;

  // If millis just overflowed, reset last_wiggled.
  if (current < last_wiggled) {
    last_wiggled = 0;
    return;
  }

  bool should_wiggle = current - last_wiggled >= time_to_wait;

  if (wiggle_enabled && should_wiggle) {
    wiggle();
    last_wiggled = current;
  }

  // check keys
  if (top_was_released()) {
    wiggle_enabled = !wiggle_enabled;
    last_wiggled = 0;
    set_rx_led(wiggle_enabled);
  }

  if (bottom_was_released()) {
    fast_mode = !fast_mode;
    set_tx_led(fast_mode);
  }

  delay(DEBOUNCE_DELAY_MS);
}
