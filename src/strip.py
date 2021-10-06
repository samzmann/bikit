from neopixel import Neopixel

class Strip():
  def __init__(self, numPixels: int, pin: int, colorOn, colorOff, colorBlink, stateMachine: int):
    self.neopixel = Neopixel(numPixels, stateMachine, pin, "GRB")
    self.colorOn = colorOn
    self.colorOff = colorOff
    self.colorBlink = colorBlink
    self.lastPixelTurnedOn = -1

    self.neopixel.brightness(50)

  def udpateBrightness(self, brightness: int):
    self.neopixel.brightness(brightness)

  def updateSwooshPixelOn(self, nextPixelIndexOn: int):
    if nextPixelIndexOn > self.lastPixelTurnedOn:
      while nextPixelIndexOn > self.lastPixelTurnedOn:
        self.lastPixelTurnedOn += 1
        self.neopixel.set_pixel(self.lastPixelTurnedOn, self.colorBlink)
    elif nextPixelIndexOn < self.lastPixelTurnedOn:
      self.resetToOffColor()
      self.lastPixelTurnedOn = -1

    self.show()

  def resetToOffColor(self):
    self.neopixel.fill(self.colorOff)

  def show(self):
    self.neopixel.show()
