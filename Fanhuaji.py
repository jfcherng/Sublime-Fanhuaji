import io
import json
import sublime
import sublime_plugin
import urllib
from .functions import prepare_fanhuaji_convert_args
from .log import msg, print_msg
from .settings import get_converters_info, get_setting, get_text_delimiter

# HTTP headers used in issuing an API call
HTTP_HEADERS = {"user-agent": "Sublime Text Fanhuaji"}


class FanhuajiConvertPanelCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        sublime.active_window().show_quick_panel(
            # fmt: off
            [
                "{name} - {desc}".format_map(converter)
                for converter in get_converters_info()
            ],
            # fmt: on
            self.on_done
        )

    def on_done(self, index: int) -> None:
        if index == -1:
            return

        converter = get_converters_info(index)

        sublime.active_window().run_command(
            "fanhuaji_convert",
            # fmt: off
            {
                "args": {
                    "converter": converter["name"],
                },
            },
            # fmt: on
        )


class FanhuajiConvertCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, args: dict = {}) -> None:
        args["text"] = get_text_delimiter().join(
            [self.view.substr(region) for region in self.view.sel()]
        )
        converter = args["converter"]

        if converter.endswith("@Local"):
            converter = converter[0 : -len("@Local")]

            if converter == "WikiSimplified":
                db = json.loads(
                    sublime.load_resource("Packages/Fanhuaji/data/zh2Hans.json"), encoding="UTF-8"
                )

                # Trie longest replacing?
                ...
        else:
            text = self._convert_online(args)

        texts = text.split(get_text_delimiter())
        blocks = [{"region": z[0], "text": z[1]} for z in zip(self.view.sel(), texts)]

        for block in reversed(blocks):
            self.view.replace(edit, block["region"], block["text"])

    def _convert_online(self, args: dict):
        real_args = prepare_fanhuaji_convert_args(self.view)
        real_args.update(args)

        try:
            result = self._doApiConvert(real_args)
        except urllib.error.HTTPError as e:
            sublime.error_message(msg("Failed to reach the server: {}".format(e)))

            return
        except ValueError:
            sublime.error_message(msg("Failed to decode the returned JSON string..."))

            return

        if result["code"] != 0:
            sublime.error_message(msg("Error: {}".format(result["msg"])))

            return

        return result["data"]["text"]

    def _doApiConvert(self, args: dict) -> None:
        if get_setting("debug"):
            print_msg("Request with: {}".format(args))

        encoding = "utf-8"
        url = get_setting("api_server") + "/convert"

        # prepare request
        data = urllib.parse.urlencode(args).encode(encoding)
        req = urllib.request.Request(url, data)
        for key, val in HTTP_HEADERS.items():
            req.add_header(key, val)

        # execute request
        with urllib.request.urlopen(req) as response:
            html = response.read().decode(encoding)

            return json.loads(html)
