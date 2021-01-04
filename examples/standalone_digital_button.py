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


def run():
    print("Running 'Standalone Digital Button' example...")
    btn = Button(Button.MODE_DIGITAL, PIN, False, Button.HIGH)
    btn.on_press(press_handler) \
        .on_double_press(press_handler) \
        .on_press_for(press_handler, 1000)

    while True:
        btn.read()


if __name__ == "__main__":
    run()
