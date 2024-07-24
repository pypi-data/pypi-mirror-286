# pylint: skip-file
import re
import unittest
from susi_lib.regex import create_regex, RegEx, Selection


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.text = "Lorem ipsum lolol sit amet".split(" ")

    def test_create_regex(self):
        self.assertEqual(
            create_regex(
                ("abc", Selection.NONE), ("def", Selection.INVERT), ("", Selection.ANY)
            ).get_pattern(),
            "^[abc][^def][.]$",
        )
        self.assertEqual(
            create_regex(length=5, letters="auto", invert=False).get_pattern(),
            "^[auto]{5}$",
        )
        self.assertEqual(
            create_regex(length=(5, 10), letters="auto", invert=False).get_pattern(),
            "^[auto]{5,10}$",
        )
        self.assertEqual(
            create_regex(length=5, letters="auto", invert=True).get_pattern(),
            "^[^auto]{5}$",
        )
        with self.assertRaises(TypeError):
            create_regex(("abc", Selection.NONE), ("def"), ("", Selection.ANY))
        with self.assertRaises(ValueError):
            create_regex(
                ("abc", Selection.NONE), ("def", Selection.INVERT), ("", Selection.NONE)
            )

    def test_regex(self):
        self.assertEqual(RegEx("^[asv]{4,7}$").get_pattern(), "^[asv]{4,7}$")
        with self.assertRaises(ValueError):
            _ = RegEx("^[]{4,8}$")

    def test_regex_find(self):
        r = RegEx("^.*[ae].*$")
        r.set_data(self.text)
        self.assertEqual(r.execute(), ["Lorem", "amet"])
        r.set_data("susi_lib/test/lorem.txt")
        with open("susi_lib/test/lorem.txt", "r", encoding="utf-8") as f:
            exp = re.findall(
                "^.*[ae].*$", "".join(f.readlines()), re.MULTILINE | re.IGNORECASE
            )
        self.assertEqual(r.execute(), exp)


if __name__ == "__main__":
    unittest.main()
