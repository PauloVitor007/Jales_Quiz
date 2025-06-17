# modelos/usuario.py

class Usuario:
    """Gerencia os dados do usuário, encapsulando nome e pontuação."""
    def __init__(self, nome):
        self.__nome = nome
        self.__pontuacao = 0

    def get_nome(self):
        return self.__nome

    def get_pontuacao(self):
        return self.__pontuacao
    
    def set_pontuacao(self, pontuacao):
        self.__pontuacao = pontuacao

    def adicionar_ponto(self):
        self.__pontuacao += 1