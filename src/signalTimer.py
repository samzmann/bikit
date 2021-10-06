from machine import Timer
import time

from constants import ANIMATION_PHASE_MS, NUM_LEDS_FRONT

class SignalTimer():

  def __init__(self):
    self.isActive = False
    self.activeSignalIds = []
    self.onTickCallbackList = []
    self.timer = Timer()
    self.tickDurationMs = ANIMATION_PHASE_MS

    self.count = 0
    self.maxCount = NUM_LEDS_FRONT

  def incrementCount(self):
    if self.count < self.maxCount:
      self.count += 1
    else:
      self.count = 0

    print('incrementCount:', self.count)

  def addOnTickCallback(self, callback):
    self.onTickCallbackList.append(callback)

  def executeCallbacks(self):
    for i in range(len(self.onTickCallbackList)):
      self.onTickCallbackList[i](self.count)
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
    print('startTimer')
    if self.isActive:

      self.incrementCount()

      self.executeCallbacks()
      
      self.timer.init(
        mode=Timer.ONE_SHOT,
        period=self.tickDurationMs,
        callback=self.startTimer
      )
    else:
      return

  def stopTimer(self):
    self.isActive = False
    self.count = 0

globalSignalTimer = SignalTimer()