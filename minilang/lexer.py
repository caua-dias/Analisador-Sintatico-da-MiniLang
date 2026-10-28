class Token:
    def __init__(self, type, lexeme, line, column):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type}({repr(self.lexeme)}) em {self.line}:{self.column}"

class Diagnostic:
    def __init__(self, char, line, column, message):
        self.char = char
        self.line = line
        self.column = column
        self.message = message

    def __repr__(self):
        return f"diagnóstico para {self.char} em {self.line}:{self.column}; {self.message}"

class Lexer:
    def __init__(self, source):
        self.source = source      # código-fonte completo
        self.start = 0            # índice do primeiro símbolo do lexema atual
        self.current = 0          # índice do próximo símbolo disponível
        self.line = 1             # posição associada a current
        self.column = 1           # posição associada a current
        self.start_line = 1       # posição do primeiro símbolo do lexema atual
        self.start_column = 1     # posição do primeiro símbolo do lexema atual
        self.tokens = []          # tokens produzidos
        self.diagnostics = []     # diagnósticos produzidos


    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        
        if c == '\n' or c == '\r':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        return c

    def peek(self):
        if self.at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def match(self, expected):
        if self.at_end():
            return False
        if self.source[self.current] != expected:
            return False
            
        self.advance()
        return True

    def add_token(self, token_type):
        lexeme = self.source[self.start:self.current]
        token = Token(token_type, lexeme, self.start_line, self.start_column)
        self.tokens.append(token)

    def report_invalid_character(self, c):
        message = f"Símbolo inesperado"
        diagnostic = Diagnostic(c, self.start_line, self.start_column, message)
        self.diagnostics.append(diagnostic)

    # Adicione estes métodos dentro da classe Lexer do arquivo lexer.py

    # --- Verificadores Manuais de Alfabeto (Substitutos para isalpha e isdigit) ---
    def is_alpha(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def is_digit(self, c):
        return '0' <= c <= '9'

    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    # --- Reconhecedores de Continuidade ---
    def identifier(self):
        # Consome enquanto houver letras ASCII, dígitos ASCII ou _
        while self.is_alpha_numeric(self.peek()):
            self.advance()
            
        lexeme = self.source[self.start:self.current]
        
        # Consulta tabela de palavras reservadas
        keywords = {
            "int": "KW_INT",
            "print": "KW_PRINT",
            "if": "KW_IF",
            "else": "KW_ELSE",
            "while": "KW_WHILE"
        }
        
        token_type = keywords.get(lexeme, "IDENT")
        self.add_token(token_type)

    def number(self):
        # Consome os dígitos restantes de um literal inteiro
        while self.is_digit(self.peek()):
            self.advance()
            
        self.add_token("INT_LITERAL")

    def line_comment(self):
        # Consome os símbolos do comentário até CR, NL ou fim da entrada
        while not self.at_end() and self.peek() not in ('\n', '\r'):
            self.advance()
        # Não é necessário consumir a quebra de linha aqui; scan_token tratará como whitespace

    # --- Lógica de Decisão e Laço Principal ---
    def scan_token(self):
        # Identifica a classe iniciada na posição atual e consome os símbolos necessários
        
        # Tratamento especial para início de comentário de linha //
        if self.peek() == "/" and self.peek_next() == "/":
            self.advance() # Consome primeira /
            self.advance() # Consome segunda /
            self.line_comment()
            return
            
        c = self.advance()
        
        if self.is_alpha(c):
            self.identifier()
        elif self.is_digit(c):
            self.number()
        elif c == "/":
            self.add_token("SLASH")
        elif c == "=":
            if self.match("="):
                self.add_token("EQUAL_EQUAL")
            else:
                self.add_token("ASSIGN")
        elif c == "!":
            if self.match("="):
                self.add_token("BANG_EQUAL")
            else:
                self.report_invalid_character(c)
        elif c == "<":
            if self.match("="):
                self.add_token("LESS_EQUAL")
            else:
                self.add_token("LESS")
        elif c == ">":
            if self.match("="):
                self.add_token("GREATER_EQUAL")
            else:
                self.add_token("GREATER")
        elif c in {"+", "-", "*", "(", ")", "{", "}", ";"}:
            # Mapeamento direto de símbolos simples
            simbolos = {
                "+": "PLUS", "-": "MINUS", "*": "STAR",
                "(": "LPAREN", ")": "RPAREN", "{": "LBRACE",
                "}": "RBRACE", ";": "SEMICOLON"
            }
            self.add_token(simbolos[c])
        elif c in {' ', '\t', '\r', '\n'}:
            # Elementos descartados: consome sequências de whitespace
            while self.peek() in {' ', '\t', '\r', '\n'}:
                self.advance()
        else:
            self.report_invalid_character(c)

    def scan_tokens(self):
        # Controla a varredura e registra o início de cada lexema
        while not self.at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self.scan_token()
            
        # Adiciona EOF com lexema vazio na posição imediatamente posterior
        self.tokens.append(Token("EOF", "", self.line, self.column))
        return self.tokens, self.diagnostics