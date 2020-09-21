Trigger an event when the HTTP request finishes sending (but before any data is received from the server)

::

    import time

    def sent_callback():
        print('The request has finished sending at', time.time())

    resp = get('http://google.com', timeout=60, send_callback=sent_callback)
    print('response received at', time.time())

    print('resp.text=', resp.text)

Output

::

    The request has finished sending at 1600697112.7917674
    b'HTTP/1.0 301 Moved Permanently\r\nLocation: http://www.google.com/\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Mon, 21 Sep 2020 14:05:06 GMT\r\nExpires: Wed, 21 Oct 2020 14:05:06 GMT\r\nCache-Control: public, max-age=2592000\r\nServer: gws\r\nContent-Length: 219\r\nX-XSS-Protection: 0\r\nX-Frame-Options: SAMEORIGIN\r\n\r\n<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">\n<TITLE>301 Moved</TITLE></HEAD><BODY>\n<H1>301 Moved</H1>\nThe document has moved\n<A HREF="http://www.google.com/">here</A>.\r\n</BODY></HTML>\r\n'
    response received at 1600697112.8598087
    resp.text= HTTP/1.0 301 Moved Permanently
    Location: http://www.google.com/
    Content-Type: text/html; charset=UTF-8
    Date: Mon, 21 Sep 2020 14:05:06 GMT
    Expires: Wed, 21 Oct 2020 14:05:06 GMT
    Cache-Control: public, max-age=2592000
    Server: gws
    Content-Length: 219
    X-XSS-Protection: 0
    X-Frame-Options: SAMEORIGIN

    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
    <TITLE>301 Moved</TITLE></HEAD><BODY>
    <H1>301 Moved</H1>
    The document has moved
    <A HREF="http://www.google.com/">here</A>.
    </BODY></HTML>