import time
from machine import Pin
from constants import BUTTON_DEBOUNCE_MS, COLOR_OFF, COLOR_ON_BLINK, COLOR_ON_FRONT, NUM_LEDS_FRONT
from signalTimer import globalSignalTimer
from strip import Strip

class TurnSignal():
  def __init__(
    self,
    id: str,
    buttonPin: int,
    frontStripPin: int,
    backStripPin: int,
    stateMachine: int,
  ):
    self.id = id
    self.isOn = False
    self.lastButtonPressTimestamp = 0

    self.debounceMs = BUTTON_DEBOUNCE_MS

    button = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
    button.irq(trigger = Pin.IRQ_RISING, handler = self.handleButtonPress)

    self.frontStrip = Strip(NUM_LEDS_FRONT, frontStripPin, COLOR_ON_FRONT, COLOR_OFF, COLOR_ON_BLINK, stateMachine)

    globalSignalTimer.addOnTickCallback(self.onBlinkTick)

  def onBlinkTick(self, ledOnIndex: int):
    if self.isOn:
      self.frontStrip.updateSwooshPixelOn(ledOnIndex)
      self.frontStrip.show()

  def handleButtonPress(self, irq):
    now = time.ticks_ms()

    if now - self.lastButtonPressTimestamp > self.debounceMs:
      self.lastButtonPressTimestamp = now
      self.toggleIsOn()

  def toggleIsOn(self):
    self.isOn = not self.isOn

    print("toggleIsOn", self.isOn)

    if self.isOn:
      globalSignalTimer.requestStartTimer(self.id)

      self.frontStrip.resetToOffColor()
      self.frontStrip.show()
    else:
      globalSignalTimer.requestStopTimer(self.id)
      
      self.frontStrip.resetToOnColor()
      self.frontStrip.show()
