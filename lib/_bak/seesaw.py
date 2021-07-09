"""
This is a lightweight port from CircuitPython to MicroPython
of Dean Miller's https://github.com/adafruit/Adafruit_CircuitPython_seesaw/blob/master/adafruit_seesaw/seesaw.py

* Author(s): Mihai Dinculescu

Implementation Notes
--------------------

**Hardware:**
* Adafruit ATSAMD09 Breakout with SeeSaw: https://www.adafruit.com/product/3657

**Software and Dependencies:**
* MicroPython firmware: https://micropython.org

**Tested on:**
* Hardware: Adafruit HUZZAH32 - ESP32 Feather https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/overview
* Firmware: MicroPython v1.12 https://micropython.org/resources/firmware/esp32-idf3-20191220-v1.12.bin
"""

import time

STATUS_BASE = const(0x00)
TOUCH_BASE = const(0x0F)

_STATUS_HW_ID = const(0x01)
_STATUS_SWRST = const(0x7F)

_HW_ID_CODE = const(0x55)

class Seesaw:
    """Driver for SeeSaw I2C generic conversion trip.
       :param I2C i2c: I2C bus the SeeSaw is connected to.
       :param int addr: I2C address of the SeeSaw device."""
    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr
        self.sw_reset()

    def sw_reset(self):
        """Trigger a software reset of the SeeSaw chip"""
        self._write8(STATUS_BASE, _STATUS_SWRST, 0xFF)
        time.sleep(.500)

        chip_id = self._read8(STATUS_BASE, _STATUS_HW_ID)

        if chip_id != _HW_ID_CODE:
            raise RuntimeError("SeeSaw hardware ID returned (0x{:x}) is not "
                               "correct! Expected 0x{:x}. Please check your wiring."
                               .format(chip_id, _HW_ID_CODE))

    def _write8(self, reg_base, reg, value):
        self._write(reg_base, reg, bytearray([value]))

    def _read8(self, reg_base, reg):
        ret = bytearray(1)
        self._read(reg_base, reg, ret)
        return ret[0]

    def _read(self, reg_base, reg, buf, delay=.005):
        self._write(reg_base, reg)

        time.sleep(delay)

        self.i2c.readfrom_into(self.addr, buf)

    def _write(self, reg_base, reg, buf=None):
        full_buffer = bytearray([reg_base, reg])
        if buf is not None:
            full_buffer += buf

        self.i2c.writeto(self.addr, full_buffer)
