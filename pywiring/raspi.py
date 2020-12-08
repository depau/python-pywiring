# -*- coding: utf-8 -*-

__all__ = "RasPiIO"

from abc import ABC

from RPi import GPIO

from . import IOBase

# BOARD2BCM = [None, None    # 3.3v   5v
#              2,    None,   #        5v
#              3,    None,   #        gnd
#              4,    14,
#              None, 15,     # gnd
#              17,   18,
#              27,   None,   #        gnd
#              22,   23,
#              None, 24,     # 3.3v
#              10,   None,   #        gnd
#              9,    25,
#              11,   8,
#              None, 7,      # gnd
#              0,    1,
#              5,    None,   #        gnd
#              6,    12,
#              13,   None,   #        gnd
#              19,   16,
#              26,   20,
#              None, 21]     # gnd

PINMODES = [["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "HWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "HWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "HWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"],
            ["INPUT", "OUTPUT", "PWM", "SWPWM", "EDGE"]]

map = lambda x, in_min, in_max, out_min, out_max: \
    (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class RasPiIO(IOBase, ABC):
    """
    A wrapper for RPi.GPIO that allows programs written for PyWiring
    to interface with hardware attached to a Raspberry Pi.

    This library uses Broadcom (BCM) pin numbers. Make sure you don't
    manually call RPi.GPIO.setmode(BOARD) while using it running, as it
    will mess things up.

    Make sure you read the Raspberry Pi pinout (http://pinout.xyz)
    before blindly using this module: even though `get_pin_modes`
    may say a pin is suitable for a certain purpose, there might be
    a better one.

    In the pin modes table, "HWPWM" is used to specify that the pulse width
    modulation is hardware-backed; "SWPWM" if it's software-backed. Make
    sure you don't use too many software PWM pins at the same time, as
    they're not very accurate and consume a lot of CPU.
    """

    number_of_pins = 28
    had_adc = False
    has_pwm = True
    has_input = True
    avg_exec_time = 0.005
    pullup_resistors = True
    pulldown_resistors = True

    _pwm = {}

    def __init__(self):
        super(RasPiIO, self).__init__()
        GPIO.setmode(GPIO.BCM)

    def get_pin_modes(self):
        return PINMODES

    def pin_mode(self, pin, input, pullup=False, pulldown=False):
        if pullup and pulldown:
            raise ValueError("Pin {0} can't have both a pull-up and a pull-down resistor attached to it.".format(pin))
        if not pullup and not pulldown:
            pud = GPIO.PUD_OFF
        else:
            pud = GPIO.PUD_UP if pullup else GPIO.PUD_DOWN

        GPIO.setup(pin, GPIO.IN if input else GPIO.OUT, pull_up_down=pud, initial=GPIO.LOW)

    def digital_read(self, pin):
        return bool(GPIO.input(pin))

    def digital_write(self, pin, high):
        GPIO.output(pin, GPIO.HIGH if high else GPIO.LOW)

    def analog_write(self, pin, value):
        self.raspi_pwm_write(pin, 800, map(value, 0, 255, 0, 100))

    def raspi_pwm_write(self, pin, freq=None, dutycycle=None):
        """
        Enables or updates PWM on a pin of choice. If PWM was not enabled
        on that pin, it is enabled. If it is, then its frequency (Hz) and
        duty cicle (1-100) are updated.

        Both `freq` and `dutycycle` must be provided to enable PWM.
        To disable, set them to 0.
        """

        if pin not in self._pwm.keys() and None in (freq, dutycycle):
            raise ValueError("Both freq and dutycycle must be provided in order to enable PWM.")
        elif pin not in self._pwm.keys():
            if 0 in (freq, dutycycle):
                return
            pwm = GPIO.PWM(pin, freq)
            pwm.start(dutycycle)
            self._pwm[pin] = pwm
        else:
            if 0 in (freq, dutycycle):
                self._pwm.pop(pin).stop()
                return
            if freq is not None:
                self._pwm[pin].ChangeFrequency(freq)
            if dutycycle is not None:
                self._pwm[pin].ChangeDutyCycle(dutycycle)

    def enable_event_detect(self, pin, edge, callback=None, bounce=0):
        rpiedge = None
        if edge == "RISING":
            rpiedge = RPi.GPIO.RISING
        elif edge == "FALLING":
            rpiedge = Rpi.GPIO.FALLING
        elif edge == "BOTH":
            rpiedge = Rpi.GPIO.BOTH
        if callback:
            return RPi.GPIO.add_event_detect(pin, rpiedge, callback, bounce)
        else:
            return RPi.GPIO.add_event_detect(pin, rpiedge, bouncetime=bounce)

    def add_event_callback(self, pin, callback):
        return RPi.GPIO.add_event_callback(pin, callback)

    def disable_event_detect(self, pin):
        return RPi.GPIO.remove_event_detect(pin)

    def event_detected(self, pin):
        return RPi.GPIO.event_detected(pin)

    def close(self):
        GPIO.cleanup()
