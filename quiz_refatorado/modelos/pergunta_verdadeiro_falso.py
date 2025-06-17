# modelos/pergunta_verdadeiro_falso.py
from .pergunta import Pergunta # Importação relativa

class PerguntaVerdadeiroFalso(Pergunta):
    """Classe para perguntas de verdadeiro ou falso."""
    def __init__(self, enunciado, resposta_correta):
        super().__init__(enunciado, resposta_correta)
        self.opcoes = ["Verdadeiro", "Falso"]