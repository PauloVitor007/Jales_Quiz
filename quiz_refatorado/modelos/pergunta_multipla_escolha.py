# modelos/pergunta_multipla_escolha.py
from .pergunta import Pergunta # Importação relativa

class PerguntaMultiplaEscolha(Pergunta):
    """Classe para perguntas de múltipla escolha."""
    def __init__(self, enunciado, opcoes, resposta_correta):
        super().__init__(enunciado, resposta_correta)
        self.opcoes = opcoes