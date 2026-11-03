"""Imprime a AST em formato hierárquico, como no exemplo da atividade."""

from ast_nodes import (Inteiro, Variavel, Binaria, Declaracao,
                       Atribuicao, Saida, Programa)


def formatar_ast(no, recuo=""):
    if isinstance(no, Programa):
        linhas = [recuo + "Programa" + ("([])" if not no.itens else "")]
        for item in no.itens:
            linhas.append(formatar_ast(item, recuo + "  "))
    elif isinstance(no, Declaracao):
        linhas = [recuo + f"Declaracao({no.nome})"]
    elif isinstance(no, Atribuicao):
        linhas = [recuo + f"Atribuicao({no.nome})", formatar_ast(no.valor, recuo + "  ")]
    elif isinstance(no, Saida):
        linhas = [recuo + "Saida", formatar_ast(no.expressao, recuo + "  ")]
    elif isinstance(no, Binaria):
        linhas = [recuo + f"Binaria({no.operador})",
                  formatar_ast(no.esquerda, recuo + "  "),
                  formatar_ast(no.direita, recuo + "  ")]
    elif isinstance(no, Inteiro):
        linhas = [recuo + f"Inteiro({no.valor})"]
    elif isinstance(no, Variavel):
        linhas = [recuo + f"Variavel({no.nome})"]
    else:
        linhas = [recuo + f"?{type(no).__name__}"]
    return "\n".join(linhas)


def print_ast(no):
    print(formatar_ast(no))
