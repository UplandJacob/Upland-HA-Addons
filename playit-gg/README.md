# Playit.gg Agent

![Addon Stage](https://img.shields.io/badge/Addon%20stage-ready-green.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-yes-green.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-no-red.svg)

## About

Playit.gg is a global proxy that allows anyone to host a server without port forwarding.

Original inspiration thanks to the [Benjamin589 PR](https://github.com/williamcorsel/hassio-addons/pull/26) `williamcorsel/hassio-addons` that used the `alex33856/playitgg-docker` image. The Dockerfile for this addon uses the majority of that Dockerfile.

## Install

**Add repository**

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: https://github.com/UplandJacob/Upland-HA-Addons

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_playitgg)

## Setup

1. If you don't already have a Playit.gg account, head over to [Playit.gg](https://playit.gg) and sign up.
2. Follow the install instructions above and start it, then go to the "Log" tab.
3. Find the claim link, copy and paste it into a browser, and go through the claim process to add your node to your Playit.gg account.
4. Check the add-on logs to ensure the add-on has successfully connected to your Playit.gg account.
5. Back [on the website](https://playit.gg/account/agents), click on the agent, then "+Add Tunnel" to expose whatever services you want to the internet.
