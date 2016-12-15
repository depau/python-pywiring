# -*- coding: utf-8 -*-

__all__ = ("ChipIO")

from . import IOBase
from CHIP_IO.GPIO import GPIO
# import CHIP_IO.LRADC as ADC
import CHIP_IO.PWM as HWPWM
import CHIP_IO.SOFTPWM as SWPWM
import CHIP_IO.OverlayManager as OM
from warnings import warn

PINALIASES = ["TWI1-SDA", "KPD-I2C-SDA", "U13_9",
              "TWI1-SCK", "KPD-I2C-SCL", "U13_11",
              "LCD-D2", "LCD-D2", "U13_17",
              "PWM0", "PWM0", "U13_18",
              "LCD-D4", "LCD-D4", "U13_19",
              "LCD-D3", "LCD-D3", "U13_20",
              "LCD-D6", "LCD-D6", "U13_21",
              "LCD-D5", "LCD-D5", "U13_22",
              "LCD-D10", "LCD-D10", "U13_23",
              "LCD-D7", "LCD-D7", "U13_24",
              "LCD-D12", "LCD-D12", "U13_25",
              "LCD-D11", "LCD-D11", "U13_26",
              "LCD-D14", "LCD-D14", "U13_27",
              "LCD-D13", "LCD-D13", "U13_28",
              "LCD-D18", "LCD-D18", "U13_29",
              "LCD-D15", "LCD-D15", "U13_30",
              "LCD-D20", "LCD-D20", "U13_31",
              "LCD-D19", "LCD-D19", "U13_32",
              "LCD-D22", "LCD-D22", "U13_33",
              "LCD-D21", "LCD-D21", "U13_34",
              "LCD-CLK", "LCD-CLK", "U13_35",
              "LCD-D23", "LCD-D23", "U13_36",
              "LCD-VSYNC", "LCD-VSYNC", "U13_37",
              "LCD-HSYNC", "LCD-HSYNC", "U13_38",
              "LCD-DE", "LCD-DE", "U13_40",
              "UART1-TX", "UART-TX", "U14_3",
              "UART1-RX", "UART-RX", "U14_5",
              "LRADC", "ADC", "U14_11",
              "XIO-P0", "XIO-P0", "U14_13",
              "XIO-P1", "XIO-P1", "U14_14",
              "XIO-P2", "GPIO1", "U14_15",
              "XIO-P3", "GPIO2", "U14_16",
              "XIO-P4", "GPIO3", "U14_17",
              "XIO-P5", "GPIO4", "U14_18",
              "XIO-P6", "GPIO5", "U14_19",
              "XIO-P7", "GPIO6", "U14_20",
              "AP-EINT1", "KPD-INT", "U14_23",
              "AP-EINT3", "AP-INT3", "U14_24",
              "TWI2-SDA", "I2C-SDA", "U14_25",
              "TWI2-SCK", "I2C-SCL", "U14_26",
              "CSIPCK", "SPI-SEL", "U14_27",
              "CSICK", "SPI-CLK", "U14_28",
              "CSIHSYNC", "SPI-MOSI", "U14_29",
              "CSIVSYNC", "SPI-MISO", "U14_30",
              "CSID0", "CSID0", "U14_31",
              "CSID1", "CSID1", "U14_32",
              "CSID2", "CSID2", "U14_33",
              "CSID3", "CSID3", "U14_34",
              "CSID4", "CSID4", "U14_35",
              "CSID5", "CSID5", "U14_36",
              "CSID6", "CSID6", "U14_37",
              "CSID7", "CSID7", "U14_38"]

PINMODES = [("INPUT", "OUTPUT", "PWM", "SWPWM", "I2C1SDA"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "I2C1SCK"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "HWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "LCD"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "UARTTX"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "UARTRX"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "ANALOG"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "XIO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "I2C2SDA"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "I2C2SCK"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "SPISEL"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "SPICLK"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "SPIMOSI"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM", "SPIMISO"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM"),
            ("INPUT", "OUTPUT", "PWM", "SWPWM")]

map = lambda x, in_min, in_max, out_min, out_max: \
    (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

pin_num = lambda x: PINALIASES.index(x)/3

class ChipIO(IOBase):
    """
    A wrapper for CHIP_IO.GPIO that allows programs written for PyWiring
    to interface with hardware attached to a NTC CHIP computer.

    You can use pin names instead of pin numbers. Check the pinout at
    http://docs.getchip.com/chip.html#gpio and CHIP_IO's documentation at
    https://github.com/xtacocorex/CHIP_IO#chip_io . If you check their
    Readme page you can find a table of possible aliases. The line numbers
    of that table (starting from zero) are also accepted.

    In the pin modes list, a few additional values are provided: "HWPWM"
    for PWM0, the only hardware-backed PWM pin; "SWPWM" for software-only
    PWM pins; "XIO" for pins provided by the I2C expansion module; "SPI*"
    for pins that may be used for SPI; "I2C*" for the four I2C pins; "LCD"
    for the pins originally intended for use with LCD displays.

    Make sure you don't use too many software PWM pins at the same time,
    as they're not very accurate and consume a lot of CPU.
    """

    number_of_pins = 52
    had_adc = False #ADC.get_device_exists() # not implemented ATM
    has_pwm = True
    has_input = True
    avg_exec_time = 0.005
    pullup_resistors = True
    pulldown_resistors = True

    _pwm = []
    # _adc_setup = False

    def __init__(self):
        super(ChipIO, self).__init__()
        if not OM.get_pwm_loaded():
            OM.load("PWM0")

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

    def port_mode(self, input, pullup=False, pulldown=False):
        for i in xrange(self.number_of_pins):
            self.pin_mode(input, pullup, pulldown)

    def digital_read(self, pin):
        return bool(GPIO.input(pin))

    def digital_read_bulk(self, *pins):
        tor = {}
        for pin in pins:
            if type(pin) == str and pin in PINALIASES or \
              (type(pin) == int and pin >= 0 and pin < self.number_of_pins):
                tor[pin] = self.digital_read(pin)
            else:
                tor[pin] = None
        return tor

    def digital_write(self, pin, high):
        GPIO.output(pin, GPIO.HIGH if high else GPIO.LOW)

    def digital_write_bulk(self, pins):
        for pin in pins:
            if type(pin) == str and pin in PINALIASES or \
              (type(pin) == int and pin >= 0 and pin < self.number_of_pins):
                self.digital_write(pin, pins[pin])

    # def analog_read(self, pin):
    #     if not self._adc_setup:
    #         ADC.setup()
    #         self._adc_setup = True

    def analog_write(self, pin, value):
        self.chip_pwm_write(pin, 800, map(value, 0, 255, 0, 100))

    def chip_pwm_write(self, pin, freq=None, dutycycle=None, polarity=None):
        """
        Enables or updates PWM on a pin of choice. If PWM was not enabled
        on that pin, it is enabled. If it is, then its frequency (Hz) and
        duty cicle (1-100) are updated.

        Both `freq` and `dutycycle` must be provided to enable PWM.
        To disable, set them to 0.
        """

        if pin in ("PWM0", "U13_18", 3):
            PWM = HWPWM
        else:
            PWM = SWPWM
        
        if type(pin) == int:
            pin_n = pin
            pin = PINALIASES[pin_n*3]
        else:
            pin_n = pin_num(pin)

        if pin_n not in self._pwm and None in (freq, dutycycle):
            raise ValueError("Both freq and dutycycle must be provided in order to enable PWM.")
        elif pin_n not in self._pwm:
            if 0 in (freq, dutycycle):
                PWM.stop(pin)
                PWM.cleanup()
            pwm = PWM.start(pin, dutycycle, freq, polarity if polarity is not None else 0)
            self._pwm.append(pin_n)
        else:
            if 0 in (freq, dutycycle):
                self._pwm.remove(pin_n)
                PWM.stop(pin)
                PWM.cleanup()
                return
            if freq is not None:
                PWM.set_frequency(pin, freq)
            if dutycycle is not None:
                PWM.set_duty_cycle(pin, dutycycle)
            if polarity is not None:
                warn("Polarity cannot be changed", RuntimeWarning)

    def close(self):
        GPIO.cleanup()