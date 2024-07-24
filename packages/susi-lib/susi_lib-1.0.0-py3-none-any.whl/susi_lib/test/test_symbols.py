# pylint: skip-file
import unittest
from susi_lib.types import Symbols, Braille, Semaphore, Morse, NumberSystems


class SymbolsTestCase(unittest.TestCase):
    def setUp(self):
        self.a = Symbols("a")
        self.meno_mesto = Symbols("meno mesto")

    def test_to_string(self):
        self.assertEqual(str(self.a), "a")
        self.assertEqual(str(self.meno_mesto), "meno mesto")

    def test_conversions(self):
        self.assertEqual(str(self.a.to_morse()), str(Morse("a")))
        self.assertEqual(str(self.a.to_braille()), str(Braille("a")))
        self.assertEqual(str(self.a.to_semaphore()), str(Semaphore("a")))
        self.assertEqual(str(self.a.to_number_systems()), str(NumberSystems("a")))

    def test_from_string(self):
        self.assertEqual(Symbols.from_string(str(self.a.to_morse())), "a")
        self.assertEqual(Symbols.from_string(str(self.a.to_braille())), "a")
        self.assertEqual(Symbols.from_string(str(self.a.to_semaphore())), "a")
        self.assertEqual(Symbols.from_string(str(self.a.to_number_systems())), "a")

        self.assertEqual(
            Symbols.from_string(str(self.meno_mesto.to_morse())), "meno mesto"
        )
        self.assertEqual(
            Symbols.from_string(str(self.meno_mesto.to_braille())), "meno mesto"
        )
        self.assertEqual(
            Symbols.from_string(str(self.meno_mesto.to_semaphore())), "meno mesto"
        )
        self.assertEqual(
            Symbols.from_string(str(self.meno_mesto.to_number_systems())), "menomesto"
        )

    def test_add(self):
        self.assertEqual(self.a + self.a, Symbols("aa"))
        self.assertEqual(self.a + "a", Symbols("aa"))

    def test_iter(self):
        for c, exp in zip(self.meno_mesto, (Symbols(x) for x in "meno mesto")):
            self.assertEqual(c, exp)


if __name__ == "__main__":
    unittest.main()
