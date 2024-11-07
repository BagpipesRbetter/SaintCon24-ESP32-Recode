import time
import board
import displayio
import digitalio
from adafruit_st7789 import ST7789
import busio

# Set IO6 as power control for backlight
power_pin = digitalio.DigitalInOut(board.IO6)
power_pin.direction = digitalio.Direction.OUTPUT
power_pin.value = True  # Power on display backlight

# Short delay to allow power-up
time.sleep(1)

# Manually set up SPI using busio.SPI
spi = busio.SPI(clock=board.IO10, MOSI=board.IO11)

# Possible CS and DC pins to try
cs_pins = [board.IO0, board.IO1, board.IO2, board.IO3]
dc_pins = [board.IO4, board.IO5, board.IO7, board.IO8]

for cs_pin in cs_pins:
    for dc_pin in dc_pins:
        print(f"Trying CS={cs_pin}, DC={dc_pin}")
        try:
            # Setup CS and DC pins for display
            tft_cs = digitalio.DigitalInOut(cs_pin)
            tft_dc = digitalio.DigitalInOut(dc_pin)

            # Initialize display bus and display object
            display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=None)
            display = ST7789(display_bus, width=240, height=320)

            # Fill screen with red as a test
            splash = displayio.Group()
            color_bitmap = displayio.Bitmap(240, 320, 1)
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFF0000  # Red color

            bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
            splash.append(bg_sprite)
            display.show(splash)

            # Keep display on for a moment to observe
            time.sleep(5)

        except Exception as e:
            print(f"Failed with CS={cs_pin}, DC={dc_pin}: {e}")

        # Safely turn off display and power off backlight before next iteration
        if 'display' in locals():
            display.show(None)
            del display

        power_pin.value = False
        time.sleep(1)  # Short delay between tests
        power_pin.value = True
        time.sleep(1)
