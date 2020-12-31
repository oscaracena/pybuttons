import time
from machine import Pin, ADC


class Button:
    MODE_DIGITAL, MODE_ANALOG_ARRAY = range(2)
    LOW, HIGH = range(2)
    IDLE, PRESSING = range(2)
    SINGLE_PRESS, DOUBLE_PRESS, LONG_PRESS = range(3)

    def __init__(self, mode, pin, pullup=True, button_logic=LOW):
        self._id = pin
        self._mode = mode
        self._button_logic = button_logic
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
        if mode == self.MODE_DIGITAL:
            self._pin = Pin(
                self._id, Pin.IN, Pin.PULL_UP if pullup else None)

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

        cur_time = time.ticks_ms()
        if cur_time - self._last_loop >= self._loop_interval:
            self._last_loop = cur_time
            x = self._pin.value()
            if x == self._button_logic:
                self.update_state(self.PRESSING)
            else:
                self.update_state(self.IDLE)
            self.loop()

    def loop(self):
        cur_time = time.ticks_ms()
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

        if self._prev_state == self.PRESSING and \
            self._state == self.PRESSING:

            if self._is_debouncing:
                self._press_count += 1
                if self._first_pressed_at == 0:
                    self._first_pressed_at = cur_time
                if self._pressed_since == 0:
                    self._pressed_since = cur_time
                self._is_debouncing = False

            press_for_cb = self._callbacks.get("press_for")
            if press_for_cb and self._press_count > 0 and \
                cur_time - self._pressed_since >= self._press_for_timeout:

                press_for_cb(self, self.LONG_PRESS)
                self._press_count = 0
                self._first_pressed_at = 0
                self._pressed_since = 0
                return

            double_press_cb = self._callbacks.get("double_press")
            if double_press_cb and self._press_count > 1 and \
                cur_time - self._first_pressed_at <= self._double_press_timeout:

                double_press_cb(self, self.DOUBLE_PRESS)
                self._press_count = 0
                self._first_pressed_at = 0

        if self._prev_state == self.PRESSING and \
            self._state == self.IDLE:
            self._pressed_since = 0

    def get_id(self):
        return self._id

    def get_pin(self):
        return self.get_id()


class ButtonManager:
    def __init__(self, pin, btn_num):
        self._pin = pin
        self._button_count = btn_num
        self._buttons = {}

        self._adc_resolution = 4096
        self._last_loop = 0
        self._loop_interval = 20

        self._adc = ADC(Pin(pin))
        self._adc.atten(ADC.ATTN_11DB)

    def set_adc_resolution(self, resolution):
        self._adc_resolution = resolution
        return self

    def add_button(self, btn, min_volt_reading, max_volt_reading):
        b = btn.get_id()
        self._buttons[b] = (btn, min_volt_reading, max_volt_reading)
        return self

    def get_button(self, id_):
        return self._buttons.get(id_)[0]

    def begin(self):
        self._adc.read()
        time.sleep_ms(1)

    def loop(self):
        cur_time = time.ticks_ms()
        if cur_time - self._last_loop >= self._loop_interval:
            self._last_loop = cur_time
            self._update_button_state()

    @classmethod
    def print_reading(cls, pin):
        adc = ADC(Pin(pin))
        adc.atten(ADC.ATTN_11DB)

        z = adc.read()
        if z > 100:
            print(z)
        return z

    def _update_button_state(self):
        b = self._read_button()
        for i, fields in self._buttons.items():
            btn = fields[0]
            state = Button.PRESSING if i == b else Button.IDLE
            btn.update_state(state)
            btn.loop()

    def _read_button(self):
        button = -1
        sum_ = 0

        for _ in range(4):
            sum_ += self._adc.read()
        z = sum_ / 4

        if z >= 100 or z < self._adc_resolution:
            for i, fields in self._buttons.items():
                vmin, vmax = fields[1:]
                if vmin < z < vmax:
                    button = i
                    break

        return button
