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
