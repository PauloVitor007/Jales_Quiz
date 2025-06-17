# gui_quiz.py
import tkinter as tk
from tkinter import messagebox, simpledialog, OptionMenu
import random
import os
import json
from PIL import Image, ImageTk

# Importa as classes dos outros arquivos
from modelos import Usuario, Ranking, PerguntaMultiplaEscolha, PerguntaVerdadeiroFalso, PerguntaComImagem

class QuizInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Plataforma de Quiz Avançada")
        self.root.geometry("650x600")
        self.root.resizable(False, False)

        # Dados do Quiz
        self.usuario = None
        self.perguntas = []
        self.pergunta_atual_index = 0
        self.ranking = Ranking()
        self.custom_questions_file = "perguntas_customizadas.json"

        # Variáveis de controle do Tkinter
        self.resposta_var = tk.StringVar()
        self.image_label = None
        
        # Estrutura de Frames para gerenciar as telas
        self.frame_menu = tk.Frame(root)
        self.frame_quiz = tk.Frame(root)
        self.frame_ranking = tk.Frame(root)
        self.frame_criar_pergunta = tk.Frame(root)

        self.criar_menu_principal()

    def limpar_tela(self):
        """Esconde todos os frames principais."""
        self.frame_menu.pack_forget()
        self.frame_quiz.pack_forget()
        self.frame_ranking.pack_forget()
        self.frame_criar_pergunta.pack_forget()

    def criar_menu_principal(self):
        self.limpar_tela()
        
        # ### CORREÇÃO APLICADA AQUI ###
        # Destrói todos os widgets antigos dentro do frame do menu antes de recriá-lo
        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        self.frame_menu.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(self.frame_menu, text="Bem-vindo ao Quiz!", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        categorias_disponiveis = [f.split('.')[0] for f in os.listdir('categorias') if f.endswith('.py') and not f.startswith('__')]

        tk.Label(self.frame_menu, text="Escolha uma categoria:", font=("Helvetica", 14)).pack(pady=10)
        for categoria in sorted(categorias_disponiveis):
            tk.Button(self.frame_menu, text=categoria.title(), font=("Helvetica", 12),
                      command=lambda c=categoria: self.iniciar_quiz(c)).pack(fill="x", pady=5)
        
        tk.Button(self.frame_menu, text="Criar Nova Pergunta", font=("Helvetica", 12, "bold"), bg="#D0E0D0",
                  command=self.mostrar_tela_criar_pergunta).pack(fill="x", pady=(20, 5))

        tk.Button(self.frame_menu, text="Ver Ranking", font=("Helvetica", 12, "italic"),
                  command=self.mostrar_ranking).pack(fill="x", pady=(5, 5))

    def carregar_todas_perguntas(self, categoria):
        try:
            modulo_perguntas = __import__(f"categorias.{categoria}", fromlist=["carregar_perguntas"])
            perguntas_base = modulo_perguntas.carregar_perguntas()
        except (ImportError, AttributeError, FileNotFoundError):
            perguntas_base = []
        
        perguntas_customizadas = []
        try:
            with open(self.custom_questions_file, 'r', encoding='utf-8') as f:
                todas_customizadas = json.load(f)
                perguntas_dict = todas_customizadas.get(categoria, [])
                for p_dict in perguntas_dict:
                    if p_dict['tipo'] == 'multipla_escolha':
                        perguntas_customizadas.append(PerguntaMultiplaEscolha(p_dict['enunciado'], p_dict['opcoes'], p_dict['resposta_correta']))
                    elif p_dict['tipo'] == 'verdadeiro_falso':
                         perguntas_customizadas.append(PerguntaVerdadeiroFalso(p_dict['enunciado'], p_dict['resposta_correta']))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        return perguntas_base + perguntas_customizadas

    def iniciar_quiz(self, categoria):
        nome_usuario = simpledialog.askstring("Nome do Jogador", "Digite seu nome:", parent=self.root)
        if not nome_usuario:
            return
        self.usuario = Usuario(nome_usuario)
        
        self.perguntas = self.carregar_todas_perguntas(categoria)
        if not self.perguntas:
            messagebox.showinfo("Sem Perguntas", f"Não há perguntas disponíveis para a categoria '{categoria}'.")
            return

        random.shuffle(self.perguntas)
        self.pergunta_atual_index = 0
        self.usuario.set_pontuacao(0)
        self.criar_tela_quiz()

    def mostrar_tela_criar_pergunta(self):
        self.limpar_tela()
        
        # Limpa o frame de criação de perguntas antes de desenhar
        for widget in self.frame_criar_pergunta.winfo_children():
            widget.destroy()

        self.frame_criar_pergunta.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(self.frame_criar_pergunta, text="Cadastro de Novas Perguntas", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.frame_criar_pergunta, text="Categoria:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        categorias = [f.split('.')[0] for f in os.listdir('categorias') if f.endswith('.py') and not f.startswith('__')]
        self.categoria_var = tk.StringVar(self.root)
        self.categoria_var.set(categorias[0])
        OptionMenu(self.frame_criar_pergunta, self.categoria_var, *categorias).grid(row=1, column=1, sticky="ew")

        tk.Label(self.frame_criar_pergunta, text="Tipo:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tipos = ["Múltipla Escolha", "Verdadeiro / Falso"]
        self.tipo_var = tk.StringVar(self.root)
        self.tipo_var.set(tipos[0])
        self.tipo_var.trace("w", self.atualizar_campos_pergunta)
        OptionMenu(self.frame_criar_pergunta, self.tipo_var, *tipos).grid(row=2, column=1, sticky="ew")
        
        tk.Label(self.frame_criar_pergunta, text="Enunciado:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.enunciado_entry = tk.Entry(self.frame_criar_pergunta, font=("Helvetica", 12), width=50)
        self.enunciado_entry.grid(row=3, column=1, pady=5)

        self.opcoes_labels = []
        self.opcoes_entries = []
        for i in range(4):
            label = tk.Label(self.frame_criar_pergunta, text=f"Opção {i+1}:", font=("Helvetica", 12))
            entry = tk.Entry(self.frame_criar_pergunta, font=("Helvetica", 12), width=50)
            self.opcoes_labels.append(label)
            self.opcoes_entries.append(entry)
            label.grid(row=4+i, column=0, sticky="w", padx=5, pady=2)
            entry.grid(row=4+i, column=1, pady=2)

        self.resposta_label = tk.Label(self.frame_criar_pergunta, text="Resposta Correta:", font=("Helvetica", 12))
        self.resposta_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.resposta_entry = tk.Entry(self.frame_criar_pergunta, font=("Helvetica", 12), width=50)
        self.resposta_entry.grid(row=8, column=1, pady=5)
        
        tk.Button(self.frame_criar_pergunta, text="Salvar Pergunta", command=self.salvar_pergunta).grid(row=9, column=1, sticky="e", pady=20)
        tk.Button(self.frame_criar_pergunta, text="Voltar ao Menu", command=self.criar_menu_principal).grid(row=9, column=0, sticky="w", pady=20)
        
        self.atualizar_campos_pergunta()

    def atualizar_campos_pergunta(self, *args):
        tipo_selecionado = self.tipo_var.get()
        if tipo_selecionado == "Verdadeiro / Falso":
            for label in self.opcoes_labels:
                label.grid_remove()
            for entry in self.opcoes_entries:
                entry.grid_remove()
            self.resposta_label.config(text="Resposta (Verdadeiro/Falso):")
        else:
            for label in self.opcoes_labels:
                label.grid()
            for entry in self.opcoes_entries:
                entry.grid()
            self.resposta_label.config(text="Resposta Correta (texto exato):")

    def salvar_pergunta(self):
        categoria = self.categoria_var.get()
        tipo = self.tipo_var.get()
        enunciado = self.enunciado_entry.get().strip()
        resposta_correta = self.resposta_entry.get().strip()

        if not all([categoria, tipo, enunciado, resposta_correta]):
            messagebox.showerror("Erro de Validação", "Todos os campos devem ser preenchidos.")
            return

        nova_pergunta = {"enunciado": enunciado, "resposta_correta": resposta_correta}

        if tipo == "Múltipla Escolha":
            nova_pergunta['tipo'] = 'multipla_escolha'
            opcoes = [entry.get().strip() for entry in self.opcoes_entries if entry.get().strip()]
            if len(opcoes) < 2:
                messagebox.showerror("Erro de Validação", "Pelo menos duas opções devem ser fornecidas para múltipla escolha.")
                return
            if resposta_correta not in opcoes:
                 messagebox.showerror("Erro de Validação", "A resposta correta deve ser idêntica a uma das opções fornecidas.")
                 return
            nova_pergunta['opcoes'] = opcoes
        else:
            nova_pergunta['tipo'] = 'verdadeiro_falso'
            if resposta_correta.lower() not in ['verdadeiro', 'falso']:
                 messagebox.showerror("Erro de Validação", "Para 'Verdadeiro / Falso', a resposta deve ser 'Verdadeiro' ou 'Falso'.")
                 return
        
        try:
            with open(self.custom_questions_file, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            dados = {}

        if categoria not in dados:
            dados[categoria] = []
        
        dados[categoria].append(nova_pergunta)

        with open(self.custom_questions_file, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        messagebox.showinfo("Sucesso", "Pergunta salva com sucesso!")
        self.enunciado_entry.delete(0, 'end')
        self.resposta_entry.delete(0, 'end')
        for entry in self.opcoes_entries:
            entry.delete(0, 'end')

    def criar_tela_quiz(self):
        self.limpar_tela()
        self.frame_quiz.pack(pady=20, padx=20, fill="both", expand=True)
        self.label_pergunta = tk.Label(self.frame_quiz, text="", font=("Helvetica", 14, "bold"), wraplength=550, justify="center")
        self.label_pergunta.pack(pady=20)
        self.image_label = tk.Label(self.frame_quiz)
        self.image_label.pack(pady=10)
        self.frame_opcoes = tk.Frame(self.frame_quiz)
        self.frame_opcoes.pack(pady=10)
        self.feedback_label = tk.Label(self.frame_quiz, text="", font=("Helvetica", 12, "italic"))
        self.feedback_label.pack(pady=10)
        self.botao_responder = tk.Button(self.frame_quiz, text="Responder", font=("Helvetica", 12), command=self.verificar_resposta)
        self.botao_responder.pack(pady=20)
        self.carregar_proxima_pergunta()

    def limpar_opcoes(self):
        for widget in self.frame_opcoes.winfo_children():
            widget.destroy()

    def carregar_proxima_pergunta(self):
        self.feedback_label.config(text="")
        self.resposta_var.set(None)
        self.limpar_opcoes()
        self.botao_responder.config(state="normal", text="Responder", command=self.verificar_resposta)
        if self.image_label: self.image_label.config(image='')
        if self.pergunta_atual_index < len(self.perguntas):
            pergunta_obj = self.perguntas[self.pergunta_atual_index]
            self.label_pergunta.config(text=pergunta_obj.enunciado)
            if isinstance(pergunta_obj, PerguntaComImagem):
                try:
                    img = Image.open(pergunta_obj.caminho_imagem)
                    img.thumbnail((300, 200))
                    self.photo_img = ImageTk.PhotoImage(img)
                    self.image_label.config(image=self.photo_img)
                except FileNotFoundError:
                    self.image_label.config(text=f"[Imagem não encontrada em {pergunta_obj.caminho_imagem}]")
            for i, opcao in enumerate(pergunta_obj.opcoes):
                rb = tk.Radiobutton(self.frame_opcoes, text=opcao, variable=self.resposta_var, value=opcao, font=("Helvetica", 11), command=self.ativar_hotkeys)
                rb.pack(anchor="w", padx=20)
            self.desativar_hotkeys()
        else:
            self.mostrar_resultado()
            
    def ativar_hotkeys(self):
        pergunta_obj = self.perguntas[self.pergunta_atual_index]
        for i in range(len(pergunta_obj.opcoes)): self.root.bind(f"<KeyPress-{i+1}>", self.processar_hotkey)
            
    def desativar_hotkeys(self):
        for i in range(1, 10): self.root.unbind(f"<KeyPress-{i}>")

    def processar_hotkey(self, event):
        indice_selecionado = int(event.keysym) - 1
        pergunta_obj = self.perguntas[self.pergunta_atual_index]
        if 0 <= indice_selecionado < len(pergunta_obj.opcoes):
            self.resposta_var.set(pergunta_obj.opcoes[indice_selecionado])
            self.verificar_resposta()

    def verificar_resposta(self):
        self.desativar_hotkeys()
        resposta_selecionada = self.resposta_var.get()
        if not resposta_selecionada or resposta_selecionada == 'None':
            messagebox.showwarning("Atenção", "Por favor, selecione uma resposta.")
            self.ativar_hotkeys(); return
        pergunta_obj = self.perguntas[self.pergunta_atual_index]
        if pergunta_obj.verificar_resposta(resposta_selecionada):
            self.usuario.adicionar_ponto()
            self.feedback_label.config(text="Resposta Correta! ✅", fg="green")
        else:
            self.feedback_label.config(text=f"Incorreto! A resposta era: {pergunta_obj.resposta_correta} ❌", fg="red")
        self.pergunta_atual_index += 1
        self.botao_responder.config(state="disabled")
        self.root.after(1500, self.carregar_proxima_pergunta)

    def mostrar_resultado(self):
        self.limpar_tela()
        self.ranking.adicionar_score(self.usuario.get_nome(), self.usuario.get_pontuacao())
        resultado_frame = tk.Frame(self.root)
        resultado_frame.pack(pady=50, padx=20, fill="both", expand=True)
        tk.Label(resultado_frame, text="Fim do Quiz!", font=("Helvetica", 20, "bold")).pack(pady=10)
        tk.Label(resultado_frame, text=f"{self.usuario.get_nome()}, sua pontuação final foi:", font=("Helvetica", 14)).pack()
        tk.Label(resultado_frame, text=f"{self.usuario.get_pontuacao()} / {len(self.perguntas)}", font=("Helvetica", 22, "bold")).pack(pady=10)
        tk.Button(resultado_frame, text="Jogar Novamente", command=self.criar_menu_principal).pack(pady=20)
        tk.Button(resultado_frame, text="Sair", command=self.root.quit).pack()

    def mostrar_ranking(self):
        self.limpar_tela()
        # Limpa o frame de ranking antes de desenhar
        for widget in self.frame_ranking.winfo_children():
            widget.destroy()
        self.frame_ranking.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(self.frame_ranking, text="Ranking - Top 10", font=("Helvetica", 20, "bold")).pack(pady=10)
        scores = self.ranking.carregar()
        if not scores:
            tk.Label(self.frame_ranking, text="Nenhuma pontuação registrada ainda.", font=("Helvetica", 12, "italic")).pack(pady=20)
        else:
            for i, score in enumerate(scores):
                texto = f"{i+1}. {score['nome']} - {score['pontuacao']} pontos"
                tk.Label(self.frame_ranking, text=texto, font=("Helvetica", 12)).pack(anchor="w")
        tk.Button(self.frame_ranking, text="Voltar ao Menu", command=self.criar_menu_principal).pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizInterface(root)
    root.mainloop()