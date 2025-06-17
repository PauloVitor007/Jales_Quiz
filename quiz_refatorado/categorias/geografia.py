# categorias/geografia.py
from modelos import PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso

def carregar_perguntas():
    return [
        PerguntaMultiplaEscolha(
            "Qual é a capital do Brasil?",
            ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
            "Brasília"
        ),
        PerguntaVerdadeiroFalso(
            "O Rio Nilo é o rio mais longo do mundo.",
            "Verdadeiro"
        ),
        PerguntaMultiplaEscolha(
            "Qual país é o maior em área territorial?",
            ["China", "Estados Unidos", "Canadá", "Rússia"],
            "Rússia"
        ),
         PerguntaVerdadeiroFalso(
            "O Monte Everest está localizado no Nepal.",
            "Verdadeiro"
        )
    ]