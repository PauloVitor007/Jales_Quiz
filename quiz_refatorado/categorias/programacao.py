# categorias/programacao.py
from modelos import PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso, PerguntaComImagem

def carregar_perguntas():
    return [
        PerguntaComImagem(
            "Qual linguagem de programação tem este logo?",
            ["Java", "Python", "C++", "JavaScript"],
            "Python",
            "assets/python_logo.png"
        ),
        PerguntaMultiplaEscolha(
            "Qual pilar da POO foca em 'esconder' a complexidade?",
            ["Herança", "Polimorfismo", "Encapsulamento", "Abstração"],
            "Encapsulamento"
        ),
        PerguntaVerdadeiroFalso(
            "Em Python, o método para inicializar um objeto é o `__main__`.",
            "Falso"
        ),
        PerguntaMultiplaEscolha(
            "O que `git clone` faz?",
            ["Cria um novo branch", "Envia alterações para o repositório remoto", "Copia um repositório remoto para sua máquina local", "Lista os commits"],
            "Copia um repositório remoto para sua máquina local"
        )
    ]