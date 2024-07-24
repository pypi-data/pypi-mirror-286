# pylint: skip-file
import unittest
from susi_lib.finder import Finder
from susi_lib.functions import is_palindrome


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.text = "Lorem ipsum lolol sit amet".split(" ")
        self.f1 = is_palindrome
        self.f2 = lambda word: len(word) == 5

    def test_find_first(self):
        finder = Finder(self.text, self.f2)
        self.assertEqual(finder.find_first(), "Lorem")

    def test_find_all(self):
        finder = Finder(self.text, self.f2)
        self.assertEqual(finder.find_all(), ["Lorem", "ipsum", "lolol"])

    def test_modify_function(self):
        finder = Finder(self.text, self.f2)
        finder.change_function(self.f1)
        self.assertEqual(finder.find_first(), "lolol")
        self.assertEqual(finder.find_all(), ["lolol"])
        finder.add_function(self.f2)
        self.assertEqual(finder.find_first(), "lolol")
        self.assertEqual(finder.find_all(), ["lolol"])
        finder.add_function(lambda word: False)
        self.assertEqual(finder.find_first(), None)
        self.assertEqual(finder.find_all(), [])

    def test_iterate(self):
        finder = Finder(self.text, self.f2)
        for found, exp in zip(finder, ["Lorem", "ipsum", "lolol"]):
            self.assertEqual(found, exp)

    def test_from_file(self):
        finder = Finder("susi_lib/test/lorem.txt", self.f2)
        self.assertEqual(finder.find_first(), "Lorem")
        exp = [
            "Lorem",
            "ipsum",
            "dolor",
            "amet,",
            "elit.",
            "ipsum",
            "Nulla",
            "felis",
            "vitae",
            "justo",
            "augue",
            "nibh.",
            "Morbi",
            "metus",
            "Proin",
            "justo",
            "eros.",
            "purus",
            "odio.",
            "Donec",
            "neque",
            "Lorem",
            "ipsum",
            "dolor",
            "amet,",
            "elit.",
            "Lorem",
            "ipsum",
            "dolor",
            "amet,",
            "elit.",
            "elit,",
            "ipsum",
            "Nulla",
            "quam,",
            "Nulla",
            "massa",
            "eros,",
            "Fusce",
            "magna",
            "Etiam",
            "ipsum",
            "Nulla",
            "odio,",
            "magna",
            "nisi.",
            "nibh.",
            "magna",
            "arcu.",
            "diam,",
            "Morbi",
            "risus",
            "lorem",
            "metus",
            "velit",
            "justo",
            "nulla",
            "justo",
            "porta",
            "nunc.",
            "Nulla",
            "urna,",
            "dolor",
            "Donec",
            "purus",
            "velit",
            "vitae",
            "augue",
            "diam.",
            "risus",
            "vitae",
            "Morbi",
            "quam.",
            "amet,",
            "arcu,",
            "nulla",
            "Nulla",
            "vitae",
            "Fusce",
            "elit,",
            "quam.",
            "felis",
            "Donec",
            "augue",
            "eros.",
            "Etiam",
            "odio.",
        ]
        self.assertEqual(finder.find_all(), exp)
        for found, ex in zip(finder, exp):
            self.assertEqual(found, ex)


if __name__ == "__main__":
    unittest.main()
