# -*- coding: utf-8 -*-

__all__ = ("ParallelIO")

from . import IOBase
from numpy import uint8
from warnings import warn
import parallel

def num2boolgen(num):
    for bit in reversed(bin(num)[2:]):
        yield bit == "1"

class ParallelIO(IOBase):
    """
    Base class for parallel port I/O.

    Make sure you unload the lp kernel module and load parport before
    using. Also make sure you have read/write permissions.

    :py:data:`port` must be the port number to use (default: 0).

    Note: inputs and outputs are placed on different pins, even if the
    pin number is the same. The pin numbers in the library don't
    match the actual pin numbers. Check the mapping below. Also, the
    input pins have pullup resistors, which means they'll return True
    when not connected.

    ![Parallel port pinout](https://upload.wikimedia.org/wikipedia/commons/e/e1/25_Pin_D-sub_pinout.svg)

    ### Output pins

    ============= ==============
    Library pin # Parallel pin #
    ============= ==============
    0             1
    1             2
    2             3
    3             4
    4             5
    5             6
    6             7
    7             8
    8             9
    9             14
    10            16
    11            17
    ============= ==============

    ### Input pins

    ============= ==============
    Library pin # Parallel pin #
    ============= ==============
    0             10
    1             11
    2             12
    3             13
    4             15
    ============= ==============

    Pins from 18 to 25 are ground. There is no voltage source.
    Either take current from USB, VGA, HDMI, DVI
    (see (http://davideddu.org/blog/posts/graphics-card-i2c-port-howto/)[this]),
    or pull one pin high and use it as a voltage source. It might not be
    enough though.
    """

    number_of_pins = 12 # Only output pins
    had_adc = False
    has_pwm = False
    has_input = True
    pullup_resistors = True
    pulldown_resistors = False

    def __init__(self, port=0):
        super(ParallelIO, self).__init__()
        self._lpt = parallel.Parallel(port)
        self._outputs = [0]*4

        self.digital_write_bulk({i:False for i in xrange(0, 12)})

    def pin_mode(self, *a):
        warn("Pin mode can't be set on a parallel port", RuntimeWarning)

    def port_mode(self, *a):
        warn("Port mode can't be set on a parallel port", RuntimeWarning)

    def digital_read(self, pin):
        if pin == 0:
            return self._lpt.getInAcknowledge()
        elif pin == 1:
            return self._lpt.getInBusy()
        elif pin == 2:
            return self._lpt.getInPaperOut()
        elif pin == 3:
            return self._lpt.getInSelected()
        elif pin == 4:
            return self._lpt.getInError()

    def digital_read_bulk(self, *pins):
        tor = {}
        for pin in pins:
            tor[pin] = self.digital_read(pin)
        return tor

    def digital_write(self, pin, high):
        if pin > 0 and pin < 9:
            bpin = 1 << (pin - 1)
            mask = self._lpt.getData()
            if high:
                mask |= bpin
            else:
                mask &= ~uint8(bpin)
            self._lpt.setData(mask)
        elif pin == 0:
            self._lpt.setDataStrobe(high)
        elif pin == 9:
            self._lpt.setAutoFeed(high)
        elif pin == 10:
            self._lpt.setInitOut(high)
        elif pin == 11:
            self._lpt.setSelect(high)

    def digital_write_bulk(self, pins):
        dpins = []
        for pin in pins:
            if pin == 0 or pin >= 9:
                self.digital_write(pin, pins[pin])
            else:
                dpins.append(pin-1)

        mask = self._lpt.getData()
        for i in dpins:
            if pins[i]:
                mask |= 1 << i
            else:
                mask &= ~uint8(1 << i)
        self._lpt.setData(mask)

    def analog_read(self, pin):
        return 255 if self.digital_read(pin) else 0

    def analog_write(self, pin, value):
        self.digital_write(pin, value > 0)