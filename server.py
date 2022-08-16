import dataclasses
from pathlib import Path

from jetforce import GeminiServer, StaticDirectoryApplication, CompositeApplication, Response, Status

from retrograde.jetforce import install_orbit_routes


def static_app(site_hostname):
    root = Path.home() / "gemini" / site_hostname
    return StaticDirectoryApplication(root_directory=str(root))


static_sites = [
    "raek.se",
    "blog.raek.se",
    "xn--rk-via.se",  # räk.se
    "xn--gt9h.xn--rk-via.se",  # 🦐.räk.se
]

apps = {None: static_app("fallback")}

for static_site in static_sites:
    apps[static_site] = static_app(static_site)

install_orbit_routes(apps["raek.se"], "demo", "/orbits/demo")
install_orbit_routes(apps["raek.se"], "omloppsbanan", "/orbits/omloppsbanan")


app = CompositeApplication(apps)
host = "::"  # Seems to work for both IPv4 and IPv6...

config_dir = Path.home() / ".config" / "gemini" / "server"


if __name__ == "__main__":
    server = GeminiServer(
        app,
        host=host,
        certfile=str(config_dir / "cert.pem"),
        keyfile=str(config_dir / "privkey.pem"))
    server.run()
