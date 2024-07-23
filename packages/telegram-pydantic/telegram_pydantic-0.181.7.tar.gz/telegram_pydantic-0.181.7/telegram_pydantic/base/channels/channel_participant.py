from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types

# channels.ChannelParticipant - Layer 181
# NOTICE: This is a workaround for pydantic. Discriminated unions doesn't work with single type in Union
# pydantic.Discriminator(base_type_discriminator)
ChannelParticipant = typing.Union[
    typing.Annotated[
        types.channels.ChannelParticipant,
        pydantic.Tag('channels.ChannelParticipant'),
        pydantic.Tag('ChannelParticipant')
    ]
]
