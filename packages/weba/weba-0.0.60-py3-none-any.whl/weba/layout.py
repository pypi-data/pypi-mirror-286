import json
import pathlib
from typing import TYPE_CHECKING, Any, NotRequired, Optional, Unpack, cast

from bs4 import NavigableString

from weba import HTML, HTMLKwargs, env, ui

from .tag.context_manager import TagContextManager as Tag

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

    from .component import Component


def load_manifest(name: str) -> dict[str, Any]:
    if not env.is_prd:
        return {}

    manifest = pathlib.Path(f"dist/manifest-{name}.json").read_text()

    return json.loads(manifest)


class LayoutKwargs(HTMLKwargs):
    header: NotRequired["Component"]
    main: NotRequired["Component"]
    footer: NotRequired["Component"]


Manifest = dict[str, dict[str, Any]]


class Layout(HTML):
    src = """--html
        <!doctype html>
        <html lang="en-US">

        <head>
            <title>Weba</title>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        </head>

        <body>
            <header/>
            <main />
            <footer />
        </body>

        </html>
    """

    main: Tag
    footer: Tag

    manifest: dict[str, Any] = load_manifest("main")

    title = "Weba"

    lang = "en-US"

    cached_tags: dict[str, dict[str, list[Tag]]] = {}

    manifest_id: str = "main"

    def __init__(self, *_args: Any, **kwargs: Unpack[LayoutKwargs]):
        self.lang = kwargs.get("lang", self.__class__.lang)
        self.title = kwargs.get("title", self.__class__.title)
        self._last_component: Optional["Component"] = None
        self.manifest_id = kwargs.get("manifest_id", self.__class__.manifest_id)

    def set_script_and_link_tags(self, manifest_id: str) -> None:
        def imported_chunks(manifest: Manifest, name: str) -> list[dict[str, Any]]:
            """Recursively get all imported chunks for a given entry."""
            chunks: list[dict[str, Any]] = []
            stack: list[str] = [name]
            visited: set[str] = set()
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                chunk = manifest.get(current)
                if not chunk:
                    continue
                chunks.append(chunk)
                stack.extend(chunk.get("imports", []))
            return chunks

        if env.is_prd:
            # Check if we have cached tags for the current manifest
            if manifest_id in Layout.cached_tags:
                self.head.extend(Layout.cached_tags[manifest_id]["head"])
                self.body.extend(Layout.cached_tags[manifest_id]["body"])
                return

            added_css_files: set[str] = set()

            head_tags: list[Tag] = []
            body_tags: list[Tag] = []

            # loop over key value pairs in manifest and append to head
            for name, info in self.manifest.items():
                if info.get("isEntry") or info.get("isDynamicEntry"):
                    js_file: str = info["file"]
                    css_files: list[str] = info.get("css", [])
                    script_tag = ui.script(src=f"/{js_file}", type="module", defer="defer")
                    self.body.append(script_tag)
                    body_tags.append(script_tag)
                    for css_file in css_files:
                        if css_file not in added_css_files:
                            link_tag = ui.link(href=f"/{css_file}", rel="stylesheet", type="text/css")
                            self.head.append(link_tag)
                            head_tags.append(link_tag)
                            added_css_files.add(css_file)
                    # Recursively handle imported chunks
                    for chunk in imported_chunks(self.manifest, name):
                        for css_file in chunk.get("css", []):
                            if css_file not in added_css_files:
                                link_tag = ui.link(href=f"/{css_file}", rel="stylesheet", type="text/css")
                                self.head.append(link_tag)
                                head_tags.append(link_tag)
                                added_css_files.add(css_file)
                        preload_tag = ui.link(rel="modulepreload", href=f"/{chunk['file']}")
                        self.head.append(preload_tag)
                        head_tags.append(preload_tag)
                    # NOTE: Until we have proper critical css detection this will slow down the page load using hx-boost
                    # for css_file in css_files:
                    #     css = pathlib.Path(f"dist/{css_file}").read_text()
                    #     self.head.append(ui.style(css))
            # Cache the generated tags for the current manifest
            Layout.cached_tags[manifest_id] = {"head": head_tags, "body": body_tags}

        else:
            scripts: list[Tag] = cast(list[Tag], self.select("head > script") + self.select("body > script"))

            for script in scripts:
                if script and script.has_key("src"):
                    script["src"] = f"{env.script_dev_url_prefix}/{script['src']}"
                    script["defer"] = "defer"

    def remove_tags(self, tag_name: str):
        for tag in self.select(tag_name):
            tag.decompose()

    def add(self, page: "Component | BeautifulSoup"):
        # NOTE: If we have already called #add, then we don't need to add it again with #_last_component
        self._last_component = None

        if body := page.find("body", recursive=False):
            self.add_content(self.body, "body", body.extract())  # type: ignore
            return

        header = page.find("header", recursive=False)
        footer = page.find("footer", recursive=False)
        main = page.find("main", recursive=False) or page

        if self.header and header:
            self.add_content(self.header, "header", header.extract())  # type: ignore

        if self.footer and footer:
            self.add_content(self.footer, "footer", footer.extract())  # type: ignore

        if self.body and body:
            self.add_content(self.body, "body", body.extract())  # type: ignore

        self.add_content(self.main, "main", main)  # type: ignore

    def add_content(self, tag: "Tag", tag_name: str, content: "NavigableString | Tag"):
        if not tag:
            return

        if isinstance(content, NavigableString):
            content = ui.div(content).find().extract()  # type: ignore

        if content.name == tag_name:
            classes = tag["class"]
            attrs = tag.attrs or {}

            self.replace_content(tag_name, tag, content, classes, attrs)  # type: ignore
        else:
            tag.append(content)

    def replace_content(self, tag_name: str, tag: "Tag", content: "Tag", classes: Any, attrs: dict[str, Any]):
        classes = content["class"] if content.has_attr("class") else []
        tag_classes = tag["class"] or []

        if classes:
            for class_ in classes:
                if class_ not in tag_classes:
                    tag_classes.append(class_)

        content.attrs.update(attrs)

        content["class"] = tag_classes

        setattr(self, tag_name, tag.replace_with(content))

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        # Automatically add the last component if it exists
        if self._last_component:
            if self._last_component._render_cache:
                if (
                    hasattr(self._last_component._render_cache, "_content")
                    and self._last_component._render_cache._content is not None
                ):
                    self.add(self._last_component._render_cache._content)  # type: ignore
                else:
                    self.add(self._last_component._render_cache)  # type: ignore
            else:
                self.add(self._last_component)  # type: ignore

            self._last_component = None

        self.set_script_and_link_tags(self.manifest_id)

        super().__exit__(exc_type, exc_value, traceback)
