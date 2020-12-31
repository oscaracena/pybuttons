# This demo print voltage reading of analog pin when button
# in button array pressed

import time
from pybuttons import ButtonManager

# change according to your needs
PIN = 36


def run():
    print("Running 'Print Analog Buttons Reading' example...")
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


if __name__ == "__main__":
    run()
