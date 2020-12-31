
# Note

This is a Python implementation of [ButtonFever](https://github.com/mickey9801/ButtonFever), from `mickey9801`, intended to be used on Micropython port for ESP32. The following is an adaptation of its documentation.


# pybuttons

Powerful button tools for managing various button events of standalone button or button array. Tested on ESP32 with MicroPython.

`Button` class handled standalone button debouncing, trigger callback function for single press, double press, and long press events. The class can distinguish different pressing pattern and trigger corresponding callback, i.e. single press vs double press.

`ButtonManager` class manage multiple buttons with single analog pin. The class also provide `print_reading()` method for you to check the analog pin reading. In theory you may add more buttons in the circuit.

## Installation

1. Just copy the file `pybuttons.py` from this repository inside your proyect and import it.

## Standalone Button Usage

`Button` class can be used alone to handle press event of a single digital button.

1. **Import `Button` class**

   ```python
   from pybuttons import Button
   ```

2. **Create button object**

   ```python
   btn = Button(mode, pin, pullup, button_logic)
   ```

   By default, the object will use internal pullup of the board, but you may also use external pullup/pulldown as [example](examples/standalone_digital_button.py/) you concern, e.g. awake from deep sleep mode using button.

   Parameters:

   Parameter                     | Description
   ------------------------------|------------
   mode                          | Declare button mode. Assign `Button.MODE_DIGITAL` for standalone digital button.
   pin                           | GPIO of the button
   pullup=True                   | Use internal pullup
   button_ogic=Button.LOW        | Button logic. Possible value: `Button.HIGH` (pulldown) or `Button.LOW` (pullup, default)

   ```python
   btn_pin = 12
   btn = Button(Button.MODE_DIGITAL, btn_pin, False, Button.HIGH) # using external pulldown
   ```

3. **Declare button callback**

   Button callback must contain 2 parameters:

   Parameter                 | Description
   --------------------------|------------
   btn                       | Button object itself
   pattern                   | Press pattern of the event. Possible value:<ul><li>Button.SINGLE\_PRESS</li><li>Button.DOUBLE\_PRESS</li><li>Button.LONG\_PRESS</li><ul>

   You may declare different callback for different press pattern, or you may use single callback for all patterns.

   ```python
    def press_handler(btn, pattern):
        print("button id {} ".format(btn.get_id()), end="")
        if pattern == Button.SINGLE_PRESS:
            print("pressed.")
        elif pattern == Button.DOUBLE_PRESS:
            print("double pressed.")
        elif pattern == Button.LONG_PRESS:
            print("long pressed.")
   ```

4. **Assign callback for button press events**

   ```python
    btn.on_press(press_handler)
        .on_double_press(press_handler)     # default timeout
        .on_press_for(press_handler, 1000)  # custom timeout for 1 second
   ```

   - `on_press(callback)`

     Single press event handler

   - `on_double_press(callback, timeout=300)`

     Detect double press within timeout.

   - `on_press_for(callback, timeout=3000)`

     Trigger long press event when continue pressed for a while (ie. `timeout`).

5. **In your event loop, read button status.**

   ```python
      while True:
        # ... do other things here
        btn.read()
   ```

### Example

```python
from pybuttons import Button

# change according to your needs
PIN = 36

def press_handler(btn, pattern):
    print("button id {} ".format(btn.get_id()), end="")
    if pattern == Button.SINGLE_PRESS:
        print("pressed.")
    elif pattern == Button.DOUBLE_PRESS:
        print("double pressed.")
    elif pattern == Button.LONG_PRESS:
        print("long pressed.")

btn = Button(Button.MODE_DIGITAL, PIN, False, Button.HIGH)
btn.on_press(press_handler) \
    .on_double_press(press_handler) \
    .on_press_for(press_handler, 1000)

while True:
    btn.read()
```

## Button Array

`ButtonManager` class manage multiple buttons with single analog pin.

### Reference Circuit

![Multiple Button Circuit](https://4.bp.blogspot.com/_mhuuHR0dxnU/TF7Kesn5gmI/AAAAAAAAENg/JeRCtP2oNNs/s1600/analog_button_input.png)

### Determine Voltage Readings for Each Button

To determine voltage range for each button in the array, you may check the actual readings with `print_reading()` method.

The following script calculate the avarage reading of a button from 5 readings:

```python
import time
from pybuttons import ButtonManager

# change according to your needs
PIN = 36

sum_ = i = 0
while True:
    reading = ButtonManager.print_reading(PIN)

    # button pressed
    if reading > 100:
        sum_ += reading
        i += 1
        if i > 4:
            print("Average Reading: {}".format(sum_ / i))
            sum_ = i = 0

    # button released
    else:
        sum_ = i = 0

    time.sleep_ms(200)
```

**NOTE:** Readings of analog pin may vary upon other connected devices. Voltage ranges for each button should determine based on measurement of the final circuit with all required devices initialized.

### Usage

1. **Import `Button` class and `ButtonManager` class**

   ```python
   from pybuttons import Button, ButtonManager
   ```

2. **Create `ButtonMmanager` object**

   ```python
   manager = ButtonManager(pin, btn_num)
   ```

   Parameters:

   Parameter        | Description
   -----------------|------------
   pin              | Analog pin of the button array
   btn_num          | Number of buttons in the array

   ```python
   btn_pin = 35
   manager = ButtonManager(btn_pin, 4)
   ```

3. **Create `Button` objects and assign an ID for the button**

   ```python
   Button(mode, id)
   ```

   Parameters:

   Parameter                     | Description
   ------------------------------|------------
   mode                          | Declare button mode. Assign `Button.MODE_ANALOG_ARRAY` for button in button array.
   id                            | ID of the button

   ```python
    btn0 = Button(Button.MODE_ANALOG_ARRAY, 0)
    btn1 = Button(Button.MODE_ANALOG_ARRAY, 1)
    btn2 = Button(Button.MODE_ANALOG_ARRAY, 2)
    btn3 = Button(Button.MODE_ANALOG_ARRAY, 3)
   ```

4. **Declare button callback**

   (see above: Standalone Button Usage)

5. **Assign callback to events**

   (see above: Standalone Button Usage)

6. **Add button to button manager and provide the voltage range of the button**

   ```python
   add_button(btn, min_volt_reading, max_volt_reading)
   ```

   Parameters:

   Parameter                  | Description
   ---------------------------|------------
   btn                        | Button object
   minVoltageReading          | Minimum voltage reading of the button
   maxVoltageReading          | Maximum voltage reading of the button

   ```python
   manager.add_button(btn0, 3100, 3500)
   ```

7. **Initialize button manager for reading analog pin**

   ```python
   manager.begin()
   ```

8. **In your event loop, update button state**

    ```python
    while True:
        # ... do other things here
        manager.loop()
   ```

### Example

```python
from pybuttons import Button, ButtonManager

# change according to your needs
PIN = 36

def press_handler(btn, pattern):
    print("button id {} ".format(btn.get_id()), end="")
    if pattern == Button.SINGLE_PRESS:
        print("pressed.")
    elif pattern == Button.DOUBLE_PRESS:
        print("double pressed.")
    elif pattern == Button.LONG_PRESS:
        print("long pressed.")

def special_press_handler(btn, pattern):
    print("button id {} is special!!".format(btn.get_id()))

manager = ButtonManager(PIN, 4)
manager.set_adc_resolution(4096)

btn0 = Button(Button.MODE_ANALOG_ARRAY, 0)
btn1 = Button(Button.MODE_ANALOG_ARRAY, 1)
btn2 = Button(Button.MODE_ANALOG_ARRAY, 2)
btn3 = Button(Button.MODE_ANALOG_ARRAY, 3)

btn0.on_press(press_handler)
btn0.on_double_press(press_handler)
btn0.on_press_for(press_handler, 2000)
manager.add_button(btn0, 3100, 3500)

btn1.on_press(press_handler)
btn1.on_press_for(press_handler, 1500)
manager.add_button(btn1, 2200, 2800)

btn2.on_press_for(press_handler, 1000) \
    .on_press(press_handler) \
    .on_double_press(special_press_handler, 300)
manager.add_button(btn2, 1500, 2000)

btn3.on_press(press_handler)
manager.add_button(btn3, 600, 1000)

manager.begin()

while True:
    manager.loop()
```

## Other methods
### `Button` class

- `get_id()`

  Return button pin number for digital button, or ID for button in button array.

- `get_pin()`

  Alias of getID().

### `ButtonManager` class

- `set_adc_resolution(resolution)`

  Set resolution for ADC. The library will set build-in ADC for ESP32 by default.

- `print_reading(pin)`

  Print analog pin reading through Serial port and return the reading.

  ```python
  reading = ButtonManager.print_reading(36)
  ```


## Button Array In Theory
### Voltage Divider Rule

* Vout = Vin(R2/R1+R2)
* Vin = 3.3V # ESP32
* R1+R2 = 5K&#8486; = 5000&#8486;


### Voltage of each button

- Button 1 Vout = 3.3(4000/5000) = 2.64V
- Button 2 Vout = 3.3(3000/5000) = 1.98V
- Button 3 Vout = 3.3(2000/5000) = 1.32V
- Button 4 Vout = 3.3(1000/5000) = 0.66V

### ADC convertion (12bit for ESP32)

0 ~ 3.3V = 0 ~ 4095
3.3V/4095 = 0.81mV

Button|MultiMeter Measurement|Expected Value
:----:|----------------------|-----------------
1     |2.62V                 |3259
2     |1.96V~1.97V           |2420~2432
3     |1.30V~1.31V           |1605~1617
4     |0.65V                 |802

It is required an adjustment for ESP32 ADC with the following equation:

`Vout = e / 4095.0 * 3.3 + 0.1132`

Button|Circuit Measurement|Serial Debug Data|Calculated Voltage w' Adjustment
:----:|-------------------|-----------------|------------------
1     |2.61V              |3070~3103        |2.59V~2.61V
2     |1.95V~1.96V        |2237~2255        |1.92V~1.93V
3     |1.30V              |1456~1461        |~1.29V
4     |0.64V~0.65V        |658~664          |0.64V~0.65V

## Reference

- [ButtonFever from mickey9801](https://github.com/mickey9801/ButtonFever)
- [Multiple button inputs using Arduino analog pin](https://rayshobby.net/wordpress/multiple-button-inputs-using-arduino-analog-pin/)
- [How to Debouce Six Buttons on One Analog Pin With Arduino (tcrosley)](https://electronics.stackexchange.com/a/101414)