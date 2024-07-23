from httpx import AsyncClient, Client, HTTPError

from tourist.core.page import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT, DEFAULT_WINDOW_SIZE


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class TouristScraper:
    __metaclass__ = Singleton

    def __init__(
        self,
        base_url: str,
        secret: str,
        version_prefix: str = "/v1",
    ) -> None:
        self.base_url = base_url
        self.secret = secret
        self.version_prefix = version_prefix

    async def aio_post(self, uri: str, body: dict = None, **httpx_kws):
        headers = httpx_kws.pop("headers", {})
        headers["X-SECRET"] = self.secret
        async with AsyncClient(
            base_url=self.base_url, headers=headers, **httpx_kws
        ) as client:
            try:
                response = await client.post(uri, json=body)
                response.raise_for_status()
                return response.json()
            except HTTPError:
                return {
                    "error": True,
                    "detail": f"Bad status code: {response.status_code}",
                }

    def post(self, uri: str, body: dict = None, **httpx_kws):
        headers = httpx_kws.pop("headers", {})
        headers["X-SECRET"] = self.secret
        with Client(base_url=self.base_url, headers=headers, **httpx_kws) as client:
            try:
                response = client.post(uri, json=body)
                response.raise_for_status()
                return response.json()
            except HTTPError:
                return {
                    "error": True,
                    "detail": f"Bad status code: {response.status_code}",
                }

    async def aio_get_page(
        self,
        target_url: str,
        warmup_url: str = None,
        cookies: list[dict[str, str]] = [],
        include_b64_png: bool = False,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE,
        **httpx_kws,
    ) -> dict:
        uri = self.version_prefix + "/tour/page"
        payload = {
            "target_url": target_url,
            "warmup_url": warmup_url,
            "cookies": cookies,
            "include_b64_png": include_b64_png,
            "user_agent": user_agent,
            "timeout": timeout,
            "window_size": window_size,
        }
        return await self.aio_post(uri, payload, **httpx_kws)

    def get_page(
        self,
        target_url: str,
        warmup_url: str = None,
        cookies: list[dict[str, str]] = [],
        include_b64_png: bool = False,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE,
        **httpx_kws,
    ) -> dict:
        uri = self.version_prefix + "/tour/page"
        payload = {
            "target_url": target_url,
            "warmup_url": warmup_url,
            "cookies": cookies,
            "include_b64_png": include_b64_png,
            "user_agent": user_agent,
            "timeout": timeout,
            "window_size": window_size,
        }
        return self.post(uri, payload, **httpx_kws)

    async def aio_do_actions(
        self,
        actions: str,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE,
        **httpx_kws,
    ) -> dict:
        uri = self.version_prefix + "/tour/actions"
        payload = {
            "actions": actions,
            "user_agent": user_agent,
            "timeout": timeout,
            "window_size": window_size,
        }
        return await self.aio_post(uri, payload, **httpx_kws)

    def do_actions(
        self,
        actions: str,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE,
        **httpx_kws,
    ) -> dict:
        uri = self.version_prefix + "/tour/actions"
        payload = {
            "actions": actions,
            "user_agent": user_agent,
            "timeout": timeout,
            "window_size": window_size,
        }
        return self.post(uri, payload, **httpx_kws)
