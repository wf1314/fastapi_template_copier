from contextvars import ContextVar
from time import perf_counter
from typing import cast
from uuid import uuid4

from loguru import logger
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER = "X-Request-ID"
TRACE_ID_HEADER = "X-Trace-ID"
MAX_CONTEXT_ID_LENGTH = 128

_request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)
_trace_id_context: ContextVar[str | None] = ContextVar(
    "trace_id",
    default=None,
)


def get_request_id() -> str | None:
    """返回当前请求的 request_id。"""
    return _request_id_context.get()


def get_trace_id() -> str | None:
    """返回当前请求的 trace_id。"""
    return _trace_id_context.get()


def _clean_context_id(value: str | None) -> str | None:
    """清理外部传入的上下文 ID，避免空值、超长值和换行注入。"""
    if value is None:
        return None
    candidate = value.strip()
    if not candidate or len(candidate) > MAX_CONTEXT_ID_LENGTH:
        return None
    if "\r" in candidate or "\n" in candidate:
        return None
    return candidate


class RequestContextMiddleware:
    """为每个 HTTP 请求注入 request_id/trace_id 并记录耗时。"""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        request_id = _clean_context_id(headers.get(REQUEST_ID_HEADER)) or uuid4().hex
        trace_id = _clean_context_id(headers.get(TRACE_ID_HEADER)) or request_id
        state = cast(dict[str, object], scope.setdefault("state", {}))
        state["request_id"] = request_id
        state["trace_id"] = trace_id
        method = str(scope.get("method", ""))
        path = str(scope.get("path", ""))
        started_at = perf_counter()
        status_code: int | None = None

        request_token = _request_id_context.set(request_id)
        trace_token = _trace_id_context.set(trace_id)

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
                raw_headers = cast(
                    list[tuple[bytes, bytes]],
                    message.setdefault("headers", []),
                )
                response_headers = MutableHeaders(raw=raw_headers)
                response_headers[REQUEST_ID_HEADER] = request_id
                response_headers[TRACE_ID_HEADER] = trace_id
            await send(message)

        try:
            with logger.contextualize(
                request_id=request_id,
                trace_id=trace_id,
                method=method,
                path=path,
            ):
                try:
                    await self.app(scope, receive, send_wrapper)
                except Exception:
                    duration_ms = round((perf_counter() - started_at) * 1000, 2)
                    logger.bind(
                        status_code=500,
                        duration_ms=duration_ms,
                    ).exception("Request failed")
                    raise

                duration_ms = round((perf_counter() - started_at) * 1000, 2)
                logger.bind(
                    status_code=status_code,
                    duration_ms=duration_ms,
                ).info("Request completed")
        finally:
            _request_id_context.reset(request_token)
            _trace_id_context.reset(trace_token)
