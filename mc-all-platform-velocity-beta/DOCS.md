# Configuring Minecraft All-Platform Velocity Proxy

**These docs are split into multiple sections for configuring Velocity and each plugin.**

***

<!--markdownlint-disable MD001 -->
### Special data types
<!--markdownlint-enable MD001 -->
The `Type` column may use these special data types:

#### Chat

Chat messages may be provided in [MiniMessage](https://docs.advntr.dev/minimessage/format.html) format.
RGB support is available for Minecraft 1.16 and later versions.

#### Address

An address is a pairing of an IP address or hostname, and a port, separated by a colon (`:`). For instance, `127.0.0.1:25577` and `server01.example.com:25565` are valid addresses.

***

## Addon configuration

|Setting Name|Type|Description|
|-|-|-|
|`logLevel` - Log Level|Integer (1-5)|Amount of logs to be shown on startup.|
|`allocatedRAM` - Allocated RAM (MB)|Integer|MiB of RAM to be allocated to the Java process.|
|`maxRAM` - Max RAM (MB)|Integer|Max MiB of RAM the Java process can use.|
|`max_players` - Max Players|Integer|Max number of players can connect to the server. *This value will be copied to the config locations of all plugins that use it.*|
|`server_name` - Server Name|String|Name of the server. *This value will be copied to the config locations of all plugins that use it.*|
|`motd1` - MOTD Line 1|Chat|Line 1 of the Message of the Day shown in players' server lists.|
|`motd2` - MOTD Line 2|Chat|Line 2 of the MOTD. - not visible for most Bedrock players.|

***

## Configuring Velocity

Settings not shown here for UI configuration can be set by editing the `velocity.toml` file found in `addon_configs/d78ad65c_mc-all-platform-velocity/server` through something like [Filebrowser](https://github.com/alexbelgium/hassio-addons). These options can be found at [docs.papermc.io](https://docs.papermc.io/velocity/configuration).

### Velocity Config (`rootConfig`)

These settings mostly cover the basic, most essential settings of the proxy.

|Setting Name|Type|Description|
|-|-|-|
| `online-mode` | Boolean | Should we authenticate players with Mojang? By default, this is on. |
| `force-key-authentication` | Boolean | Should the proxy enforce the new public key security standard? By default, this is on. |
| `prevent-client-proxy-connections` | Boolean | If client's ISP/AS sent from this proxy is different from the one from Mojang's authentication server, the player is kicked. This disallows some VPN and proxy connections but is a weak form of protection. |
| `player-info-forwarding-mode` | Enum | See [Configuring player information forwarding](/velocity/player-information-forwarding) for more information. |
| `announce-forge` | Boolean | This setting determines whether Velocity should present itself as a Forge/FML-compatible server. By default, this is disabled. |
| `kick-existing-players` | Boolean | Allows restoring the Vanilla behavior of kicking users on the proxy if they try to reconnect (e.g. lost internet connection briefly). |
| `ping-passthrough` | String | Allows forwarding nothing (the default), the `MODS` (for Forge), the `DESCRIPTION`, or everything (`ALL`) from the `try` list (or forced host server connection order). |
| `enable-player-address-logging` | Boolean | If disabled (default is true), player IP addresses will be replaced by " " in logs. |

### `servers` section (seperated in 2 parts for the addon)

#### Backend Servers - `servers`

Each list value:

|Setting Name|Type|Description|
|-|-|-|
| name | String | The name the proxy gives a server it can connect to. These names will be reference later. |
| address | Address | The address given to that name. |

```yaml
- name: lobby
  address: internal-hostname:25565
- name: game1
  address: example.com:25565
- name: game2
  address: 192.168.1.22:25565
```

#### Server attempt join order - `serverAttemptJoinOrder`

This specifies what servers Velocity should try to connect to upon player login and when a player is kicked from a server.

ex: if set to "`lobby`, `backup`", it will try `lobby` first, then `backup` if it fails.

### Forced Hosts - `forced-hosts` section (`forcedHosts`)

In this addon, this option will be a list with a `hostname` with another list of servernames (`servNames`) to attempt to connect to (like with serverAttemptJoin order):

```yaml
- hostname: lobby.example.com
  servNames:
    - lobby
- hostname: game.example.com
  servNames:
    - game1
    - game2
```

### Velocity Advanced Config - `advanced` section

|Setting Name|Type|Description|
|-|-|-|
| `compression-threshold` | Integer | This is the minimum size (in bytes) that a packet must be before the proxy compresses it. Minecraft uses 256 bytes by default. |
| `compression-level` | Integer | This setting indicates what `zlib` compression level the proxy should use to compress packets. The default value uses the default zlib level. |
| `login-ratelimit` | Integer | This setting determines the minimum amount of time (in milliseconds) that must pass before a connection from the same IP address will be accepted by the proxy. A value of `0` disables the rate limit." |
| `connection-timeout` | Integer | This setting determines how long the proxy will wait to connect to a server before timing out. |
| `read-timeout` | Integer | This setting determines how long the proxy will wait to receive data from the server before timing out. |
| `haproxy-protocol` | Boolean | This setting determines whether or not Velocity should receive HAProxy PROXY messages. If you don't use HAProxy, leave this setting off. |
| `tcp-fast-open` | Boolean |This setting allows you to enable TCP Fast Open support in Velocity. Your proxy must run on Linux kernel >=4.14 for this setting to apply. |
| `bungee-plugin-message-channel` | Boolean | This setting allows you to enable or disable support for the BungeeCord plugin messaging channel. |
| `show-ping-requests` | Boolean |  This setting allows you to log ping requests sent by clients to the proxy. |
| `failover-on-unexpected-server-disconnect` | Boolean | This setting allows you to determine if the proxy should failover or disconnect the user in the event of an unclean disconnect. |
| `announce-proxy-commands` | Boolean | This setting allows you to enable or disable explicitly sending proxy commands to the client (for Minecraft 1.13+ tab completion). |
| `log-command-executions` | Boolean | Determines whether or not the proxy should log all commands run by the user. |
| `log-player-connections` | Boolean | Enables logging of player connections when connecting to the proxy, switching servers and disconnecting from the proxy. |
| `accepts-transfers` | Boolean | Determines whether or not the proxy accepts incoming transfers from other servers. If disabled, the proxy will disconnect transferred clients. |

### `query` section is not configurable in the UI

***

## Configuring EaglerXServer

The EaglercraftXServer plugin allows Eaglercraft clients to connect to the server.

### Eaglercraft

Basic EaglercraftXServer configuration.

|Setting Name|Type|Description|
|-|-|-|
|`http_websocket_compression_level`|Integer|Compression level for WebSocket connections.|
|`http_websocket_ping_intervention`|Boolean|Enable intervention if WebSocket pings are not received in time. (Helps reduce "Stream has ended" messages)|
|`enable_is_eagler_player_property`|Boolean|Enable the `is_eagler` property for player identification.|
|`eagler_players_vanilla_skin`|String|Default skin username to use for Eaglercraft players. (Leave empty for Steve)|
|`enable_authentication_events`|Boolean|Enable events related to player authentication.|
|`enable_backend_rpc_api`|Boolean|Enable the backend RPC API. Only needed if you add the backend RPC APT plugin to your backend servers.|
|`use_modernized_channel_names`|Boolean|Use updated channel names for plugin messaging.|
|`eagler_players_view_distance`|Integer|Default view distance for Eaglercraft players.|
|`protocol_v4_defrag_send_delay`|Integer|Delay (in ms) for sending defragmented protocol v4 packets.|
|`brand_lookup_ratelimit`|Integer|Rate limit for client brand lookups (requests per second).|
|`webview_download_ratelimit`|Integer|Rate limit for webview downloads (bytes per second).|
|`webview_message_ratelimit`|Integer|Rate limit for webview messages (messages per second).|

### Eaglercraft - Skin Database

Settings for the Eaglercraft skins database.

|Setting Name|Type|Description|
|-|-|-|
|`download_vanilla_skins_to_clients`|Boolean|Download vanilla Minecraft skins to Eaglercraft clients.|
|`valid_skin_download_urls`|List (Strings)|URLs permitted to download skins.|
|`enable_fnaw_skin_models_global`|Boolean|Globally allow Five Nights at Winstons (FNAW) skin models for all players.|
|`enable_fnaw_skin_models_servers`|List (Strings)|Server names where FNAW skin models are enabled.|
|`enable_skinsrestorer_apply_hook`|Boolean|Apply the SkinsRestorer plugin hook for Eaglercraft clients to see non-Eaglercraft player's skins.|

### Eaglercraft - Voice

Settings for Eaglercraft voice chat.

|Setting Name|Type|Description|
|-|-|-|
|`enable_voice_service`|Boolean|Enable the Eaglercraft voice chat service.|
|`enable_voice_all_servers`|Boolean|Enable voice chat on all servers.|
|`enable_voice_on_servers`|List (Strings)|List of server names where voice chat is enabled (ignored if `enable_voice_all_servers` is true).|
|`separate_server_voice_channels`|Boolean|Use separate voice channels for each server.|
|`voice_backend_relayed_mode`|Boolean|Use relayed mode for the voice backend (improves NAT traversal, may increase latency).|
|`voice_connect_ratelimit`|Integer|Maximum number of voice connection attempts per minute per client.|
|`voice_request_ratelimit`|Integer|Maximum number of voice requests per minute per client.|
|`voice_ice_ratelimit`|Integer|Maximum number of ICE (Interactive Connectivity Establishment) messages per minute per client.|

### Eaglercraft - Update Service

Loads the latest Eaglercraft version from eaglercraft.com and sends it to clients in case of an available update.

|Setting Name|Type|Description|
|-|-|-|
|`enable_update_system`|Boolean|Enable or disable the Eaglercraft update system.|
|`download_latest_certs`|Boolean|Automatically download the latest certificates from eaglercraft.com for secure updates.|
|`check_for_update_every`|Integer|Interval (in seconds) to check for updates.|

### Eaglercraft - Update Checker

Sends a message if the EaglerXServer plugin has an update available.

|Setting Name|Type|Description|
|-|-|-|
|`enable_update_checker`|Boolean|Enable or disable the EaglerXServer plugin update checker.|
|`check_for_update_every`|Integer|Interval (in seconds) to check for plugin updates.|
|`print_chat_messages`|Boolean|Print update checker messages in chat when an update is available.|

### Eaglercraft - Listeners

Most listener settings are available in the addon's config folder. The settings defined here will ALWAYS overwrite changes you make to listener0 in that file.

|Setting Name|Type|Description|
|-|-|-|
|`forward_ip`|Boolean|Forward the real IP address of connecting players to the backend server.|
|`spoof_player_address_forwarded`|Boolean|Spoof the player address using the forwarded IP for compatibility such as with antibot or auth plugins.|
|`show_motd_player_list`|Boolean|Show the player list to clients in the server's MOTD.|
|`allow_query`|Boolean|Allow server status queries from external tools.|
|`allow_motd`|Boolean|Allow the server MOTD to be displayed to clients.|

***

## Configuring Floodgate

### Floodgate

Basic Floodgate config

|Setting Name|Type|Description|
|-|-|-|
|`username-prefix`|String|Prefix added to Bedrock player usernames. "." recommended|
|`replace-spaces`|Boolean|Replace spaces in Bedrock usernames with underscores.|
|`default-locale`|String|Default locale for Bedrock players.|
|`send-floodgate-data`|Boolean|Send Floodgate-specific data to the backend servers.|

### Floodgate - Player Link

Local and global player link settings: See <https://geysermc.org/wiki/floodgate/linking>.

If you enable local linking, the database driver will automattically be downloaded. After the first startup, Floodgate will generate the config file that can then be configured at `addon_configs/d78ad65c_mc-all-platform-velocity/server/plugins/floodgate/{type}/{type}.yml`.

|Setting Name|Type|Description|
|-|-|-|
|`enabled`|Boolean|Enable player linking.|
|`require-link`|Boolean|Require Bedrock players to link their accounts before joining.|
|`enable-own-linking`|Boolean|Allow local linking with a database.|
|`allowed`|Boolean|Allow players to use `/linkaccount` and `/unlinkaccount`.|
|`link-code-timeout`|Integer|Time in seconds before a link code expires.|
|`type`|String|Storage type for player linking ("sqlite", "mysql", or "mongodb").|
|`enable-global-linking`|Boolean|Enable global linking with `link.geysermc.org`.|

***

## Configuring Geyser

Detailed descriptions and more settings (can be edited at `addon_configs/d78ad65c_mc-all-platform-velocity/server/plugins/Geyser-Velocity/config.yml`) can be found on [geysermc.org](https://geysermc.org/wiki/geyser/understanding-the-config).

### Geyser - Bedrock

Basic Geyser client connection config

|Setting Name|Type|Description|
|-|-|-|
|`compression-level`|Integer|Compression level for Bedrock connections.|
|`enable-proxy-protocol`|Boolean|Enable Proxy Protocol support for Bedrock connections.|

### Geyser - Remote

Basic Geyser connection settings

|Setting Name|Type|Description|
|-|-|-|
|`auth-type`|String|Authentication method for remote server ("online", "offline", or "floodgate").|
|`use-proxy-protocol`|Boolean|Use Proxy Protocol when connecting to the server.|
|`forward-hostname`|Boolean|Forward the Bedrock client's hostname to the server.|

### Geyser

General Geyser config

|Setting Name|Type|Description|
|-|-|-|
|`command-suggestions`|Boolean|Enable command suggestions for Bedrock players.|
|`passthrough-player-counts`|Boolean|Show player counts to Bedrock clients.|
|`ping-passthrough-interval`|Integer|Interval in seconds for ping passthrough updates.|
|`forward-player-ping`|Boolean|Forward player ping to the server.|
|`show-cooldown`|String|Display type for cooldowns ("false", "title" (or "true"), or "actionbar").|
|`show-coordinates`|Boolean|Show coordinates to Bedrock players in the top left.|
|`disable-bedrock-scaffolding`|Boolean|Disable scaffolding-style bridging for Bedrock players. (Prevents cheating compared to Java players)|
|`emote-offhand-workaround`|String|Workaround for emote/offhand conflicts ("disabled", "no-emotes", or "emotes-and-offhand").|
|`allow-custom-skulls`|Boolean|Allow custom skulls for Bedrock players.|
|`max-visible-custom-skulls`|Integer|Maximum number of custom skulls visible to Bedrock players.|
|`custom-skull-render-distance`|Integer|Render distance for custom skulls.|
|`add-non-bedrock-items`|Boolean|Add Java-only items for Bedrock players.|
|`above-bedrock-nether-building`|Boolean|Allow building above the nether ceiling for Bedrock players. (Makes the Nether act like the End)|
|`force-resource-packs`|Boolean|Force resource packs on Bedrock clients.|
|`xbox-achievements-enabled`|Boolean|Enable Xbox achievements for Bedrock players.|
|`log-player-ip-addresses`|Boolean|Log Bedrock player IP addresses.|

***

## Ports

### "25565/tcp" - Java Edition and Eaglercraft port

Both the Eaglercraft websocket and Java socket are served through this port.

### "19132/udp" - Bedrock Edition port

Bedrock connections are served through this port.
