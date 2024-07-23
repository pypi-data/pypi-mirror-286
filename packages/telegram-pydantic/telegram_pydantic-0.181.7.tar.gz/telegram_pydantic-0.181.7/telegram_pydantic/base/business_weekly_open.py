from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types

# BusinessWeeklyOpen - Layer 181
# NOTICE: This is a workaround for pydantic. Discriminated unions doesn't work with single type in Union
# pydantic.Discriminator(base_type_discriminator)
BusinessWeeklyOpen = typing.Union[
    typing.Annotated[
        types.BusinessWeeklyOpen,
        pydantic.Tag('BusinessWeeklyOpen')
    ]
]
