import dataclasses
from pathlib import Path

from jetforce import GeminiServer, StaticDirectoryApplication, CompositeApplication, Request, Response, Status

from retrograde.jetforce import install_orbit_routes


class MultilangApplication:
    def __init__(self, path_to_lang, default_lang=None, *args, **kwargs):
        self.path_to_lang = path_to_lang
        self.lang_to_app = {None: StaticDirectoryApplication(default_lang=default_lang, *args, **kwargs)}
        for lang in set(path_to_lang.values()):
            self.lang_to_app[lang] = StaticDirectoryApplication(default_lang=lang, *args, **kwargs)

    @property
    def default(self):
        return self.lang_to_app[None]

    def __call__(self, environ, send_status):
        try:
            request = Request(environ)
        except Exception:
            send_status(Status.BAD_REQUEST, "Invalid URL")
            return

        lang = None
        for path_prefix, prefix_lang in self.path_to_lang.items():
            if request.path.startswith(path_prefix):
                lang = prefix_lang
        return self.lang_to_app[lang](environ, send_status)


def static_app(site_hostname, path_to_lang):
    root = Path.home() / "gemini" / site_hostname
    return MultilangApplication(root_directory=str(root), default_lang="en", path_to_lang=path_to_lang)


static_sites = {
    "raek.se": {
        "/gemlog/2023-01-03-pali-anu-lape.gmi": "tok",
        "/toki-pona/": "tok",
    },
    "blog.raek.se": {
        "/2009/07/09/moted-ela-volapuk-info/": "vo",
    },
    "xn--rk-via.se": {},  # räk.se
    "xn--gt9h.xn--rk-via.se": {},  # 🦐.räk.se
}

apps = {None: static_app("fallback", {})}
for static_site, path_to_lang in static_sites.items():
    apps[static_site] = static_app(static_site, path_to_lang)

install_orbit_routes(apps["raek.se"].default, "demo", "/orbits/demo")
install_orbit_routes(apps["raek.se"].default, "omloppsbanan", "/orbits/omloppsbanan")
install_orbit_routes(apps["raek.se"].default, "space-elevator", "/orbits/space-elevator")


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
