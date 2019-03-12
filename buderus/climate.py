"""
Platform to control a Buderus KM200 unit.
"""
import logging

from homeassistant.const import (TEMP_CELSIUS, ATTR_TEMPERATURE)
from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import SUPPORT_TARGET_TEMPERATURE
from custom_components.buderus import (DOMAIN, BuderusBridge)

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE)

def setup_platform(hass, config, add_devices, discovery_info=None):
    bridge = hass.data[DOMAIN]

    thermostat = BuderusThermostat(
        name="%s %s" % (bridge.name, 'Thermostat'),
        bridge=bridge
    )

    add_devices([thermostat], True)

class BuderusThermostat(ClimateDevice):
    """Representation of a Buderus thermostat."""

    def __init__(self, name, bridge):
        """Initialize the thermostat."""
        self.logger = logging.getLogger(__name__)
        self._name = name
        self._bridge = bridge
        self._current_temperature = None
        self._target_temperature = None

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        return self._name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self._bridge._submit_data('/heatingCircuits/hc1/temperatureRoomSetpoint', temperature)
        self._target_temperature = temperature

    def update(self):
        """Get the latest data."""
        plain = self._bridge._get_data('/heatingCircuits/hc1/roomtemperature')
        if plain is not None:
            data = self._bridge._get_json(plain)
            self._current_temperature = self._bridge._get_value(data)
        
        if self._target_temperature is None:
            plain = self._bridge._get_data('/heatingCircuits/hc1/temperatureRoomSetpoint')
            if plain is not None:
                data = self._bridge._get_json(plain)
                self._target_temperature = self._bridge._get_value(data)