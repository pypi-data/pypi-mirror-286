from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types

# messages.ChatFull - Layer 181
# NOTICE: This is a workaround for pydantic. Discriminated unions doesn't work with single type in Union
# pydantic.Discriminator(base_type_discriminator)
ChatFull = typing.Union[
    typing.Annotated[
        types.messages.ChatFull,
        pydantic.Tag('messages.ChatFull'),
        pydantic.Tag('ChatFull')
    ]
]
