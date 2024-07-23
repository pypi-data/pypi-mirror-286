from __future__ import annotations

import typing

import pydantic

from telegram_pydantic import types
from telegram_pydantic.utils import base_type_discriminator

# auth.CodeType - Layer 181
CodeType = typing.Annotated[
    typing.Union[
        typing.Annotated[
            types.auth.CodeTypeCall,
            pydantic.Tag('auth.CodeTypeCall'),
            pydantic.Tag('CodeTypeCall')
        ],
        typing.Annotated[
            types.auth.CodeTypeFlashCall,
            pydantic.Tag('auth.CodeTypeFlashCall'),
            pydantic.Tag('CodeTypeFlashCall')
        ],
        typing.Annotated[
            types.auth.CodeTypeFragmentSms,
            pydantic.Tag('auth.CodeTypeFragmentSms'),
            pydantic.Tag('CodeTypeFragmentSms')
        ],
        typing.Annotated[
            types.auth.CodeTypeMissedCall,
            pydantic.Tag('auth.CodeTypeMissedCall'),
            pydantic.Tag('CodeTypeMissedCall')
        ],
        typing.Annotated[
            types.auth.CodeTypeSms,
            pydantic.Tag('auth.CodeTypeSms'),
            pydantic.Tag('CodeTypeSms')
        ]
    ],
    pydantic.Discriminator(base_type_discriminator)
]
