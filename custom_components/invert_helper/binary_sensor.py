"""Binary sensor platform for Invert / Not-True Helper."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    ATTR_INVERTED,
    ATTR_MODE,
    ATTR_SOURCE_ENTITY,
    ATTR_SOURCE_STATE,
    ATTR_TARGET_VALUE,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_MODE,
    CONF_SOURCE_ENTITY,
    CONF_TARGET_VALUE,
    DEFAULT_NAME,
    DEVICE_CLASS_NONE,
    MODE_INVERT_BOOLEAN,
    MODE_NUMERIC_NOT_EQUAL,
    MODE_STATE_NOT_EQUAL,
    MODE_STATE_NOT_IN,
)

_LOGGER = logging.getLogger(__name__)

TRUTHY_STATES = {"on", "true", "1", "open", "locked", "home", "active", "problem"}
FALSY_STATES = {"off", "false", "0", "closed", "unlocked", "not_home", "inactive", "idle"}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Invert / Not-True binary sensor from config entry."""
    async_add_entities([InvertBinarySensor(entry)], True)


class InvertBinarySensor(BinarySensorEntity):
    """Representation of an Invert / Not-True Binary Sensor."""

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        config = {**entry.data, **entry.options}

        self._source_entity: str = config.get(CONF_SOURCE_ENTITY, "")
        self._mode: str = config.get(CONF_MODE, MODE_STATE_NOT_EQUAL)
        self._target_value: str = config.get(CONF_TARGET_VALUE, "")
        device_class = config.get(CONF_DEVICE_CLASS, DEVICE_CLASS_NONE)
        icon = config.get(CONF_ICON)

        self._attr_name = config.get(CONF_NAME, DEFAULT_NAME)
        self._attr_unique_id = f"{entry.entry_id}_invert"

        if device_class and device_class != DEVICE_CLASS_NONE:
            try:
                self._attr_device_class = BinarySensorDeviceClass(device_class)
            except ValueError:
                self._attr_device_class = None
        else:
            self._attr_device_class = None

        if icon:
            self._attr_icon = icon

        self._source_state_str: str | None = None
        self._attr_is_on: bool | None = None
        self._attr_available: bool = True

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        return {
            ATTR_SOURCE_ENTITY: self._source_entity,
            ATTR_SOURCE_STATE: self._source_state_str,
            ATTR_MODE: self._mode,
            ATTR_TARGET_VALUE: self._target_value,
            ATTR_INVERTED: self._attr_is_on,
        }

    async def async_added_to_hass(self) -> None:
        """Register state listener when added to hass."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._source_entity],
                self._async_source_state_changed,
            )
        )
        self._evaluate_source_state()

    @callback
    def _async_source_state_changed(self, event: Event) -> None:
        """Handle state change of source entity."""
        self._evaluate_source_state()
        self.async_write_ha_state()

    @callback
    def _evaluate_source_state(self) -> None:
        """Evaluate inverted / not-true logic from current source state."""
        source_state = self.hass.states.get(self._source_entity)

        if source_state is None or source_state.state in (
            STATE_UNAVAILABLE,
            STATE_UNKNOWN,
        ):
            self._attr_available = False
            self._attr_is_on = None
            self._source_state_str = None if source_state is None else source_state.state
            return

        self._attr_available = True
        raw_state = source_state.state
        self._source_state_str = raw_state
        state_clean = raw_state.strip().lower()

        if self._mode == MODE_STATE_NOT_EQUAL:
            target_clean = self._target_value.strip().lower()
            self._attr_is_on = state_clean != target_clean

        elif self._mode == MODE_NUMERIC_NOT_EQUAL:
            try:
                source_num = float(raw_state)
                target_num = float(self._target_value.strip())
                self._attr_is_on = abs(source_num - target_num) > 1e-6
            except (ValueError, TypeError):
                # Fallback to string inequality if non-numeric
                self._attr_is_on = raw_state.strip() != self._target_value.strip()

        elif self._mode == MODE_STATE_NOT_IN:
            target_list = [
                v.strip().lower()
                for v in self._target_value.split(",")
                if v.strip()
            ]
            self._attr_is_on = state_clean not in target_list

        elif self._mode == MODE_INVERT_BOOLEAN:
            if state_clean in TRUTHY_STATES:
                self._attr_is_on = False
            elif state_clean in FALSY_STATES:
                self._attr_is_on = True
            else:
                try:
                    num_val = float(raw_state)
                    self._attr_is_on = num_val == 0
                except (ValueError, TypeError):
                    self._attr_is_on = not bool(raw_state)

        else:
            # Default fallback to state inequality
            self._attr_is_on = state_clean != self._target_value.strip().lower()

