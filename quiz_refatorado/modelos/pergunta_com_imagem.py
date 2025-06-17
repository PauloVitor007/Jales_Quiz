# modelos/pergunta_com_imagem.py
from .pergunta_multipla_escolha import PerguntaMultiplaEscolha # Importação relativa

class PerguntaComImagem(PerguntaMultiplaEscolha):
    """Classe filha que adiciona um caminho de imagem à pergunta."""
    def __init__(self, enunciado, opcoes, resposta_correta, caminho_imagem):
        super().__init__(enunciado, opcoes, resposta_correta)
        self.caminho_imagem = caminho_imagem