# modelos/ranking.py
import json
import os

class Ranking:
    """Gerencia o placar de líderes em um arquivo JSON."""
    def __init__(self, arquivo="ranking.json"):
        self.arquivo = arquivo

    def carregar(self):
        """Carrega os scores do arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar(self, scores):
        """Salva a lista de scores no arquivo JSON."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=4)

    def adicionar_score(self, nome, pontuacao):
        """Adiciona um novo score, ordena a lista e a mantém com no máximo 10 entradas."""
        scores = self.carregar()
        scores.append({"nome": nome, "pontuacao": pontuacao})
        scores_ordenados = sorted(scores, key=lambda x: x['pontuacao'], reverse=True)
        self.salvar(scores_ordenados[:10])