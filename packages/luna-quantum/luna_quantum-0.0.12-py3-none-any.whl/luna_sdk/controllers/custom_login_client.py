import logging
from http.client import UNAUTHORIZED

from httpx import Client, ReadTimeout, Response

from luna_sdk.constants import LUNA_SDK_VERSION
from luna_sdk.error.http_error_utils import HttpErrorUtils
from luna_sdk.exceptions.timeout_exception import TimeoutException


class CustomLoginClient(Client):
    _login_url: str
    _email: str
    _password: str
    _bearer_token: str

    _user_agent: str = f"LunaSDK/{LUNA_SDK_VERSION}"

    def __init__(self, email: str, password: str, login_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._email = email
        self._password = password
        self._login_url = login_url

        self.headers["User-Agent"] = self._user_agent

    def login(self, email: str, password: str):
        with Client() as client:
            headers = {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": self._user_agent,
            }

            response: Response = client.post(
                self._login_url,
                data={"username": email, "password": password},
                headers=headers,
            )
            HttpErrorUtils.check_for_error(response)

            self._bearer_token = response.json()["access_token"]

    def request(self, *args, **kwargs) -> Response:
        try:
            response: Response = super().request(*args, **kwargs)
            if response.status_code == UNAUTHORIZED:
                logging.info("Unauthorized - trying to login")

                self.login(self._email, self._password)

                logging.info("Re-login successful")
                self.headers.update(
                    headers={"authorization": f"Bearer {self._bearer_token}"}
                )
                logging.info("Trying request again")
                response = super().request(*args, **kwargs)
        except ReadTimeout as e:
            raise TimeoutException()
        HttpErrorUtils.check_for_error(response)
        return response
