from random import randint

class Dice:
    maxValue: int = 0
    currentValue: int = 0
    
    def __init__(self, maxValue = 6):
        self.changeMaxValue(maxValue)
    
    # Change the max value and re-roll the dice
    # Set value to -1 to disable the dice
    def changeMaxValue(self, newMaxValue: int) -> None:
        self.maxValue = newMaxValue
        self.rollDice()
            
    # Roll the dice and save the value in self.currentValue
    def rollDice(self) -> int:
        if self.maxValue != -1:         
            self.currentValue = randint(1, self.maxValue)
            return self.currentValue