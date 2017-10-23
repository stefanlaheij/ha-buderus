# ha-buderus
Home Assistant component for communicating with Buderus KM200/KM50 and Nefit IP modules used in Enviline (Tower) heatpump systems.

## Installation

1. Create ```custom_components/``` in your homeassistant config directory and copy the file ```buderus.py``` into it.
2. Create ```custom_components/sensor/``` in your homeassistant config directory and copy the file ```sensor/buderus.py``` into it.

## Password
Create a password at https://ssl-account.com/km200.andreashahn.info/ by entering your device password (from sticker or menu) and your personal password.

## Issues
**FIXED:** The thermostat does not yet succesfully update the setpoint. Help on this is appreciated.

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
      - supply_temperature
      - return_temperature
      - room_temperature
      - hotwater_temperature
      - heating_current_roomsetpoint
      - heating_manual_roomsetpoint
      - heating_temp_roomsetpoint
      - hotwater_current_temperature
      - hotwater_current_setpoint
      - hotwater_current_workingtime
      - hotwater_current_waterflow
      - heatsource_modulation
      - heating_templevel_eco
      - heating_templevel_comfort
      - heating_activeprogram
      - heating_operation_mode
      - boiler_flame
      - boiler_starts
      - pump_modulation
      - system_pressure
      
```

## Credits
Special thanks to Raoul Thill for sharing his Python code to communicate with the module: https://github.com/rthill/buderus
