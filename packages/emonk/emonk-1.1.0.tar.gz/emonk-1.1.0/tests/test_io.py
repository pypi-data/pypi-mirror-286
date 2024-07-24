import unittest

import emonk.config
import emonk.io


class TestTimestamp(unittest.TestCase):
    def test_timestamp(self):
        yup = "2023-11-24 17:21"
        nope = "hello"
        fmt = "%Y-%m-%d %H:%M"
        self.assertTrue(emonk.io.is_timestamp(yup, fmt))
        self.assertFalse(emonk.io.is_timestamp(nope, fmt))


class TestSplit(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(emonk.io.split(""), {})

    def test_date(self):
        s = """
        2023-10-12 11:41
        When in the course of human events it becomes necessary...

        2023-10-12 11:59
        for one people to dissolve the political bands which have
        connected them with another.

        2023-11-24 17:21
        and to assume among the powers of the earth.
        """
        d = emonk.io.split(s)
        self.assertEqual(len(d), 3)
        b1 = d["2023-10-12 11:41"]
        b2 = d["2023-10-12 11:59"]
        b3 = d["2023-11-24 17:21"]
        self.assertTrue("When in the course of human events" in b1)
        self.assertTrue("for one people to dissolve" in b2)
        self.assertTrue("and to assume among the powers" in b3)


class TestJoin(unittest.TestCase):
    def test_date(self):
        s = """
        2023-10-12 11:41
        Declaration Part I
        When in the course of human events it becomes necessary...

        2023-10-12 11:59
        Declaration Part II
        for one people to dissolve the political bands which have
        connected them with another.

        2023-11-24 17:21
        Declaration Part III
        and to assume among the powers of the earth.
        """
        d = emonk.io.split(s)
        joined = emonk.io.join(d)
        self.assertTrue("2023-10-12 11:41\nDeclaration Part I" in joined)
        self.assertTrue("2023-10-12 11:59\nDeclaration Part II" in joined)
        self.assertTrue("2023-11-24 17:21\nDeclaration Part III" in joined)


class TestCustomDate(unittest.TestCase):
    def setUp(self):
        emonk.config.CONFIG["date_format"] = "%m/%d/%y %H:%M"

    def test_custom_date(self):
        iso = "2023-10-12 11:41"
        self.assertEqual(emonk.io.iso2custom(iso), "10/12/23 11:41")
        custom = "03/14/27 03:01"
        self.assertEqual(emonk.io.custom2iso(custom), "2027-03-14 03:01")

    def tearDown(self):
        emonk.config.CONFIG["date_format"] = "%Y-%m-%d %H:%M"


if __name__ == "__main__":
    unittest.main()
