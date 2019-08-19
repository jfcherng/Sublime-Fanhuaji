import sublime


def get_package_name() -> str:
    return __package__


def get_package_path() -> str:
    return "Packages/" + get_package_name()


def get_settings_file() -> str:
    return "Fanhuaji.sublime-settings"


def get_settings_object() -> sublime.Settings:
    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default=None):
    return get_settings_object().get(key, default)


def get_text_delimiter() -> str:
    """
    The delimiter used to concat/split multiple selected text,
    so we could convert multiple text with only a single API call.
    """

    return r"\n\5\n"


def get_converters_info(index=None) -> dict:
    info = [
        {"name": "Simplified", "desc": "简体化"},
        {"name": "Traditional", "desc": "繁體化"},
        {"name": "China", "desc": "中国化"},
        {"name": "Hongkong", "desc": "香港化"},
        {"name": "Taiwan", "desc": "台灣化"},
        {"name": "Pinyin", "desc": "拼音化"},
        {"name": "Bopomofo", "desc": "注音化"},
        {"name": "Mars", "desc": "火星化"},
        {"name": "WikiSimplified", "desc": "维基简体化"},
        {"name": "WikiTraditional", "desc": "維基繁體化"},
        # local
        {"name": "WikiSimplified@Local", "desc": "维基简体化（本地）"},
        {"name": "WikiTraditional@Local", "desc": "維基繁體化（本地）"},
    ]

    return info[index] if isinstance(index, int) else info
