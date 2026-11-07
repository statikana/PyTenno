"""Module holding the Auth interface class."""

from typing import Optional

from .._backends.auth import AuthBackend
from ..models.users import CurrentUser


class Auth(AuthBackend):
    """Interface for authenticating with Warframe.market."""

    async def login(
        self,
        email: str,
        password: str,
        device_id: Optional[str] = None,
    ) -> CurrentUser:
        """Signs into Warframe.market and configures the client's ``Authorization: Bearer`` token.

        Parameters
        ----------
        email : str
            Account email address.
        password : str
            Account password.
        device_id : str, optional
            Optional device identifier string.

        Returns
        -------
        CurrentUser
            The authenticated user's profile.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     user = await tenno.auth.login("email@example.com", "password")
        ...     print("Signed in as:", user.ingame_name)
        """
        return await self._login(email, password, device_id=device_id)

    async def signout(self) -> None:
        """Signs out and terminates the current session (`POST /v2/auth/signout`)."""
        await self._signout()

    async def restore(self, email: str) -> None:
        """Sends a password reset email for the given account (`POST /v1/auth/restore`).

        Parameters
        ----------
        email : str
            The email address to send the recovery link to.
        """
        await self._restore(email)
