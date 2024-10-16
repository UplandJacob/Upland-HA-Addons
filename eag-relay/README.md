# Eaglercraft Relay

![Addon Stage][stage-badge]
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)


![Supports aarch64 Architecture][aarch64-badge]
![Supports amd64 Architecture][amd64-badge]
![Supports armhf Architecture][armhf-badge]
![Supports armv7 Architecture][armv7-badge]
![Supports i386 Architecture][i386-badge]



## About
Run and Eaglerctaft relay server from Home Assistant, allowing players connected to the same relay to join each other's shared worlds.

Includes a [Coturn](https://github.com/coturn/coturn) turn/stun server because the external ones are either garbage or dead.

Eaglercraft created by lax1dude and ayunami2000.
The Eaglercraft relay files can be found [here](https://git.eaglercraft.rip/eaglercraft/eaglercraft-builds/src/branch/main/Eaglercraft_SharedWorldRelay)

## Install
**Add repository**

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: https://github.com/UplandJacob/Upland-HA-Addons

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_eag-relay)

## Setup
1. Because most players use client with https, you need some things to make your relay work:
* A domain (or subdomain) name:
  * You can get a free subdomain at [duckdns.org](https://duckdns.org) (100% free)
  * You may set up the [duckdns addon](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_duckdns) for dynamic DNS (DDNS)
* Port forwarding: you will need to port forward port 80 (for Let's Encrypt) and port 443 (for the actual websocket). This is different for every router, so you'll need to look it up yourself.
* A certificate and proxy:
  * Can be done with any just one addon: [Nginx Proxy Manager](https://my.home-assistant.io/redirect/supervisor_addon/?addon=a0d7b954_nginxproxymanager)
    * This addon uses Let’s Encrypt to get certificates and an NGINX proxy for converting http (ws) to https (wss)
  * Once the addon is installed and started, open the web UI, sign in with **admin@example.com** and **changeme**, and change you account information. (Make sure you save it). Then you need to set some things up:
    1. Go to the **SSL Certificates** tab, **Add SSL Certificate** -> **Let’s Encrypt**.
    2. Enter the subdomain you got from DuckDNS (ex: somth.duckdns.org) or from another site and click **add…**
    3. Enter your email (just to register the cert. it’s 100% free)
    4. Check **I agree to the Let’s Encrypt Terms of Service**
    5. **Save**
    6. Go to the **Hosts** tab -> **Proxy Hosts**
    7. **Add Proxy Host**
    8. Enter the subdomain again (ex: somth.duckdns.org)
    9. Leave the **Scheme** on **http**
    10. Set the **Forward Hostname** to **homeassistant.local** or the ip of your HA server
    11. Set the **Forward Port** to **6699** or whatever you have it set in your relay configuration.
    12. Check **Websocket Support**
    13. Go to the **SSL** tab within this popup.
    14. Set the **SSL Certificate** to the one for your subdomain.
    15. You can change anything else in this popup to your liking then click **Save**
    16. If the addon is running and you did everything right, you should see **online** on the far right.
2. You can change any of the settings in the **configuration** tab of the addon and start it if you haven’t already.




[aarch64-badge]: https://img.shields.io/badge/aarch64-yes-green.svg?style=flat
[amd64-badge]: https://img.shields.io/badge/amd64-yes-green.svg?style=flat
[armhf-badge]: https://img.shields.io/badge/armhf-no-red.svg?style=flat
[armv7-badge]: https://img.shields.io/badge/armv7-no-red.svg
[i386-badge]: https://img.shields.io/badge/i386-no-red.svg
[stage-badge]: https://img.shields.io/badge/Addon%20stage-ready-green.svg

[install-badge]: https://img.shields.io/badge/Install%20on%20my-Home%20Assistant-41BDF5?logo=home-assistant
[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant
[repo-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg

[install-url]: https://my.home-assistant.io/redirect/supervisor_addon?addon=1f1b42b3_twingate
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons
