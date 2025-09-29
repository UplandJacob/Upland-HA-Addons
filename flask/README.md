# Flask Server

![Addon Stage](https://img.shields.io/badge/Addon%20stage-ready-green.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-np-red.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-no-red.svg)

## About

Flask is a Python webserver primarily used for testing web applications with APIs, but is an great server for any sort of simple site or API you need.

## Install

<!-- markdownlint-disable MD036 -->
**Add repository**
<!-- markdownlint-enable MD036 -->

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: <https://github.com/UplandJacob/Upland-HA-Addons>

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_flask)

## Setup

1. Install the addon and start it to generate the environment.
2. Any Python libraries you need, you can add to 'requirements.txt' in 'addon_configs/d78ad65c_flask'. (To get the version, run `pip install --dry-run PACKAGE` [requires `--break-system-packages` flag inside addon] and look at the first version on the 'Would install...' line.) Restart the addon to let them automatically download.
3. You may then edit the app using the VS Code Server addon, SFTP+VSCode on another computer, or by opening <https://vscode.dev/tunnel/TUNNEL_NAME/addon_configs/d78ad65c_flask/flask> with my [VSCode Tunnel addon](/vscode-tunnel/).
4. While `debug=True`, anytime `main.py` is saved, Flask will detect it and automatically restart the server.
