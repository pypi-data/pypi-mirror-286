from __future__ import annotations

from dataclasses import dataclass
import enum
from typing import TypedDict

class CCLSensor:
    """Class that represents a CCLSensor object in the aioCCL API."""
    
    def __init__(self, key: str):
        """Initialize a CCL sensor."""
        self.value: None | str | int | float
    
        if key in CCL_SENSORS.keys():
            self._key = key
    
    @property
    def key(self):
        return self._key
    
    @property
    def name(self):
        return CCL_SENSORS[self._key].name
    
    @property
    def sensor_type(self):
        return CCL_SENSORS[self._key].sensor_type

@dataclass
class CCLSensorPreset:
    name: str
    sensor_type: str
    
class CCLSensorTypes(enum.Enum):
    PRESSURE = 1
    TEMPERATURE = 2
    HUMIDITY = 3
    WIND_DIRECITON = 4
    WIND_SPEED = 5
    
CCL_SENSORS: dict[str, CCLSensorPreset] = {
    'rbar': CCLSensorPreset('Air Pressure', CCLSensorTypes.PRESSURE),
    'intem': CCLSensorPreset('Indoor Temperature', CCLSensorTypes.TEMPERATURE),
    'inhum': CCLSensorPreset('Indoor Humidity', CCLSensorTypes.HUMIDITY),
    't1tem': CCLSensorPreset('Outdoor Temperature', CCLSensorTypes.TEMPERATURE),
    't1hum': CCLSensorPreset('Outdoor Humidity', CCLSensorTypes.HUMIDITY),
    't1wdir': CCLSensorPreset('Outdoor Wind Direction', CCLSensorTypes.WIND_DIRECITON),
    't1ws': CCLSensorPreset('Outdoor Wind Speed', CCLSensorTypes.WIND_SPEED),
}
