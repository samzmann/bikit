# Bikit - It's a kit, for your bike. It's a Bikit 🤩

[WTF is Bikit](#project-structure)
- [The problem with bike lights](#the-problem-with-bike-lights)
- [The solution](#the-solution)

[Project Structure](#project-structure)
- [Libraries](#libraries)
  - [Neopixel](#neopixel)
- [Classes](#classes)
  - [Strip](#neopixel)
  - [TurnSignal](#neopixel)
  - [SignalTimer](#neopixel)
- [Utils](#utils)
  - [Gamma correction](#gamma-correction)

[Contribute](#project-structure)

# WTF is Bikit

Yes, riding a bike is definitly the best way to get around in a city! But it can also be pretty dangerous and inconveninent:
- some crazy sriver doesn't see you, runs you over. Game over.
- some douchebag cuts off your lock, rides away and you walk home. The sadness.

The idea behind Bikit if to create open source systems to make bikes more safe and conveninent in cities. First step: lights!

## The problem with bike lights
There are a few problem with most lights currently available:
- they don't always make you visible enough to cars
- they are easily and often stolen
- they aren't always battery powered. When they are, it's usually a two part system (front + back), which means two batteries, two chargers, need to remember to charge both.
- they lack a key feature that every single car lights has: turn signals.
- finally, they could just be way more cool.

## The solution

**Better visibility to traffic**

By attaching LED strips on the bike frame, especially on the fork (front) and the sea stays (back), you can make your bike way more visible to traffic.

Note: these are really position lights, meant to make you more visible to ongoing traffic. They are really not great at lighting the road ahead of you. The intended use in on city streets, where lighting up the road is not such a concern (street lights are common since the 1800s). If you're riding through the woods, or in other dark areas, these lights aren't for you.

**Better theft protection**

LED strips are very thin and hardly noticable when attached to the bike (when turned off of course). Also, the system is made up of many parts (LED strips, cables, battery mount) which makes it very impractical to steal.

**Better battery**

The system is powered by a single 5V battery. You only need to keep that single battery charged. Since it's a regular phone battery bank, it can come in really handy if your phone is running out of battery. The battery can easily be swapped if you need more or less capacity.

**Turn signals**

Gone are the days of thrusting your arm out in the air, hoping that the mad driver behind you will have mercy on your poor soul, and hoping your wheels wont get caugh in the tram track beneath you. (*Voice of Jony Ive, ex head of Design at Apple*) You can now keep your hands nice and comfy on your handlebars, and simply move your thumb to press a button indicating you're turning.

**More Swag 😎**

I mean, the light just look super cool. Like your bike is straight out of Tron. How can you compete with that!

<table>
    <tr>
        <td>
          <img src="https://github.com/LaVielle/bikit/blob/main/assets/side_with_rider.jpeg" alt="This could be you" />
        </td>
        <td>
          <img src="https://github.com/LaVielle/bikit/blob/main/assets/dark_alleyway.jpeg" alt="In a dark alleyway" />
        </td>
    </tr>
</table>

# Project Structure

## Libraries

### `Neopixel`
The neopixel library is what controls the LED strips. It's taken from https://github.com/blaz-r/pi_pico_neopixel and copied into `lib/neopixel.py`

The only modification to the library is in the `brightness` method, where we set the minumum brightness value to `0` (instead of `1` in the original version).

## Classes

### `Strip`
The `Strip` class is meant to represent a physical LED strip and to provide a wrapper around the Neopixel library.

Params:
 - `numPixels: int`, the number of pixels on the physical strip
 - `pin: int`, the pin to which we connect the data pin of the physical strip
 - `colorOn`: RGB Tuple (eg (0,0,0) -> black, (255,255,255) -> white), the color the strip will take when it is on (full brightness)
 - `colorOff`: RGB Tuple, the color the strip will take when it is off (dark)
 - `colorBlink`: RGB Tuple, the color the strip will take when it is blinking
 - `stateMachine: int`, I don't know what the hell this is 😅


### `TurnSignal`

The `TurnSignal` class is meant to encapsulate everything that should toggle a turn signal on/off (button), and everything that needs to update when the signal is on/off (LED strips).

Params:
- `id: str`, used to identify the turn signal when registering `SignalTimer` listeners
- `buttonPin: int`, the pin to which we'll connect the ground pin of the button
- `frontStripPin: int`, the pin to which we'll connect the data pin of the front strip
- `backStripPin: int`, the pin to which we'll connect the data pin of the back strip
- `stateMachineFront: int`, ???
- `stateMachineBack: int`, ???

### `SignalTimer`

The `SignalTimer` singleton serves as a global timer that keeps track of what signals are on, and sends them unified data (ledOnIndex, brightness, animationPhase) on each timer tick.

**Public methods**
- `addOnTickCallback(callback)`: used to register a callback that will be executed on each timer interval
- `requestStartTimer(signalId)`: when called, we check if the timer is already active. We only set `self.isActive` to `True` if it is not already. We append the given `signalId` to `self.activeSignalIds`. Like this, the timer is only started if it is not running already.
- `requestStopTimer(signalId)`: when called, we remove the given `signalId` from `self.activeSignalIds`. If the length of `self.activeSignalIds` is 0, this means we just removed the last signal that was listening to events from the timer, and we can therefore stop the timer. Like this, we only stop the timer if no other signals are epexting events from it.

**Animation logic**

Animations are divided in to two phases:
- `swoosh`: the LED strip is progressively turned on pixel by pixel, with each pixel always being at full brightness
- `fadeOut`: the entire strip progressivle fades out

`SignalTimer` has counters to update the index of the next LED that should be turned on during the `swoosh` phase, and to update the desired brightness of LED strips during the `fadeOut` phase.

## Utils

### Gamma correction
The human eye does not perceive colors linearly from 0 to 255. Increases in the lower range appear more dramatic than increases in the higher range. This leads to issues such as colors not apearing quite right, and to brightness variations feeling either too intense or not intense enough. Read more about this on the [Adafruit site](https://learn.adafruit.com/led-tricks-gamma-correction/the-issue).

To solve this, we apply gamma correction. The file `gammaCorrection.py` exports two utilities that allow to gamma correct values from 0 to 255:
- `gammaCorrectSingleValue` to convert songle values
- `gammaCorrectRgb` to convert RGB tuples
