"""Mapping to create a CCL Device copy."""
from __future__ import annotations

import logging
import time
from typing import Callable

from .sensor import CCLSensor

_LOGGER = logging.getLogger(__name__)

CCL_DEVICE_INFO_TYPES = ("serial_no", "mac_address", "model", "version")

class CCLDevice:
    def __init__(self, passkey: str):
        """Initialize a CCL device."""
        _LOGGER.debug('Initializing CCL Device: %s', self)
        self._passkey = passkey
        
        self.serial_no: str | None
        self.mac_address: str | None
        self.model: str | None
        self.version: str | None

        self.last_updated_time: float = -10.0 # Offset
        
        self.sensors: dict[str, CCLSensor] | None = {}

        self._new_sensors: list[CCLSensor] | None = []
        
        self._update_callbacks = set() 
        self._new_sensor_callbacks = set()
    
    @property
    def passkey(self) -> str:
        return self._passkey
    
    @property
    def device_id(self) -> str:
        return self.mac_address.replace(":", "").lower()[-6:]
    
    def update_info(self, info: dict[str, None | str]) -> None:
        """Add or update device info."""
        self.serial_no = info.get('serial_no')
        self.mac_address = info.get('mac_address')
        self.model = info.get('model')
        self.version = info.get('version')
    
    def update_sensors(self, sensors: dict[str, None | str | int | float]) -> None:
        """Add or update all sensor values."""
        for sensor, value in sensors.items():
            if not self.sensors.get(sensor):
                self.sensors[sensor] = CCLSensor(sensor)
                self._new_sensors.append(self.sensors[sensor])
            self.sensors[sensor].value = value
        self._publish_new_sensors()
        self._publish_updates()
        self.last_updated_time = time.monotonic()
        _LOGGER.debug("Sensors Updated: %s", self.last_updated_time)

    def register_update_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._update_callbacks.add(callback)

    def remove_update_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._update_callbacks.discard(callback)

    def _publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        try:
            for callback in self._update_callbacks:
                callback()
        except Exception as err:
            _LOGGER.warning("Error while publishing sensor updates: %s", err)

    def register_new_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._new_sensor_callbacks.add(callback)

    def remove_new_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._new_sensor_callbacks.discard(callback)

    def _publish_new_sensors(self) -> None:
        """Schedule call all registered callbacks."""
        try:
            for sensor in self._new_sensors:
                _LOGGER.debug("Publishing new sensor: %s", sensor)
                _LOGGER.debug("Sensors remaining: %s", self._new_sensors)
                for callback in self._new_sensor_callbacks:
                    callback(sensor)
            self._new_sensors.clear()
        except Exception as err:
            _LOGGER.warning("Error while publishing new sensors: %s", err)
