import json
import datetime
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

class Produto:
    def __init__(self, codigo, nome, quantidade, preco):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

class SistemaEstoque:
    def __init__(self):
        self.produtos = {}
        self.carregar_estoque()
        
    def carregar_estoque(self):
        if os.path.exists("estoque.json"):
            with open("estoque.json", "r") as f:
                dados = json.load(f)
                for codigo, info in dados.items():
                    self.produtos[codigo] = Produto(
                        codigo, info['nome'], info['quantidade'], info['preco'])
    
    def salvar_estoque(self):
        dados = {}
        for codigo, produto in self.produtos.items():
            dados[codigo] = {
                'nome': produto.nome,
                'quantidade': produto.quantidade,
                'preco': produto.preco
            }
        with open("estoque.json", "w") as f:
            json.dump(dados, f, indent=4)
    
    def registrar_log(self, operacao, codigo, quantidade, responsavel):
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
        os.makedirs("logs", exist_ok=True)
        
        # Log detalhado (operações)
        arquivo_detalhado = f"logs/estoque_log_{data_atual}.txt"
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(arquivo_detalhado, "a") as f:
            f.write(f"{data_hora} - {operacao} - Produto: {codigo} - Quantidade: {quantidade} - Responsável: {responsavel}\n")
        
        # Log simplificado (apenas quantidades)
        arquivo_quantidades = f"logs/quantidades_{data_atual}.txt"
        if not os.path.exists(arquivo_quantidades):
            with open(arquivo_quantidades, "w") as f:
                f.write("DATA,HORA,CODIGO,NOME,QUANTIDADE\n")
        
        with open(arquivo_quantidades, "a") as f:
            f.write(f"{data_atual},{data_hora.split(' ')[1]},{codigo},{self.produtos[codigo].nome},{quantidade}\n")
    
    def cadastrar_produto(self, codigo, nome, quantidade, preco):
        if codigo in self.produtos:
            return False, "Produto já cadastrado!"
        self.produtos[codigo] = Produto(codigo, nome, quantidade, preco)
        self.salvar_estoque()
        self.registrar_log("CADASTRO", codigo, quantidade, "Sistema")
        return True, "Produto cadastrado com sucesso!"
    
    def entrada_estoque(self, codigo, quantidade, responsavel):
        if codigo not in self.produtos:
            return False, "Produto não encontrado!"
        self.produtos[codigo].quantidade += quantidade
        self.salvar_estoque()
        self.registrar_log("ENTRADA", codigo, quantidade, responsavel)
        return True, f"Entrada de {quantidade} unidades registrada para o produto {codigo}"
    
    def saida_estoque(self, codigo, quantidade, responsavel):
        if codigo not in self.produtos:
            return False, "Produto não encontrado!"
        if self.produtos[codigo].quantidade < quantidade:
            return False, "Quantidade insuficiente em estoque!"
        self.produtos[codigo].quantidade -= quantidade
        self.salvar_estoque()
        self.registrar_log("SAIDA", codigo, quantidade, responsavel)
        return True, f"Saída de {quantidade} unidades registrada para o produto {codigo}"
    
    def listar_produtos(self):
        return self.produtos.values()

class AplicativoEstoque:
    def __init__(self, root):
        self.root = root
        self.sistema = SistemaEstoque()
        
        self.root.title("Sistema de Controle de Estoque")
        self.root.geometry("900x600")
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", rowheight=30, font=('Arial', 10))
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, fill=BOTH, expand=True)
        
        self.criar_aba_cadastro()
        self.criar_aba_movimentacao()
        self.criar_aba_consulta()
    
    def criar_aba_cadastro(self):
        frame = Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(frame, text="Cadastro de Produtos")
        
        # Formulário de cadastro
        Label(frame, text="Código:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.codigo_entry = Entry(frame, font=('Arial', 10))
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        
        Label(frame, text="Nome:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.nome_entry = Entry(frame, font=('Arial', 10))
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5, sticky=EW)
        
        Label(frame, text="Quantidade:", font=('Arial', 10)).grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.quantidade_entry = Entry(frame, font=('Arial', 10))
        self.quantidade_entry.grid(row=2, column=1, padx=5, pady=5, sticky=EW)
        
        Label(frame, text="Preço:", font=('Arial', 10)).grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.preco_entry = Entry(frame, font=('Arial', 10))
        self.preco_entry.grid(row=3, column=1, padx=5, pady=5, sticky=EW)
        
        Button(frame, text="Cadastrar", command=self.cadastrar_produto, font=('Arial', 10), bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=10, sticky=EW)
    
    def criar_aba_movimentacao(self):
        frame = Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(frame, text="Movimentação")
        
        # Frame de entrada
        entrada_frame = LabelFrame(frame, text="Entrada no Estoque", padx=10, pady=10, font=('Arial', 10, 'bold'))
        entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        Label(entrada_frame, text="Código:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
        self.entrada_codigo = Entry(entrada_frame, font=('Arial', 10))
        self.entrada_codigo.grid(row=0, column=1, padx=5, pady=5)
        
        Label(entrada_frame, text="Quantidade:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5)
        self.entrada_quantidade = Entry(entrada_frame, font=('Arial', 10))
        self.entrada_quantidade.grid(row=1, column=1, padx=5, pady=5)
        
        Label(entrada_frame, text="Responsável:", font=('Arial', 10)).grid(row=2, column=0, padx=5, pady=5)
        self.entrada_responsavel = Entry(entrada_frame, font=('Arial', 10))
        self.entrada_responsavel.grid(row=2, column=1, padx=5, pady=5)
        
        Button(entrada_frame, text="Registrar Entrada", command=self.registrar_entrada, font=('Arial', 10), bg="#2196F3", fg="white").grid(row=3, column=0, columnspan=2, pady=5, sticky=EW)
        
        # Frame de saída
        saida_frame = LabelFrame(frame, text="Saída do Estoque", padx=10, pady=10, font=('Arial', 10, 'bold'))
        saida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        Label(saida_frame, text="Código:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
        self.saida_codigo = Entry(saida_frame, font=('Arial', 10))
        self.saida_codigo.grid(row=0, column=1, padx=5, pady=5)
        
        Label(saida_frame, text="Quantidade:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5)
        self.saida_quantidade = Entry(saida_frame, font=('Arial', 10))
        self.saida_quantidade.grid(row=1, column=1, padx=5, pady=5)
        
        Label(saida_frame, text="Responsável:", font=('Arial', 10)).grid(row=2, column=0, padx=5, pady=5)
        self.saida_responsavel = Entry(saida_frame, font=('Arial', 10))
        self.saida_responsavel.grid(row=2, column=1, padx=5, pady=5)
        
        Button(saida_frame, text="Registrar Saída", command=self.registrar_saida, font=('Arial', 10), bg="#F44336", fg="white").grid(row=3, column=0, columnspan=2, pady=5, sticky=EW)
    
    def criar_aba_consulta(self):
        frame = Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(frame, text="Consulta de Estoque")
        
        # Treeview para exibir produtos
        self.tree = ttk.Treeview(frame, columns=("Codigo", "Nome", "Quantidade", "Preco"), show="headings", height=15)
        self.tree.heading("Codigo", text="Código")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Preco", text="Preço")
        
        self.tree.column("Codigo", width=120, anchor=CENTER)
        self.tree.column("Nome", width=250, anchor=W)
        self.tree.column("Quantidade", width=120, anchor=CENTER)
        self.tree.column("Preco", width=120, anchor=E)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill=BOTH, expand=True)
        
        # Frame para botões
        btn_frame = Frame(frame)
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="Atualizar Lista", command=self.atualizar_lista, font=('Arial', 10)).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Copiar Log de Quantidades", command=self.copiar_log_quantidades, font=('Arial', 10)).pack(side=LEFT, padx=5)
        
        # Configura cores para estoque baixo
        self.tree.tag_configure('estoque_zero', background='#ffdddd')  # Vermelho claro
        self.tree.tag_configure('estoque_baixo', background='#fff3cd')  # Amarelo claro
        
        self.atualizar_lista()
    
    def cadastrar_produto(self):
        codigo = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()
        preco = self.preco_entry.get().strip()
        
        if not codigo or not nome or not quantidade or not preco:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            quantidade = int(quantidade)
            preco = float(preco)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser inteiro e preço deve ser número válido!")
            return
        
        sucesso, mensagem = self.sistema.cadastrar_produto(codigo, nome, quantidade, preco)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.codigo_entry.delete(0, END)
            self.nome_entry.delete(0, END)
            self.quantidade_entry.delete(0, END)
            self.preco_entry.delete(0, END)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def registrar_entrada(self):
        codigo = self.entrada_codigo.get().strip()
        quantidade = self.entrada_quantidade.get().strip()
        responsavel = self.entrada_responsavel.get().strip()
        
        if not codigo or not quantidade or not responsavel:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
            return
        
        sucesso, mensagem = self.sistema.entrada_estoque(codigo, quantidade, responsavel)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.entrada_codigo.delete(0, END)
            self.entrada_quantidade.delete(0, END)
            self.entrada_responsavel.delete(0, END)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def registrar_saida(self):
        codigo = self.saida_codigo.get().strip()
        quantidade = self.saida_quantidade.get().strip()
        responsavel = self.saida_responsavel.get().strip()
        
        if not codigo or not quantidade or not responsavel:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
            return
        
        sucesso, mensagem = self.sistema.saida_estoque(codigo, quantidade, responsavel)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.saida_codigo.delete(0, END)
            self.saida_quantidade.delete(0, END)
            self.saida_responsavel.delete(0, END)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def atualizar_lista(self):
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adiciona os produtos com formatação condicional
        for produto in self.sistema.listar_produtos():
            tags = ()
            if produto.quantidade == 0:
                tags = ('estoque_zero',)
            elif produto.quantidade < 5:
                tags = ('estoque_baixo',)
            
            self.tree.insert("", END, values=(
                produto.codigo, 
                produto.nome, 
                produto.quantidade, 
                f"R$ {produto.preco:.2f}"
            ), tags=tags)
    
    def copiar_log_quantidades(self):
        try:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
            arquivo_log = f"logs/quantidades_{data_atual}.txt"
            
            if not os.path.exists(arquivo_log):
                messagebox.showwarning("Aviso", "Nenhum log encontrado para hoje!")
                return
            
            with open(arquivo_log, "r") as f:
                conteudo = f.read()
            
            self.root.clipboard_clear()
            self.root.clipboard_append(conteudo)
            messagebox.showinfo("Sucesso", "Log de quantidades copiado para a área de transferência!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar log: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoEstoque(root)
    root.mainloop()