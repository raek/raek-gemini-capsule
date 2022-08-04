from jetforce import GeminiServer, StaticDirectoryApplication
from jetforce.app.composite import CompositeApplication


def static_app(site_hostname):
    root = "/home/raek/gemini/" + site_hostname
    return StaticDirectoryApplication(root_directory=root)


static_sites = [
    "raek.se",
    "blog.raek.se",
    "xn--rk-via.se",  # räk.se
    "xn--gt9h.xn--rk-via.se",  # 🦐.räk.se
]

app_map = {None: static_app("fallback")}

for static_site in static_sites:
    app_map[static_site] = static_app(static_site)

app = CompositeApplication(app_map)
host = "::"  # Seems to work for both IPv4 and IPv6...


if __name__ == "__main__":
    server = GeminiServer(
        app,
        host=host,
        certfile="/home/raek/.config/gemini/server/cert.pem",
        keyfile="/home/raek/.config/gemini/server/privkey.pem")
    server.run()
