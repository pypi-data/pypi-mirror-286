# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["PathParamNullableParamsParams"]


class PathParamNullableParamsParams(TypedDict, total=False):
    nullable_param_1: Required[Optional[str]]

    nullable_param_2: Required[Optional[str]]

    foo: str
