# ws2812b.py
import array, time
from machine import Pin
import rp2

# PIO program for WS2812
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)  [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)  [T1 - 1]
    jmp("bitloop")          .side(1)  [T2 - 1]
    label("do_zero")
    nop()                   .side(0)  [T2 - 1]
    wrap()

class WS2812:
    def __init__(self, pin_num, num_leds, brightness=1.0):
        self.num_leds = num_leds
        self.brightness = brightness
        # Setup the state machine
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(pin_num))
        self.sm.active(1)
        # LED buffer (GRB order)
        self.ar = array.array("I", [0 for _ in range(num_leds)])

    def _set_led(self, index, color):
        r, g, b = color
        # scale brightness
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        # WS2812 uses GRB
        self.ar[index] = (g<<16) | (r<<8) | b

    def set_pixel(self, index, color):
        """Set one LED (index starting from 0) to (r,g,b)."""
        if 0 <= index < self.num_leds:
            self._set_led(index, color)

    def fill(self, color):
        """Fill all LEDs with (r,g,b)."""
        for i in range(self.num_leds):
            self._set_led(i, color)

    def clear(self):
        """Turn off all LEDs."""
        self.fill((0,0,0))

    def show(self):
        """Send the buffer to the LEDs."""
        self.sm.put(self.ar, 8)

    def set_brightness(self, brightness):
        """Brightness: 0.0 – 1.0."""
        self.brightness = max(0.0, min(1.0, brightness))
