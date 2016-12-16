# -*- coding: utf-8 -*-

"""
This module aims to bring a Wiring-like interface to Python.
It tries to implement most Wiring functions using different
ports (parallel, PCF8574 through I2C, GPIO).
"""

__all__ = ("IOBase", "i2c")

class IOBase(object):
    """
    Base class with the basic methods.
    """

    number_of_pins = 0
    """
    Number of available I/O pins for this specific interface.
    If 0, the number is unknown. If negative, the number of pins is its
    absolute value, but it might change.
    """

    has_adc = False
    """
    True if the interface has analog-digital converters on at least one
    pin. If True, the :py:meth:`~IOBase.analog_read` method will return
    analog values if used on the right pins.
    """

    has_pwm = False
    """
    True if the interface can send PWM waves on at least one pin. If
    True, :py:meth:`~IOBase.analog_write` will write analog values if
    used on the right pins.
    """

    has_input = False
    """
    True if at least one of the pins can be used as a digital input.
    If False, the read value will be the logic level previously set
    with digital_write.
    """

    pullup_resistors = False
    """
    True if the interface has pullup resistors.
    """

    pulldown_resistors = False
    """
    True if the interface has pulldown resistors.
    """

    avg_exec_time = 0
    """
    Average time of a read/write operation in milliseconds.

    Note: this is a preset value. It's not updated at runtime.
    """

    def pin_mode(self, pin, input, pullup=False, pulldown=False):
        """
        Sets :py:const:`pin` in a specified direction. If :py:const:`input` is
        :py:const:`True`, it will be set as input, otherwise as output.

        If :py:const:`pullup`
        """
        raise NotImplementedError

    def port_mode(self, input, pullup=False, pulldown=False):
        """
        Same as :py:meth:`~IOBase.pin_mode`, but sets the direction of
        all the pins at once.
        """
        for i in xrange(self.number_of_pins):
            self.pin_mode(input, pullup, pulldown)

    def digital_read(self, pin):
        """
        Reads the logic level of a particular pin. True means "high",
        and False means "low". The pin needs to be configured as input,
        otherwise False will be returned regardless of the pin's actual state.

        If the pin doesn't fall within the port's pin range, None will be
        returned.
        """
        raise NotImplementedError

    def digital_read_bulk(self, *pins):
        """
        Reads the level of multiple pins in only one operation, if possible.
        Send the pin numbers you want to read as positional arguments.

        Returns a dict whose keys are the pin numbers you asked for, with the
        respective level as value.
        """
        tor = {}
        for pin in pins:
            if pin >= 0 and pin < self.number_of_pins:
                tor[pin] = self.digital_read(pin)
            else:
                tor[pin] = None
        return tor

    def digital_write(self, pin, high):
        """
        Writes a level to a particular pin. True means "high" and False means
        "low". The pin needs to be configured as output.
        """
        raise NotImplementedError

    def digital_write_bulk(self, pins):
        """
        Writes logic levels to multiple pins in only one operation, if possible.
        :py:data:`pins` must be a dict whose keys are the pin numbers and whose
        values are the logic levels.

        You should prefer this method if you need to write multiple pins in a
        short amount of time, as a write operation takes some time on protocols
        like i2c.
        """
        for pin in pins:
            if pin >= 0 and pin < self.number_of_pins:
                self.digital_write(pin, pins[pin])

    def analog_read(self, pin):
        """
        If :py:data:`pin` has an analog-digital converter, returns the voltage
        in a range between 0 and 1023, where 0 is 0 volts and 1023 is the
        working voltage.

        If it doesn't have an ADC, returns 1023 if digital_read(pin) == True,
        otherwise 0.
        """
        raise NotImplementedError

    def analog_write(self, pin, value):
        """
        If :py:data:`pin` is a PWM pin, write an analog value (PWM wave) to it,
        otherwise pulls it high if value > 0 or low if value == 0.
        """
        raise NotImplementedError

    def get_pin_modes(self):
        """
        Get the supported modes for all the pins. If the resolution can be
        obtained, returns a list of dicts in which every dict curresponds to
        a pin. Each dict contains mode-resolution key-value pairs. If the
        implementation does not support resolution, a list of lists/tuples
        will be returned, containing the supported modes.
        The "officially" supported modes are "INPUT", "OUTPUT", "ANALOG" and
        "PWM". Other modes and methods to use them may be added by each
        implementation.
        """
        raise NotImplementedError

    def close(self):
        """
        Close the interface after using.
        """
        pass