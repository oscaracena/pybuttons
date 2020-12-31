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


def run():
    print("Running 'Analog Button Array' example...")
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


if __name__ == "__main__":
    run()
