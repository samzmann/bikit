from signalTimer import globalSignalTimer
from turnSignal import TurnSignal

# Button **************************
LEFT_BUTTON_PIN = 16
RIGHT_BUTTON_PIN = 15

# Front Strips **************************
LEFT_FRONT_STRIP_PIN = 0
RIGHT_FRONT_STRIP_PIN = 4

# Back Strips **************************
LEFT_BACK_STRIP_PIN = 1
RIGHT_BACK_STRIP_PIN = 5

# State Machines **************************
LEFT_STATE_MACHINE = 0
RIGHT_STATE_MACHINE = 1

leftTurnSignal = TurnSignal(
  'leftTurnSignal',
  LEFT_BUTTON_PIN,
  LEFT_FRONT_STRIP_PIN,
  LEFT_BACK_STRIP_PIN,
  LEFT_STATE_MACHINE
)

rightTurnSignal = TurnSignal(
  'rightTurnSignal',
  RIGHT_BUTTON_PIN,
  RIGHT_FRONT_STRIP_PIN,
  RIGHT_BACK_STRIP_PIN,
  RIGHT_STATE_MACHINE
)

print('main done')