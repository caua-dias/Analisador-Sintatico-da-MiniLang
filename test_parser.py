import unittest

from lexer import Lexer
from parser import Parser, ErroSintatico
from ast_nodes import *


def analisar(codigo):
    tokens, _ = Lexer(codigo).scan_tokens()
    return Parser(tokens).parse()


def expr(codigo):
    return analisar(codigo).itens[0].expressao


class TestParser(unittest.TestCase):
    def test_precedencia(self):
        self.assertEqual(expr("print(2 + 3 * 4);"),
            Binaria(Inteiro(2), "+", Binaria(Inteiro(3), "*", Inteiro(4))))

    def test_parenteses(self):
        self.assertEqual(expr("print((2 + 3) * 4);"),
            Binaria(Binaria(Inteiro(2), "+", Inteiro(3)), "*", Inteiro(4)))

    def test_associatividade_esquerda(self):
        self.assertEqual(expr("print(10 - 3 - 2);"),
            Binaria(Binaria(Inteiro(10), "-", Inteiro(3)), "-", Inteiro(2)))
        self.assertEqual(expr("print(8 / 4 / 2);"),
            Binaria(Binaria(Inteiro(8), "/", Inteiro(4)), "/", Inteiro(2)))

    def test_variavel_valida(self):
        self.assertEqual(expr("print(y);"), Variavel("y"))

    def test_entrada_vazia(self):
        self.assertEqual(analisar(""), Programa([]))
        self.assertEqual(analisar("  \n "), Programa([]))

    def test_comentario_ignorado(self):
        self.assertEqual(analisar("// nada\nint x; // fim"), Programa([Declaracao("x")]))

    def test_programa_completo(self):
        self.assertEqual(analisar("int x;\nx = 2 + 3 * 4;\nprint(x);"), Programa([
            Declaracao("x"),
            Atribuicao("x", Binaria(Inteiro(2), "+", Binaria(Inteiro(3), "*", Inteiro(4)))),
            Saida(Variavel("x")),
        ]))

    def test_erro_expressao_incompleta(self):
        with self.assertRaises(ErroSintatico) as c:
            analisar("print(2 + );")
        self.assertIn("linha 1, coluna 11", str(c.exception))
        self.assertIn("')'", str(c.exception))

    def test_erros(self):
        for codigo in ["int x", "x = ;", "print 3;", "x = 3 4;", "int 5;",
                       ")", "print((2 + 3);", "= 3;",
                       "if (x) { }", "x = 1 == 2;"]:
            with self.subTest(codigo=codigo):
                with self.assertRaises(ErroSintatico):
                    analisar(codigo)

    def test_posicao_multilinha(self):
        with self.assertRaises(ErroSintatico) as c:
            analisar("int x;\nx = 2 +;")
        self.assertIn("linha 2, coluna 8", str(c.exception))

    def test_para_no_primeiro_erro(self):
        with self.assertRaises(ErroSintatico) as c:
            analisar("x = ;\ny = ;")
        self.assertIn("linha 1", str(c.exception))

    def test_diagnostico_lexico(self):
        _, diagnosticos = Lexer("x = 2 @ 3;").scan_tokens()
        self.assertEqual(len(diagnosticos), 1)


if __name__ == "__main__":
    unittest.main()
