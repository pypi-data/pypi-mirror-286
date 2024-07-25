from __future__ import annotations

from json import JSONDecodeError
from logging import Logger, getLogger
from typing import Any

import aiohttp
from pydantic import BaseModel


class Result(BaseModel):
    """The result of a request to the De Lijn API

    Attributes:
        status_code (int): The status code of the request
        message (str, optional): The message of the request. Defaults to "".
        data (dict[str, Any] | None, optional): The data of the request. Defaults to None.
    """

    status_code: int
    message: str = ""
    data: dict[str, Any] | None = None


class DeLijnAPIException(Exception): ...


class RestAdapter:
    def __init__(
        self,
        hostname: str = "api.delijn.be",
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: Logger | None = None,
    ):
        """
        Constructor for RestAdapter

        Args:
            hostname (str, optional): The hostname of the API. Defaults to "api.delijn.be".
            api_key (str, optional): The API key to use for authentication. Defaults to "".
            ver (str, optional): The version of the API to use. Defaults to "v1".
            ssl_verify (bool, optional): Whether to verify the SSL certificate. Defaults to True.
            logger (Logger | None, optional): The logger to use for logging. Defaults to None.
        """
        self.url = f"https://{hostname}/{ver}"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or getLogger(__name__)

    async def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params: dict | None = None,
        data: dict | None = None,
    ) -> Result:
        """Perform an HTTP request to the API and return a Result object

        Args:
            http_method (str): The HTTP method to use (GET, POST, DELETE)
            endpoint (str): The endpoint on the API to request
            ep_params (dict | None, optional): Parameters to give to the endpoint. Defaults to None.
            data (dict | None, optional): Data to pass through to the endpoint. Defaults to None.

        Raises:
            DeLijnAPIException: If the request fails or the response is not in the 200-299 range

        Returns:
            Result: The result of the request
        """
        full_url = self.url + endpoint
        headers = {"Ocp-Apim-Subscription-Key": self._api_key}

        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )
        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            self._logger.debug(msg=log_line_pre)
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=http_method,
                    url=full_url,
                    headers=headers,
                    params=ep_params,
                    json=data,
                ) as result:
                    response = result
                    data_out = await response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise DeLijnAPIException("Bad JSON in response") from e
        except Exception as e:
            self._logger.error(msg=(str(e)))
            raise DeLijnAPIException("Request failed") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status >= 200
        log_line = log_line_post.format(is_success, response.status, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(
                status_code=response.status,
                message=response.reason or "No reason given",
                data=data_out,
            )
        self._logger.error(msg=log_line)
        raise DeLijnAPIException(f"{response.status}: {response.reason}")

    async def get(self, endpoint: str, ep_params: dict | None = None) -> Result:
        """Perform a GET request to the API

        Args:
            endpoint (str): The endpoint on the API to GET
            ep_params (dict | None, optional): Parameters to give to the endpoint. Defaults to None.

        Returns:
            Result: The result of the GET request
        """
        return await self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    async def post(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None
    ) -> Result:
        """Perform a POST request to the API

        Args:
            endpoint (str): The endpoint on the API to POST
            ep_params (dict | None, optional): Parameters to give to the endpoint. Defaults to None.
            data (dict | None, optional): Data to pass through to the endpoint. Defaults to None.

        Returns:
            Result: The result of the POST request
        """
        return await self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )

    async def delete(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None
    ) -> Result:
        """Perform a DELETE request to the API

        Args:
            endpoint (str): The endpoint on the API to DELETE
            ep_params (dict | None, optional): Parameters to give to the endpoint. Defaults to None.
            data (dict | None, optional): Data to pass through to the endpoint. Defaults to None.

        Returns:
            Result: The result of the DELETE request
        """
        return await self._do(
            http_method="DELETE", endpoint=endpoint, ep_params=ep_params, data=data
        )
