"""Constants for the Invert / Not-True Helper integration."""
from __future__ import annotations

DOMAIN = "invert_helper"

CONF_SOURCE_ENTITY = "source_entity"
CONF_MODE = "mode"
CONF_TARGET_VALUE = "target_value"
CONF_DEVICE_CLASS = "device_class"
CONF_ICON = "icon"

DEFAULT_NAME = "Not-True Helper"

MODE_STATE_NOT_EQUAL = "state_not_equal"
MODE_NUMERIC_NOT_EQUAL = "numeric_not_equal"
MODE_STATE_NOT_IN = "state_not_in"
MODE_INVERT_BOOLEAN = "invert_boolean"

MODES = [
    MODE_STATE_NOT_EQUAL,
    MODE_NUMERIC_NOT_EQUAL,
    MODE_STATE_NOT_IN,
    MODE_INVERT_BOOLEAN,
]

ATTR_SOURCE_ENTITY = "source_entity"
ATTR_SOURCE_STATE = "source_state"
ATTR_MODE = "mode"
ATTR_TARGET_VALUE = "target_value"
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

