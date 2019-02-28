"""
Platform to read a Buderus KM200 unit.
"""
import logging

from custom_components.buderus import (
    DOMAIN, BuderusBridge)
from homeassistant.const import (
    CONF_RESOURCES, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {}

def setup_platform(hass, config, add_devices, discovery_info=None):

    global SENSOR_TYPES
    SENSOR_TYPES = {
        'return_temperature': [
            'Return Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/system/sensors/temperatures/return'
        ],
        'heatsource_modulation': [
            'Modulation',
            '%',
            'mdi:percent',
            '/system/heatSources/hs1/actualModulation'
        ],
        'outside_temperature': [
            'Outside Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/system/sensors/temperatures/outdoor_t1'
        ],
        'supply_temperature': [
            'Supply Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/system/sensors/temperatures/supply_t1'
        ],
        'hotwater_temperature': [
            'Hotwater Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/system/sensors/temperatures/hotWater_t2'
        ],
         'room_temperature': [
            'Room Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/heatingCircuits/hc1/roomtemperature'
        ],
         'heating_current_roomsetpoint': [
            'Heating Room Setpoint',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/heatingCircuits/hc1/currentRoomSetpoint'
        ],
         'heating_manual_roomsetpoint': [
            'Heating Manual Room Setpoint',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/heatingCircuits/hc1/manualRoomSetpoint'
        ],
         'heating_temp_roomsetpoint': [
            'Heating Temporary Room Setpoint',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/heatingCircuits/hc1/temporaryRoomSetpoint'
        ],
         'heating_templevel_eco': [
            'Heating Eco Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/heatingCircuits/hc1/temperatureLevels/eco'
        ],
         'heating_templevel_comfort': [
            'Heating Comfort Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/heatingCircuits/hc1/temperatureLevels/comfort2'
        ],
         'heating_activeprogram': [
            'Heating Active Program',
            None,
            None,
            '/heatingCircuits/hc1/activeSwitchProgram'
        ],
         'heating_operation_mode': [
            'Heating Operation Mode',
            None,
            None,
            '/heatingCircuits/hc1/operationMode'
        ],
        'boiler_flame': [
            'Boiler Flame',
            None,
            None,
            '/heatSources/flameStatus'
        ],
         'boiler_starts': [
            'Boiler Starts',
            None,
            None,
            '/heatSources/hs1/numberOfStarts'
        ],
         'hotwater_current_temperature': [
            'Hotwater Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/dhwCircuits/dhw1/actualTemp'
        ],
         'hotwater_current_setpoint': [
            'Hotwater Setpoint',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/dhwCircuits/dhw1/currentSetpoint'
        ],
        'hotwater_current_waterflow': [
            'Hotwater Waterflow',
            None,
            None,
            '/dhwCircuits/dhw1/waterFlow'
        ],
         'hotwater_current_workingtime': [
            'Hotwater Workingtime',
            None,
            None,
            '/dhwCircuits/dhw1/workingTime'
        ],
         'pump_modulation': [
            'Pump Modulation',
            None,
            None,
            '/system/appliance/CHpumpModulation'
        ],
         'system_pressure': [
            'System Pressure',
            None,
            None,
            '/system/appliance/systemPressure'
        ],
    }

    bridge = hass.data[DOMAIN]

    sensors = []
    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()

        if sensor_type not in SENSOR_TYPES:
            _LOGGER.warning("Sensor type: %s is not a valid sensor.",
                            sensor_type)
            continue

        sensors.append(
            BuderusSensor(
                name="%s %s" % (bridge.name, SENSOR_TYPES[sensor_type][0]),
                bridge=bridge,
                sensor_type=sensor_type,
                unit=SENSOR_TYPES[sensor_type][1],
                icon=SENSOR_TYPES[sensor_type][2],
                km_id=SENSOR_TYPES[sensor_type][3]
            )
        )

    add_devices(sensors, True)


class BuderusSensor(Entity):
    """Representation of a Buderus sensor."""

    def __init__(self, name, bridge: BuderusBridge, sensor_type, unit, icon, km_id):
        """Initialize the Buderus sensor."""
        self._name = name
        self._bridge = bridge
        self._sensor_type = sensor_type
        self._unit = unit
        self._icon = icon
        self._km_id = km_id
        self._state = None

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit
        
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant."""
        _LOGGER.info("Buderus fetching data...")
        plain = self._bridge._get_data(self._km_id)
        if plain is not None:
            data = self._bridge._get_json(plain)
            self._state = self._bridge._get_value(data)
        _LOGGER.info("Buderus fetching data done.")
        
