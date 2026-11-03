# MiniLang — Trabalho 02: Analisador Sintático

Pipeline do compilador: **Código-fonte -> Lexer -> Tokens -> Parser -> AST**

---

## 📁 Arquivos do Projeto

- `lexer.py`: Analisador léxico (`Token`, `Diagnostic` e `Lexer`).
- `ast_nodes.py`: Definição dos nós da AST (`Programa`, `Declaracao`, `Atribuicao`, `Saida`, `Binaria`, `Inteiro`, `Variavel`).
- `parser.py`: Analisador sintático descendente recursivo (*Recursive Descent Parser*).
- `ast_printer.py`: Visualizador e formatador hierárquico da AST.
- `main.py`: Ponto de entrada — processa arquivos `.mini`, exibindo tokens, AST e exemplo de erro sintático.
- `test_parser.py`: Bateria completa de testes automatizados com `unittest`.
- `calcula_bonus.mini`: Programa de exemplo na linguagem MiniLang.

---

## 🚀 Como Executar

### Executar o analisador sobre o programa de exemplo
```bash
python main.py
```
*(Executa por padrão o arquivo `calcula_bonus.mini`, exibe os tokens encontrados, a árvore sintática gerada e um exemplo de diagnóstico de erro sintático).*

### Executar sobre outro arquivo `.mini`
```bash
python main.py caminho/para/outro_programa.mini
```

### Executar os testes automatizados
```bash
python -m unittest -v
```
*(Executa todos os 12 testes unitários cobrindo casos válidos, precedência, associatividade e erros sintáticos).*

---

## ⚠️ Diagnóstico Sintático

O parser segue a política *fail-fast*, interrompendo no **primeiro erro sintático** encontrado e emitindo a localização exata (linha e coluna), o token recebido e o que era esperado:

```text
Entrada: print(2 + );
Saída:   Erro sintático na linha 1, coluna 11: esperado número, identificador ou '(', encontrado ')'.
```

> **Escopo:** O analisador é puramente sintático. Não há análise semântica (como verificação de tipos ou de declaração prévia de variáveis) nem execução/avaliação de expressões.

---

# 🎙️ Roteiro de Apresentação (Divisão para 5 Pessoas)

- **Tempo total sugerido:** 10 a 15 minutos (2 a 3 minutos por integrante).
- **Embasamento:** Aulas 08 (Fundamentos Teóricos LL(1), FIRST e FOLLOW) e 09 (Trabalho 02 - Analisador Sintático MiniLang).

---

### Visão Geral da Divisão

| Integrante | Tópico | Propósito no Projeto | Base nos PDFs |
| :--- | :--- | :--- | :--- |
| **Pessoa 1** | **Introdução e Fundamentos LL(1)** | Contextualizar o pipeline e os princípios teóricos de análise preditiva. | Aula 08 (Slides 1–4, 54–57) & Aula 09 (Slide 1) |
| **Pessoa 2** | **Gramática da MiniLang e Escopo** | Apresentar a gramática formal e delimitar o escopo (não-tangenciamento). | Aula 09 (Slides 2 e 3) |
| **Pessoa 3** | **Arquitetura do Parser e Expressões** | Explicar o parser descendente recursivo, precedência e associatividade. | Aula 08 (Exercício 7) & Aula 09 (Slide 5 - Etapa 1) |
| **Pessoa 4** | **Construção da AST e Comandos** | Detalhar os nós da AST e o reconhecimento dos comandos do programa. | Aula 09 (Slides 2, 4 e 5 - Etapa 2) |
| **Pessoa 5** | **Diagnósticos de Erro, Testes e Conclusão** | Demonstrar robustez com localização de erros, bateria de testes e entrega. | Aula 09 (Slides 5, 6 e 7) |

---

### 👤 Pessoa 1: Introdução, Pipeline e Fundamentação LL(1)

- **Tempo:** 2 a 3 minutos.
- **Tópico:** O papel do analisador sintático no compilador e a fundamentação preditiva LL(1).
- **Propósito no projeto:** Situar a relevância do trabalho, explicar a transição `Tokens -> AST` e conectar os conceitos teóricos de lookahead e análise preditiva aprendidos na Aula 08 com a prática.
- **Pontos a apresentar:**
  1. **Objetivo do projeto:** Receber uma sequência linear de tokens do lexer, verificar se obedece às regras sintáticas da MiniLang e produzir a Árvore Sintática Abstrata (AST).
  2. **Pipeline do compilador (Aula 09, Slide 1):** Apresentar o fluxo `Código-fonte -> Lexer -> Tokens -> Parser -> AST`.
  3. **Conceitos de LL(1) (Aula 08, Slides 4 e 55):**
     - Leitura da esquerda para a direita ($L$).
     - Derivação mais à esquerda ($L$).
     - **1 token de lookahead**: consulta antecipada com `peek()`.
     - *Regra fundamental:* **Consultar não consome**. O parser inspeciona o próximo símbolo para escolher a produção correta sem descartar o token antes da hora.
- **Dica de tela/slide:** Diagrama em blocos do pipeline do compilador e diagrama de lookahead/pilha da Aula 08.
- **Fala de transição:** *"Para entender como essas decisões são tomadas pelo parser, a [Pessoa 2] vai apresentar a gramática formal da MiniLang e a delimitação do nosso escopo."*

---

### 👤 Pessoa 2: A Gramática da MiniLang e Delimitação de Escopo

- **Tempo:** 2 a 3 minutos.
- **Tópico:** Especificação gramatical e garantia de não-tangenciamento do tema.
- **Propósito no projeto:** Demonstrar as regras formais da linguagem reconhecidas pelo parser e evidenciar o rigor no cumprimento do escopo definido na especificação.
- **Pontos a apresentar:**
  1. **A Gramática da MiniLang (`parser.py`):**
     - `programa    -> lista_itens EOF`
     - `lista_itens -> item lista_itens | ε`
     - `item        -> declaracao | atribuicao | saida`
     - `declaracao  -> 'int' IDENT ';'`
     - `atribuicao  -> IDENT '=' expressao ';'`
     - `saida       -> 'print' '(' expressao ')' ';'`
  2. **Obrigatório Reconhecer (Aula 09, Slide 3):** Declarações inteiras (`int x;`), comandos de atribuição, saída com `print`, operadores aritméticos, expressões com parênteses e fim de arquivo obrigatório (`EOF`).
  3. **Delimitação de Escopo e Não-Tangenciamento (Aula 09, Slide 3):**
     - O projeto **não tangenciou**: não implementou estruturas condicionais (`if/else`) ou de repetição (`while`), não possui escopos aninhados, não avalia operadores booleanos/unários e não executa o código.
     - Destacar que variáveis não declaradas são aceitas sintaticamente (ex: `print(y);`), pois a checagem semântica é uma etapa posterior que está fora do escopo.
- **Dica de tela/slide:** Tabela com a gramática da linguagem e quadro comparativo *"Obrigatório vs. Fora do Escopo"*.
- **Fala de transição:** *"Com a gramática e o escopo bem delimitados, a [Pessoa 3] vai explicar a arquitetura do parser descendente recursivo e como resolvemos a precedência e associatividade das expressões."*

---

### 👤 Pessoa 3: Arquitetura do Parser e Expressões Aritméticas (Etapa 1)

- **Tempo:** 2 a 3 minutos.
- **Tópico:** Implementação do parser descendente recursivo, operadores e expressões aritméticas.
- **Propósito no projeto:** Explicar a lógica algorítmica de [`parser.py`](file:///c:/Users/User/Downloads/files/files/parser.py) e como a gramática resolve precedência e associatividade sem recursão à esquerda direta.
- **Pontos a apresentar:**
  1. **Técnica Descendente Recursiva:**
     - Cada regra não-terminal vira uma função correspondente no código (`expressao()`, `termo()`, `fator()`).
     - Primitivas essenciais: `peek()` (inspeciona), `advance()` (consome), `match(*tipos)` (consome se casar com o tipo) e `expect(tipo)` (exige token obrigatório ou dispara erro).
  2. **Hierarquia de Expressões (Aula 09, Slide 5 - Etapa 1):**
     - `expressao()` $\to$ lida com `+` e `-`, delegando para `termo()`.
     - `termo()` $\to$ lida com `*` e `/`, delegando para `fator()`.
     - `fator()` $\to$ consome números inteiros, identificadores ou subexpressões agrupadas entre parênteses `( expressao )`.
  3. **Precedência e Associatividade à Esquerda (Aula 09, Slide 6):**
     - **Precedência:** `*` e `/` são avaliados em níveis mais profundos da árvore, garantindo que `2 + 3 * 4` execute a multiplicação primeiro.
     - **Associatividade à esquerda:** Implementada via laço iterativo `while (op := self.match("PLUS", "MINUS"))`, compondo os nós `Binaria(esquerda, op, direita)` da esquerda para a direita, garantindo que `10 - 3 - 2` resulte em `((10 - 3) - 2)`.
- **Dica de tela/slide:** Trecho do método `expressao()` e `termo()` em Python ao lado da árvore gerada para `2 + 3 * 4`.
- **Fala de transição:** *"Agora que vimos o motor de expressões, a [Pessoa 4] vai mostrar como esses blocos são integrados para construir a Árvore Sintática Abstrata (AST) do programa e dos comandos."*

---

### 👤 Pessoa 4: Construção da AST e Reconhecimento de Comandos (Etapa 2)

- **Tempo:** 2 a 3 minutos.
- **Tópico:** Estrutura dos nós da AST em [`ast_nodes.py`](file:///c:/Users/User/Downloads/files/files/ast_nodes.py) e o parsing dos comandos (Etapa 2).
- **Propósito no projeto:** Demonstrar a modelagem da estrutura de dados intermediária e reforçar o princípio de que a AST expressa a estrutura e sintaxe do programa, sem avaliá-lo.
- **Pontos a apresentar:**
  1. **Nós da AST ([`ast_nodes.py`](file:///c:/Users/User/Downloads/files/files/ast_nodes.py)):**
     - Classes implementadas com `@dataclass`: `Programa`, `Declaracao`, `Atribuicao`, `Saida`, `Binaria`, `Inteiro`, `Variavel`.
  2. **Parsing de Comandos e Programa (Aula 09, Slide 5 - Etapa 2):**
     - Método `item()` inspeciona o primeiro token e direciona:
       - Se `KW_INT` $\to$ aciona `declaracao()` e cria `Declaracao(nome)`.
       - Se `IDENT` $\to$ aciona `atribuicao()` e cria `Atribuicao(nome, valor)`.
       - Se `KW_PRINT` $\to$ aciona `saida()` e cria `Saida(expr)`.
     - `lista_itens()` itera reunindo todos os comandos em uma lista até o fim do arquivo.
     - `programa()` valida o `EOF` e empacota tudo na raiz `Programa(itens)`.
  3. **Visualização Textual da AST ([`ast_printer.py`](file:///c:/Users/User/Downloads/files/files/ast_printer.py)):**
     - Demonstrar o exemplo do Slide 2:
       ```c
       int x;
       x = 2 + 3 * 4;
       print(x);
       ```
     - Mostrar como a saída hierárquica preserva a relação pai-filho e operadores binários sem computar valores numéricos.
- **Dica de tela/slide:** Diagrama em árvore da AST do exemplo canônico comparado com a saída textual de `ast_printer.py`.
- **Fala de transição:** *"Mas e quando o usuário digita um código inválido? A [Pessoa 5] vai apresentar o nosso sistema de diagnóstico sintático, os testes automatizados e a conclusão do projeto."*

---

### 👤 Pessoa 5: Diagnósticos de Erro Sintático, Testes e Demonstração (Etapa 3)

- **Tempo:** 2 a 3 minutos.
- **Tópico:** Sistema de diagnóstico sintático com posição, validação automatizada e demonstração prática.
- **Propósito no projeto:** Evidenciar o atendimento aos critérios de qualidade exigidos pela especificação (Slide 7), demonstrando a execução de testes e do programa principal.
- **Pontos a apresentar:**
  1. **Diagnóstico Preciso (Aula 09, Slide 5 - Etapa 3):**
     - O parser implementa a estratégia *fail-fast*, disparando `ErroSintatico` imediatamente no primeiro erro encontrado.
     - A mensagem informa com clareza a **linha**, a **coluna**, o que era **esperado** e o que foi **encontrado**:
       > `Erro sintático na linha 1, coluna 11: esperado número, identificador ou '(', encontrado ')'.`
  2. **Bateria de Testes Automatizados ([`test_parser.py`](file:///c:/Users/User/Downloads/files/files/test_parser.py)):**
     - 12 testes unitários cobrindo:
       - Todos os casos do Slide 6 (precedência, associatividade à esquerda, parênteses, variáveis isoladas, programa vazio).
       - Comentários ignorados pelo lexer.
       - Erros sintáticos diversos (`int 5;`, `x = ;`, `print((2 + 3);`, etc.).
       - Parada garantida no primeiro erro sintático.
       - Relato de 100% de sucesso (`12 tests in 0.001s, OK`).
  3. **Demonstração Prática (`main.py`):**
     - Mostrar a execução sobre [`calcula_bonus.mini`](file:///c:/Users/User/Downloads/files/files/calcula_bonus.mini):
       - Impressão dos tokens com suas coordenadas.
       - Impressão hierárquica da AST completa.
       - Simulação do erro sintático proposital em `print(2 + );`.
  4. **Fechamento e Entregáveis (Aula 09, Slide 7):**
     - Confirmar a entrega de todos os itens exigidos: código completo, testes executados, exemplos de AST e diagnóstico, e este README detalhado.
- **Dica de tela/slide:** Terminal executando `python -m unittest -v` e `python main.py`.

---

## 💡 Dicas Gerais para o Sucesso da Apresentação

1. **Ensaiem a transição de fala:** Cada integrante deve chamar o próximo pelo nome, mantendo a narrativa fluida e sem pausas desconfortáveis.
2. **Usem o terminal ao vivo ou slides estáticos:** Caso projetem o código, aumentem a fonte do terminal (`Ctrl + +`) para facilitar a visualização da árvore AST e dos testes.
3. **Mantenham o foco no sintático:** Lembrem-se de reforçar aos avaliadores que o parser não calcula contas nem verifica se variáveis foram declaradas antes do uso, pois essa é uma regra deliberada do escopo do Trabalho 02.
