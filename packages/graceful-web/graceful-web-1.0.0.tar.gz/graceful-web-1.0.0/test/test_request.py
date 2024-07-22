import sys
import unittest


sys.path.append("../graceful")


from graceful.request import HttpRequest


class TestHttpRequest(unittest.TestCase):
    def test_init(self):
        request = HttpRequest(
            method="POST",
            url="/test",
            body=b"Test Body",
            urlkeys={"key1": "value1"},
            queries={"query1": "value1"},
            headers={"Header1": "Value1"},
            cookies={"cookie1": "value1"},
            ver="HTTP/2",
        )

        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url, "/test")
        self.assertEqual(request.body, b"Test Body")
        self.assertEqual(request.urlkeys, {"key1": "value1"})
        self.assertEqual(request.queries, {"query1": "value1"})
        self.assertEqual(request.headers, {"Header1": "Value1"})
        self.assertEqual(request.cookies, {"cookie1": "value1"})
        self.assertEqual(request.ver, "HTTP/2")

    def test_encode(self):
        request = HttpRequest(
            method="POST",
            url="/test",
            body=b"Test Body",
            queries={"query1": "value1", "query2": "value2"},
            headers={"Header1": "Value1", "Header2": "Value2"},
            cookies={"cookie1": "value1", "cookie2": "value2"},
            ver="HTTP/2",
        )
        encoded = request.encode()

        expected = (
            b"POST /test?query1=value1&query2=value2 HTTP/2\r\n"
            b"Header1: Value1\r\n"
            b"Header2: Value2\r\n"
            b"Cookie: cookie1=value1; cookie2=value2\r\n"
            b"\r\n"
            b"Test Body"
        )

        self.assertEqual(encoded, expected)

    def test_from_bytes(self):
        raw_request = (
            b"POST /test?query1=value1&query2=value2 HTTP/2\r\n"
            b"Header1: Value1\r\n"
            b"Header2: Value2\r\n"
            b"Cookie: cookie1=value1; cookie2=value2\r\n"
            b"\r\n"
            b"Test Body"
        )
        request = HttpRequest.from_bytes(raw_request)

        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url, "/test")
        self.assertEqual(request.ver, "HTTP/2")
        self.assertEqual(request.queries, {"query1": "value1", "query2": "value2"})
        self.assertEqual(request.headers, {"Header1": "Value1", "Header2": "Value2"})
        self.assertEqual(request.cookies, {"cookie1": "value1", "cookie2": "value2"})
        self.assertEqual(request.body, b"Test Body")

    def test_encode_decode(self):
        original_request = HttpRequest(
            method="GET",
            url="/example",
            body=b"Example Body",
            queries={"foo": "bar"},
            headers={"Host": "example.com"},
            cookies={"sessionid": "12345"},
            ver="HTTP/1.1",
        )
        encoded = original_request.encode()
        decoded_request = HttpRequest.from_bytes(encoded)

        self.assertEqual(original_request.method, decoded_request.method)
        self.assertEqual(original_request.url, decoded_request.url)
        self.assertEqual(original_request.ver, decoded_request.ver)
        self.assertEqual(original_request.queries, decoded_request.queries)
        self.assertEqual(original_request.headers, decoded_request.headers)
        self.assertEqual(original_request.cookies, decoded_request.cookies)
        self.assertEqual(original_request.body, decoded_request.body)


if __name__ == "__main__":
    unittest.main()
