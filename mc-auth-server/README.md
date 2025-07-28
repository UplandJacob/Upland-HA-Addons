# MC auth server

![Addon Stage](https://img.shields.io/badge/Addon%20stage-ready-green.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-no-red.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-no-red.svg)

## About

Minecraft Leaf (Paper fork) auth server for proxy setups that use AuthMe.

## Install

**Add repository**

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: https://github.com/UplandJacob/Upland-HA-Addons

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_mc-auth-server)

## Setup

1. Install the addon (see above).
2. Configure proxy forwarding mode and any other settings you want in the 'Configuration' tab.
3. Use something like Filebrowser to open 'addon_configs/d78ad65c_mc-auth-server/plugins.yaml' and use the overrides to enable any optional plugins you want for your proxy setup.
