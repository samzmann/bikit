from machine import Timer
import time
from constants import ANIMATION_PHASE_MS, BRIGHTNESS_OFF, BRIGHTNESS_ON, FADE_OUT_ANIMATION_STEPS, NUM_LEDS_FRONT

class SignalTimer():

  def __init__(self):
    self.isActive = False
    self.activeSignalIds = []
    self.onTickCallbackList = []
    self.timer = Timer()
    self.swooshTickDurationMs = int(ANIMATION_PHASE_MS / NUM_LEDS_FRONT)
    self.fadeOutTickDurationMs = int(ANIMATION_PHASE_MS / FADE_OUT_ANIMATION_STEPS)

    self.ledOnIndex = -1
    self.maxLedOnIndex = NUM_LEDS_FRONT - 1

    self.brightness = BRIGHTNESS_ON
    self.brightnessIncrement = int((BRIGHTNESS_ON - BRIGHTNESS_OFF) / FADE_OUT_ANIMATION_STEPS)

    self.animationPhase = 'swoosh'

  def setAnimationPhase(self, animationPhase):
    self.animationPhase = animationPhase

  def incrementLedOnIndex(self):
    if self.ledOnIndex < self.maxLedOnIndex:
      self.ledOnIndex += 1
    else:
      # self.ledOnIndex = 0
      self.setAnimationPhase('fadeOut')

  def decrementBrightness(self):
    if self.brightness > BRIGHTNESS_OFF:
      self.brightness -= self.brightnessIncrement
    else:
      self.ledOnIndex = 0
      self.brightness = BRIGHTNESS_ON
      self.setAnimationPhase('swoosh')

  def addOnTickCallback(self, callback):
    self.onTickCallbackList.append(callback)

  def executeCallbacks(self):
    for i in range(len(self.onTickCallbackList)):
      self.onTickCallbackList[i](self.ledOnIndex, self.brightness, self.animationPhase)
    return

  def clearOnTickCallbackList(self):
    self.onTickCallbackList = []

  def getOnTickCallbackListLength(self):
    return len(self.onTickCallbackList)

  def requestStartTimer(self, signalId):
    print('requestTimerStart')
    if self.isActive == False:
      self.isActive = True
      self.startTimer()
    
    self.activeSignalIds.append(signalId)

  def requestStopTimer(self, signalId):
    print('requestStopTimer')
    self.activeSignalIds.remove(signalId)

    if len(self.activeSignalIds) == 0:
      # we just removed the last active signalId, this means we can actually stop the timer
      self.stopTimer()

  def startTimer(self, t=None):
    if self.isActive:

      periodDuration = 0

      # print('-- -- -- -- --')
      # print('self.animationPhase', self.animationPhase)
      # print('self.ledOnIndex', self.ledOnIndex)
      # print('self.brightness', self.brightness)
      # print('')

      if self.animationPhase == 'swoosh':
        self.incrementLedOnIndex()
        periodDuration = self.swooshTickDurationMs

      elif self.animationPhase == 'fadeOut':
        self.decrementBrightness()
        periodDuration = self.fadeOutTickDurationMs

      self.executeCallbacks()
      
      self.timer.init(
        mode=Timer.ONE_SHOT,
        period=periodDuration,
        callback=self.startTimer
      )
    else:
      return

  def stopTimer(self):
    self.isActive = False
    self.ledOnIndex = -1
    self.brightness = BRIGHTNESS_ON
    self.animationPhase = 'swoosh'

globalSignalTimer = SignalTimer()