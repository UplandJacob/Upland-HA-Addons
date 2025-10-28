<!-- markdownlint-disable MD041 -->
[![Build Status](https://github.com/UplandJacob/Upland-HA-Addons/actions/workflows/builder.yaml/badge.svg)](https://github.com/UplandJacob/Upland-HA-Addons/actions/workflows/builder.yaml)
[![Hadolint Status](https://github.com/UplandJacob/Upland-HA-Addons/actions/workflows/hadolint.yaml/badge.svg)](https://github.com/UplandJacob/Upland-HA-Addons/actions/workflows/hadolint.yaml)

# Upland-HA-Addons

A repository for all my Home Assistant addons. Since I host a Minecraft server, many of these are related to hosting one.

## Install

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: <https://github.com/UplandJacob/Upland-HA-Addons>

## Functional Addons

### [Flask Server](/vscode-tunnel)

Flask is a Python webserver primarily used for testing web applications with APIs, but is an great server for any sort of simple site or API you need.

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_flask)

### [VSCode Tunnel](/vscode-tunnel)

The VSCode Tunnel addon runs a fully featured VSCode tunnel server that can be accessed from [vscode.dev](https://vscode.dev) and supports all extentions (at least all I have tested with a bit of work).

`git`, `ssh`, and anything `docker` is supported ('Protection Mode' must be disabled for Docker.) Anything that is stored in `~` (including ssh keys, git configs, etc.) are saved. If you want to install other features, you may use the `vscode-tunnel.sh` file in the config to auto-run on addon startup (this is how I got Hadolint to work).

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_vscode-tunnel)

### [Playit.gg](/playit-gg)

Playit.gg is a global proxy that allows anyone to host a server without port forwarding.
<!-- CSpell: words williamcorsel -->
Original inspiration thanks to the Benjamin589 PR williamcorsel/hassio-addons that used the alex33856/playitgg-docker image. The Dockerfile for this addon uses the majority of that Dockerfile.

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_playitgg)

### [MC All-Platform Velocity Proxy](/mc-all-platform-velocity)

Allow players on Java Edition (1.7.2 - latest), Bedrock Edition, and Eaglercraft (unofficial web browser, including v1.5 with EaglerXRewind if enabled) clients to join your Minecraft server(s).

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_mc-all-platform-velocity)

### [MC auth server](/mc-auth-server)

Minecraft Leaf (Paper fork) auth server for proxy setups that use AuthMe.

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_mc-auth-server)

### [Eaglercraft Relay](/eag-relay)

Run and Eaglercraft relay server from Home Assistant, allowing players connected to the same relay to join each other's shared worlds.

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_eag-relay)

### [MC All-Platform Velocity Proxy Beta](/mc-all-platform-velocity-beta)

Allow players on Java Edition (1.7.2 - latest), Bedrock Edition, and Eaglercraft (unofficial web browser, including v1.5 with EaglerXRewind if enabled) clients to join your Minecraft server(s).

This beta version includes new features before they fully release. The list is available on the addon page.

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_mc-all-platform-velocity-beta)
