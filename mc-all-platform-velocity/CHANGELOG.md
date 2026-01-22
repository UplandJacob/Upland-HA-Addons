# Changelog

## 2.3.x (01/20/2026)

- Config update error handling
- Behind-the-scenes cleanup
- Fix HAProxy setting not setting correct value in velocity.toml
- Partial support for running outside of HA

## 2.2.x (11/26/2025)

- Update to Geyser config version 5
- Handle HAProxy settings automatically between plugin configs
- (2.2.1) - Fix missing HAProxy schema
- (2.2.2) - Add the rest of Geyser gameplay settings to the config UI, update translations and docs, clean up default Geyser config
- (2.2.3+) - Plugin updates

## 2.1.x (09/02/2025)

- Save and update jar file names dynamically
- Support running outside of Home Assistant
- Update plugins and Velocity
- Behind-the-scenes cleanup
- (2.1.1 - 2.1.2) - Bug fixes
- (2.1.3 - 2.1.21) - PLugin Updates

## 2.0.x (07/10/2025)

- **Merge beta:**
- Scripts written in Python
- Updated to EaglerXServer (new config files)
- Updated Velocity (Now that EaglerXServer supports it)
- Auto download Floodgate database drivers
- `plugins.yaml` allows you to define any plugin to be automatically downloaded and update any plugins packaged with the addon
- Any custom files for the proxy (the old version only supported certain folders)
- Updated config in the UI - Trimmed out some advanced options; you can still change them in their respective config files
- Automatically set the Server Name, Max Players, and MOTD in all 3 places: Velocity, EaglerXServer, and Geyser (with automatically converting MOTD from MiniMessage)
- Better startup logging (with a Log Level option as well)
