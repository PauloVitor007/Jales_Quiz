# modelos/pergunta.py

class Pergunta:
    """Classe base para todos os tipos de perguntas (Herança)."""
    def __init__(self, enunciado, resposta_correta):
        self.enunciado = enunciado
        self.resposta_correta = resposta_correta

    def verificar_resposta(self, resposta_usuario):
        """Método polimórfico para verificar a resposta."""
        return resposta_usuario.lower() == self.resposta_correta.lower()