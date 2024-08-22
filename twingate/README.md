# Twingate

![Addon Stage][stage-badge]
![Supports aarch64 Architecture][aarch64-badge]
![Supports amd64 Architecture][amd64-badge]
![NO Supports armhf Architecture][armhf-badge]
![Supports armv7 Architecture][armv7-badge]
![Supports i386 Architecture][i386-badge]


[![Install on my Home Assistant][install-badge]][install-url]


## About
Deploy a twingate connector from Home Assistant.

## Install
[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](repository_url)
[![Add repository on my Home Assistant][repository-badge]][repository-url]

or go to the **Add-on Store -> repositories** and add: https://github.com/UplandJacob/Upland-HA-Addons

[![Install on my Home Assistant][install-badge]][install-url]

## Setup
1. Go to [twingate.com](https://www.twingate.com) and create an account and network.
2. Create a remote network and resource.
3. Create a connector, choose 'docker', generate tokens and input the extra options however you want.
4. in the 'Configuration' tab of this addon, copy in the information from the Twingate website.




[aarch64-badge]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-badge]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-badge]: https://img.shields.io/badge/armhf-no-red.svg
[armv7-badge]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-badge]: https://img.shields.io/badge/i386-yes-green.svg
[stage-badge]: https://img.shields.io/badge/Addon%20stage-stable-green.svg

[install-badge]: https://img.shields.io/badge/Install%20on%20my-Home%20Assistant-41BDF5?logo=home-assistant
[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant

[install-url]: https://my.home-assistant.io/redirect/supervisor_addon?addon=1f1b42b3_twingate
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons