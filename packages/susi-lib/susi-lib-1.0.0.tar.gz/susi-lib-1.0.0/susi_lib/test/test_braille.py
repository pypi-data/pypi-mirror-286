# pylint: skip-file
import unittest
from susi_lib.types.braille import Braille, BrailleChar


class BrailleTestCase(unittest.TestCase):
    def setUp(self):
        self.a = Braille("a")
        self.b = Braille("b")
        self.meno = Braille("meno")

    def test_to_string(self):
        self.assertEqual(str(self.a), "⠁")
        self.assertEqual(str(self.b), "⠃")
        self.assertEqual(str(self.meno), "⠍⠑⠝⠕")

    def test_get_points(self):
        self.assertEqual(
            self.a[0].get_points(), (True, False, False, False, False, False)
        )
        self.assertEqual(
            self.b[0].get_points(), (True, True, False, False, False, False)
        )
        self.assertEqual(
            self.meno[0].get_points(), (True, False, True, True, False, False)
        )
        self.assertEqual(
            self.meno[1].get_points(), (True, False, False, False, True, False)
        )
        self.assertEqual(
            self.meno[2].get_points(), (True, False, True, True, True, False)
        )
        self.assertEqual(
            self.meno[3].get_points(), (True, False, True, False, True, False)
        )
        with self.assertRaises(IndexError):
            _ = self.a[0][6]
        with self.assertRaises(IndexError):
            _ = self.a[0][-1]

    def test_add(self):
        self.assertEqual(str(self.a + self.b), "⠁⠃")
        self.assertEqual(str(self.a + "b"), "⠁⠃")
        self.assertEqual(str(self.a + self.b[0]), "⠁⠃")
        with self.assertRaises(TypeError):
            _ = self.a + 10

    def test_iter(self):
        for c, exp in zip(self.meno, (BrailleChar(x) for x in "meno")):
            self.assertEqual(c, exp)


if __name__ == "__main__":
    unittest.main()
