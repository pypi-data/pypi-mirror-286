from datetime import date
from ssl import SSLContext
from typing import Optional, List, Dict, Union
from aia_chaser import AiaChaser

import aiohttp

from .base_pluxee_client import PassType, PluxeeBalance, PluxeeTransaction, _ResponseWrapper, _PluxeeClient
from .exceptions import PluxeeAPIError, PluxeeLoginError


class PluxeeAsyncClient(_PluxeeClient):
    """
    An asynchronous client providing information about you Pluxee balance and transactions.

    Args:
        username: The pluxee username.
        password: The pluxee password.

    Attrs:
        username: The pluxee username.
        password: The pluxee password.
    """
    def __init__(self, username: str, password: str, session: Optional[aiohttp.ClientSession] = None):
        super().__init__(username, password, session)

    async def _login(self, session: aiohttp.ClientSession):
        # call login
        async with session.post(**self.gen_login_post_args()) as response:
            # Check if we are logged in
            self.handle_login_status(response.status)

            # Setting the cookie
            try:
                key, value = response.headers["set-cookie"].split(";")[0].split("=")
                session.cookie_jar.update_cookies({key: value})
            except Exception as e:
                raise PluxeeLoginError("Could not find the cookie in the login response") from e

    async def _make_request(self, url: str, params: Dict[str, Union[str, int]], session) -> _ResponseWrapper:
        async with session.get(url, params=params) as response:
            content = await response.text()
            if 'href="/fr/user/logout"' in content:
                return _ResponseWrapper(content, response.status)

        # We got disconnected, the cookies expired
        await self._login(session)

        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise PluxeeAPIError(f"Pluxee webpage did not respond with the expected status. {response.status}")
            return _ResponseWrapper(await response.text(), response.status)

    def get_ssl_context(self, url: str) -> SSLContext:  # type: ignore
        return AiaChaser().make_ssl_context_for_url(url)

    async def get_balance(self) -> PluxeeBalance:
        """ Retrieve the balance of each pass type.

        Raises:
            PluxeeAPIError: If Pluxee webpage did not respond with the expected status or do not contain the expected information.
            PluxeeLoginError: If an error occurred with the login process.

        Returns:
            PluxeeBalance: The balance.
        """
        session = self._session
        if not session:
            ssl_context = self.get_ssl_context(self.BASE_URL_LOCALIZED)
            session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
        session: aiohttp.ClientSession

        try:
            response = await self._make_request(self.BASE_URL_LOCALIZED, {"check_logged_in": "1"}, session)
            return self._parse_balance_from_response(response)
        finally:
            if not self._session:
                await session.close()

    async def get_transactions(
        self, pass_type: PassType, since: Optional[date] = None, until: Optional[date] = None
    ) -> List[PluxeeTransaction]:
        """ Retrieve the transactions of the requested pass type in the given interval.

        Args:
            pass_type: The type of the pass for which to retrieve the transactions.
            since: The start of the interval.
            until: The start of the interval.

        Raises:
            PluxeeAPIError: If Pluxee webpage did not respond with the expected status or do not contain the expected information.
            PluxeeLoginError: If an error occurred with the login process.

        Returns:
            PluxeeBalance: The balance with the oldest elements first.
        """
        session = self._session
        if not session:
            ssl_context = self.get_ssl_context(self.BASE_URL_LOCALIZED)
            session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
        session: aiohttp.ClientSession

        try:
            transactions: List[PluxeeTransaction] = []
            page_number = 0
            complete = False
            while not complete:
                response = await self._make_request(
                    self.BASE_URL_TRANSACTIONS, {"type": pass_type.value, "page": page_number}, session
                )
                complete = self._parse_transactions_from_reponse(response, transactions, since, until)
                page_number += 1

            return transactions[::-1]
        finally:
            if not self._session:
                await session.close()
