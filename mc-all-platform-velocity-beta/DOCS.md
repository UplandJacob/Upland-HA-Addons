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
|`max_players` - Max Players|Integer|Max number of players can connecto to the server. *This value will be copied to the config locations of all plugins that use it.*|
|`server_name` - Server Name|String|Name of the server. *This value will be copied to the config locations of all plugins that use it.*|
|`motd1` - MOTD line 1|Chat|Line 1 of the Message of the Day shown in players' server lists.|
|`motd2` - MOTD line 2|Chat|Line 2 of the MOTD. - not visible for most Bedrock players.|

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

### Velocity advanced config - `advanced` section

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

### `query` section is not currently configurable in the UI

***

## Configuring EaglerXServer

### Eaglercraft Config

### Eaglercraft Skin Database

### Eaglercraft Voice

### Eaglercraft Update Service

### Eaglercraft Update Checker

### Eaglercraft Listeners

***

## Configuring Floodgate

### Floodgate Config

### Floodgate - Player Link

***

## Configuring Geyser

### Geyser - Bedrock

### Geyser - Remote

### Geyser
