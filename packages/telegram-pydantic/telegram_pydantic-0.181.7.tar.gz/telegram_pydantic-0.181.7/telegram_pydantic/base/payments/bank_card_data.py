from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types

# payments.BankCardData - Layer 181
# NOTICE: This is a workaround for pydantic. Discriminated unions doesn't work with single type in Union
# pydantic.Discriminator(base_type_discriminator)
BankCardData = typing.Union[
    typing.Annotated[
        types.payments.BankCardData,
        pydantic.Tag('payments.BankCardData'),
        pydantic.Tag('BankCardData')
    ]
]
