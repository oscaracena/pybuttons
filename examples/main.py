
import sys
import standalone_digital_button as sdb
import print_analog_buttons_reading as pabr
import analog_button_array as aba


def choose_example():
    print("Choose an example to run:")
    print(" 1. Standalone Digital Button")
    print(" 2. Print Analog Buttons Reading")
    print(" 3. Analog Button Array")
    print(" Ctrl + C to exit")
    option = input(" - example? ")

    module = {"1": sdb, "2": pabr, "3": aba}.get(option)
    if module is None:
        print("Invalid option.")
    return module


while True:
    try:
        example = choose_example()
        if example is None:
            continue
    except KeyboardInterrupt:
        print("Bye!")
        sys.exit(0)

    try:
        example.run()
    except KeyboardInterrupt:
        pass
