"""Config flow for Invert / Not-True Helper integration."""
from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_SOURCE_ENTITY,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    DEFAULT_NAME,
    DEVICE_CLASS_NONE,
    SUPPORTED_DEVICE_CLASSES,
)

_LOGGER = logging.getLogger(__name__)


class InvertHelperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Invert / Not-True Helper."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            source_entity = user_input.get(CONF_SOURCE_ENTITY)
            name = user_input.get(CONF_NAME, "").strip()

            if not source_entity:
                errors[CONF_SOURCE_ENTITY] = "empty_source"
            if not name:
                errors[CONF_NAME] = "empty_name"

            if not errors:
                return self.async_create_entry(
                    title=name,
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
                ),
                vol.Required(CONF_SOURCE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig()
                ),
                vol.Optional(
                    CONF_DEVICE_CLASS, default=DEVICE_CLASS_NONE
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": dc, "label": dc}
                            for dc in SUPPORTED_DEVICE_CLASSES
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="device_class",
                    )
                ),
                vol.Optional(CONF_ICON): selector.IconSelector(),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> InvertHelperOptionsFlow:
        """Get the options flow for this handler."""
        return InvertHelperOptionsFlow(config_entry)


class InvertHelperOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Invert / Not-True Helper."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        current_data = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            source_entity = user_input.get(CONF_SOURCE_ENTITY)
            if not source_entity:
                errors[CONF_SOURCE_ENTITY] = "empty_source"

            if not errors:
                return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SOURCE_ENTITY,
                    default=current_data.get(CONF_SOURCE_ENTITY, ""),
                ): selector.EntitySelector(selector.EntitySelectorConfig()),
                vol.Optional(
                    CONF_DEVICE_CLASS,
                    default=current_data.get(CONF_DEVICE_CLASS, DEVICE_CLASS_NONE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": dc, "label": dc}
                            for dc in SUPPORTED_DEVICE_CLASSES
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="device_class",
                    )
                ),
                vol.Optional(
                    CONF_ICON,
                    description={"suggested_value": current_data.get(CONF_ICON, "")},
                ): selector.IconSelector(),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )
