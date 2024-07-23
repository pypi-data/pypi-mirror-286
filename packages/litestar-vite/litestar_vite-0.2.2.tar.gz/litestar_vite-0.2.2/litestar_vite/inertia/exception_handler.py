import contextlib
import re
from typing import TYPE_CHECKING, Any, cast

from litestar import MediaType
from litestar.connection import Request
from litestar.connection.base import AuthT, StateT, UserT
from litestar.exceptions import (
    HTTPException,
    InternalServerException,
    NotAuthorizedException,
    NotFoundException,
    PermissionDeniedException,
)
from litestar.exceptions.responses import (
    create_debug_response,  # pyright: ignore[reportUnknownVariableType]
    create_exception_response,  # pyright: ignore[reportUnknownVariableType]
)
from litestar.plugins.flash import flash
from litestar.repository.exceptions import (
    NotFoundError,  # pyright: ignore[reportUnknownVariableType,reportAttributeAccessIssue]
    RepositoryError,  # pyright: ignore[reportUnknownVariableType,reportAttributeAccessIssue]
)
from litestar.response import Response
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from litestar_vite.inertia.response import InertiaBack, InertiaRedirect, InertiaResponse, error

if TYPE_CHECKING:
    from litestar_vite.inertia.plugin import InertiaPlugin

FIELD_ERR_RE = re.compile(r"field `(.+)`$")


class _HTTPConflictException(HTTPException):
    """Request conflict with the current state of the target resource."""

    status_code = HTTP_409_CONFLICT


def exception_to_http_response(request: Request[UserT, AuthT, StateT], exc: Exception) -> Response[Any]:  # noqa: PLR0911
    """Handler for all exceptions subclassed from HTTPException."""
    inertia_enabled = getattr(request, "inertia_enabled", False) or getattr(request, "is_inertia", False)
    if isinstance(exc, NotFoundError):
        http_exc = NotFoundException
    elif isinstance(exc, RepositoryError):
        http_exc = _HTTPConflictException  # type: ignore[assignment]
    else:
        http_exc = InternalServerException  # type: ignore[assignment]
    if not inertia_enabled:
        if request.app.debug and http_exc not in (PermissionDeniedException, NotFoundError):
            return cast("Response[Any]", create_debug_response(request, exc))
        return cast("Response[Any]", create_exception_response(request, http_exc(detail=str(exc.__cause__))))
    is_inertia = getattr(request, "is_inertia", False)
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    preferred_type = MediaType.HTML if inertia_enabled and not is_inertia else MediaType.JSON
    detail = getattr(exc, "detail", "")  # litestar exceptions
    extras = getattr(exc, "extra", "")  # msgspec exceptions
    content = {"status_code": status_code, "message": getattr(exc, "detail", "")}
    inertia_plugin = cast("InertiaPlugin", request.app.plugins.get("InertiaPlugin"))
    if extras:
        content.update({"extra": extras})
    with contextlib.suppress(Exception):
        flash(request, detail, category="error")
    if extras and len(extras) >= 1:
        message = extras[0]
        default_field = f"root.{message.get('key')}" if message.get("key", None) is not None else "root"  # type: ignore
        error_detail = cast("str", message.get("message", detail))  # type: ignore[union-attr] # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        match = FIELD_ERR_RE.search(error_detail)
        field = match.group(1) if match else default_field
        if isinstance(message, dict):
            with contextlib.suppress(Exception):
                error(request, field, error_detail)
    if status_code in {HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST} or isinstance(
        exc,
        PermissionDeniedException,
    ):
        return InertiaBack(request)
    if isinstance(exc, PermissionDeniedException):
        return InertiaBack(request)
    if status_code == HTTP_401_UNAUTHORIZED or isinstance(exc, NotAuthorizedException):
        redirect_to = (
            inertia_plugin.config.redirect_unauthorized_to is not None
            and str(request.url) != inertia_plugin.config.redirect_unauthorized_to
        )
        if redirect_to:
            return InertiaRedirect(request, redirect_to=cast("str", inertia_plugin.config.redirect_unauthorized_to))
        return InertiaBack(request)
    return InertiaResponse[Any](
        media_type=preferred_type,
        content=content,
        status_code=status_code,
    )
