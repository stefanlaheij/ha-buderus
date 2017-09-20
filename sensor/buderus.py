"""
Platform to read a Buderus KM200 unit.
"""
import logging

from custom_components.buderus import (
    DOMAIN, BuderusBridge)
from homeassistant.const import (
    CONF_RESOURCES, TEMP_CELSIUS, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['buderus']

SENSOR_TYPES = {}

"""
https://github.com/smarthomeNG/plugins/tree/master/buderus

ATTR_INFO_DATETIME
ATTR_INFO_FIRMWARE
ATTR_INFO_HARDWARE
ATTR_INFO_BRAND
ATTR_INFO_HEALTH
ATTR_OUTSIDE_TEMPERATURE
ATTR_SUPPLY_TEMPERATURE
ATTR_HOTWATER_TEMPERATURE
ATTR_BOILER_FLAME
ATTR_BOILER_STARTS
ATTR_HEATING_CURRENT_ROOMSETPOINT
ATTR_HEATING_MANUAL_ROOMSETPOINT
ATTR_HEATING_TEMP_SETPOINT
ATTR_HEATING_TEMP_ECO
ATTR_HEATING_TEMP_COMFORT
ATTR_HEATING_ACTIVEPROGRAM
ATTR_HEATING_MODE
         'hotwater_current_waterflow': [
            'Hotwater Waterflow',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/dhwCircuits/dhw1/waterFlow'
        ],
         'hotwater_current_workingtime': [
            'Hotwater Workingtime',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/dhwCircuits/dhw1/workingTime'
        ],
"""

def setup_platform(hass, config, add_devices, discovery_info=None):
    global SENSOR_TYPES
    SENSOR_TYPES = {
        'outside_temperature': [
            'Outside Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/system/sensors/temperatures/outdoor_t1'
        ],
         'hotwater_current_temperature': [
            'Hotwater Temperature',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/dhwCircuits/dhw1/actualTemp'
        ],
         'hotwater_current_setpoint': [
            'Hotwater Current Setpoint',
            TEMP_CELSIUS,
            'mdi:thermometer',
            '/dhwCircuits/dhw1/currentSetpoint'
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
                hass,
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

    def __init__(self, hass, name, bridge: BuderusBridge, sensor_type, unit, icon, km_id):
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
        
