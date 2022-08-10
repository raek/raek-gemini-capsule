import dataclasses
from pathlib import Path

from jetforce import GeminiServer, StaticDirectoryApplication, CompositeApplication, Response, Status

import omloppsbanan


def static_app(site_hostname):
    root = Path.home() / "gemini" / site_hostname
    return StaticDirectoryApplication(root_directory=str(root))


def mount_app(parent_app, path_prefix, child_app):
    for route_pattern, callback in child_app.routes:
        new_route_pattern = dataclasses.replace(route_pattern, path=path_prefix + route_pattern.path)
        parent_app.routes.append((new_route_pattern, callback))


static_sites = [
    "raek.se",
    "blog.raek.se",
    "xn--rk-via.se",  # räk.se
    "xn--gt9h.xn--rk-via.se",  # 🦐.räk.se
]

apps = {None: static_app("fallback")}

for static_site in static_sites:
    apps[static_site] = static_app(static_site)

mount_app(apps["raek.se"], "/orbits/omloppsbanan", omloppsbanan.app)


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
