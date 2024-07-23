from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types
from telegram_pydantic.utils import base_type_discriminator

# InputSecureFile - Layer 181
InputSecureFile = typing.Annotated[
    typing.Union[
        typing.Annotated[
            types.InputSecureFile,
            pydantic.Tag('InputSecureFile')
        ],
        typing.Annotated[
            types.InputSecureFileUploaded,
            pydantic.Tag('InputSecureFileUploaded')
        ]
    ],
    pydantic.Discriminator(base_type_discriminator)
]
