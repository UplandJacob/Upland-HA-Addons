# Minecraft All-Platform Velocity Proxy

![Addon Stage](https://img.shields.io/badge/Addon%20stage-stable-green.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-no-red.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-deprecated-orange.svg)

## About

Run a proxy for a Minecraft Paper server to allow java, bedrock, and Eaglercraft(unofficial web browser) clients to join.

<!-- markdownlint-disable MD026 -->
### New in 2.0.0!!

- Scripts written in python
- Updated to EaglerXServer (new config files)
- Updated Velocity (Now that EaglerXServer supports it)
- Auto download Floodgate database drivers
- `plugins.yaml` allows you to define any plugin to be automatically downloaded and update any plugins packaged with the addon
- Any custom files for the proxy (the old version only supported certain folders)
- Updated config in the UI - Trimmed out some advanced options; you can still change them in their respective config files
- Automatically set the Server Name, Max Players, and MOTD in all 3 places: Velocity, EaglerXServer, and Geyser (with automatically converting MOTD from MiniMessage)
- Better startup logging (with a Log Level option as well)

**The [beta version](/mc-all-platform-velocity-beta) will now be for small updates**

## Install

<!-- markdownlint-disable MD036 -->
**Add repository**
<!-- markdownlint-enable MD036 -->

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: <https://github.com/UplandJacob/Upland-HA-Addons>

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_mc-all-platform-velocity)

## Setup

No idea yet
