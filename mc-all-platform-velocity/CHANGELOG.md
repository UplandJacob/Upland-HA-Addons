# Changelog

## 2.0.0 (07/10/2025)

- merge beta:
- Scripts written in python
- Updated to EaglerXServer (new config files)
- Updated Velocity (Now that EaglerXServer supports it)
- Auto download Floodgate database drivers
- `plugins.yaml` allows you to define any plugin to be automatically downloaded and update any plugins packaged with the addon
- Any custom files for the proxy (the old version only supported certain folders)
- Updated config in the UI - Trimmed out some advanced options; you can still change them in their respective config files
- Automatically set the Server Name, Max Players, and MOTD in all 3 places: Velocity, EaglerXServer, and Geyser (with automatically converting MOTD from MiniMessage)
- Better startup logging (with a Log Level option as well)

## 1.10.x (02/28/2025)

- Update Geyser
- Update Floodgate
- Update EaglerXVelocity
- Add viarewind.yml config file
- Code cleanup
- 1.10.1 - fix typo in folder name ("extensions" not "extentions")
- 1.10.2 - add missing log, add some notes, fix typos in config, update Geyser and Velocity
- 1.10.3 - fix error with forcedHosts
- 1.10.4 - update Geyser for MC 1.21.5.* and update Velocity
- 1.10.5 - update Velocity, Geyser, ViaVersion, ViaBackwards, and ViaRewind and some grammer fixes
- 1.10.6 - revert Velocity update to hopfully fix ratelimit error
- 1.10.7 - update Geyser to support Bedrock 1.21.80
- 1.10.8+ - mostly more Geyser and Velocity updates

## 1.9.x (02/09/2025)

- Update Geyser
- Update EaglerXVelocity
- Clean up Dockerfile
- Fix some logs
- Floodgate local linking

## 1.8.x (01/25/2025)

- generate UUID and forwarding secret and save in config for persistance
- configurable ICE servers to fix Eaglercraft voice chat
- add missing 'send-floodgate-data' option
- add translations
- code cleanup
