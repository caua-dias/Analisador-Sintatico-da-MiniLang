import unittest

from minilang.lexer import Lexer


class LexerTestCase(unittest.TestCase):
    def scan(self, source):
        return Lexer(source).scan_tokens()

    def token_types(self, source):
        tokens, diagnostics = self.scan(source)
        self.assertEqual(diagnostics, [])
        return [token.type for token in tokens]

    def test_tokenizes_reference_program(self):
        source = "if(total2>=10){print(total2);}"
        self.assertEqual(
            self.token_types(source),
            [
                "KW_IF",
                "LPAREN",
                "IDENT",
                "GREATER_EQUAL",
                "INT_LITERAL",
                "RPAREN",
                "LBRACE",
                "KW_PRINT",
                "LPAREN",
                "IDENT",
                "RPAREN",
                "SEMICOLON",
                "RBRACE",
                "EOF",
            ],
        )

    def test_uses_longest_match_and_reserved_word_lookup(self):
        tokens, diagnostics = self.scan("intx===007; while1 != while")
        self.assertEqual(diagnostics, [])
        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [
                ("IDENT", "intx"),
                ("EQUAL_EQUAL", "=="),
                ("ASSIGN", "="),
                ("INT_LITERAL", "007"),
                ("SEMICOLON", ";"),
                ("IDENT", "while1"),
                ("BANG_EQUAL", "!="),
                ("KW_WHILE", "while"),
                ("EOF", ""),
            ],
        )

    def test_splits_number_and_identifier(self):
        tokens, diagnostics = self.scan("2if <= 03")
        self.assertEqual(diagnostics, [])
        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [
                ("INT_LITERAL", "2"),
                ("KW_IF", "if"),
                ("LESS_EQUAL", "<="),
                ("INT_LITERAL", "03"),
                ("EOF", ""),
            ],
        )

    def test_reports_invalid_characters_and_continues(self):
        tokens, diagnostics = self.scan("! @ !=")
        self.assertEqual(
            [token.type for token in tokens],
            ["BANG_EQUAL", "EOF"],
        )
        self.assertEqual(
            [(diagnostic.char, diagnostic.line, diagnostic.column) for diagnostic in diagnostics],
            [("!", 1, 1), ("@", 1, 3)],
        )

    def test_comments_and_whitespace_are_not_tokens(self):
        tokens, diagnostics = self.scan("// comment\nprint(x) // end")
        self.assertEqual(diagnostics, [])
        self.assertEqual(
            [(token.type, token.lexeme, token.line, token.column) for token in tokens],
            [
                ("KW_PRINT", "print", 2, 1),
                ("LPAREN", "(", 2, 6),
                ("IDENT", "x", 2, 7),
                ("RPAREN", ")", 2, 8),
                ("EOF", "", 2, 16),
            ],
        )

    def test_positions_and_single_eof(self):
        tokens, diagnostics = self.scan("int x;\nif(x<10){\n print(x);\n}")
        self.assertEqual(diagnostics, [])
        self.assertEqual(
            [(token.type, token.line, token.column) for token in tokens],
            [
                ("KW_INT", 1, 1),
                ("IDENT", 1, 5),
                ("SEMICOLON", 1, 6),
                ("KW_IF", 2, 1),
                ("LPAREN", 2, 3),
                ("IDENT", 2, 4),
                ("LESS", 2, 5),
                ("INT_LITERAL", 2, 6),
                ("RPAREN", 2, 8),
                ("LBRACE", 2, 9),
                ("KW_PRINT", 3, 2),
                ("LPAREN", 3, 7),
                ("IDENT", 3, 8),
                ("RPAREN", 3, 9),
                ("SEMICOLON", 3, 10),
                ("RBRACE", 4, 1),
                ("EOF", 4, 2),
            ],
        )
        self.assertEqual(sum(token.type == "EOF" for token in tokens), 1)

    def test_ascii_identifier_rejects_accented_character(self):
        tokens, diagnostics = self.scan("vãlor")
        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [("IDENT", "v"), ("IDENT", "lor"), ("EOF", "")],
        )
        self.assertEqual(
            [(diagnostic.char, diagnostic.line, diagnostic.column) for diagnostic in diagnostics],
            [("ã", 1, 2)],
        )


if __name__ == "__main__":
    unittest.main()
