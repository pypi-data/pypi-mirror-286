import sys
import unittest


sys.path.append("../graceful")


from graceful.response import HttpResponse


class TestHttpResponse(unittest.TestCase):
    def test_init(self):
        response = HttpResponse(
            body=b"Test Body",
            headers={"Content-Type": "text/plain"},
            status=404,
            reason="Not Found",
            ver="HTTP/2",
        )

        self.assertEqual(response.body, b"Test Body")
        self.assertEqual(response.headers, {"Content-Type": "text/plain"})
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, "Not Found")
        self.assertEqual(response.ver, "HTTP/2")

    def test_status_reason_default(self):
        response = HttpResponse(status=201)

        self.assertEqual(response.status, 201)
        self.assertEqual(response.reason, "Created")

        response.reason = "Custom Reason"

        self.assertEqual(response.status, 201)
        self.assertEqual(response.reason, "Custom Reason")

        response.status = 200
        response.reason = "OK"
        response.status = 202

        self.assertEqual(response.status, 202)
        self.assertEqual(response.reason, "Accepted")

    def test_set_cookie(self):
        response = HttpResponse()
        response.set_cookie("test_cookie", "test_value", max_age=3600)

        self.assertIn("test_cookie", response._cookies)
        self.assertEqual(response._cookies["test_cookie"].value, "test_value")
        self.assertEqual(response._cookies["test_cookie"].max_age, 3600)

    def test_delete_cookie(self):
        response = HttpResponse()
        response.set_cookie("test_cookie", "test_value")
        response.delete_cookie("test_cookie")

        self.assertNotIn("test_cookie", response._cookies)

    def test_encode(self):
        response = HttpResponse(
            body=b"Test Body",
            headers={"Content-Type": "text/plain"},
            status=200,
            reason="OK",
            ver="HTTP/1.1",
        )
        response.set_cookie("test_cookie", "test_value")
        encoded = response.encode()

        expected = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Set-Cookie: test_cookie=test_value\r\n"
            b"\r\n"
            b"Test Body"
        )

        self.assertEqual(encoded, expected)

    def test_from_bytes(self):
        raw_response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Set-Cookie: test_cookie=test_value\r\n"
            b"\r\n"
            b"Test Body"
        )
        response = HttpResponse.from_bytes(raw_response)

        self.assertEqual(response.ver, "HTTP/1.1")
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, "OK")
        self.assertEqual(response.headers, {"Content-Type": "text/plain"})
        self.assertEqual(response.body, b"Test Body")
        self.assertIn("test_cookie", response._cookies)
        self.assertEqual(response._cookies["test_cookie"].value, "test_value")

    def test_encode_decode(self):
        original_response = HttpResponse(
            body=b"Example Body",
            headers={"Content-Type": "application/json"},
            status=202,
            reason="Accepted",
            ver="HTTP/2",
        )
        original_response.set_cookie("sessionid", "12345")
        encoded = original_response.encode()
        decoded_response = HttpResponse.from_bytes(encoded)

        self.assertEqual(original_response.ver, decoded_response.ver)
        self.assertEqual(original_response.status, decoded_response.status)
        self.assertEqual(original_response.reason, decoded_response.reason)
        self.assertEqual(original_response.headers, decoded_response.headers)
        self.assertEqual(original_response.body, decoded_response.body)
        self.assertEqual(
            original_response._cookies["sessionid"].value,
            decoded_response._cookies["sessionid"].value,
        )


if __name__ == "__main__":
    unittest.main()
