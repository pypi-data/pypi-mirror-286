# -*- coding: utf-8 -*-
"""Altissimo FastAPI class file."""
import json

from typing import List

from fastapi import Request
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

# pylint: disable=too-few-public-methods


class JSONPrettyPrintMiddleware(BaseHTTPMiddleware):
    """Fast API JSON Pretty Prinut Middleware."""

    def __init__(self, app, excluded_paths: List[str] | None = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/docs", "/redoc", "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        """Pretty print JSON Response."""
        response = await call_next(request)

        # Skip excluded paths and non-streaming responses
        if request.url.path in self.excluded_paths or not isinstance(response, StreamingResponse):
            return response

        # Collect the stream into a single bytes object
        body = b""
        async for chunk in response.body_iterator:
            if isinstance(chunk, str):
                chunk = chunk.encode()  # Ensure chunk is bytes
            body += chunk

        # Only modify application/json responses
        if response.headers.get("content-type") == "application/json":
            data = json.loads(body.decode())
            pretty_json = json.dumps(
                data,
                ensure_ascii=False,
                allow_nan=False,
                indent=4,
                separators=(", ", ": "),
            ).encode("utf-8")

            # Create a new response with the pretty JSON and original status code
            response.headers["Content-Length"] = str(len(pretty_json))
            return Response(
                content=pretty_json,
                status_code=response.status_code,
                media_type="application/json",
                headers=dict(response.headers),
            )

        return response


# class FastAPI:
#     """Altissimo FastAPI class."""

#     def __init__(self):
#         """Initialize an Altissimo FastAPI instance."""
#         pass
