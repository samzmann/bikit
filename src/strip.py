from constants import BRIGHTNESS_ON
from gammaCorrection import gammaCorrectRgb, gammaCorrectSingleValue
from neopixel import Neopixel

class Strip():
  def __init__(self, numPixels: int, pin: int, colorOn, colorOff, colorBlink, stateMachine: int):
    self.neopixel = Neopixel(numPixels, stateMachine, pin, "GRB")
    self.numPixels = numPixels
    self.colorOn = colorOn
    self.colorOff = colorOff
    self.colorBlink = colorBlink
    self.lastPixelTurnedOn = -1

    self.udpateBrightness(BRIGHTNESS_ON)

    self.resetToOnColor()
    self.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# We should only use these methods to update the neopixels.
# They have built in gamma correction.

  def udpateBrightness(self, brightness: int):
    self.neopixel.brightness(gammaCorrectSingleValue(brightness))
  
  def updatePixel(self, index, color):
    self.neopixel.set_pixel(index, gammaCorrectRgb(color))

  def updateFill(self, color):
    self.neopixel.fill(gammaCorrectRgb(color))

  def show(self):
    self.neopixel.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

  def updateSwooshPixelOn(self, nextPixelIndexOn: int):
    if nextPixelIndexOn == self.numPixels:
      self.resetToOffColor()

    else:
      self.updatePixel(nextPixelIndexOn, self.colorBlink)
      
      if nextPixelIndexOn > self.lastPixelTurnedOn:
        for i in range(nextPixelIndexOn):
          self.updatePixel(i, self.colorBlink)

      self.lastPixelTurnedOn = nextPixelIndexOn

  def fillWithBlinkColor(self):
    self.updateFill(self.colorBlink)

  def resetToOnColor(self):
    self.udpateBrightness(BRIGHTNESS_ON)
    self.updateFill(self.colorOn)

  def resetToOffColor(self):
    self.updateFill(self.colorOff)
    self.lastPixelTurnedOn = -1
