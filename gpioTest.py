import gpioDriverLime as gpio
import time

gpio.setup()

gpio.outputLevel('FAN', 1)

