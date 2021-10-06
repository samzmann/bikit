import time
from machine import Pin
from signalTimer import globalSignalTimer
from strip import Strip

COLOR_ON_FRONT = (255, 255, 255) # white
COLOR_ON_BACK = (255, 0, 0) # red
COLOR_OFF = (0, 0, 0) # black
COLOR_ON_BLINK = (255, 215, 0) # orange

class TurnSignal():
  def __init__(
    self,
    id: str,
    buttonPin: int,
    frontStripPin: int,
    backStripPin: int,
  ):
    self.id = id
    self.isOn = False
    self.lastButtonPressTimestamp = 0

    self.debounceMs = 200 # debounce button press for 200ms

    button = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
    button.irq(trigger = Pin.IRQ_RISING, handler = self.handleButtonPress)

    self.frontStrip = Strip(18, frontStripPin, COLOR_ON_FRONT, COLOR_OFF, COLOR_ON_BLINK)

  def handleButtonPress(self, irq):
    now = time.ticks_ms()

    if now - self.lastButtonPressTimestamp > self.debounceMs:
      self.lastButtonPressTimestamp = now
      self.toggleIsOn()

  def toggleIsOn(self):
    self.isOn = not self.isOn

    if self.isOn:
      globalSignalTimer.requestStartTimer(self.id)
    else:
      globalSignalTimer.requestStopTimer(self.id)
