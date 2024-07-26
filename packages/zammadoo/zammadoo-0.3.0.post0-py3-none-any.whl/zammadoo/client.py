#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from textwrap import shorten
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
)

import requests
from requests import HTTPError, JSONDecodeError, Response

from .articles import Articles
from .groups import Groups
from .notifications import Notifications
from .organizations import Organizations
from .roles import Roles
from .tags import Tags
from .tickets import Priorities, States, Tickets
from .time_accountings import TimeAccountings
from .users import Users

if TYPE_CHECKING:
    from .utils import JsonType, StringKeyMapping

LOG = logging.getLogger(__name__)


class APIException(HTTPError):
    """APIException(...)

    Raised when the API server indicates an error.
    """

    def __init__(self, error: str, *args, response: Response, **kwargs):
        LOG.error("%s: %s", self.__class__.__name__, error)
        super().__init__(error, *args, response=response, **kwargs)


@dataclass
class Pagination:
    """pagination settings for recources ``.search()`` and ``.iter()`` methods"""

    per_page: int = 10  #: number of returned objects per page request
    #: if ``True`` the server will send additional properties for each resource
    expand: bool = False


def raise_or_return_json(response: requests.Response) -> "JsonType":
    try:
        response.raise_for_status()
    except HTTPError as exc:
        try:
            info = response.json()
            exception: HTTPError = APIException(
                info.get("error_human") or info["error"],
                request=exc.request,
                response=exc.response,
            )
        except (JSONDecodeError, KeyError):
            message = response.text
            LOG.error(
                "HTTP:%d (%s): %s", response.status_code, response.reason, message
            )
            exception = HTTPError(message, request=exc.request, response=exc.response)
        raise exception from exc

    try:
        json_response: "JsonType" = response.json()
        return json_response
    except JSONDecodeError:
        return response.text


class Client:
    """
    The root class to interact with the *REST API*.

    Almost every object keeps the initialized instance of :class:`Client` as reference.

    *Example*::

        from zammadoo import Client

        # basic authentication scheme
        client = Client("https://myhost.com/api/v1/", http_auth=("<username>", "<mysecret>"))
        # token based authentication
        client = Client("https://myhost.com/api/v1/", http_token="<secret_token>")
        # authenticate with bearer token (OAuth 2.0)
        client = Client("https://myhost.com/api/v1/", oauth2_token="<secret_token>")

    """

    _T = TypeVar("_T")

    @cached_property
    def groups(self) -> Groups:
        """Manages the ``/groups`` endpoint."""
        return Groups(self)

    @cached_property
    def notificatons(self) -> Notifications:
        """Manages the ``/online_notifications`` endpoint."""
        return Notifications(self)

    @cached_property
    def organizations(self) -> Organizations:
        """Manages the ``/organizations`` endpoint."""
        return Organizations(self)

    @cached_property
    def roles(self) -> Roles:
        """Manages the ``/roles`` endpoint."""
        return Roles(self)

    @cached_property
    def tags(self) -> Tags:
        """Manages the ``/tags``, ``/tag_list``, ``/tag_search`` endpoint."""
        return Tags(self)

    @cached_property
    def ticket_articles(self) -> Articles:
        """Manages the ``/ticket_articles`` endpoint."""
        return Articles(self)

    @cached_property
    def ticket_priorities(self) -> Priorities:
        """Manages the ``/ticket_priorities`` endpoint."""
        return Priorities(self)

    @cached_property
    def ticket_states(self) -> States:
        """Manages the ``/ticket_states`` endpoint."""
        return States(self)

    @cached_property
    def tickets(self) -> Tickets:
        """Manages the ``/tickets`` endpoint."""
        return Tickets(self)

    @cached_property
    def time_accountings(self) -> TimeAccountings:
        """Manages the ``/time_accountings`` endpoint."""
        return TimeAccountings(self)

    @cached_property
    def users(self) -> Users:
        """Manages the ``/users`` endpoint."""
        return Users(self)

    def __init__(
        self,
        url: str,
        *,
        http_auth: Optional[Tuple[str, str]] = None,
        http_token: Optional[str] = None,
        oauth2_token: Optional[str] = None,
        additional_headers: Sequence[Tuple[str, str]] = (),
    ) -> None:
        """
        For authentication use either ``http_auth`` or ``http_token`` or ``oauth2_token``.

        :param url: the zammad API url (e.g. ``https://myhost.com/api/v1``)
        :param http_auth: username and password for HTTP Basic Authentication
        :param http_token: access token when using HTTP Token Authentication
        :param oauth2_token: access token when using OAuth 2 Authentication
        :param additional_headers: additional name, value pairs that will be
                appended to the requests header ``[(name, value), ...]``
        :raises: :exc:`ValueError` if authentication settings are missing.


        """
        self.url: str = url.rstrip("/")  #: the clients API URL
        self.pagination: Pagination = Pagination()  #: initial Pagination settings
        self.session: requests.Session = (
            requests.Session()
        )  #: the requests Session instance
        self.session.headers["User-Agent"] = "zammadoo Python client"
        if http_token:
            self.session.headers["Authorization"] = f"Token token={http_token}"
        elif oauth2_token:
            self.session.headers["Authorization"] = f"Bearer {oauth2_token}"
        elif http_auth:
            self.session.auth = http_auth
        else:
            raise TypeError(f"{self.__class__} needs an authentication parameter.")

        self.session.headers.update(additional_headers)

    def __del__(self):
        self.session.close()

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.url!r}>"

    @contextmanager
    def impersonation_of(self, user: Union[str, int]):
        """
        Temporarily perform requests on behalf of another user.

        To be used as context manager::

            with client.impersonation_of(1):
                print(client.users.me().id)  # output: 1


        :param user: user id or login_name
        """
        headers = self.session.headers
        restore_value = headers.pop("X-On-Behalf-Of", None)
        try:
            headers["X-On-Behalf-Of"] = str(user)
            yield
        finally:
            if restore_value is None:
                self.session.headers.pop("X-On-Behalf-Of", None)
            else:
                headers["X-On-Behalf-Of"] = restore_value

    def request(
        self,
        method: str,
        *args,
        params: Optional["StringKeyMapping"] = None,
        json: Optional["StringKeyMapping"] = None,
        **kwargs,
    ) -> "JsonType":
        """
        Perform a request on the API URL.

        :param method: HTTP method: e.g. ``GET``, ``POST``, ``PUT``, ``DELETE``
        :param args: endpoint specifiers
        :param params: URL parameter (usually for ``GET``)
        :param json: data as dictionary (usually for ``POST`` or ``PUT``)
        :param kwargs: additional parameters passed to ``request()``
        :return: the server JSON response
        :rtype: StringKeyDict

        :raises: :exc:`APIException`, :class:`requests.HTTPError`
        """
        url = "/".join(filter(bool, map(str, args)))
        if not url.startswith(self.url):
            url = f"{self.url}/{url}" if url else self.url
        response = self.response(method, url, json=json, params=params, **kwargs)
        value = raise_or_return_json(response)
        LOG.debug("HTTP:%s returned %s", method, shorten(repr(value), width=120))
        return value

    def response(
        self,
        method: str,
        url: str,
        params: Optional["StringKeyMapping"] = None,
        json: Optional["StringKeyMapping"] = None,
        **kwargs,
    ) -> Response:
        """
        Perform a request on the API URL.

        :param method: the HTTP method (e.g. ``GET``, ``POST``, ``PUT``, ``DELETE``)
        :param url: full resource URL
        :param params: parameter that get urlencoded (usually for ``GET``)
        :param json: data as dictionary (usually for ``POST`` or ``PUT``)
        :param kwargs: additional parameters passed to ``request()``
        :rtype: :class:`requests.Response`
        """

        loglevel = LOG.getEffectiveLevel()
        response = self.session.request(
            method,
            url,
            params=(
                (key, str(value).lower() if isinstance(value, bool) else value)
                for key, value in (params.items() if params else ())
            ),
            json=json,
            **kwargs,
        )
        if kwargs.get("stream") and loglevel == logging.DEBUG:
            headers = response.headers
            mapping = dict.fromkeys(("Content-Length", "Content-Type"))
            for key in mapping:
                mapping[key] = headers.get(key)
            info = ", ".join(
                f"{key}: {value}" for key, value in mapping.items() if value
            )
            LOG.debug("HTTP:%s %s [%s]", method, response.url, info)
        elif json and loglevel == logging.DEBUG:
            LOG.debug("HTTP:%s %s json=%r", method, response.url, json)
        else:
            LOG.info("HTTP:%s %s", method, response.url)
        return response

    @overload
    def get(
        self,
        *args,
        params: Optional["StringKeyMapping"] = ...,
        _erase_return_type: Literal[False] = ...,
    ) -> "JsonType": ...

    # this allows type annotation in the assignment by mypy
    @overload
    def get(
        self,
        *args,
        params: Optional["StringKeyMapping"] = ...,
        _erase_return_type: Literal[True] = ...,
    ) -> Any: ...

    def get(self, *args, params=None, _erase_return_type=False):
        return self.request("GET", *args, params=params)

    def post(self, *args, json: Optional["StringKeyMapping"] = None):
        """shortcut for :meth:`request` with parameter ``("POST", *args, json)``"""
        return self.request("POST", *args, json=json)

    def put(self, *args, json: Optional["StringKeyMapping"] = None):
        """shortcut for :meth:`request` with parameter ``("PUT", *args, json)``"""
        return self.request("PUT", *args, json=json)

    def delete(self, *args, json: Optional["StringKeyMapping"] = None):
        """shortcut for :meth:`request` with parameter ``("DELETE", *args, json)``"""
        return self.request("DELETE", *args, json=json)

    @cached_property
    def server_version(self) -> str:
        """the Zammad server version"""
        info = self.get("version")
        assert isinstance(info, dict)
        version = info["version"]
        assert isinstance(version, str)
        return version

    @cached_property
    def weburl(self) -> str:
        url = self.url
        idx = url.rfind("/api/v")
        return url[:idx] if idx > -1 else ""
