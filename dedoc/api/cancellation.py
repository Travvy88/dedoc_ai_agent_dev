# region MODULE_CONTRACT [DOMAIN(8): DocumentProcessing, RequestLifecycle; CONCEPT(7): ClientDisconnection, AsyncCancellation; TECH(9): FastAPI, AnyIO, AsyncContextManager]
## @modulecontract
## @purpose Provide async context management for FastAPI endpoints: monitors client connection and cancels long-running processing when the client disconnects prematurely.
## @scope Request lifecycle — client disconnect detection and task cancellation.
## @input FastAPI Request object and logger.
## @output Async context manager that yields for the duration of client connection; cancels tasks on disconnect.
## @links [USES_API(9): fastapi.Request, anyio.create_task_group]
## @invariants
## - cancel_scope is always cancelled in the finally block to ensure cleanup.
## - watch_disconnect loop breaks only on http.disconnect message.
## @rationale
## Q: Why use anyio instead of asyncio directly?
## A: FastAPI/Starlette is built on anyio, which provides structured concurrency and better cancellation semantics than raw asyncio.
## @changes
## LAST_CHANGE: [v1.0.0 – Initial creation with semantic markup]
## @modulemap
## FUNC 8[Async context manager for disconnect-based cancellation] => cancel_on_disconnect
## @usecases
## - [cancel_on_disconnect]: ProcessHandler => MonitorClientConnection => CancelProcessingOnDisconnect
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: cancellation, disconnect, client, async, context manager, FastAPI, anyio, request lifecycle, task group
# STRUCTURE: ▶ async with create_task_group → ◇ start_soon(watch_disconnect) → ○ loop 〈receive message〉 → ⚡ http.disconnect? → cancel_scope.cancel → ⎷ finally cancel → ⎋ yield

import logging
from contextlib import asynccontextmanager

from anyio import create_task_group
from fastapi import Request


# region FUNC_cancel_on_disconnect [DOMAIN(8): RequestLifecycle; CONCEPT(7): ClientDisconnect; TECH(9): AsyncContextManager, AnyIO]
## @purpose Async context manager for async code that needs to be cancelled if client disconnects prematurely. The client disconnect is monitored through the Request object.
## @uses anyio.create_task_group, fastapi.Request
## @io (Request, Logger) -> AsyncContextManager[None]
## @complexity 6
@asynccontextmanager
async def cancel_on_disconnect(request: Request, logger: logging.Logger) -> None:
    """
    Source: https://github.com/dorinclisu/runner-with-api
    See discussion: https://github.com/fastapi/fastapi/discussions/8805
    """
    async with create_task_group() as task_group:
        async def watch_disconnect() -> None:
            while True:
                message = await request.receive()

                if message["type"] == "http.disconnect":
                    client = f"{request.client.host}:{request.client.port}" if request.client else "-:-"
                    logger.warning(f"[IMP:8][cancel_on_disconnect][DISCONNECT] {client} - `{request.method} {request.url.path}` 499 DISCONNECTED")

                    task_group.cancel_scope.cancel()
                    break

        task_group.start_soon(watch_disconnect)

        try:
            yield
        finally:
            task_group.cancel_scope.cancel()
# endregion FUNC_cancel_on_disconnect
