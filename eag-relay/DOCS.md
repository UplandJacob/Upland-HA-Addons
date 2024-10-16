Cleaned up from https://git.eaglercraft.rip/eaglercraft/eaglercraft-builds/src/branch/main/Eaglercraft_SharedWorldRelay/instructions.txt



## Notes

**Shared worlds work between any two eaglercraft clients that share a relay server, anyone can join your world it is not limited to just the other devices on your local network.**

When adding the relay address to the client you must provide it in URI format like "ws://address:port" or "wss://address:port", and determining the IP address and setting up port forwarding is the same as making a regular minecraft server.

**The relay is not used for transferring the actual gameplay packets, it is only used for the initial discovery process to allow clients to find each other, stuff such as coordinates and chat messages aren't visible to the relay.**

## Config

**The `origin-whitelist` config variable is a semicolon (`;`) seperated list of domains used to restrict what sites are to be allowed to use your relay. When left blank it allows all sites. Add `offline` to allow offline download clients to use your relay as well, and `null` to allow connections that do not specify an `Origin:` header. Use `*` as a wildcard, for example: `*.deev.is` allows all domains ending with "deev.is" to use the relay.**

Ratelimiting: "ping-ratelimit" is for limiting pings from clients searching for worlds, "world-ratelimit" is for limiting creating and joining new worlds.

