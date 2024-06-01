import neopixel
from machine import Pin

class LedRingManager:
    numberOfLed: int = 24
    ledRingPin: Pin
    ledRing: NeoPixel
    
    currentLedOn: int = 0
    
    def __init__(self, ledRingPin = 15):
        self.ledRingPin = Pin(ledRingPin)
        self.ledRing = neopixel.NeoPixel(self.ledRingPin, self.numberOfLed)
        self.clearLeds()
        
    def clearLeds(self) -> None:
        for i in range(self.numberOfLed - 1):
            self.ledRing[i] = (0, 0, 0)
            
        self.ledRing.write()
    
    # Return a tuple of 3 int values
    def getRgbValueForLed(self, ledIndex: int):
        hue = ledIndex / self.numberOfLed
        return self.hsv_to_rgb(hue, 1, 0.05)  # 'value' of hsv is the brightness
        
    def blinkNexLed(self, numberOfLedToTurnOn = 1) -> None:
        ledRgbColor = self.getRgbValueForLed(self.currentLedOn)
        self.currentLedOn += 1
        if self.currentLedOn == self.numberOfLed:
            self.currentLedOn = 0
        
        self.ledRing[self.currentLedOn - 1] = (0, 0, 0)
        self.ledRing[(self.currentLedOn + numberOfLedToTurnOn - 1) % self.numberOfLed] = ledRgbColor	# -1 as we don't want any offset to turn on one led
            
        self.ledRing.write()
        
    # Return a tuple of 3 int values
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return int(v * 255), int(v * 255), int(v * 255)
        
        i = int(h * 6.0)  # Assume int() truncates!
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q

        return int(r * 255), int(g * 255), int(b * 255)
