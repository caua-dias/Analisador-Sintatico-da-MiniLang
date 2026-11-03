"""Executa lexer + parser sobre um arquivo .mini e mostra tokens e AST."""

import sys
from pathlib import Path

from lexer import Lexer
from parser import Parser, ErroSintatico
from ast_printer import print_ast


def executar(codigo, mostrar_tokens=True):
    print("CÓDIGO:\n" + codigo)
    tokens, diagnosticos = Lexer(codigo).scan_tokens()

    if mostrar_tokens:
        print("\nTOKENS:")
        for t in tokens:
            print(t)

    if diagnosticos:
        print("\nDIAGNÓSTICOS LÉXICOS:")
        for d in diagnosticos:
            print(d)
        return None

    try:
        ast = Parser(tokens).parse()
    except ErroSintatico as erro:
        print(f"\n{erro}")
        return None

    print("\nAST:")
    print_ast(ast)
    return ast


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("calcula_bonus.mini")
    executar(caminho.read_text(encoding="utf-8"))
    print("\n" + "=" * 40 + "\nExemplo de erro sintático:\n")
    executar("print(2 + );", mostrar_tokens=False)


if __name__ == "__main__":
    main()
