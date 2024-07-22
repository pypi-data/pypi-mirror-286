import sys
import unittest
from datetime import datetime, timedelta


sys.path.append("../graceful")


from graceful.cookie import Cookie


class TestCookie(unittest.TestCase):
    def test_initialization_default(self):
        cookie = Cookie(name="test_cookie")

        self.assertEqual(cookie.name, "test_cookie")
        self.assertEqual(cookie.value, "")
        self.assertIsNone(cookie.expires)
        self.assertIsNone(cookie.max_age)
        self.assertIsNone(cookie.domain)
        self.assertIsNone(cookie.path)
        self.assertFalse(cookie.secure)
        self.assertFalse(cookie.httponly)
        self.assertIsNone(cookie.samesite)

    def test_initialization_with_all_params(self):
        expires_date = datetime(2024, 12, 31, 23, 59, 59)
        cookie = Cookie(
            name="test_cookie",
            value="test_value",
            expires=expires_date,
            max_age=3600,
            domain="example.com",
            path="/",
            secure=True,
            httponly=True,
            samesite="lax",
        )

        self.assertEqual(cookie.name, "test_cookie")
        self.assertEqual(cookie.value, "test_value")
        self.assertEqual(cookie.expires, expires_date)
        self.assertEqual(cookie.max_age, 3600)
        self.assertEqual(cookie.domain, "example.com")
        self.assertEqual(cookie.path, "/")
        self.assertTrue(cookie.secure)
        self.assertTrue(cookie.httponly)
        self.assertEqual(cookie.samesite, "lax")

    def test_expires_datetime(self):
        expires_date = datetime(2024, 12, 31, 23, 59, 59)
        cookie = Cookie(name="test_cookie", expires=expires_date)

        self.assertEqual(cookie.expires, expires_date)

    def test_expires_string(self):
        expires_string = "2024-12-31T23:59:59"
        cookie = Cookie(name="test_cookie", expires=expires_string)

        expected_date = datetime.fromisoformat(expires_string)

        self.assertEqual(cookie.expires, expected_date)

    def test_expires_int(self):
        now = datetime.now()
        cookie = Cookie(name="test_cookie", expires=3600)

        expected_expires = now + timedelta(seconds=3600)

        self.assertTrue(cookie.expires > now)
        self.assertTrue(cookie.expires < expected_expires + timedelta(seconds=1))

    def test_expires_none(self):
        cookie = Cookie(name="test_cookie", expires=None)

        self.assertIsNone(cookie.expires)

    def test_str_method(self):
        expires_date = datetime(2024, 12, 31, 23, 59, 59)
        cookie = Cookie(
            name="test_cookie",
            value="test_value",
            expires=expires_date,
            max_age=3600,
            domain="example.com",
            path="/",
            secure=True,
            httponly=True,
            samesite="lax",
        )

        expected_str = (
            "test_cookie=test_value; Expires=Tue, 31 Dec 2024 23:59:59 GMT; "
            "Max-Age=3600; Domain=example.com; Path=/; Secure; HttpOnly; SameSite=Lax"
        )

        self.assertEqual(str(cookie), expected_str)

    def test_str_method_no_params(self):
        cookie = Cookie(name="test_cookie")

        expected_str = "test_cookie="

        self.assertEqual(str(cookie), expected_str)

    def test_str_method_with_only_expires(self):
        expires_date = datetime(2024, 12, 31, 23, 59, 59)
        cookie = Cookie(name="test_cookie", expires=expires_date)

        expected_str = "test_cookie=; Expires=Tue, 31 Dec 2024 23:59:59 GMT"

        self.assertEqual(str(cookie), expected_str)


if __name__ == "__main__":
    unittest.main()
