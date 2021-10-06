from signalTimer import globalSignalTimer
from turnSignal import TurnSignal

LEFT_BUTTON_PIN = 16
RIGHT_BUTTON_PIN = 15

LEFT_FRONT_STRIP_PIN = 0
LEFT_BACK_STRIP_PIN = 1

RIGHT_FRONT_STRIP_PIN = 4
RIGHT_BACK_STRIP_PIN = 5

leftTurnSignal = TurnSignal(
  'leftTurnSignal',
  LEFT_BUTTON_PIN,
  LEFT_FRONT_STRIP_PIN,
  LEFT_BACK_STRIP_PIN
)

listenA = False
listenB = False

def incA(count):
  if listenA:
    print('incA:', count)

def incB(count):
  if listenB:
    print('incB:', count)

def startBlinkA():
  global listenA
  listenA = True
  globalSignalTimer.requestStartTimer('A')

def stopBlinkA():
  global listenA
  listenA = False
  globalSignalTimer.requestStopTimer('A')

def startBlinkB():
  global listenB
  listenB = True
  globalSignalTimer.requestStartTimer('B')

def stopBlinkB():
  global listenB
  listenB = False
  globalSignalTimer.requestStopTimer('B')


globalSignalTimer.addOnTickCallback(incA)
globalSignalTimer.addOnTickCallback(incB)

print(globalSignalTimer.getOnTickCallbackListLength())

# globalSignalTimer.requestStartTimer('b')
# globalSignalTimer.requestStopTimer('b')

# startBlinkA()
# startBlinkB()