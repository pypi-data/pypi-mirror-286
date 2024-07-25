import http


class HTTPException(Exception):
    """Base class for all HTTP exceptions."""

    def __init__(self, message: str = "", status_code: int = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.status_code}: {super().__str__()}"


class BadRequest(HTTPException):
    """Raised for HTTP 400 Bad Request errors."""
    status_code = http.HTTPStatus.BAD_REQUEST.value

    def __init__(self, message: str = "Bad Request", status_code: int = None) -> None:
        super().__init__(message=message, status_code=status_code or self.status_code)


class Unauthorized(HTTPException):
    """Raised for HTTP 401 Unauthorized errors."""
    status_code = http.HTTPStatus.UNAUTHORIZED.value

    def __init__(self, message: str = "Unauthorized", status_code: int = None) -> None:
        super().__init__(message=message, status_code=status_code or self.status_code)


class Forbidden(HTTPException):
    """Raised for HTTP 403 Forbidden errors."""
    status_code = http.HTTPStatus.FORBIDDEN.value

    def __init__(self, message: str = "Forbidden", status_code: int = None) -> None:
        super().__init__(message=message, status_code=status_code or self.status_code)


class NotFound(HTTPException):
    """Raised for HTTP 404 Not Found errors."""
    status_code = http.HTTPStatus.NOT_FOUND.value

    def __init__(self, message: str = "Not Found", status_code: int = None) -> None:
        super().__init__(message=message, status_code=status_code or self.status_code)


class Conflict(HTTPException):
    """Raised for HTTP 409 Conflict errors."""
    status_code = http.HTTPStatus.CONFLICT.value

    def __init__(self, message: str = "Conflict", status_code: int = None) -> None:
        super().__init__(message=message, status_code=status_code or self.status_code)


class InternalServerError(HTTPException):
    """Raised for HTTP 500 Internal Server Error."""
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    def __init__(self, message: str = "Internal Server Error", status_code: int = None) -> None:
        super().__init__(message=message, status_code=status_code or self.status_code)
