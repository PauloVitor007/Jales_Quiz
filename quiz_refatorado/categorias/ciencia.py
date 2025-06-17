# categorias/ciencia.py
from modelos import PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso

def carregar_perguntas():
    return [
        PerguntaMultiplaEscolha(
            "Qual é o símbolo químico da água?",
            ["O2", "CO2", "H2O", "NaCl"],
            "H2O"
        ),
        PerguntaVerdadeiroFalso(
            "A velocidade da luz é mais rápida no vácuo do que na água.",
            "Verdadeiro"
        ),
        PerguntaMultiplaEscolha(
            "Qual planeta é conhecido como 'Planeta Vermelho'?",
            ["Vênus", "Marte", "Júpiter", "Saturno"],
            "Marte"
        ),
        PerguntaMultiplaEscolha(
            "Quem é creditado com a teoria da relatividade?",
            ["Isaac Newton", "Galileu Galilei", "Nikola Tesla", "Albert Einstein"],
            "Albert Einstein"
        )
    ]