# pylint: skip-file
import unittest
from susi_lib.types.morse import Morse, MorseSymbol


class MorseTestCase(unittest.TestCase):
    def setUp(self):
        self.dot = MorseSymbol._MorseSymbol__dot
        self.dash = MorseSymbol._MorseSymbol__dash
        self.sym_sep = MorseSymbol._MorseSymbol__symbol_separator
        self.word_sep = MorseSymbol._MorseSymbol__word_separator
        self.empty = Morse("")
        self.separator = Morse(" ")
        self.a = Morse("a")
        self.a_morse = self.dot + self.dash
        self.x = Morse("x")
        self.x_morse = self.dash + self.dot + self.dot + self.dash
        self.e = Morse("e")
        self.e_morse = self.dot
        self.q = Morse("q")
        self.q_morse = self.dash + self.dash + self.dot + self.dash
        self.r = Morse("r")
        self.r_morse = self.dot + self.dash + self.dot
        self.text = Morse("axerq")
        self.text_morse = (
            self.dot
            + self.dash
            + self.sym_sep
            + self.dash
            + self.dot
            + self.dot
            + self.dash
            + self.sym_sep
            + self.dot
            + self.sym_sep
            + self.dot
            + self.dash
            + self.dot
            + self.sym_sep
            + self.dash
            + self.dash
            + self.dot
            + self.dash
        )
        self.text2 = Morse("axe rq")
        self.text2_morse = (
            self.dot
            + self.dash
            + self.sym_sep
            + self.dash
            + self.dot
            + self.dot
            + self.dash
            + self.sym_sep
            + self.dot
            + self.word_sep
            + self.dot
            + self.dash
            + self.dot
            + self.sym_sep
            + self.dash
            + self.dash
            + self.dot
            + self.dash
        )
        self.text3 = Morse("  axe   rq")
        self.text3_morse = (
            self.dot
            + self.dash
            + self.sym_sep
            + self.dash
            + self.dot
            + self.dot
            + self.dash
            + self.sym_sep
            + self.dot
            + self.word_sep
            + self.dot
            + self.dash
            + self.dot
            + self.sym_sep
            + self.dash
            + self.dash
            + self.dot
            + self.dash
        )

    def test_construct(self):
        self.assertEqual(str(self.empty), self.sym_sep)
        self.assertEqual(str(self.separator), self.word_sep)
        self.assertEqual(str(self.a), self.a_morse)
        self.assertEqual(str(self.x), self.x_morse)
        self.assertEqual(str(self.e), self.e_morse)
        self.assertEqual(str(self.q), self.q_morse)
        self.assertEqual(str(self.r), self.r_morse)
        self.assertEqual(str(self.text), self.text_morse)
        self.assertEqual(str(self.text2), self.text2_morse)
        self.assertEqual(str(self.text3), self.text3_morse)

    def test_add(self):
        ax = self.a + self.x
        self.assertEqual(str(ax), self.a_morse + self.sym_sep + self.x_morse)
        rax = self.r + ax
        self.assertEqual(
            str(rax),
            self.r_morse + self.sym_sep + self.a_morse + self.sym_sep + self.x_morse,
        )
        e_rax = self.empty + rax
        self.assertEqual(str(e_rax), str(rax))
        rax_e = rax + self.empty
        self.assertEqual(str(rax_e), str(rax))
        e_a = self.empty + self.a
        self.assertEqual(str(e_a), self.a_morse)
        ad = self.a + "d"
        self.assertEqual(
            str(ad), self.a_morse + self.sym_sep + self.dash + self.dot + self.dot
        )

    def test_length(self):
        self.assertEqual(len(self.empty), 0)
        self.assertEqual(len(self.separator), 0)
        self.assertEqual(len(self.a), 2)
        self.assertEqual(len(self.e), 1)
        self.assertEqual(len(self.q), 4)
        self.assertEqual(len(self.r), 3)
        self.assertEqual(len(self.text), 5)
        self.assertEqual(len(self.text2), 5)
        self.assertEqual(len(self.text3), 5)

    def test_symbol_counters(self):
        self.assertEqual(self.empty.dots, 0)
        self.assertEqual(self.empty.dashes, 0)
        self.assertEqual(self.separator.dots, 0)
        self.assertEqual(self.separator.dashes, 0)
        self.assertEqual(self.a.dots, 1)
        self.assertEqual(self.a.dashes, 1)
        self.assertEqual(self.x.dots, 2)
        self.assertEqual(self.x.dashes, 2)
        self.assertEqual(self.e.dots, 1)
        self.assertEqual(self.e.dashes, 0)
        self.assertEqual(self.q.dots, 1)
        self.assertEqual(self.q.dashes, 3)
        self.assertEqual(self.r.dots, 2)
        self.assertEqual(self.r.dashes, 1)
        self.assertEqual(self.text.dots, 7)
        self.assertEqual(self.text.dashes, 7)
        self.assertEqual(self.text2.dots, 7)
        self.assertEqual(self.text2.dashes, 7)
        self.assertEqual(self.text3.dots, 7)
        self.assertEqual(self.text3.dashes, 7)

    def test_iter(self):
        for c, exp in zip(
            self.text,
            (MorseSymbol(x) for x in ["a", "", "x", "", "e", "", "r", "", "q"]),
        ):
            self.assertEqual(c, exp)


if __name__ == "__main__":
    unittest.main()
