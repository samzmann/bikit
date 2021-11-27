import time
from machine import Pin, Timer
from constants import BRIGHTNESS_ON, BUTTON_DEBOUNCE_MS, COLOR_OFF, COLOR_ON_BACK, COLOR_ON_BLINK, COLOR_ON_FRONT, NUM_LEDS_BACK, NUM_LEDS_FRONT
from signalTimer import globalSignalTimer
from strip import Strip

class TurnSignal():
  def __init__(
    self,
    id: str,
    buttonPin: int,
    frontStripPin: int,
    backStripPin: int,
    stateMachineFront: int,
    stateMachineBack: int,
  ):
    self.id = id
    self.isOn = False
    self.lastButtonPressTimestamp = 0

    self.debounceMs = BUTTON_DEBOUNCE_MS
    self.longPressMs = 150

    self.button = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
    self.button.irq(trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING, handler = self.handleButtonPress)

    self.frontStrip = Strip(NUM_LEDS_FRONT, frontStripPin, COLOR_ON_FRONT, COLOR_OFF, COLOR_ON_BLINK, stateMachineFront)
    self.backStrip = Strip(NUM_LEDS_BACK, backStripPin, COLOR_ON_BACK, COLOR_OFF, COLOR_ON_BLINK, stateMachineBack)

    globalSignalTimer.addOnTickCallback(self.onBlinkTick)

    self.prevLedOnIndex = 0
    self.prevBrightness = BRIGHTNESS_ON

    self.timer = Timer()

  def onBlinkTick(self, ledOnIndex: int, brightness: int, animationPhase):
    if self.isOn:

      if animationPhase == 'swoosh':
        self.frontStrip.updateSwooshPixelOn(ledOnIndex)
        self.frontStrip.udpateBrightness(brightness)

        self.backStrip.updateSwooshPixelOn(ledOnIndex)
        self.backStrip.udpateBrightness(brightness)

      if animationPhase == 'fadeOut':
        self.frontStrip.udpateBrightness(brightness)
        self.frontStrip.fillWithBlinkColor()
        
        self.backStrip.udpateBrightness(brightness)
        self.backStrip.fillWithBlinkColor()

      self.frontStrip.show()
      self.backStrip.show()

  def handleButtonPress(self, irq):
    now = time.ticks_ms()

    isButtonPressed = self.button.value()

    if isButtonPressed == 1:
      if now - self.lastButtonPressTimestamp > self.debounceMs:
        self.lastButtonPressTimestamp = now
        
        self.timer.deinit()

        self.timer.init(
          mode=Timer.ONE_SHOT,
          period=self.longPressMs,
          callback=self.toggleOnTimerEnd
        )
   
  def toggleOnTimerEnd(self, t):
    isButtonPressed = self.button.value()

    if isButtonPressed == 1:
      self.toggleIsOn()

  def toggleIsOn(self):
    self.isOn = not self.isOn

    # print("toggleIsOn", self.isOn)

    if self.isOn:
      globalSignalTimer.requestStartTimer(self.id)

      self.frontStrip.resetToOffColor()
      self.frontStrip.show()

      self.backStrip.resetToOffColor()
      self.backStrip.show()

    else:
      globalSignalTimer.requestStopTimer(self.id)
      
      self.frontStrip.resetToOnColor()
      self.frontStrip.show()

      self.backStrip.resetToOnColor()
      self.backStrip.show()
