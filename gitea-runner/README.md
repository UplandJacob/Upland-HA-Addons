# Gitea Runner

![Addon Stage](https://img.shields.io/badge/Addon%20stage-in_progress-yellow.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-no-red.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-no-red.svg)

## About

This addon allows you to run actions
in your Gitea instance.

## Install

<!-- markdownlint-disable MD036 -->
**Add repository**
<!-- markdownlint-enable MD036 -->

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: <https://github.com/UplandJacob/Upland-HA-Addons>

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_gitea-runner)

## Setup

1. Open your Gitea instance and paste its URL into the addons's config. (A local option is faster if available. ex: `http://homeassistant.local:3000`)
2. Go to `Site Administration -> Actions -> Runners`, click "Create New Runner" and copy the token. (You can also do this in an Organization's or repo's settings. [See the official docs](https://docs.gitea.com/usage/actions/act-runner#obtain-a-registration-token))
3. Paste the token in this addon's configuration.
4. Change the runner's name and labels ([see here](https://docs.gitea.com/usage/actions/act-runner#labels)) if you wish.
5. Start the addon. Watch the logs for errors.
6. Go back to the Runners page in your Gitea instance and confirm it shows 'Idle'.
