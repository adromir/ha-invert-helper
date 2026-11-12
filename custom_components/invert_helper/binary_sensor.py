"""Binary sensor platform for Invert / Not-True Helper integration."""
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
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    ATTR_INVERTED,
    ATTR_SOURCE_ENTITY,
    ATTR_SOURCE_STATE,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_SOURCE_ENTITY,
    DEVICE_CLASS_NONE,
)

_LOGGER = logging.getLogger(__name__)

STATE_ON_SET = {
    STATE_ON,
    "open",
    "locked",
    "home",
    "active",
    "true",
    "yes",
    "1",
    "problem",
    "detected",
    "unsafe",
}

STATE_OFF_SET = {
    STATE_OFF,
    "closed",
    "unlocked",
    "not_home",
    "inactive",
    "false",
    "no",
    "0",
    "ok",
    "idle",
    "clear",
    "safe",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Invert / Not-True Helper binary sensor."""
    async_add_entities([InvertHelperBinarySensor(entry)], True)


class InvertHelperBinarySensor(BinarySensorEntity):
    """Binary sensor representing an inverted source entity state."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._entry_id = entry.entry_id

        config = {**entry.data, **entry.options}
        self._source_entity: str = config[CONF_SOURCE_ENTITY]
        self._custom_icon: str | None = config.get(CONF_ICON) or None
        self._configured_device_class: str = config.get(
            CONF_DEVICE_CLASS, DEVICE_CLASS_NONE
        )

        name = config.get(CONF_NAME) or entry.title
        self._attr_name = name
        self._attr_unique_id = f"{self._entry_id}_invert_helper"

        # Apply device class if configured
        if (
            self._configured_device_class
            and self._configured_device_class != DEVICE_CLASS_NONE
        ):
            try:
                self._attr_device_class = BinarySensorDeviceClass(
                    self._configured_device_class
                )
            except ValueError:
                self._attr_device_class = None
        else:
            self._attr_device_class = None

        if self._custom_icon:
            self._attr_icon = self._custom_icon

        self._attr_is_on: bool | None = None
        self._attr_available: bool = True
        self._source_state_val: str | None = None

    @property
    def icon(self) -> str | None:
        """Return custom icon or default."""
        if self._custom_icon:
            return self._custom_icon
        return super().icon

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_SOURCE_ENTITY: self._source_entity,
            ATTR_SOURCE_STATE: self._source_state_val,
            ATTR_INVERTED: True,
        }

    async def async_added_to_hass(self) -> None:
        """Register listeners and evaluate state on startup."""
        await super().async_added_to_hass()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._source_entity],
                self._async_source_state_changed,
            )
        )

        # Initial evaluation
        self._evaluate_source_state()

    @callback
    def _async_source_state_changed(self, event: Event) -> None:
        """Handle source entity state changes."""
        self._evaluate_source_state()
        self.async_write_ha_state()

    def _evaluate_source_state(self) -> None:
        """Evaluate and invert source entity state."""
        source_state = self.hass.states.get(self._source_entity)

        if source_state is None:
            self._attr_available = False
            self._attr_is_on = None
            self._source_state_val = None
            return

        state_str = source_state.state

        if state_str in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            self._attr_available = False
            self._attr_is_on = None
            self._source_state_val = state_str
            return

        self._attr_available = True
        self._source_state_val = state_str
        clean_state = state_str.lower().strip()

        # Inversion logic:
        # If source is in ON set -> Invert to False
        # If source is in OFF set -> Invert to True
        if clean_state in STATE_ON_SET:
            self._attr_is_on = False
        elif clean_state in STATE_OFF_SET:
            self._attr_is_on = True
        else:
            # Numeric evaluation fallback: 0 is False (inverted -> True), >0 is True (inverted -> False)
            try:
                numeric_val = float(clean_state)
                self._attr_is_on = numeric_val == 0
            except (ValueError, TypeError):
                # Generic fallback: truthy non-empty string inverts to False
                self._attr_is_on = False
