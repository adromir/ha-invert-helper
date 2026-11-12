# 🔄 Invert / Not-True Helper for Home Assistant

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=adromir&repository=ha-invert-helper&category=integration)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/adromir/ha-invert-helper?style=for-the-badge&color=blue)](https://github.com/adromir/ha-invert-helper/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/adromir/ha-invert-helper)

A lightweight, native **Home Assistant Helper Integration** that solves one of the biggest limitations of the Home Assistant Visual Automation Editor: **testing for negative conditions without writing Jinja2 YAML templates**.

While Home Assistant's visual automation editor makes it easy to check if a binary sensor is `on` or `off`, it offers **no direct way to check if a multi-state entity is NOT a specific state** (e.g., *Alarm is NOT disarmed*, *Person is NOT home*, *Media Player is NOT idle*) or if a **numeric sensor is NOT a specific value** (e.g., *Power is NOT 0 W*).

The **Invert / Not-True Helper** exposes a clean `binary_sensor` that turns **ON** whenever your negative condition is met.

---

## 🎯 Why You Need This

### The Problem in Home Assistant Today
In the visual automation editor:
- **Binary sensors**: You can choose `if true` or `if false`.
- **String & Multi-state sensors**: You can only test for positive equality (`state == 'value'`). There is no negative check (`state != 'value'`).
- **Numeric sensors**: You only have *Above* and *Below*, but no exact *Number is NOT equal to X*.

To achieve a negative check today, users are forced into manual Jinja2 template conditions:
```yaml
# ❌ Cumbersome template condition (breaks the visual flow):
condition: template
value_template: "{{ states('alarm_control_panel.alarmo') != 'disarmed' }}"
```

### The Solution
Create an **Invert / Not-True Helper** via the UI, and use it directly in any visual automation trigger or condition:
```yaml
# ✔️ Clean, standard visual editor state condition:
condition: state
entity_id: binary_sensor.alarm_not_disarmed
state: "on"
```

---

## ✨ Features & Comparison Modes

| Mode | Visual Editor Description | Example Use Case | Helper Output (`is_on`) |
| :--- | :--- | :--- | :--- |
| **`State is NOT equal`** | `state != target_value` | `alarm_control_panel.alarmo != 'disarmed'` | **ON** when armed (home/away/night) |
| **`Number is NOT equal`** | `num_val != target_value` | `sensor.washing_machine_power != 0` | **ON** whenever appliance is drawing power |
| **`State is NOT in list`** | `state not in [a, b, c]` | `person.andreas not in ('home', 'work')` | **ON** when traveling or in transit |
| **`Invert Boolean`** | Inverts any binary state | Inverting an active contact or motion sensor | **ON** when target is `off` / `closed` |

- 🎛️ **Native Helper Integration (`integration_type: helper`)**: Directly discoverable in Home Assistant under **Settings > Devices & Services > Helpers > Create Helper > Invert / Not-True Helper**.
- ⚙️ **100% UI Configured**: Full Config Flow and Options Flow. Change target entity, comparison mode, target values, device class, or icon on the fly without YAML restarts.
- ⚡ **Real-Time Reactive**: Listens directly to Home Assistant core state events without polling overhead.
- 🌐 **Bilingual Support**: Fully localized in English and German.
- 🏷️ **Diagnostic Attributes**: Exposes `source_entity`, `source_state`, `mode`, and `target_value` right in developer tools.

---

## 📦 Installation

### Method 1: HACS (Recommended)

1. Click the button below to add this repository directly to HACS:

   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=adromir&repository=ha-invert-helper&category=integration)

2. Or manually in HACS:
   - Go to **HACS** > **Integrations** > **Three dots menu (top right)** > **Custom repositories**.
   - URL: `https://github.com/adromir/ha-invert-helper`
   - Type: `Integration`
   - Click **Add**, then find **Invert / Not-True Helper** and click **Download**.
3. **Restart Home Assistant**.

### Method 2: Manual Installation
1. Copy the `custom_components/invert_helper` directory into your Home Assistant `<config>/custom_components/` folder.
2. Restart Home Assistant.

---

## 🚀 How to Use

1. In Home Assistant, navigate to **Settings** > **Devices & Services** > **Helpers**.
2. Click **Create Helper** (bottom right) and select **Invert / Not-True Helper**.
3. Configure your helper:
   - **Name**: e.g., `Waschmaschine aktiv` or `Alarmanlage aktiv`
   - **Target Entity**: e.g., `sensor.washer_power` or `alarm_control_panel.alarmo`
   - **Comparison Mode**:
     - `State is NOT equal to [Value]`
     - `Number is NOT equal to [Value]`
     - `State is NOT in list [Comma-separated]`
     - `Invert Boolean / Binary State`
   - **Target Value(s)**: e.g., `0`, `disarmed`, or `home, work`
   - **Device Class** & **Icon** (optional).
4. Click **Submit**. Your new binary sensor is immediately ready to be used across all your automations, scripts, and dashboards!

---

## 🛠️ Reconfiguration

Need to adjust your target values or comparison mode later?
Simply click on the helper entity in **Settings > Devices & Services > Helpers**, click the gear icon (Settings), and select **Configure**.

---

## 📄 Disclaimer

This is a custom community integration and is not officially affiliated with or endorsed by Nabu Casa or Home Assistant.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).

**Author**: [Adromir](https://github.com/adromir)  
Website: [https://github.com/adromir](https://github.com/adromir)
