import board
import busio
import displayio
import terminalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import MatrixScanner, KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry

# 1. Initialize Keyboard
keyboard = KMKKeyboard()

# -------------------------------------------------------------------------
# 2. HARDWARE PIN CONFIGURATION (Matches your Schematic)
# -------------------------------------------------------------------------

# COLUMN PINS: D3, D6, D7 
# (Col 1=D3, Col 2=D6, Col 3=D7)
col_pins = (board.D3, board.D6, board.D7)

# ROW PINS: D10, D9, D8
# (Row 1=D10, Row 2=D9, Row 3=D8)
row_pins = (board.D10, board.D9, board.D8)

# ENCODER PINS: A=D0, B=D1, Switch=D2
encoder_a = board.D0
encoder_b = board.D1
encoder_sw = board.D2

# OLED I2C PINS: SCL=D5, SDA=D4
i2c_bus = busio.I2C(board.D5, board.D4)

# -------------------------------------------------------------------------
# 3. MODULES (Encoder & Display)
# -------------------------------------------------------------------------

# --- Encoder Setup ---
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = ((encoder_a, encoder_b, None, False),)

# --- Display Setup ---
driver = None
try:
    import adafruit_displayio_ssd1306
    display_bus = displayio.I2CDisplay(i2c_bus, device_address=0x3C)
    driver = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
    
    display = Display(
        display=driver,
        entries=[
            TextEntry(text='Hack Club!', x=0, y=0, y_anchor='T'),
            TextEntry(text='Layer: ', x=0, y=12, y_anchor='T'),
            TextEntry(text='Base', x=40, y=12, y_anchor='T', layer=0),
            TextEntry(text='Media', x=40, y=12, y_anchor='T', layer=1),
        ],
        width=128,
        height=64,
        dim_time=10,
        dim_target=0.1,
        off_time=1200,
        brightness=1
    )
    keyboard.extensions.append(display)
except ImportError:
    print("OLED libraries missing! Screen will be blank.")

# -------------------------------------------------------------------------
# 4. SCANNERS 
# -------------------------------------------------------------------------

keyboard.matrix = [
    # Scanner 1: The 3x3 Grid
    MatrixScanner(
        cols=col_pins,
        rows=row_pins,
        diode_orientation=MatrixScanner.DIODE_COL2ROW,
    ),
    # Scanner 2: The Encoder Switch (D2)
    KeysScanner(
        pins=(encoder_sw,),
        value_when_pressed=False,
    ),
]

# -------------------------------------------------------------------------
# 5. KEYMAP
# -------------------------------------------------------------------------

keyboard.keymap = [
    [
        # Matrix Keys (3x3) -> Standard Layout
        KC.Q,    KC.W,    KC.E,
        KC.A,    KC.S,    KC.D,
        KC.Z,    KC.X,    KC.C,
        
        # Encoder Switch -> Mute
        KC.MUTE
    ]
]

# Rotary Encoder: Volume Down / Volume Up
encoder_handler.map = [ ((KC.VOLD, KC.VOLU, KC.NO),) ]

if __name__ == '__main__':
    keyboard.go()
