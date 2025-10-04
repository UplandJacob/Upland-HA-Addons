# VSCode Tunnel

![Addon Stage](https://img.shields.io/badge/Addon%20stage-ready-green.svg)
![GitHub License](https://img.shields.io/github/license/Uplandjacob/Upland-ha-addons)

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg?style=flat)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-no-red.svg?style=flat)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-no-red.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-no-red.svg)

## About

The VSCode Tunnel addon runs a fully featured VSCode tunnel server that can be accessed from [vscode.dev](https://vscode.dev) and supports all extentions (at least all I have tested with a bit of work).

`git`, `ssh`, and `docker-cli` come pre-installed, supporting anything with Docker ('Protection Mode' must be disabled for Docker. It uses HA's `docker.sock`) Anything that is stored in `~` (including ssh keys, git configs, etc.) are saved. If you want to install other features, you may use the `vscode-tunnel.sh` file in the config to auto-run on addon startup (see below for the Hadolint example).

## Install

<!-- markdownlint-disable MD036 -->
**Add repository**
<!-- markdownlint-enable MD036 -->

[![Add repo](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/UplandJacob/Upland-HA-Addons)

or go to the **Add-on Store -> repositories** and add: <https://github.com/UplandJacob/Upland-HA-Addons>

**Then install:**

[![Show dashboard of add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=d78ad65c_vscode-tunnel)

## Setup

1. Install the addon. If you wish to use anything with docker, you must disable 'Protection Mode'.
2. If you want your tunnel registered with GitHub, enable 'GitHub login', leave off for Microsoft.
3. Start the addon. Check the logs to open the login link and enter the code.
4. Open the link in a browser: <https://vscode.dev/tunnel/TUNNEL_NAME/config/workspace>. You can open any other folder including other addon configs and HA's configs (<https://vscode.dev/tunnel/TUNNEL_NAME> for literally everything). Or <https://vscode.dev/tunnel/TUNNEL_NAME/addons> for local addons.

## Other uses

- To reset the login, delete the `.vscode/token.json` file in the config dir.
- To reset the tunnel name, delete the `.vscode/code_tunnel.json` file.

### Hadolint example

*You must disable 'Protection Mode' for this to work (uses Docker).*

I added the following to `vscode-tunnel.sh`:

```bash
cp /config/hadolint /bin/hadolint
chmod +x /bin/hadolint
```

Then created a file named just `hadolint` (per [Hadolint install recommendations](https://github.com/hadolint/hadolint/#:~:text=VS%20Code%20Hadolint%20extension%20to%20use%20Hadolint%20in%20a%20container)) that the script above copies into `/bin`:

```bash
#!/bin/bash
dockerfile="$1"
shift
docker run --rm -i hadolint/hadolint hadolint "$@" - < "$dockerfile"
```

Then I simply ran `docker pull hadolint/hadolint`. Anytime the Hadolint extention requests, the container is started in HA.
