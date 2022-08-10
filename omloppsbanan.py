from pathlib import Path
from urllib.parse import quote

from gemurl import normalize_url
from jetforce import JetforceApplication, Response, Status


LINKS_TEMPLATE = """# Omloppsbanan Navigation Links

For a page to be a member of the orbit it needs to be of MIME type text/gemtext and contain links to these pages:

```
Required:
=> gemini://raek.se/orbits/omloppsbanan/ About Omloppsbanan
=> gemini://raek.se/orbits/omloppsbanan/next?<YOUR URL> Next Page
=> gemini://raek.se/orbits/omloppsbanan/prev?<YOUR URL> Previous Page

Optional:
=> gemini://raek.se/orbits/omloppsbanan/random?<YOUR URL> Random Page
```

The link texts ("Next Page" etc) are merely suggestions and do not need to match these examples. The links can appear anywhere on the page.
"""

app = JetforceApplication()


@app.route("/genlinks")
def genlinks(request):
    if not request.query:
        return Response(Status.INPUT, "Page URL")
    url = quote(normalize_url(request.query), safe="")
    return Response(Status.SUCCESS, "text/gemini", LINKS_TEMPLATE.replace("<YOUR URL>", url))


@app.route("/next")
def next_page(request):
    if not request.query:
        return Response(Status.INPUT, "Page URL")
    return Response(Status.TEMPORARY_FAILURE, "Not implemented.")


@app.route("/prev")
def prev_page(request):
    if not request.query:
        return Response(Status.INPUT, "Page URL")
    return Response(Status.TEMPORARY_FAILURE, "Not implemented.")


@app.route("/random")
def random_page(request):
    return Response(Status.TEMPORARY_FAILURE, "Not implemented.")


@app.route("/status")
def page_status(request):
    if not request.query:
        return Response(Status.INPUT, "Page URL")
    return Response(Status.TEMPORARY_FAILURE, "Not implemented.")


@app.route("/check")
def check_page(request):
    if not request.query:
        return Response(Status.INPUT, "Page URL")
    return Response(Status.TEMPORARY_FAILURE, "Not implemented.")


@app.route("/list")
def list_pages(request):
    return Response(Status.TEMPORARY_FAILURE, "Not implemented.")
