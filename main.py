import sys
from minilang.lexer import Lexer

def main():
    if len(sys.argv) != 2:
        print("Uso correto: python main.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            source = arquivo.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)

    lexer = Lexer(source)
    tokens, diagnostics = lexer.scan_tokens()

    print("=== TOKENS ===")
    for token in tokens:
        print(token)

    if diagnostics:
        print("\n=== DIAGNÓSTICOS (ERROS LÉXICOS) ===")
        for diagnostic in diagnostics:
            print(diagnostic)

if __name__ == "__main__":
    main()