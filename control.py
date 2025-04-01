import json
import datetime
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

class Produto:
    def __init__(self, codigo, nome, quantidade, preco, novo, seminovo, categoria):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.novo = novo
        self.seminovo = seminovo
        self.categoria = categoria

class SistemaEstoque:
    def __init__(self):
        self.produtos = {}
        self.categorias = ["Apple", "Xiaomi", "Samsung", "Video Games"]
        self.carregar_estoque()
        
    def carregar_estoque(self):
        if os.path.exists("estoque.json"):
            try:
                with open("estoque.json", "r", encoding='utf-8') as f:
                    dados = json.load(f)
                    for codigo, info in dados.items():
                        self.produtos[codigo] = Produto(
                            codigo, 
                            info['nome'], 
                            info['quantidade'], 
                            info['preco'],
                            info.get('novo', False),
                            info.get('seminovo', False),
                            info.get('categoria', '')
                        )
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar estoque: {str(e)}")
                self.produtos = {}
    
    def salvar_estoque(self):
        try:
            dados = {}
            for codigo, produto in self.produtos.items():
                dados[codigo] = {
                    'nome': produto.nome,
                    'quantidade': produto.quantidade,
                    'preco': produto.preco,
                    'novo': produto.novo,
                    'seminovo': produto.seminovo,
                    'categoria': produto.categoria
                }
            with open("estoque.json", "w", encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar estoque: {str(e)}")
            return False
    
    def registrar_log(self, operacao, codigo, quantidade, responsavel):
        try:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
            os.makedirs("logs", exist_ok=True)
            
            arquivo_detalhado = f"logs/estoque_log_{data_atual}.txt"
            data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(arquivo_detalhado, "a", encoding='utf-8') as f:
                f.write(f"{data_hora} - {operacao} - Produto: {codigo} - Quantidade: {quantidade} - Responsável: {responsavel}\n")
            
            arquivo_quantidades = f"logs/quantidades_{data_atual}.txt"
            if not os.path.exists(arquivo_quantidades):
                with open(arquivo_quantidades, "w", encoding='utf-8') as f:
                    f.write("NOME,QUANTIDADE,CATEGORIA\n")
            
            produto = self.produtos.get(codigo)
            if produto:
                with open(arquivo_quantidades, "a", encoding='utf-8') as f:
                    f.write(f"{produto.nome},{quantidade},{produto.categoria}\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar log: {str(e)}")
    
    def cadastrar_produto(self, codigo, nome, quantidade, preco, novo, seminovo, categoria):
        if codigo in self.produtos:
            return False, "Produto já cadastrado!"
        
        try:
            quantidade = int(quantidade)
            preco = float(preco)
        except ValueError:
            return False, "Quantidade deve ser inteiro e preço deve ser número válido!"
        
        self.produtos[codigo] = Produto(codigo, nome, quantidade, preco, novo, seminovo, categoria)
        if self.salvar_estoque():
            self.registrar_log("CADASTRO", codigo, quantidade, "Sistema")
            return True, "Produto cadastrado com sucesso!"
        return False, "Erro ao salvar produto"
    
    def entrada_estoque(self, codigo, quantidade, responsavel):
        if codigo not in self.produtos:
            return False, "Produto não encontrado!"
        
        try:
            quantidade = int(quantidade)
        except ValueError:
            return False, "Quantidade deve ser um número inteiro!"
        
        self.produtos[codigo].quantidade += quantidade
        if self.salvar_estoque():
            self.registrar_log("ENTRADA", codigo, quantidade, responsavel)
            return True, f"Entrada de {quantidade} unidades registrada para o produto {codigo}"
        return False, "Erro ao registrar entrada"
    
    def saida_estoque(self, codigo, quantidade, responsavel):
        if codigo not in self.produtos:
            return False, "Produto não encontrado!"
        
        try:
            quantidade = int(quantidade)
        except ValueError:
            return False, "Quantidade deve ser um número inteiro!"
        
        if self.produtos[codigo].quantidade < quantidade:
            return False, "Quantidade insuficiente em estoque!"
        
        self.produtos[codigo].quantidade -= quantidade
        if self.salvar_estoque():
            self.registrar_log("SAIDA", codigo, quantidade, responsavel)
            return True, f"Saída de {quantidade} unidades registrada para o produto {codigo}"
        return False, "Erro ao registrar saída"
    
    def listar_produtos(self):
        return list(self.produtos.values())

class AplicativoEstoque:
    def __init__(self, root):
        self.root = root
        self.sistema = SistemaEstoque()
    
        self.root.title("Sistema de Controle de Estoque")
        self.root.geometry("1100x750")
        self.center_window()
    
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", rowheight=30, font=('Arial', 10))
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
        self.criar_aba_cadastro()
        self.criar_aba_movimentacao()
        self.criar_aba_consulta()
    
        self.atualizar_lista()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    
    def init_ui(self):
        self.root.deiconify()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.criar_aba_cadastro()
        self.criar_aba_movimentacao()
        self.criar_aba_consulta()
        
        # Atualiza a lista inicial
        self.atualizar_lista()
    
    def criar_aba_cadastro(self):
        frame = Frame(self.notebook, padx=20, pady=20)
        self.notebook.add(frame, text="Cadastro de Produtos")
        
        # Formulário
        campos = [
            ("Código:", "codigo_entry"),
            ("Nome:", "nome_entry"),
            ("Quantidade:", "quantidade_entry"),
            ("Preço:", "preco_entry")
        ]
        
        for i, (label, var_name) in enumerate(campos):
            Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=W)
            entry = Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=EW)
            setattr(self, var_name, entry)
        
        Label(frame, text="Categoria:").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.categoria_var = StringVar()
        self.categoria_combobox = ttk.Combobox(
            frame, 
            textvariable=self.categoria_var,
            values=self.sistema.categorias,
            state="readonly"
        )
        self.categoria_combobox.grid(row=4, column=1, padx=5, pady=5, sticky=EW)
        self.categoria_combobox.set("Selecione")  # Valor padrão
        
        # Checkboxes
        self.novo_var = BooleanVar()
        Checkbutton(frame, text="Novo", variable=self.novo_var).grid(row=5, column=0, padx=5, pady=5, sticky=W)
        
        self.seminovo_var = BooleanVar()
        Checkbutton(frame, text="Semi-novo", variable=self.seminovo_var).grid(row=5, column=1, padx=5, pady=5, sticky=W)
        
        Button(frame, text="Cadastrar", command=self.cadastrar_produto).grid(row=6, column=0, columnspan=2, pady=10, sticky=EW)
        
        frame.columnconfigure(1, weight=1)
    
    def criar_aba_movimentacao(self):
        frame = Frame(self.notebook, padx=20, pady=20)
        self.notebook.add(frame, text="Movimentação")
        
        # Entrada
        entrada_frame = LabelFrame(frame, text="Entrada no Estoque", padx=10, pady=10)
        entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.add_movimentacao_fields(entrada_frame, "entrada")
        Button(entrada_frame, text="Registrar Entrada", command=self.registrar_entrada).grid(row=3, column=0, columnspan=2, pady=5, sticky=EW)
        
        # Saída
        saida_frame = LabelFrame(frame, text="Saída do Estoque", padx=10, pady=10)
        saida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.add_movimentacao_fields(saida_frame, "saida")
        Button(saida_frame, text="Registrar Saída", command=self.registrar_saida).grid(row=3, column=0, columnspan=2, pady=5, sticky=EW)
        
        # Configura peso
        frame.columnconfigure(0, weight=1)
    
    def add_movimentacao_fields(self, parent, prefix):
        campos = [
            ("Código:", f"{prefix}_codigo"),
            ("Quantidade:", f"{prefix}_quantidade"),
            ("Responsável:", f"{prefix}_responsavel")
        ]
        
        for i, (label, var_name) in enumerate(campos):
            Label(parent, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=W)
            entry = Entry(parent)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=EW)
            setattr(self, var_name, entry)
        
        parent.columnconfigure(1, weight=1)
    
    def criar_aba_consulta(self):
        frame = Frame(self.notebook)
        self.notebook.add(frame, text="Consulta de Estoque", padding=10)
        
        container = Frame(frame)
        container.pack(fill=BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(container, orient="vertical")
        scroll_x = ttk.Scrollbar(container, orient="horizontal")
        
        self.tree = ttk.Treeview(
            container,
            columns=("Codigo", "Nome", "Quantidade", "Preco", "Categoria", "Novo", "SemiNovo"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configura colunas
        colunas = [
            ("Codigo", 100, CENTER),
            ("Nome", 200, W),
            ("Quantidade", 80, CENTER),
            ("Preco", 80, E),
            ("Categoria", 100, CENTER),
            ("Novo", 60, CENTER),
            ("SemiNovo", 80, CENTER)
        ]
        
        for heading, width, anchor in colunas:
            self.tree.heading(heading, text=heading)
            self.tree.column(heading, width=width, anchor=anchor)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.tree.tag_configure('estoque_zero', background='#ffdddd')
        self.tree.tag_configure('estoque_baixo', background='#fff3cd')
        
        btn_frame = Frame(frame)
        btn_frame.pack(fill=X, pady=5)
        
        Button(btn_frame, text="Atualizar", command=self.atualizar_lista).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Copiar Log", command=self.copiar_log_quantidades).pack(side=LEFT, padx=5)
    
    def cadastrar_produto(self):
        codigo = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()
        preco = self.preco_entry.get().strip()
        novo = self.novo_var.get()
        seminovo = self.seminovo_var.get()
        categoria = self.categoria_var.get()
        
        if not all([codigo, nome, quantidade, preco]) or categoria == "Selecione":
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        sucesso, mensagem = self.sistema.cadastrar_produto(
            codigo, nome, quantidade, preco, novo, seminovo, categoria
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.codigo_entry.delete(0, END)
            self.nome_entry.delete(0, END)
            self.quantidade_entry.delete(0, END)
            self.preco_entry.delete(0, END)
            self.categoria_combobox.set("Selecione")
            self.novo_var.set(False)
            self.seminovo_var.set(False)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def registrar_entrada(self):
        codigo = self.entrada_codigo.get().strip()
        quantidade = self.entrada_quantidade.get().strip()
        responsavel = self.entrada_responsavel.get().strip()
        
        if not all([codigo, quantidade, responsavel]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
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
        
        if not all([codigo, quantidade, responsavel]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for produto in self.sistema.listar_produtos():
            tags = []
            if produto.quantidade == 0:
                tags.append('estoque_zero')
            elif produto.quantidade < 5:
                tags.append('estoque_baixo')
            
            self.tree.insert("", END, values=(
                produto.codigo,
                produto.nome,
                produto.quantidade,
                f"R$ {produto.preco:.2f}",
                produto.categoria,
                "Sim" if produto.novo else "Não",
                "Sim" if produto.seminovo else "Não"
            ), tags=tags)
    
    def copiar_log_quantidades(self):
        try:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
            arquivo_log = f"logs/quantidades_{data_atual}.txt"
            
            if not os.path.exists(arquivo_log):
                messagebox.showwarning("Aviso", "Nenhum log encontrado para hoje!")
                return
            
            with open(arquivo_log, "r", encoding='utf-8') as f:
                conteudo = f.read()
            
            self.root.clipboard_clear()
            self.root.clipboard_append(conteudo)
            messagebox.showinfo("Sucesso", "Log de quantidades copiado para a área de transferência!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao copiar log: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoEstoque(root)
    root.mainloop() 