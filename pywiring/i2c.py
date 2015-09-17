# -*- coding: utf-8 -*-

__all__ = ("I2CIOBase", "PCF8574IO", "LCDBackpack")

from . import IOBase
from numpy import uint8
import smbus

def num2boolgen(num):
    for bit in reversed(bin(num)[2:]):
        yield bit == "1"

class I2CIOBase(IOBase):
    """
    Base class for I2C-based I/O ports.
    """

    def __init__(self, bus, address):
        super(I2CIOBase, self).__init__()
        self._bus = smbus.SMBus()
        self._bus.open(bus)
        self.address = address

    def close(self):
        """
        Closes the I2C bus.
        """
        self._bus.close()

class PCF8574IO(I2CIOBase):
    """
    Class that provides basic I2C communication methods,
    adapted for the PCF8574 integrated circuit.

    :py:const:`bus` must be an integer curresponding to
    the I2C bus you want to use. :py:const:`address` is the I2C
    address of the device.

    The port has 8 pins. It has no ADC or PWM pins.
    """

    number_of_pins = 8
    had_adc = False
    has_pwm = False
    has_input = True
    avg_exec_time = 0.005
    pullup_resistors = False
    pulldown_resistors = False

    def __init__(self, bus, address):
        super(PCF8574IO, self).__init__(bus, address)
        self._dirmask = uint8(0xFF)    # All inputs
        self._shadow = self._bus.read_byte(self.address)

    def pin_mode(self, pin, input, pullup=False, pulldown=False):
        if input:
            self._dirmask |= uint8(1 << pin)
        else:
            self._dirmask &= ~uint8(1 << pin)

    def port_mode(self, input, pullup=False, pulldown=False):
        self._dirmask = uint8(0xFF) if input else uint8(0x00)

    def read(self):
        return self._dirmask & uint8(self._bus.read_byte(self.address))

    def write(self, value):
        self._shadow = value & ~uint8(self._dirmask)
        self._bus.write_byte(self.address, self._shadow)

    def digital_read(self, pin):
        return digital_read_bulk(pin)[pin]

    def digital_read_bulk(self, *pins):
        tor = {}
        portstate = self.read()
        for pin in pins:
            if pin >= 0 and pin < self.number_of_pins:
                pval = portstate & self._dirmask
                tor[pin] = bool((pval >> pin) & 0x01)
            else:
                tor[pin] = None
        return tor

    def digital_write(self, pin, high):
        self.digital_write_bulk({pin:high})

    def digital_write_bulk(self, pins):
        shadow = self._shadow

        for pin in pins:
            if pin >= 0 and pin < self.number_of_pins:
                bpin = 1 << pin
                if pins[pin]:
                    shadow |= bpin
                else:
                    shadow &= ~uint8(bpin)
        self.write(shadow)

    def analog_read(self, pin):
        return 255 if self.digital_read(pin) else 0

    def analog_write(self, pin, value):
        self.digital_write(pin, value > 0)

# Simple alias for easier usage
LCDBackpack = PCF8574IO