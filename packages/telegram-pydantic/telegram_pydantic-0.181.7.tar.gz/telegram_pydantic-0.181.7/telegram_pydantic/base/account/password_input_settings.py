from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types

# account.PasswordInputSettings - Layer 181
# NOTICE: This is a workaround for pydantic. Discriminated unions doesn't work with single type in Union
# pydantic.Discriminator(base_type_discriminator)
PasswordInputSettings = typing.Union[
    typing.Annotated[
        types.account.PasswordInputSettings,
        pydantic.Tag('account.PasswordInputSettings'),
        pydantic.Tag('PasswordInputSettings')
    ]
]
