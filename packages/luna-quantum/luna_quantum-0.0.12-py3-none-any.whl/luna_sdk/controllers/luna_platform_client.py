import os

from httpx import Client
from luna_sdk.controllers.custom_login_client import CustomLoginClient

from luna_sdk.interfaces.clients.client_i import IClient


class LunaPlatformClient(IClient):
    _base_url: str = ""

    _client: Client = None  # type: ignore

    def __init__(
        self,
        email: str,
        password: str,
        base_url: str = os.getenv("LUNA_BASE_URL", "https://api.aqarios.com"),
        timeout: float = 10.0,
    ):
        """
        ClientCtrl is a main entrypoint of the SDK.
        All the operations with entities should be processed using an instance of
        ClientCtrl.

        Parameters
        ----------
        email:
            User's email
        password:
            User's password
        base_url:
            Base API URL.
            If you want to use API not on your local PC then change it.
            You can do that by setting the environment variable LUNA_BASE_URL.
            Default value https://api.aqarios.com.
        timeout:
            Timeout for the requests.
            Default value 10.

        Returns
        -------
        """
        self._base_url = f"{base_url}/api"

        # setup client

        self._client = CustomLoginClient(
            email=email,
            password=password,
            login_url=f"{base_url}/accessToken",
            base_url=self._base_url,
            follow_redirects=True,
            timeout=timeout,
        )

    def __del__(self):
        if hasattr(self, "_client"):
            try:
                self._client.close()
            except Exception:
                pass  # doesn't seem to be a big deal, so just ignore
