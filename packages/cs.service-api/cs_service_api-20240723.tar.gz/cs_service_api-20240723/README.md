ServiceAPI, a base class for APIs which talk to a service,
typically a web service via HTTP.

*Latest release 20240723*:
ServiceAPI: acquire the fstags automatically at init.

An instance of a `ServiceAPI` embodies some basic features
that feel common to web based services:
- a notion of a login
- local state, an `SQLTags` for data about entities of the service
- downloads, if that is a thing, with `FSTags` for file annotations

## Class `HTTPServiceAPI(ServiceAPI)`

`HTTPServiceAPI` base class for other APIs talking to HTTP services.

Subclasses must define:
* `API_BASE`: the base URL of API calls.
  For example, the `PlayOnAPI` defines this as `f'https://{API_HOSTNAME}/v3/'`.

*`HTTPServiceAPI.json(self, suburl, _response_encoding=None, **kw)`*:
Request `suburl` from the service, by default using a `GET`.
Return the result decoded as JSON.

Parameters are as for `HTTPServiceAPI.suburl`.

*`HTTPServiceAPI.suburl(*a, upd: Optional[cs.upd.Upd] = <function uses_upd.<locals>.<lambda> at 0x102fe7060>, **kw)`*:
Request `suburl` from the service, by default using a `GET`.
The `suburl` must be a URL subpath not commencing with `'/'`.

Keyword parameters:
* `_base_url`: the base request domain, default from `self.API_BASE`
* `_method`: the request method, default `'GET'`
* `_no_raise_for_status`: do not raise an HTTP error if the
  response status is not 200, default `False` (raise if not 200)
* `cookies`: optional cookie jar, default from `self.cookies`
Other keyword parameters are passed to the requests method.

## Class `RequestsNoAuth(requests.auth.AuthBase)`

This is a special purpose subclass of `requests.auth.AuthBase`
to apply no authorisation at all.
This is for services with their own special purpose authorisation
and avoids things like automatic netrc based auth.

## Class `ServiceAPI(cs.resources.MultiOpenMixin)`

`SewrviceAPI` base class for other APIs talking to services.

*`ServiceAPI.available(self) -> Set[cs.sqltags.SQLTagSet]`*:
Return a set of the `SQLTagSet` instances representing available
items at the service, for example purchased books
available to your login.

*`ServiceAPI.get_login_state(self, do_refresh=False) -> cs.sqltags.SQLTagSet`*:
The login state, a mapping. Performs a login if necessary
or if `do_refresh` is true (default `False`).

*`ServiceAPI.login(self) -> Mapping`*:
Do a login: authenticate to the service, return a mapping of related information.

Not all services require this and we expect such subclasses
to avoid use of login-based methods.

*`ServiceAPI.login_expiry`*:
Expiry UNIX time for the login state.
This implementation returns `None`.

*`ServiceAPI.login_state`*:
The login state, a mapping. Performs a login if necessary.

*`ServiceAPI.startup_shutdown(self)`*:
Open/close the FSTags and SQLTags.

# Release Log



*Release 20240723*:
ServiceAPI: acquire the fstags automatically at init.

*Release 20230703*:
Retry logic for requests.

*Release 20230217*:
Initial release.
