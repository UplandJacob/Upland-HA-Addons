# Twingate

![Addon Stage](https://img.shields.io/badge/Addon%20stage-not_ready-red.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-yes-green.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-yes-green.svg)

## About

Deploy a twingate connector from Home Assistant.

## Install

<!-- markdownlint-disable MD036 -->
**Add repository**
<!-- markdownlint-enable MD036 -->

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: <https://github.com/UplandJacob/Upland-HA-Addons>

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=1f1b42b3_twingate)

## Setup

1. Go to [twingate.com](https://www.twingate.com) and create an account and network.
2. Create a remote network and resource.
3. Create a connector, choose 'docker', generate tokens and input the extra options however you want.
4. in the 'Configuration' tab of this addon, copy in the information from the Twingate website.

[install-badge]: https://img.shields.io/badge/Install%20on%20my-Home%20Assistant-41BDF5?logo=home-assistant
[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant
[repo-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
