"""Constants for the Invert / Not-True Helper integration."""
from __future__ import annotations

DOMAIN = "invert_helper"

CONF_SOURCE_ENTITY = "source_entity"
CONF_DEVICE_CLASS = "device_class"
CONF_ICON = "icon"

DEFAULT_NAME = "Inverted Sensor"

ATTR_SOURCE_ENTITY = "source_entity"
ATTR_SOURCE_STATE = "source_state"
ATTR_INVERTED = "inverted"

DEVICE_CLASS_NONE = "none"

SUPPORTED_DEVICE_CLASSES = [
    DEVICE_CLASS_NONE,
    "battery",
    "battery_charging",
    "carbon_monoxide",
    "cold",
    "connectivity",
    "door",
    "garage_door",
    "gas",
    "heat",
    "light",
    "lock",
    "moisture",
    "motion",
    "moving",
    "occupancy",
    "opening",
    "plug",
    "power",
    "presence",
    "problem",
    "running",
    "safety",
    "smoke",
    "sound",
    "tamper",
    "update",
    "vibration",
    "window",
]
