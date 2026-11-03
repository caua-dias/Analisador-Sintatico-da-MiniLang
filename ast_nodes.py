"""Declara os nós da árvore sintática abstrata (AST) da MiniLang."""

from dataclasses import dataclass, field


class ASTNode:
    pass


@dataclass
class Inteiro(ASTNode):
    valor: int


@dataclass
class Variavel(ASTNode):
    nome: str


@dataclass
class Binaria(ASTNode):
    esquerda: ASTNode
    operador: str
    direita: ASTNode


@dataclass
class Declaracao(ASTNode):
    nome: str


@dataclass
class Atribuicao(ASTNode):
    nome: str
    valor: ASTNode


@dataclass
class Saida(ASTNode):
    expressao: ASTNode


@dataclass
class Programa(ASTNode):
    itens: list = field(default_factory=list)
