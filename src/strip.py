from neopixel import Neopixel

class Strip():
  def __init__(self, numPixels: int, pin: int, colorOn, colorOff, colorBlink):
    self.neopixel = Neopixel(numPixels, 0, pin, "GRB")
    self.colorOn = colorOn
    self.colorOff = colorOff
    self.colorBlink = colorBlink

  def udpateBrightness(self, brightness: int):
    self.neopixel.brightness(brightness)

  def updateSwooshPixelOn(self, nextPixelIndexOn: int):
    self.neopixel.set_pixel(nextPixelIndexOn, self.colorBlink)

  def show(self):
    self.neopixel.show()
