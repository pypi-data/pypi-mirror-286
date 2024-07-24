# pylint: skip-file
import unittest
from susi_lib.functions import is_palindrome
from susi_lib.types import Symbols


class MyTestCase(unittest.TestCase):
    def test_is_palindrome(self):
        self.assertEqual(is_palindrome("tacocat"), True)
        self.assertEqual(is_palindrome("abc"), False)
        self.assertEqual(is_palindrome([1, 2, 1]), True)
        self.assertEqual(is_palindrome(Symbols("tacocat")), True)


if __name__ == "__main__":
    unittest.main()
