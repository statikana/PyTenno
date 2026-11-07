"""Module containing custom exception classes raised by PyTenno."""

from typing import Any, Optional


class PyTennoError(Exception):
    """Base exception class for all PyTenno errors."""


class InvalidResponseError(PyTennoError):
    """Raised when the Warframe.market API returns an error status or invalid response."""

    def __init__(
        self,
        message: str = "Invalid response from Warframe.market API",
        status_code: Optional[int] = None,
        api_error: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.api_error = api_error


class UnauthorizedError(InvalidResponseError):
    """Raised when an endpoint requires authentication or credentials are invalid (HTTP 401/403)."""


class NotFoundError(InvalidResponseError):
    """Raised when the requested resource does not exist (HTTP 404)."""


class RateLimitError(InvalidResponseError):
    """Raised when the Warframe.market API rate limit is exceeded (HTTP 429)."""


class ValidationError(PyTennoError):
    """Raised when client-side or server-side request validation fails."""
