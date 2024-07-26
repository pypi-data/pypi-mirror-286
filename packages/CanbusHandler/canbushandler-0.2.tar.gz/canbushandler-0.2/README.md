# CanbusHandler
(for python)
With this canbus library, you can handle CAN bus data more easily.

<img src="https://github.com/user-attachments/assets/7e15bb34-002b-4576-933a-595057a284bc" width=30% >

i used 2-Channel Isolated CAN Expansion HAT for Raspberry Pi, Dual Chips Solution

in this project https://www.waveshare.com/2-ch-can-hat.htm
my rasberry pi is 4 model b.


## Installation
```bash
pip install CanbusHandler

```
#or
```bash
pip install git+https://github.com/jaakka/PythonCanbusHandler.git

```
#Remember start canbus
```
sudo ip link set can0 up type can bitrate 500000
sudo ifconfig can0 up

sudo ip link set can1 up type can bitrate 500000
sudo ifconfig can1 up

```
500000 is 500kbps, you need to find out the right speed for your car.

In my mercedes have two speeds
CanB is for radio, windows, and other amusement devices, speed is 83,3kbps
CanC is for motor and more important devices and speed is 500kbps (+ 5times faster)

Also remember to check that you don't have the end resistors in use, you probably won't need them if you're reading messages from the car

Usage
Here's a simple example of how to use the CanBusHandler library:

from CanbusHandler import Handler, Channel

# Initialize CAN bus on channel B
```
bus = Handler(Channel.CanB)
```
# Add variables to monitoring list
```
bus.AddCheckList(0x0016, 0, 8, "Battery")

bus.AddCheckList(0x0000, 3, 1, "Terminal50")

bus.AddCheckList(0x0000, 5, 1, "Terminal15")
```
# Start the CAN bus communication
```
bus.Begin()
```

# Send canbus message (never stop for example car light)
```
devicePid = 0x1

msg = [0x3,0x4,0x5,0x3]

times = -1 #send every second and never stop

busB.SendMessage(devicePid, msg, times) 
```
-1 means message sends every second and never stop

# Send canbus message
```
devicePid = 0x3

msg = [0x5,0x7,0x3,0x5,0x3,0x5,0x3,0x5]

times = 15 #send every second 15 times

busB.SendMessage(devicePid, msg, times) 
```
15 means message sends every second and ends after 15 messages.


Features
Send and receive CAN messages
Monitor specific variables on the CAN bus

CHECK tutorial.py

if you like canbus playing check out my car project,
I created custom carcomputer with rasberry pi and 3d printer.
https://www.instagram.com/project_yel_mb_e/
