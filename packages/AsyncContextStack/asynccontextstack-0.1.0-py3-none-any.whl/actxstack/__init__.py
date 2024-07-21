"""
AsyncContextStack
---------------
Async context manager for nesting async context stacks

Authors:
Chris Lee <chris@cosmosnexus.co>
"""

from __future__ import annotations  # noqa

from contextlib import AsyncExitStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, AsyncContextManager, Iterable


class AsyncContextMixin:
    if TYPE_CHECKING:
        _async_exit_stack: AsyncExitStack

    @property
    def async_contexts(self) -> "Iterable[AsyncContextManager[Any]]":
        return []

    async def __aenter__(self) -> "list[Any]":
        self._async_exit_stack = AsyncExitStack()
        entered_contexts = []
        for context in self.async_contexts:
            entered_contexts.append(
                await self._async_exit_stack.enter_async_context(context)
            )
        return entered_contexts

    async def __aexit__(self, *exc_details) -> None:
        await self._async_exit_stack.__aexit__(*exc_details)
