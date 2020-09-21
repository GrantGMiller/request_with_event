import socket


class Response:

    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = f

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            finally:
                pass
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import json
        return json.loads(self.content)


def request(method, url, data=None, json=None, headers={}, stream=None, timeout=None, send_callback=None):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
    ai = ai[0]

    s = socket.socket(ai[0], ai[1], ai[2])
    try:
        s.connect(ai[-1])
        if proto == "https:":
            s = ussl.wrap_socket(s, server_hostname=host)
        s.send("{} /{} HTTP/1.0\r\n".format(method, path).encode())
        if not "Host" in headers:
            s.send("Host: {}\r\n".format(host).encode())
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.send(k)
            s.send(b": ")
            s.send(headers[k])
            s.send(b"\r\n")
        if json is not None:
            assert data is None
            import json
            data = json.dumps(json)
            s.send(b"Content-Type: application/json\r\n")
        if data:
            s.send(b"Content-Length: %d\r\n" % len(data))
        s.send(b"\r\n")
        if data:
            s.send(data)

        if send_callback:
            send_callback()

        l = readline(s)
        raw = l
        print(l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()

        while True:
            l = readline(s)
            raw += l
            if not l or l == b"\r\n":
                break
            # print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
    except OSError:
        s.close()
        raise

    resp = Response(raw)
    resp.status_code = status
    resp.reason = reason
    return resp


def readline(s):
    l = b''
    while True:
        r = s.recv(1)
        l += r
        if r == '\n' or r == b'':
            break
    return l


def head(url, **kw):
    return request("HEAD", url, **kw)


def get(url, **kw):
    return request("GET", url, **kw)


def post(url, **kw):
    return request("POST", url, **kw)


def put(url, **kw):
    return request("PUT", url, **kw)


def patch(url, **kw):
    return request("PATCH", url, **kw)


def delete(url, **kw):
    return request("DELETE", url, **kw)


if __name__ == '__main__':
    import time


    def sent_callback():
        print('The request has finished sending at', time.time())


    resp = get('http://google.com', timeout=60, send_callback=sent_callback)
    print('response received at', time.time())
    print('resp.text=', resp.text)
