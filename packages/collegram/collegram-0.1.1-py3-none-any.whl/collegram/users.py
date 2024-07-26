from __future__ import annotations

import inspect
import logging
import typing

import polars as pl
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import TypeInputChannel, User

import collegram.utils

if typing.TYPE_CHECKING:
    from typing import Iterable

    from telethon import TelegramClient

logger = logging.getLogger(__name__)


def get_channel_participants(
    client: TelegramClient,
    channel: TypeInputChannel,
) -> Iterable[User]:
    """
    We're missing the bio here, can be obtained with GetFullUserRequest
    """
    try:
        participants = client.loop.run_until_complete(client.get_participants(channel))
    except ChatAdminRequiredError:
        logger.warning(f"No access to participants of {channel}")
        participants = []
    return participants


def anon_user_d(user_d: dict, anon_func):
    for field in ("first_name", "last_name", "username", "phone", "photo"):
        user_d[field] = None
    user_d["id"] = anon_func(user_d["id"])
    return user_d


CHANGED_USER_FIELDS = {"id": pl.Utf8}
DISCARDED_USER_FIELDS = (
    "_",
    "contact",
    "mutual_contact",
    "close_friend",
    "first_name",
    "last_name",
    "username",
    "usernames",
    "phone",
    "restriction_reason",
    "photo",
    "emoji_status",
    "color",
    "profile_color",
    "status",
)


def flatten_dict(p: dict):
    flat_p = p.copy()
    for f in DISCARDED_USER_FIELDS:
        flat_p.pop(f, None)
    return flat_p


def get_pl_schema():
    annots = inspect.getfullargspec(User).annotations
    user_schema = {
        arg: collegram.utils.py_to_pl_types(annots[arg])
        for arg in set(annots.keys()).difference(DISCARDED_USER_FIELDS)
    }
    user_schema.update(CHANGED_USER_FIELDS)
    return user_schema
