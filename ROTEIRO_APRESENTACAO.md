# 🎙️ Roteiro de Apresentação (Divisão para 5 Pessoas)
## Trabalho 02: Analisador Sintático da MiniLang

- **Duração Total Sugerida:** 10 a 15 minutos (~2 a 3 minutos por pessoa).
- **Referências:** 
  - *Aula 08: FIRST, FOLLOW e Análise LL(1)*
  - *Aula 09: Trabalho 02 - Analisador Sintático da MiniLang*

---

### Tabela Resumo das Funções

| Integrante | Tópico Principal | Propósito no Projeto | Base nos PDFs |
| :--- | :--- | :--- | :--- |
| **Pessoa 1** | **Introdução e Fundamentos LL(1)** | Contextualizar o pipeline e os princípios teóricos de análise preditiva. | Aula 08 (Slides 1–4, 54–57) & Aula 09 (Slide 1) |
| **Pessoa 2** | **Gramática da MiniLang e Escopo** | Apresentar a gramática formal e delimitar o escopo (não-tangenciamento). | Aula 09 (Slides 2 e 3) |
| **Pessoa 3** | **Arquitetura do Parser e Expressões** | Explicar o parser descendente recursivo, precedência e associatividade. | Aula 08 (Exercício 7) & Aula 09 (Slide 5 - Etapa 1) |
| **Pessoa 4** | **Construção da AST e Comandos** | Detalhar os nós da AST e o reconhecimento dos comandos do programa. | Aula 09 (Slides 2, 4 e 5 - Etapa 2) |
| **Pessoa 5** | **Diagnósticos de Erro, Testes e Conclusão** | Demonstrar robustez com localização de erros, bateria de testes e entrega. | Aula 09 (Slides 5, 6 e 7) |

---

## 👤 Pessoa 1: Introdução, Pipeline e Fundamentação LL(1)

* **Tempo:** 2 a 3 minutos.
* **Tópico:** O papel do analisador sintático no pipeline do compilador e a fundamentação preditiva LL(1).
* **Propósito no projeto:** Situar o problema, demonstrar a transição dos dados (`Código -> Tokens -> AST`) e conectar a teoria de parsers determinísticos da Aula 08 com a prática do projeto.
* **Pontos da Fala:**
  1. **Objetivo geral:** Desenvolver um analisador sintático para a linguagem MiniLang que recebe uma sequência de tokens do Lexer e gera a Árvore Sintática Abstrata (AST).
  2. **Pipeline do compilador (Aula 09, Slide 1):** Destacar o fluxo `Código-fonte -> Lexer -> Tokens -> Parser -> AST`.
  3. **Conceitos de LL(1) e Lookahead (Aula 08, Slides 4 e 55):**
     - $L$: Leitura da esquerda para a direita (*Left-to-right*).
     - $L$: Construção da derivação mais à esquerda (*Leftmost derivation*).
     - $1$: Uso de **1 token de consulta antecipada** (*lookahead*).
     - *Regra fundamental da aula:* **Consultar não consome**. A operação `peek()` apenas inspeciona o primeiro token não consumido, permitindo decidir qual produção gramatical aplicar sem descartá-lo antes da hora.
* **Telas/Slides sugeridos:** Diagrama em blocos do pipeline do compilador e esquema conceitual de consulta antecipada com pilha.
* **Frase de transição:** *"Para entender como essas decisões são tomadas pelo parser, a [Pessoa 2] vai apresentar a gramática formal da MiniLang e as fronteiras do nosso escopo."*

---

## 👤 Pessoa 2: A Gramática da MiniLang e Delimitação de Escopo

* **Tempo:** 2 a 3 minutos.
* **Tópico:** Especificação gramatical e garantia de não-tangenciamento do tema.
* **Propósito no projeto:** Apresentar formalmente as regras de produção da linguagem e justificar as decisões de projeto que garantem a aderência estrita à especificação da Aula 09.
* **Pontos da Fala:**
  1. **A Gramática da MiniLang (`parser.py`):**
     - `programa    -> lista_itens EOF`
     - `lista_itens -> item lista_itens | ε`
     - `item        -> declaracao | atribuicao | saida`
     - `declaracao  -> 'int' IDENT ';'`
     - `atribuicao  -> IDENT '=' expressao ';'`
     - `saida       -> 'print' '(' expressao ')' ';'`
  2. **Requisitos Obrigatórios (Aula 09, Slide 3):**
     - Suporte a declaração de inteiros, identificadores, atribuições, comando `print`, expressões com operadores `+`, `-`, `*`, `/`, parênteses e fim completo de arquivo (`EOF`).
  3. **Garantia de Não-Tangenciamento (Aula 09, Slide 3):**
     - Explicar por que o projeto **não tangenciou**: não implementou estruturas condicionais (`if/else`) ou de repetição (`while`), escopos aninhados ou operadores unários.
     - Enfatizar que variáveis não declaradas são aceitas sintaticamente (ex: `print(y);`), pois a análise semântica e a execução do código estão explicitamente fora do escopo do Trabalho 02.
* **Telas/Slides sugeridos:** Tabela da gramática formal e quadro comparativo *"Obrigatório vs. Fora do Escopo"*.
* **Frase de transição:** *"Com as regras da linguagem estabelecidas, a [Pessoa 3] vai explicar a arquitetura do parser descendente recursivo e como resolvemos a precedência e associatividade das expressões."*

---

## 👤 Pessoa 3: Arquitetura do Parser e Expressões Aritméticas (Etapa 1)

* **Tempo:** 2 a 3 minutos.
* **Tópico:** Implementação do parser descendente recursivo e análise de expressões aritméticas.
* **Propósito no projeto:** Explicar como a gramática foi mapeada em código Python e como a hierarquia de funções resolve precedência e associatividade sem recursão à esquerda direta.
* **Pontos da Fala:**
  1. **Técnica Descendente Recursiva:**
     - Cada símbolo não-terminal da gramática vira um método em Python (`expressao()`, `termo()`, `fator()`).
     - Primitivas implementadas: `peek()` (inspeção), `advance()` (consumo), `match(*tipos)` (consumo condicional) e `expect(tipo)` (consumo obrigatório ou erro).
  2. **Decomposição em Camadas (Aula 09, Slide 5 - Etapa 1):**
     - `expressao()` $\to$ resolve adições e subtrações (`+` e `-`), chamando `termo()`.
     - `termo()` $\to$ resolve multiplicações e divisões (`*` e `/`), chamando `fator()`.
     - `fator()` $\to$ consome números inteiros, identificadores ou subexpressões delimitadas por parênteses `( expressao )`.
  3. **Precedência e Associatividade à Esquerda (Aula 09, Slide 6):**
     - **Precedência:** `*` e `/` são resolvidos em camadas mais profundas da chamada, fazendo com que em `2 + 3 * 4` a multiplicação seja calculada antes.
     - **Associatividade à esquerda:** Resolvida sem recursão à esquerda por meio de um laço `while (op := self.match("PLUS", "MINUS"))`, aninhando nós `Binaria(esquerda, op, direita)` da esquerda para a direita (ex: `10 - 3 - 2` vira `((10 - 3) - 2)`).
* **Telas/Slides sugeridos:** Trecho do código dos métodos `expressao()` e `termo()` em Python e diagrama da árvore da expressão `2 + 3 * 4`.
* **Frase de transição:** *"Visto o motor de expressões, a [Pessoa 4] vai detalhar como o parser monta a Árvore Sintática Abstrata (AST) para os comandos e para o programa completo."*

---

## 👤 Pessoa 4: Construção da AST e Reconhecimento de Comandos (Etapa 2)

* **Tempo:** 2 a 3 minutos.
* **Tópico:** Modelagem dos nós da AST em `ast_nodes.py` e o fluxo de comandos (Etapa 2).
* **Propósito no projeto:** Apresentar a estrutura de dados intermediária produzida pelo compilador e consolidar a distinção entre representar a sintaxe e executar o código.
* **Pontos da Fala:**
  1. **Nós da AST (`ast_nodes.py`):**
     - Apresentar as classes construídas com `@dataclass`: `Programa`, `Declaracao`, `Atribuicao`, `Saida`, `Binaria`, `Inteiro`, `Variavel`.
  2. **Parsing de Comandos e Programa (Aula 09, Slide 5 - Etapa 2):**
     - O método `item()` inspeciona o primeiro token e direciona:
       - Se `KW_INT` $\to$ chama `declaracao()` e cria `Declaracao(nome)`.
       - Se `IDENT` $\to$ chama `atribuicao()` e cria `Atribuicao(nome, valor)`.
       - Se `KW_PRINT` $\to$ chama `saida()` e cria `Saida(expr)`.
     - `lista_itens()` itera acumulando comandos em uma lista até o fim do arquivo.
     - `programa()` valida o `EOF` e empacota tudo na raiz `Programa(itens)`.
  3. **Visualização Hierárquica (`ast_printer.py`):**
     - Apresentar o exemplo clássico da Aula 09 (Slide 2):
       ```c
       int x;
       x = 2 + 3 * 4;
       print(x);
       ```
     - Mostrar a impressão textual formatada e reforçar: a AST reflete a ordem e o encadeamento dos nós sintáticos sem calcular ou executar operações.
* **Telas/Slides sugeridos:** Ilustração da árvore sintática gerada versus a saída formatada do `ast_printer.py`.
* **Frase de transição:** *"Mas o que acontece quando a entrada possui erros sintáticos? A [Pessoa 5] vai demonstrar o sistema de diagnóstico com posição, a bateria de testes e a conclusão do projeto."*

---

## 👤 Pessoa 5: Diagnósticos de Erro Sintático, Testes e Conclusão (Etapa 3)

* **Tempo:** 2 a 3 minutos.
* **Tópico:** Tratamento de erros sintáticos com localização exata, validação automatizada e demonstração prática.
* **Propósito no projeto:** Evidenciar que o projeto atende com rigor a todos os critérios de avaliação (Slide 7), demonstrando a execução dos testes e o script principal.
* **Pontos da Fala:**
  1. **Diagnóstico Preciso com Posição (Aula 09, Slide 5 - Etapa 3):**
     - O parser segue a política *fail-fast*, interrompendo no primeiro erro sintático encontrado.
     - A exceção `ErroSintatico` detalha a **linha**, a **coluna**, o que era **esperado** e o que foi **encontrado**:
       > `Erro sintático na linha 1, coluna 11: esperado número, identificador ou '(', encontrado ')'.`
  2. **Bateria de Testes Automatizados (`test_parser.py`):**
     - 12 testes unitários com `unittest` cobrindo 100% dos cenários do Slide 6:
       - Precedência e associatividade à esquerda.
       - Parênteses e variáveis válidas.
       - Entradas vazias e comentários ignorados pelo lexer.
       - Casos inválidos (`int 5;`, `x = ;`, `print((2 + 3);`, etc.).
       - Parada garantida no primeiro erro sintático.
       - Resultado da execução: `12 tests in 0.001s, OK`.
  3. **Demonstração Prática (`main.py`):**
     - Mostrar a execução sobre o arquivo `calcula_bonus.mini`:
       - Listagem dos tokens com linha e coluna.
       - Impressão hierárquica da AST completa.
       - Simulação do erro proposital `print(2 + );`.
  4. **Conclusão e Entregáveis (Aula 09, Slide 7):**
     - Resumir a entrega: código do parser implementado, testes validados, exemplos de AST e diagnósticos, e documentação completa.
* **Telas/Slides sugeridos:** Terminal exibindo `python -m unittest -v` e a execução do `python main.py`.

---

## 💡 Dicas de Apresentação em Grupo

1. **Pratiquem as passagens de bastão:** O final da fala de cada um já deixa um gancho claro para o colega seguinte entrar com confiança.
2. **Postura sobre o escopo:** Se o professor perguntar por que o código não calcula a soma ou não reclama de variáveis não declaradas, enfatizem que essa restrição está documentada no Slide 3 da Aula 09 (escopo estritamente sintático).
3. **Legibilidade:** Se forem projetar o terminal durante a demonstração, configurem fonte média/grande (`Ctrl + +`) e fundo escuro com bom contraste.
