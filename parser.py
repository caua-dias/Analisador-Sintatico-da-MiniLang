"""Parser descendente recursivo da MiniLang: tokens -> AST.

Gramática:
    programa    -> lista_itens EOF
    lista_itens -> item lista_itens | vazio
    item        -> declaracao | atribuicao | saida
    declaracao  -> KW_INT IDENT ';'
    atribuicao  -> IDENT '=' expressao ';'
    saida       -> KW_PRINT '(' expressao ')' ';'
    expressao   -> termo (('+' | '-') termo)*
    termo       -> fator (('*' | '/') fator)*
    fator       -> INT_LITERAL | IDENT | '(' expressao ')'
"""

from ast_nodes import (Inteiro, Variavel, Binaria, Declaracao,
                       Atribuicao, Saida, Programa)

# Nomes legíveis dos tipos de token, usados nas mensagens de erro.
NOMES = {
    "KW_INT": "'int'", "KW_PRINT": "'print'", "IDENT": "identificador",
    "INT_LITERAL": "número inteiro", "ASSIGN": "'='", "PLUS": "'+'",
    "MINUS": "'-'", "STAR": "'*'", "SLASH": "'/'", "SEMICOLON": "';'",
    "LPAREN": "'('", "RPAREN": "')'", "EOF": "fim da entrada",
}


class ErroSintatico(SyntaxError):
    """Erro sintático com token encontrado e posição."""


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens      # tokens produzidos pelo Lexer
        self.current = 0          # índice do token que será analisado

    # ---------- operações auxiliares ----------
    def peek(self):
        return self.tokens[self.current]

    def at_end(self):
        return self.peek().type == "EOF"

    def advance(self):
        token = self.peek()
        if not self.at_end():
            self.current += 1
        return token

    def match(self, *tipos):
        # Consome o token atual somente se for de um dos tipos pedidos.
        if self.peek().type in tipos:
            return self.advance()
        return None

    def error(self, esperado):
        t = self.peek()
        encontrado = "fim da entrada" if t.type == "EOF" else f"'{t.lexeme}'"
        raise ErroSintatico(
            f"Erro sintático na linha {t.line}, coluna {t.column}: "
            f"esperado {esperado}, encontrado {encontrado}.")

    def expect(self, tipo):
        token = self.match(tipo)
        if token is None:
            self.error(NOMES.get(tipo, tipo))
        return token

    # ---------- regras da gramática ----------
    def parse(self):
        return self.programa()

    def programa(self):
        itens = self.lista_itens()
        self.expect("EOF")
        return Programa(itens)

    def lista_itens(self):
        itens = []
        while not self.at_end():
            itens.append(self.item())
        return itens

    def item(self):
        tipo = self.peek().type
        if tipo == "KW_INT":
            return self.declaracao()
        if tipo == "IDENT":
            return self.atribuicao()
        if tipo == "KW_PRINT":
            return self.saida()
        self.error("comando ('int', identificador ou 'print')")

    def declaracao(self):
        self.expect("KW_INT")
        nome = self.expect("IDENT")
        self.expect("SEMICOLON")
        return Declaracao(nome.lexeme)

    def atribuicao(self):
        nome = self.expect("IDENT")
        self.expect("ASSIGN")
        valor = self.expressao()
        self.expect("SEMICOLON")
        return Atribuicao(nome.lexeme, valor)

    def saida(self):
        self.expect("KW_PRINT")
        self.expect("LPAREN")
        expr = self.expressao()
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        return Saida(expr)

    def expressao(self):
        esquerda = self.termo()
        while (op := self.match("PLUS", "MINUS")):
            direita = self.termo()
            esquerda = Binaria(esquerda, op.lexeme, direita)
        return esquerda

    def termo(self):
        esquerda = self.fator()
        while (op := self.match("STAR", "SLASH")):
            direita = self.fator()
            esquerda = Binaria(esquerda, op.lexeme, direita)
        return esquerda

    def fator(self):
        if (t := self.match("INT_LITERAL")):
            return Inteiro(int(t.lexeme))
        if (t := self.match("IDENT")):
            return Variavel(t.lexeme)
        if self.match("LPAREN"):
            expr = self.expressao()
            self.expect("RPAREN")
            return expr
        self.error("número, identificador ou '('")
