# ha-buderus
Home Assistant component for communicating with Buderus and Nefit IP modules

## Installation

1. Create ```custom_components/``` in your homeassistant config directory and copy the file ```buderus.py``` into it.
2. Create ```custom_components/sensor/``` in your homeassistant config directory and copy the file ```sensor/buderus.py``` into it.

## Password
Create a password at https://ssl-account.com/km200.andreashahn.info/ by entering your device password (from sticker or menu) and your personal password.

## Configuration


```
buderus:
  host: <IP_ADDRESS>
  password: <GENERATED 64 CHARACTER KEY>
  name: <OPTIONAL CUSTOM DEVICENAME, INSTEAD OF BUDERUS>

sensor:
  - platform: buderus
    resources:
      - outside_temperature
      - hotwater_current_temperature
      - hotwater_current_setpoint
```
