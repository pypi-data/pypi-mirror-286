from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types

# channels.AdminLogResults - Layer 181
# NOTICE: This is a workaround for pydantic. Discriminated unions doesn't work with single type in Union
# pydantic.Discriminator(base_type_discriminator)
AdminLogResults = typing.Union[
    typing.Annotated[
        types.channels.AdminLogResults,
        pydantic.Tag('channels.AdminLogResults'),
        pydantic.Tag('AdminLogResults')
    ]
]
