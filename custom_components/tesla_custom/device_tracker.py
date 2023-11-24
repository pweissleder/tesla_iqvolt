"""Support for Tesla device tracker."""
import logging

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant

from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


# TODO: Stys  as it might be interesting(otherwise delete) Check back with tobi

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla device trackers by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarLocation(car, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarLocation(TeslaCarEntity, TrackerEntity):
    """Representation of a Tesla car location device tracker."""

    type = "location tracker"

    @property
    def source_type(self):
        """Return device tracker source type."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return longitude."""
        return self._car.longitude

    @property
    def latitude(self):
        """Return latitude."""
        return self._car.latitude

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "heading": self._car.heading,
            "speed": self._car.speed,
        }

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
