from signalTimer import globalSignalTimer

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