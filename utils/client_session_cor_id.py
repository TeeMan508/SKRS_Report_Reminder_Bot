from typing import Any
from uuid import uuid4

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager # noqa
from aiohttp.typedefs import StrOrURL

from bot.logger import correlation_id_ctx
from bot.logger import logger


class ClientSessionCorId(ClientSession):
    def post(
        self, url: StrOrURL, *, data: Any = None, **kwargs: Any
    ) -> "_RequestContextManager":
        headers = kwargs.get("headers", {})
        try:
            headers["X-CORRELATION-ID"] = correlation_id_ctx.get()
        except LookupError:
            logger.info("No correlation id specified for request")

        return super().post(url, data=data, headers=headers, **kwargs)

    def get(
            self, url: StrOrURL, *, allow_redirects: bool = True, **kwargs: Any
    ) -> "_RequestContextManager":
        headers = kwargs.get("headers", {})
        try:
            headers["X-CORRELATION-ID"] = correlation_id_ctx.get()
        except LookupError:
            logger.info("No correlation id specified for request")

        return super().post(url, allow_redirects=allow_redirects, headers=headers, **kwargs)