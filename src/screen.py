from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI


# GPIO numbers
pin_DIN = 19
pin_CLK = 18
pin_CS =  17
pin_DC =  20
pin_RST = 21


pin_button = Pin(28, mode=Pin.IN, pull=Pin.PULL_UP)

spi = SPI(0, baudrate=14500000, sck=Pin(pin_CLK), mosi=Pin(pin_DIN))
display = Display(spi, dc=Pin(pin_DC), cs=Pin(pin_CS), rst=Pin(pin_RST))


# colors
black = color565(0, 0, 0)
blue = color565(64, 0, 255)

def draw_smiley():
    display.clear(blue)
    display.draw_circle(32, 85, 20, black)
    display.draw_circle(96, 85, 20, black)
    display.draw_hline(32, 42, 64, black)


sprite = display.load_sprite("diodon.raw", 64, 64)

sprite_X = 0

def interruption_handler(pin):
    global sprite_X
    sprite_X += 1
    print("slt")

pin_button.irq(trigger= Pin.IRQ_FALLING, handler=interruption_handler)


while True:
    display.draw_sprite(sprite, sprite_X, 0, 64, 64)
    sleep(0.5)