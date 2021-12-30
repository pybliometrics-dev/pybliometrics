#!/usr/bin/env python
# Taken from: https://stackoverflow.com/a/60031108/1719931

import sys
import re

if sys.version_info[0] == 2:
    import httplib
    import urlparse
else:
    import http.client as httplib
    import urllib.parse as urlparse

import requests
from requests.packages import urllib3
from requests.compat import urlparse as _urlparse

def dbg_print(fmt, *args):
    if False:
        sys.stderr.write(fmt % args)
        sys.stderr.write("\n")

# HTTP Digest authentication for proxy
# The main differences with HTTPDigestAuth are:
#   - Proxy HTTP status is 407 when authentication is required (instead of 401)
#   - The related request/response headers are Proxy-Authorization/Proxy-Authenticate (instead of
#     Authorization/WWW-Authenticate)
#   - When proxying HTTPS, the method is CONNECT and the uri is the address:port of the webserver
#   - A webserver authentication instance can be associated with HTTPDigestAuth so that proxy
#     authentication does not prevent webserver authentication

class HTTPProxyDigestAuth(requests.auth.HTTPDigestAuth):
    # self._thread_local.num_401_calls should be self._thread_local.num_407_calls
    # handle_401() should be handle_407()
    # We keep the original names to reduce the changes count

    def __init__(self, username, password, auth=None):
        super(HTTPProxyDigestAuth, self).__init__(username, password)

        # AuthBase instance for website (not proxy)
        self.auth = auth

    def build_digest_header(self, method, url):
        # For HTTPS, replace uri and method
        url_parsed = urlparse.urlparse(url)
        if url_parsed.scheme.lower() == 'https':
            # URI is the CONNECT path
            if url_parsed.port is None:
                url = url_parsed.netloc + ':443'
            else:
                url = url_parsed.netloc
            method = 'CONNECT'

        return super(HTTPProxyDigestAuth, self).build_digest_header(method, url)

    def handle_401(self, r, **kwargs):
        """
        Takes the given response and tries digest-auth, if needed.
        :rtype: requests.Response
        """

        # If response is not 407, do not auth
        if r.status_code != 407:
            self._thread_local.num_401_calls = 1
            return r

        dbg_print("handle_407")

        if self._thread_local.pos is not None:
            # Rewind the file position indicator of the body to where
            # it was to resend the request.
            r.request.body.seek(self._thread_local.pos)
        s_auth = r.headers.get('proxy-authenticate', '')

        if 'digest' in s_auth.lower() and self._thread_local.num_401_calls < 2:
            self._thread_local.num_401_calls += 1
            pat = re.compile(r'digest ', flags=re.IGNORECASE)
            self._thread_local.chal = requests.utils.parse_dict_header(
                    pat.sub('', s_auth, count=1))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.close()
            prep = r.request.copy()
            requests.cookies.extract_cookies_to_jar(prep._cookies, r.request, r.raw)
            prep.prepare_cookies(prep._cookies)

            # FIXME Put that header in the proxy headers
            prep.headers['Proxy-Authorization'] = self.build_digest_header(prep.method, prep.url)
            _r = r.connection.send(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep

            return _r

        self._thread_local.num_401_calls = 1
        return r

    def __call__(self, r):
        # Initialize per-thread state, if needed
        self.init_per_thread_state()
        # If we have a saved nonce, skip the 401
        if self._thread_local.last_nonce:
            # FIXME When connection is tunneled, there's no need to add this header for each request
            r.headers['Proxy-Authorization'] = self.build_digest_header(r.method, r.url)
        try:
            self._thread_local.pos = r.body.tell()
        except AttributeError:
            # In the case of HTTPDigestAuth being reused and the body of
            # the previous request was a file-like object, pos has the
            # file position of the previous body. Ensure it's set to
            # None.
            self._thread_local.pos = None
        r.register_hook('response', self.handle_401)
        r.register_hook('response', self.handle_redirect)
        self._thread_local.num_401_calls = 1

        if self.auth is not None:
            # Forward to site auth
            r = self.auth(r)

        return r

# The following code changes the behavior of urllib3 and httplib/http.client to be able to forward
# proxy authentication error as a HTTP response (instead of an I/O exception) when tunneling
# a HTTPS connection. The main idea is to make httplib/http.client believe the proxy response
# is the webserver response, so that it forwards it to urllib3.
# The changes are:
#   - The httplib.HTTPConnection._tunnel() method is called when there is a need to proxy
#     HTTPS requests. If the proxy reports an authentication error (407), we raise a ProxyError.
#     As we cannot alter the _tunnel() method without re-coding it, we change the class for HTTP
#     response with our own (HTTPProxyResponse), and this is that class that will raise the
#     ProxyError when parsing the HTTP status line from proxy. Raising a ProxyError prevents the
#     _tunnel() method from consuming the proxy response (except its status line that we store
#     in httplib.HTTPConnection to pretend later it comes from webserver).
#   - The ProxyError is catched in the hooked urllib3.connection.HTTPSConnection.connect() method.
#     In the exception handler, we replace the HTTP response class again with our own
#     (BufferedHTTPResponse) so that we can forward the proxy status line as if it came from the
#     webserver.
#   - The exception prevents the establishement of the SSL/TLS communication, so the connection
#     must not be used anymore after the processing of current request. This explains why the
#     BufferedHTTPResponse._check_close() method always returns True.
#   - Once the connection has been established, the request is sent to the webserver. Since
#     we already know the proxy refused the connection, there is no need to send the request
#     to webserver, so we drop it by hooking the urllib3.connection.HTTPConnection.send() method.
#   - The BufferedHTTPResponse instance will be created in HTTPConnection.getresponse(). Once the
#     stored status line has been read, the rest of the reponse is read directly from the socket
#     as this is the case when reading webserver response (except the reponse comes from proxy
#     this time).
#   - To make sure proxy authentication data is sent to proxy (and only it), we hook the
#     urllib3.connectionpool.HTTPConnectionPool.urlopen() method to move Proxy-Authorization header
#     from request to the dedicated list of proxy headers (proxy_headers property). These headers
#     will be sent to proxy by the _tunnel() method.

def hook(cls, name=None):
    def decorator(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(original, *args, **kwargs)

        if name is None:
            # cls is name
            g = globals()
            original = g[cls]
            g[cls] = wrapper
        else:
            def dummy(*args, **kwargs):
                pass

            original = getattr(cls, name, dummy)
            setattr(cls, name, wrapper)

        return wrapper

    return decorator

def hook_trace(cls, name=None):
    path = cls if name is None else (cls.__name__ + '.' + name)

    def print_trace(original, *args, **kwargs):
        dbg_print('TRACE<%s>', path)
        return original(*args, **kwargs)

    hook(cls, name)(print_trace)

class ProxyError(RuntimeError):
    pass

class HTTPProxyResponse(httplib.HTTPResponse):
    _status_line = None

    def __init__(self, sock, *args, **kwargs):
        httplib.HTTPResponse.__init__(self, sock, *args, **kwargs)
        # This is the proxy response (for CONNECT), make sure it is not buffered
        # as we want to pretend this is the server response in case of 407
        if sys.version_info[0] == 2:
            self.fp = sock.makefile('rb', 0)
        else:
            self.fp = sock.makefile("rb", buffering=0)

    def _read_status(self):
        (version, status, reason) = httplib.HTTPResponse._read_status(self)
        dbg_print(str((version, status, reason)))

        if status == 407:
            # We need to forward error from proxy
            self._status_line = (version, status, reason)
            raise ProxyError()

        return (version, status, reason)

class BufferedHTTPResponse(httplib.HTTPResponse):
    _status_line = None

    def _read_status(self):
        dbg_print('%s', self.fp)
        return self._status_line

    def _check_close(self):
        res = httplib.HTTPResponse._check_close(self)
        dbg_print("_check_close => %s", res)
        # Make sure to close the connection because it is supposed to be encrypted
        # and we made sure it is not
        return True
        # return False

# class Proxy(object):
#     _target = None
# 
#     def __init__(self, target):
#         self._target = target
# 
#     def __getattr__(self, name):
#         if name == '_target': return super(Proxy, self).__getattr__(name)
# 
#         dbg_print('%s.%s', self._target, name)
#         # import traceback; traceback.print_stack()
# 
#         return getattr(self._target, name)
# 
#     def __setattr__(self, name, value):
#         if name == '_target': return super(Proxy, self).__setattr__(name, value)
#         return setattr(self._target, name, value)
# 
#     def __delattr__(self, name):
#         if name == '_target': return super(Proxy, self).__delattr__(name)
#         return delattr(self._target, name)
# 
# class ReaderProxy(Proxy):
#     def readline(self, size=-1):
#         dbg_print('%s.readline(%s)', self._target, size)
#         return self._target.readline(size)

@hook(httplib.HTTPConnection, '_tunnel')
def HTTPConnection__tunnel_hook(original, self, *args, **kwargs):
    # Replace response_class in order to hook response
    resp = [None]
    def resp_builder(*args, **kwargs):
        dbg_print('HTTPProxyResponse.__init__')
        resp[0] = r = HTTPProxyResponse(*args, **kwargs)
        # r.fp = ReaderProxy(r.fp)
        return r
    response_class = self.response_class
    self.response_class = resp_builder

    try:
        original(self, *args, **kwargs)
    finally:
        resp = resp[0]
        if resp is not None and resp._status_line is not None:
            # Copy status line to send it to client later
            self._status_line = resp._status_line

        # Undo our changes
        self.response_class = response_class

# @hook(urllib3.connection.HTTPConnection, '_new_conn')
# def urllib3_connection_HTTPConnection__new_conn_hook(original, self, *args, **kwargs):
#     if self._sock is not None:
#         # Connection to proxy that refused first CONNECT
#         return self._sock
#     return original(self, *args, **kwargs)

@hook(urllib3.connection.HTTPSConnection, 'connect')
def urllib3_connection_HTTPSConnection_connect_hook(original, self, *args, **kwargs):
    # Reset
    self._status_line = None

    try:
        original(self, *args, **kwargs)
    except ProxyError as e:
        # Raising and catching this exception prevent the connection from being encrypted
        dbg_print("ProxyError")
        self.is_verified = True

        # HTTPConnection.getresponse must process proxy response (not site)
        # This can be done by changing response_class in case of proxy error so that the
        # new response will forward the already read HTTP status and continue parsing
        # the response body from proxy as if it comes from client
        # We should only do that for 4xx and 5xx status to prevent abuse from proxy

        # Replace response_class in order to hook response
        def resp_builder(*args, **kwargs):
            dbg_print('BufferedHTTPResponse.__init__')
            r = BufferedHTTPResponse(*args, **kwargs)
            r._status_line = self._status_line
            # r.fp = ReaderProxy(r.fp)
            self.response_class = response_class
            return r

        # import pdb; pdb.set_trace()

        response_class = self.response_class
        self.response_class = resp_builder

@hook(urllib3.connection.HTTPConnection, 'send')
def urllib3_connection_HTTPConnection_send_hook(original, self, *args, **kwargs):
    if self._status_line is not None:
        dbg_print("send(%d)", len(args[0]))
        # Prevent sending anything more to proxy
        pass
    else:
        # if args[0].startswith('CONNECT '):
        #     args = list(args)
        #     args[0] = args[0].replace('HTTP/1.0', 'HTTP/1.1')
        #     print(args[0])
        return original(self, *args, **kwargs)

@hook(urllib3.connection.HTTPConnection, '__init__')
def urllib3_connection_HTTPConnection___init___hook(original, self, *args, **kwargs):
    self._status_line = None
#     self._sock = None
    return original(self, *args, **kwargs)

@hook(urllib3.connectionpool.HTTPConnectionPool, 'urlopen')
def urllib3_connectionpool_HTTPConnectionPool_urlopen_hook(original, self, *args, **kwargs):
    headers = kwargs.get('headers', self.headers)

    # Put proxy headers in proxy_headers
    # self.proxy_headers['Proxy-Connection'] = 'Keep-Alive'
    for (name, value) in list(headers.items()):
        if name.lower() == 'proxy-authorization':
            del headers[name]
            self.proxy_headers[name] = value
            dbg_print("<PROXY> %s: %s", name, value)

    return original(self, *args, **kwargs)

# @hook(urllib3.connectionpool.HTTPConnectionPool, '_get_conn')
# def urllib3_connectionpool_HTTPConnectionPool__get_conn_hook(original, self, *args, **kwargs):
#     conn = original(self, *args, **kwargs)
#     if conn._status_line is not None:
#         # Pretend socket is not defined so that SSL/TLS connection is setup again
#         # if proxy does not refuse password
#         conn._sock = conn.sock
#         conn.sock = None
# 
#     return conn

# hook_trace(httplib.HTTPConnection, 'close')
