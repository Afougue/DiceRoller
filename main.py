from machine import Pin, SPI, Timer
from time import sleep
from lib.ssd1351 import Display, color565

from src.sceneManager import SceneManager
from src.ledRing import LedRingManager

# GPIO numbers of every input
pin_DIN = 19
pin_CLK = 18
pin_CS =  17
pin_DC =  20
pin_RST = 21
pin_main_button = 0
pin_second_button = 4

# Object which will handle the main logic
sceneManager = SceneManager()
isMainButtonPressed = False
isSecondButtonPressed = False

def interruption_handler(pin):
    global isMainButtonPressed
    flags = pin.irq().flags()
    
    # Rising and falling are swapped in PULL_UP
    # I'm using a boolean in adition as sometimes, the raspberrry was triggering this function twice for the same state
    if flags & Pin.IRQ_RISING:
        if isMainButtonPressed:
            isMainButtonPressed = False
    else:
        if not isMainButtonPressed:
            isMainButtonPressed = True
            sceneManager.buttonHasBeenPressed()
            
def interruption_second_handler(pin):
    global isSecondButtonPressed
    flags = pin.irq().flags()
    
    # Rising and falling are swapped in PULL_UP
    # I'm using a boolean in adition as sometimes, the raspberrry was triggering this function twice for the same state
    if flags & Pin.IRQ_RISING:
        if isSecondButtonPressed:
            isSecondButtonPressed = False
    else:
        if not isSecondButtonPressed:
            isSecondButtonPressed = True
            sceneManager.secondButtonHasBeenPressed()

def main():    
    # Setup buttons
    main_button = Pin(pin_main_button, mode=Pin.IN, pull=Pin.PULL_UP)
    main_button.irq(trigger= Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=interruption_handler)
    
    second_button = Pin(pin_second_button, mode=Pin.IN, pull=Pin.PULL_UP)
    second_button.irq(trigger= Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=interruption_second_handler)

    # Create the display object
    spi = SPI(0, baudrate=14500000, sck=Pin(pin_CLK), mosi=Pin(pin_DIN))
    display = Display(spi, dc=Pin(pin_DC), cs=Pin(pin_CS), rst=Pin(pin_RST))
    sceneManager.setDisplay(display)
    
    # Create the led ring
    ledRing = LedRingManager()
    
    while True:
        sceneManager.update()
        sceneManager.draw()
        ledRing.blinkNexLed()
        sleep(0.05)

if __name__ == '__main__':
    main()
    