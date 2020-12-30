import time
from machine import Pin


class Button:
    MODE_DIGITAL, MODE_ANALOG_ARRAY = range(2)
    LOW, HIGH = range(2)
    IDLE, PRESSING = range(2)
    SINGLE_PRESS, DOUBLE_PRESS, LONG_PRESS = range(3)

    def __init__(self, mode, pin, pullup, button_logic):
        self._id = pin
        self._mode = mode
        self._button_logic = self.LOW
        self._last_loop = 0
        self._loop_interval = 20
        self._double_press_timeout = 300
        self._press_for_timeout = 3000

        self._prev_state = self.IDLE
        self._state = self.IDLE
        self._press_count = 0
        self._first_pressed_at = 0
        self._pressed_since = 0
        self._is_debouncing = False

        self._callbacks = {}

        self._pin = None
        if _mode == self.MODE_DIGITAL:
            self._pin = Pin(
                self._id, Pin.IN, Pin.PULL_UP if pullup else None)
            self._button_logic = button_logic

    def on_press(self, cb):
        self._callbacks["press"] = cb
        return self

    def on_double_press(self, cb, timeout=300):
        self._callbacks["double_press"] = cb
        self._double_press_timeout = timeout
        return self

    def on_press_for(self, cb, timeout=3000):
        self._callbacks["press_for"] = cb
        self._press_for_timeout = timeout
        return self

    def update_state(self, state):
        self._prev_state = self._state
        self._state = state
        return self

    def read(self):
        if self._mode != self.MODE_DIGITAL:
            return

        cur_time = time.tick_ms()
        if cur_time - self._last_loop >= self._loop_interval:
            self._last_loop = cur_time
            x = self._pin.value()
            if x == self._button_logic:
                self.update_state(self.PRESSING)
            else:
                self.update_state(self.IDLE)
            self.loop()

    def loop(self):
        cur_time = time.tick_ms()
        if self._prev_state == self.IDLE and \
            self._state == self.PRESSING:
            self._is_debouncing = True
            return

        if self._press_count > 0 and \
            not ("double_press" in self._callbacks and \
                cur_time - self._first_pressed_at <= self._double_press_timeout) and \
            not ("press_for" in self._callbacks and \
                self._pressed_since != 0 and \
                self._state == self.PRESSING):

            press_cb = self._callbacks.get("press")
            if press_cb:
                press_cb(self, self.SINGLE_PRESS)
            self._press_count = 0
            self._first_pressed_at = 0






