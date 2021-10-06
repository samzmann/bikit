from neopixel import Neopixel

class Strip():
  def __init__(self, numPixels: int, pin: int, colorOn, colorOff, colorBlink, stateMachine: int):
    self.neopixel = Neopixel(numPixels, stateMachine, pin, "GRB")
    self.numPixels = numPixels
    self.colorOn = colorOn
    self.colorOff = colorOff
    self.colorBlink = colorBlink
    self.lastPixelTurnedOn = -1

    self.neopixel.brightness(50)

  def udpateBrightness(self, brightness: int):
    self.neopixel.brightness(brightness)

  def updateSwooshPixelOn(self, nextPixelIndexOn: int):
    if nextPixelIndexOn == self.numPixels:
      self.resetToOffColor()

    else:
      self.neopixel.set_pixel(nextPixelIndexOn, self.colorBlink)
      
      if nextPixelIndexOn > self.lastPixelTurnedOn:
        for i in range(nextPixelIndexOn):
          self.neopixel.set_pixel(i, self.colorBlink)

      self.lastPixelTurnedOn = nextPixelIndexOn

  def resetToOffColor(self):
    self.neopixel.fill(self.colorOff)
    self.lastPixelTurnedOn = -1

  def show(self):
    self.neopixel.show()
