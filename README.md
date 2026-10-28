# MiniLang Lexer - Analisador Léxico Manual

## Integrantes

- [Cauã Dias] -1988941
- [Guilherme Toyoda] - 1991964
- [Joseph] -1994122
- [Lucas Belia] - 1996497
- [Lucas Naves] - 1996521
- [Lucas Henrique] - 1996594
- [Ricardo] - 2001309

## Comandos de Execução e Teste

O comando esperado para executar o analisador léxico com um arquivo-fonte é:
`python main.py examples/programa.min`.

Para executar os testes automatizados:
`python -m unittest discover -s tests -v`.

Arquivos de exemplo disponíveis:

- `examples/programa.min`: identificadores, números, operadores e diagnósticos.
- `examples/palavras_reservadas.min`: palavras reservadas, delimitadores e operadores.
- `examples/comentarios.min`: comentários de linha e código válido.
- `examples/diagnosticos.min`: caracteres ASCII inválidos e continuidade da análise.
- `examples/programa_realista.min`: exemplo de programa completo, com alguns erros

## Organização do Lexer

O analisador léxico foi implementado de forma totalmente manual e avança símbolo por símbolo da esquerda para a direita.

- Não dividimos previamente a entrada, e a leitura prioriza o maior casamento possível (lexema válido de maior comprimento) para evitar ambiguidades.
- É garantido que não utilizamos bibliotecas de tokenização, expressões regulares (`re`), a função `split` ou geradores de analisadores léxicos.
- As funções de checagem nativas `isalpha()` e `isdigit()` também não foram utilizadas para definir o alfabeto da linguagem.
- O controle de fluxo ocorre por um laço na função `scan_tokens()`, que registra a posição inicial de cada lexema e invoca `scan_token()` para decidir a classe a partir do caractere atual.
- Funções auxiliares como `advance()`, `peek()`, `peek_next()` e `match()` orquestram o consumo da string de entrada e mantêm o estado de posições (`line` e `column`) atualizado.
- Palavras reservadas são processadas consumindo primeiro o maior identificador (`IDENT`) para, em seguida, consultar a tabela de palavras-chave (`int`, `print`, `if`, `else`, `while`).

## Classes Lexicais Suportadas

O lexer processa e classifica as 11 categorias obrigatórias descritas na especificação:

- **KEYWORD_CORE:** `int`, `print`.
- **KEYWORD_EXT:** `if`, `else`, `while`.
- **IDENT:** Letras de A-Z e a-z, `_` e dígitos (apenas após o primeiro caractere).
- **INT_LITERAL:** Sequências de dígitos, suportando zeros à esquerda (sinais numéricos geram tokens separados).
- **ASSIGN:** `=`.
- **ARITH_OP:** `+`, `-`, `*`, `/`.
- **REL_OP:** `==`, `!=`, `<`, `<=`, `>`, `>=`.
- **DELIMITER_CORE:** `(`, `)`, `;`.
- **BLOCK_DELIMITER:** `{`, `}`.
- **LINE_COMMENT:** `//` contendo os símbolos seguidos até um NL, CR ou fim do arquivo.
- **WHITESPACE:** Espaços, TAB, CR e NL.

## Limitações Conhecidas e Diagnósticos

- O analisador reconhece estritamente caracteres ASCII e difere letras maiúsculas de minúsculas.
- Acentos (ex: `ã`) não pertencem ao padrão e, assim como quaisquer símbolos não reconhecidos (ex: `!` isolado ou `@`), causam a geração de um diagnóstico de erro na saída.
- Quando um erro desse tipo ocorre, o lexer registra o diagnóstico (contendo o símbolo, linha, coluna e mensagem explicativa), consome o caractere inválido e continua a varredura normalmente para evitar laços infinitos.
- Comentários e espaços em branco atualizam corretamente a contagem de posições, mas são descartados intencionalmente da lista final de tokens devolvida.
- O lexer reporta um único token `EOF` ao final, posicionado imediatamente após o último símbolo válido registrado.
