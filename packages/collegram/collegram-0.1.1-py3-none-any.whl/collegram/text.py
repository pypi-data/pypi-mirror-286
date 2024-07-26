from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lingua import LanguageDetector


def get_clean_chan_text(full_channel_d: dict, inverse_anon_map: dict):
    # TODO: maybe add a sample of messages?
    channel_d = [
        c
        for c in full_channel_d["chats"]
        if c["id"] == full_channel_d["full_chat"]["id"]
    ][0]
    title = channel_d.get("title", "")
    title = inverse_anon_map.get(title, title)
    clean_text = f"{title}. {full_channel_d['full_chat'].get('about', '')}"
    hash_at_pattern = r"(?:^|\B)((@|#)\w+)(?:$|\b)"
    url_pattern = r"(?:^|\s)(\S+\/t.co\/\S+)(?:$|\b)"
    regex_filter = re.compile("({})|({})".format(hash_at_pattern, url_pattern))
    clean_text = regex_filter.sub("", clean_text)
    return clean_text


def detect_chan_lang(
    full_channel_d: dict, inverse_anon_map: dict, lang_detector: LanguageDetector
) -> str | None:
    # TODO:  handle multilingual?
    text = get_clean_chan_text(full_channel_d, inverse_anon_map)
    lang = lang_detector.detect_language_of(text)
    lang_code = None if lang is None else lang.iso_code_639_1.name
    return lang_code
