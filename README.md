# Optical Liquid Level Sensor

Simple optical liquid level dectector scripts in Python.

## Things used in this project

* * *

### Hardware:

- x1 Raspberry Pi (any model)
- x1 Optical Liquid Level Sensor like FS-IR02 - [Documentation](https://www.dfrobot.com/wiki/index.php/Liquid_Level_Sensor-FS-IR02_SKU:_SEN0205)
- x1 Passive Buzzer
- x1 red LED  (or any color you like)
- x1 breadboard + a couple of connector wires

### Software apps and online services:

- Raspbian Stretch Lite 4.19 and after - [Documentation](https://www.raspberrypi.org/downloads/raspbian/)

## The story

* * *

### Introduction

When the liquid comes in to contact with the sensor probe the microcontroller will output HIGH logic. When the liquid is not in contact with the probe the microcontroller will output LOW logic.

### Device schema:

- Connect the liquid level sensor to the PIN 5
- Connect the passive buzzer to the PIN 6
- The red LED will light on/off. It could useful if you would like to connect a lifting pump for example.

## Take a look to the code

* * *

Define the GPIOs to use on Raspberry Pi
```python
GPIO_OPTICAL_LIQUID_LEVEL_SENSOR  = 5
GPIO_BUZZER                       = 6
```

To drive the GPIO pin, first we need to initialize it.
Then we will monitor the low/high level on the GPIO and return a binary value (0 for dry and 1 for wet) whether water is present or not.
Here is the Python code:

```python
while True:
    if (GPIO.input(pin) == GPIO.LOW):
        reading += 1
    if reading >= 1000:
        return 0
    if (GPIO.input(pin) != GPIO.LOW):
        return 1
```

Et voilà !

## Additional resources

* * *

- [Raspbian downloads page](https://www.raspberrypi.org/downloads/raspbian/)
- [Liquid Level Sensor FS-IR02 documentation](https://www.dfrobot.com/wiki/index.php/Liquid_Level_Sensor-FS-IR02_SKU:_SEN0205)
