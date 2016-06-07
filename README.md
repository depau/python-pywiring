#PyWiring
This module tries to bring a Wiring-like interface to Python.
It tries to implement most Wiring functions using different
ports (parallel, PCF8574 through I²C, GPIO). The [LiquidCrystal python module](https://github.com/Davideddu/python-liquidcrystal) uses it.

## IOBase documentation
`pywiring.IOBase` is the base class for all PyWiring I/O implementations. All methods need to be replaced with working ones in the actual implementation.

### Attributes
All these values are usually preset and not updated at runtime. Check the implementation's documentation for more information.

* **number_of_pins:** Number of available I/O pins for this specific interface. If 0, the number is unknown. If negative, the number of pins is its absolute value, but it might change.
* **has_adc: ** True if the interface has analog-digital converters on at least one pin. If True, the `analog_read` method will return analog values if used on the right pins.
* **had_pwm:** True if the interface can send PWM waves on at least one pin. If True, `analog_write` will write analog values if used on the right pins.
* **has_input:** True if at least one of the pins can be used as a digital input. If False, the read value will be the logic level previously set with digital_write.
* **pullup_resistors**, **pulldown_resistors**: True if the interface has at least one pullup/pulldown resistor.
* **avg_exec_time:** Average time of a read/write operation in milliseconds. **Note:** this is a preset value. It's not updated at runtime.

### Methods

#### pin_mode(`pin`, `input`, `pullup=False`, `pulldown=False`)
Sets the pin mode. If `input` is True, it will be set as an input, otherwise as an output. If `pullup`/`pulldown` is True and a pullup/pulldown resistor is present, it will be enabled.

#### port_mode(`input`, `pullup=False`, `pulldown=False`)
Same as `pin_mode`, but changes the mode of all the port instead, if possible. If it's not possible, an `IOError` will be raised.

#### digital_read(`pin`)
Reads the logic level of a particular pin. True means "high", and False means "low". The pin needs to be configured as input, otherwise False will be returned regardless of the pin's actual state.
If the pin doesn't fall within the port's pin range, None will be returned.

#### digital_read_bulk(`*pins`)
Reads the level of multiple pins in only one operation, if possible. Send the pin numbers you want to read as positional arguments.
Returns a dict whose keys are the pin numbers you asked for, with the respective level as value.

#### digital_write(`pin`, `level`)
Writes a logic level to a particular pin. True means "high" and False means "low". The pin needs to be configured as output for this to work.

#### digital_write_bulk(`pins`)
Writes logic levels to multiple pins in only one operation, if possible. `pins` must be a dict whose keys are the pin numbers and whose values are the logic levels.
You should prefer this method over `digital_write` if you need to write multiple pins in a short amount of time, as a write operation takes some time on protocols like I²C.

#### analog_read(`pin`)
If `pin` has an analog-digital converter, returns the voltage in a range between 0 and 1023 where 0 is 0 volts and 1023 is the working voltage.
If it doesn't have an ADC, returns 1023 if `digital_read(pin) == True`, otherwise 0.

#### analog_write(`pin`, `value`)
If `pin` is a PWM pin, writes an analog value (PWM wave) to it, otherwise pulls it high if `value > 0` or low if `value == 0`.

#### close()
Closes the interface after using. It should always be called to clean up the environment and make sure the adapter can be used by other programs.

## Actual implementations documentation
### I²C
For I²C-based implementations (in the `i2c` submodule), you need to provide the I²C bus number and the device's I²C address as positional arguments. For example:

```python
from pywiring import i2c
ioi = i2c.PCF8574IO(1, 0x27)
```

You can get a list of I²C buses on Linux by running `i2cdetect -l`. You can scan a bus for connected devices with `i2cdetect -y <bus number>`. Make sure the `i2c-dev` kernel module is loaded (`sudo modprobe i2c-dev`).

Make sure you have read/write access to the bus.

Beware that a write transaction through I²C usually takes between 4 to 6 milliseconds. You may want to avoid any calls to `time.sleep` if you need to wait shorter than that. You should also prefer using `digital_write_bulk` instead of multiple `digital_write`s, as `digital_write_bulk` tries to set the pins with as little operations as possible.

Make sure you close the interface after using.

### Raspberry Pi
The Raspberry Pi module is a wrapper of RPi.GPIO, and as such it has to be installed first.

The usage is pretty much standard.

```python
from pywiring import raspi
ioi = raspi.RasPiIO()
```

The [pinout](http://pinout.xyz) is your friend: some pins might not be the best for a specific task. Only Broadcom (BCM) pin numbers are currently supported. Do not manually change to board numbers! Things may get messy.

#### Analog input
As you might now, the Raspberry Pi has no analog input. As such, the `analog_read` method will always raise `NotImplementedError`.

#### PWM (analog output)
Raspberry Pi has hardware PWM on only on pins 12, 13 and 18. PWM on other pins is software-emulated. As such, you need to make sure you don't use too many of them at the same time, as the CPU usage will raise quickly.

There are two ways to enable PWM: one is the *classic* `analog_write`, which works as you might expect (LEDs may flicker on software PWM), and `raspi_pwm_write`.

##### raspy_pwm_write(`pin`, `freq`, `dutycycle`)
If PWM is not enabled on pin, it enables it with the provided parameters. IF it's already enabled, the parameters are updated.

`freq` is in Hz and must be greater than 1; `dutycycle` must be between 1 and 100. Both must be provided upon enabling.

Setting either one of them to 0 will turn off PWM on that specific pin.

### Parallel port
As parallel ports were not meant to be used for I/O, they have a few limitations. First, they don't have a power source. You can get some power from USB, VGA, DVI or HDMI (some pinouts [here](http://davideddu.org/blog/posts/graphics-card-i2c-port-howto/)). Second, they do have both inputs and outputs, but not on the same pins, and not in order; there is a pin mapping below. Third, all inputs have pullup resistors, which means they're not very useful in some situations.

#### Pin mapping
The table below refers to the following pin out.

![Parallel port pinout](https://upload.wikimedia.org/wikipedia/commons/e/e1/25_Pin_D-sub_pinout.svg)

##### Output pins

| Library pin number | Parallel port pin |
|:------------------:|:-----------------:|
|          0         |         1         |
|          1         |         2         |
|          2         |         3         |
|          3         |         4         |
|          4         |         5         |
|          5         |         6         |
|          6         |         7         |
|          7         |         8         |
|          8         |         9         |
|          9         |         14        |
|         10         |         16        |
|         11         |         17        |

##### Input pins

| Library pin number | Parallel port pin |
|:------------------:|:-----------------:|
|          0         |         10        |
|          1         |         11        |
|          2         |         12        |
|          3         |         13        |
|          4         |         15        |

Pins from 18 to 25 are ground.

Prefer using output pins from 1 to 8 if possible.

If your computer has multiple parallel ports, you need to specify the port number as an argument. For example

```python
from pywiring import parport
ioi = parport.ParallelIO(1) # default is 0
```

On Linux, the `lp` kernel module needs to be unloaded before using this, and the `parport` module needs to be loaded.

```shell
sudo modprobe -r lp
sudo modprobe parport
```

You also need to make sure you have read/write access to the parallel port.

## Adding features
Features in this package are grouped in submodules based on their dependencies only. Pull requests for modules like `arduino.py` will be refused unless they're based on an Arduino-specific library. Arduino code should go into a module for serial devices (ex. `serport.py`).

Make sure you use unique names (e.g. don't use `serial`, there is already a `serial` module around, it would cause ImportErrors; `serport` is better; `parport` is another example).

All methods must be implemented. If a feature can't be implemented, replace it with a stub method and add a warning for the user into it (see `parport.ParallelIO.pin_mode`), or try to replicate it as best as you can (see `i2c.PCF8574IO.pin_mode`). If the behavior differs, make sure you write it in the documentation and, eventually, throw a warning.

"Bulk" methods are time critical! They **must** take as little time as possible! Don't replace them with `for pin in pins: digital_write(pin, pins[pin])`, unless there is no other way to do it!!! If you can set multiple pins at once, **do it!**
