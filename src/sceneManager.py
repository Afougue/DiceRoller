from lib.ssd1351 import Display, color565
from xglcd_font import XglcdFont

from src.dice import Dice

class SceneState():
    START_SCREEN = 0
    SELECT_DICES = 1
    ROLL_DICES = 2
    DICES_RESULT = 3
    
class SceneManager:
    sceneState = SceneState.START_SCREEN
    
    # Dice variables
    diceList = []
    currentDiceIndex: int = -1
    
    # Display variables
    display = None
    font = XglcdFont('fonts/Unispace12x24.c', 12, 24)
    fontColor = color565(255, 0, 255)
    initialDiceOffset = 25
    heightBetweenDiceLine = 15
    
    # Variables to know what to clear on the screen
    shouldRefreshScreen: bool = False
    shouldRefreshButton: bool = False
    
    def __init__(self):
        self.diceList.append(Dice())
        self.currentDiceIndex = 0
        self.shouldRefreshScreen = True # Tell the screen to draw the start menu
 
    # Clear and add one default dice in the list
    def resetDiceList(self):
        self.diceList.clear()
        self.diceList.append(Dice())
 
    def setDisplay(self, display):
        self.display = display
        
    def buttonHasBeenPressed(self):
        self.shouldRefreshScreen = True
        
        if self.sceneState == SceneState.START_SCREEN:
            self.resetDiceList()
            self.sceneState = SceneState.SELECT_DICES
            
        elif self.sceneState == SceneState.SELECT_DICES:
            self.shouldRefreshScreen = False
            self.shouldRefreshButton = True
            self.changeDiceMaxValue(self.currentDiceIndex)
            
        elif self.sceneState == SceneState.ROLL_DICES:
            print(f'{self.currentDiceIndex=}')
            if self.currentDiceIndex >= (len(self.diceList) - 1):
                self.sceneState = SceneState.DICES_RESULT	# Go to next scene if we roll every dices
            else:
                self.currentDiceIndex += 1
            
        elif self.sceneState == SceneState.DICES_RESULT:
            self.sceneState = SceneState.START_SCREEN
            
    def secondButtonHasBeenPressed(self):
        self.shouldRefreshScreen = True
        
        if self.sceneState == SceneState.SELECT_DICES:
            if self.diceList[self.currentDiceIndex].maxValue != -1 and self.currentDiceIndex <= 5:
                self.diceList.append(Dice(-1)) # Append a new dice with initial value of -1, to let the user quicly exit this menu
                self.currentDiceIndex += 1
            else:
                self.diceList.pop()			# If the user chose not to add the currently selected dice, remove it
                self.currentDiceIndex = 0	# Now we want to roll the dices from the 1st to the last
                self.sceneState = SceneState.ROLL_DICES
            
    def changeDiceMaxValue(self, diceIndex: int):
        if len(self.diceList) <= diceIndex:
            print("Error: dice index is out of bound")
            return
        
        currentDiceIndexMaxValue = self.diceList[diceIndex].maxValue
        newDiceMaxValue = 6 # Default value
        
        if currentDiceIndexMaxValue == 6:
            newDiceMaxValue = 10
            
        elif currentDiceIndexMaxValue == 10:
            newDiceMaxValue = 20
            
        elif currentDiceIndexMaxValue == 20:
            if self.currentDiceIndex == 0:	# Don't let the user disable the 1st dice
                newDiceMaxValue = 6
            else:
                newDiceMaxValue = -1
            
        elif currentDiceIndexMaxValue == -1:
            newDiceMaxValue = 6
        
        self.diceList[diceIndex].changeMaxValue(newDiceMaxValue)
    
    def update(self):
        if self.sceneState == SceneState.ROLL_DICES:
            self.diceList[self.currentDiceIndex].rollDice()
            self.shouldRefreshButton = True            
    
    def draw(self):
        if self.display is None:
            print("Error: display has not been set !")
            return
        
        # If there's nothing new to draw
        if not self.shouldRefreshScreen and self.shouldRefreshButton == -1:
            return
        
        self.clearOldPixels()
        
        # Draw the current state
        if self.sceneState == SceneState.START_SCREEN:
            self.display.draw_text(0, 0, 'Salut mec', self.font, self.fontColor)
            self.display.draw_text(0, 50, 'Appuie sur', self.font, self.fontColor)
            self.display.draw_text(0, 75, 'le bouton !', self.font, self.fontColor)
            
        elif self.sceneState == SceneState.SELECT_DICES:
            self.display.draw_text(0, 0, 'Select', self.font, self.fontColor)
            self.drawChooseDicesMaxValue()
            
        elif self.sceneState == SceneState.ROLL_DICES:
            self.display.draw_text(0, 0, 'Roll', self.font, self.fontColor)
            self.drawRollDices()
            
        elif self.sceneState == SceneState.DICES_RESULT:
            self.display.draw_text(0, 0, 'Result', self.font, self.fontColor)
            self.drawResult()
            
        else:
            self.display.draw_text(0, 0, 'Error', self.font, self.fontColor)
        
            
    def clearOldPixels(self):
        if self.shouldRefreshScreen:        
            self.display.clear()
            self.shouldRefreshScreen = False
            
        elif self.shouldRefreshButton:
            emptyText = '    '  # Remove the last digit to remove the 0 of the tens
            verticalOffset = self.initialDiceOffset + self.currentDiceIndex * self.heightBetweenDiceLine
            self.display.draw_text8x8(55, verticalOffset, emptyText, self.fontColor)
            self.shouldRefreshButton = False
            
    def drawChooseDicesMaxValue(self):    
        for i, dice in enumerate(self.diceList):
            verticalOffset = self.initialDiceOffset + i * self.heightBetweenDiceLine
            displayedValue = "None" if dice.maxValue == -1 else dice.maxValue
            
            self.display.draw_text8x8(0, verticalOffset, f'De {i}: {displayedValue}', self.fontColor)
            
    def drawRollDices(self):
         for i, dice in enumerate(self.diceList):
            verticalOffset = self.initialDiceOffset + i * self.heightBetweenDiceLine          
            self.display.draw_text8x8(0, verticalOffset, f'De {i}: {dice.currentValue} ({dice.maxValue}) ', self.fontColor)
            
    def drawResult(self):
        self.drawRollDices()
        verticalOffset = self.initialDiceOffset + self.heightBetweenDiceLine * len(self.diceList)
        resultValue = sum([dice.currentValue for dice in self.diceList])
        totalMaxValue = sum([dice.maxValue for dice in self.diceList])
        self.display.draw_text8x8(0, verticalOffset, f'Total: {resultValue} ({totalMaxValue})', self.fontColor)
        