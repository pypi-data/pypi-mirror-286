# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.names.reserved_names.public.private import Private

__all__ = ["PrivateResource", "AsyncPrivateResource"]


class PrivateResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PrivateResourceWithRawResponse:
        return PrivateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PrivateResourceWithStreamingResponse:
        return PrivateResourceWithStreamingResponse(self)

    def private(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Private:
        return self._get(
            "/names/reserved_names/public/private",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Private,
        )


class AsyncPrivateResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPrivateResourceWithRawResponse:
        return AsyncPrivateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPrivateResourceWithStreamingResponse:
        return AsyncPrivateResourceWithStreamingResponse(self)

    async def private(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Private:
        return await self._get(
            "/names/reserved_names/public/private",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Private,
        )


class PrivateResourceWithRawResponse:
    def __init__(self, private: PrivateResource) -> None:
        self._private = private

        self.private = to_raw_response_wrapper(
            private.private,
        )


class AsyncPrivateResourceWithRawResponse:
    def __init__(self, private: AsyncPrivateResource) -> None:
        self._private = private

        self.private = async_to_raw_response_wrapper(
            private.private,
        )


class PrivateResourceWithStreamingResponse:
    def __init__(self, private: PrivateResource) -> None:
        self._private = private

        self.private = to_streamed_response_wrapper(
            private.private,
        )


class AsyncPrivateResourceWithStreamingResponse:
    def __init__(self, private: AsyncPrivateResource) -> None:
        self._private = private

        self.private = async_to_streamed_response_wrapper(
            private.private,
        )
