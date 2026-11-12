# 🔄 Invert / Not-True Helper for Home Assistant

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=adromir&repository=ha-invert-helper&category=integration)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/adromir/ha-invert-helper?style=for-the-badge&color=blue)](https://github.com/adromir/ha-invert-helper/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/adromir/ha-invert-helper)

A lightweight, native **Home Assistant Helper Integration** that solves a major pain point in the Home Assistant Visual Automation Editor: testing for negative or inverted states without writing cumbersome Jinja2 YAML templates (`{{ not is_state(...) }}`).

The Invert Helper exposes a clean `binary_sensor` entity that automatically mirrors the **inverted** state of any target entity (`off` ➔ `on`, `on` ➔ `off`).

---

## 🎯 The Problem This Solves

In Home Assistant's visual automation editor, triggers and conditions frequently only test for positive truthiness. If you want an automation to trigger when a contact sensor is **NOT** closed, when a person is **NOT** home, or when a boolean switch is **NOT** active, you usually have to write manual Jinja2 template conditions:

```yaml
# ❌ The tedious template workaround (breaks visual editor flow):
condition: template
value_template: "{{ not is_state('binary_sensor.fenster_schlafzimmer', 'off') }}"
```

With the **Invert / Not-True Helper**, you simply create a helper in the UI and use it directly in the Visual Editor as a standard state trigger or condition:

```yaml
# ✔️ Clean, native visual editor condition:
condition: state
entity_id: binary_sensor.fenster_schlafzimmer_invertiert
state: "on"
```

---

## ✨ Key Features & Advantages

- 🎛️ **Native Helper Integration (`integration_type: helper`)**: Directly discoverable in Home Assistant under **Settings > Devices & Services > Helpers > Create Helper**.
- ⚙️ **Modern UI Config Flow & Options Flow**: Configure and reconfigure target entities, custom icons, and device classes entirely in the user interface without YAML restarts.
- 🔄 **Universal Inversion Engine**:
  - Handles all standard ON states (`on`, `open`, `locked`, `home`, `active`, `true`, `1`, `problem`) ➔ inverts to `off`.
  - Handles all standard OFF states (`off`, `closed`, `unlocked`, `not_home`, `inactive`, `false`, `0`, `idle`) ➔ inverts to `on`.
  - Handles numeric sensors (`0` inverts to `on`, positive values invert to `off`).
  - Gracefully respects `unavailable` and `unknown` availability states.
- 📐 **Configurable Device Classes**: Choose any binary sensor device class (e.g. `opening`, `window`, `door`, `motion`, `presence`, `problem`, `occupancy`) to get native localized labels and icons in Lovelace.
- 🌐 **Fully Bilingual**: German and English UI config flow, options dialog, and error messages.

---

## 📦 Installation via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=adromir&repository=ha-invert-helper&category=integration)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. In Home Assistant, open **HACS** > **Integrations**.
3. Click the three dots (top right corner) and select **Custom repositories**.
4. Enter the repository URL:
   ```
   https://github.com/adromir/ha-invert-helper
   ```
5. Select category: **Integration**.
6. Click **Add**, find **Invert / Not-True Helper**, and click **Download**.
7. Restart Home Assistant.

---

## 🚀 Creating an Invert Helper in Home Assistant

1. Go to **Settings > Devices & Services > Helpers**.
2. Click **+ Create Helper** and select **Invert / Not-True Helper**.
3. Fill in:
   - **Name**: e.g. `Schlafzimmerfenster nicht geschlossen` or `Niemand Zuhause`.
   - **Target Entity**: Pick any binary sensor, switch, light, or boolean entity from the dropdown.
   - **Device Class** *(optional)*: e.g. `window`, `door`, `presence`, `opening`.
   - **Icon** *(optional)*: Custom MDI icon (e.g. `mdi:window-open-variant`).
4. Click **Submit**.

---

## 👤 Author

Developed with care by **Adromir**  
Website: [https://github.com/adromir](https://github.com/adromir)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
