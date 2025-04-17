import json, os, datetime
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from pathlib import Path 

class Produto:
    def __init__(self, codigo: str, nome: str, quantidade: int, preco: float, novo: bool, seminovo: bool, categoria: str):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.novo = novo
        self.seminovo = seminovo
        self.categoria = categoria

class SistemaEstoque:
    def __init__(self):
        self.diretorio_base = Path(os.path.expanduser("~")) / "ControleEstoqueData"
        self.diretorio_dados = self.diretorio_base / "dados"
        self.logs_dir = self.diretorio_base / "logs"
        self.estoque_path = self.diretorio_dados / "estoque.json" 
        self.log_quantidades_path = self.logs_dir / "log_quantidades.txt"
        
        self._criar_diretorios()
        
        self.produtos = {}
        self.categorias = {
            "APPLE": [
            "ACESSÓRIOS",
            "IPAD",
            "APPLE WATCH",
            "MAIS ANTIGOS",
            "IPHONE 8 & PLUS",
            "IPHONE X | XR | XS | XS MAX",
            "IPHONE 11 | PRO | PRO MAX",
            "IPHONE SE (2.ª GERAÇÃO) | (3.ª GERAÇÃO)",
            "IPHONE 12 | MINI | PRO | PRO MAX",
            "IPHONE 13 | MINI | PRO | PRO MAX",
            "IPHONE 14 | PLUS | PRO | PRO MAX",
            "IPHONE 15 | PLUS | PRO | PRO MAX",
            "IPHONE 16 | PLUS | PRO | PRO MAX | 16E"
            ],
            "XIAOMI": [
            "SMARTWATCH", 
            "FONE", 
            "POCO M", 
            "POCO F", 
            "POCO X",
            "REDMI A", 
            "REDMI 8", 
            "REDMI 9", 
            "REDMI 10",
            "REDMI 12", 
            "REDMI 13", 
            "REDMI 14", 
            "NOTE 7",
            "NOTE 8", 
            "NOTE 9", 
            "NOTE 10", 
            "NOTE 11 & PRO",
            "NOTE 12 & PRO", 
            "NOTE 13 & PRO", 
            "NOTE 14 & PRO",
            "11 LITE", 
            "12 LITE", 
            "13 LITE", 
            "REDMI PAD"
            ],
            "MOTOROLA": [
            "MOTO E6", 
            "MOTO E7"
            ],
            "SAMSUNG": [
            "GALAXY A",
            "GALAXY M", 
            "GALAXY S"
            ],
            "REALME": [
            "REALME C", 
            "REALME NOTE"
            ],
            "VIDEO GAMES": [
            "PLAYSTATION 3",
            "PLAYSTATION 4", 
            "XBOX 360",
            "XBOX ONE", 
            "XBOX S & X",
            "NINTENDO"
            ]
        }
        self.armazenamentos = {
            "APPLE": [" ","32GB", "64GB", "128GB", "256GB", "512GB"],
            "XIAOMI": [" ", "2/32GB", "3/64GB", "4/64GB", "4/128GB", "6/128GB", "8/128GB", "8/256GB", "12/256GB", "12/512GB"],
            "SAMSUNG": [" ", "128GB", "2/32GB", "4/128GB", "6/128GB", "6/238GB"],
            "MOTOROLA": [" ", "2/32GB"],
            "REALME": [" ", "3/64GB", "8/256GB"],
            "VIDEO GAMES": [" ", "320GB", "500GB", "512GB", "1TB"]
        }
        self.carregar_estoque()

    def _criar_diretorios(self):
        try:
            self.diretorio_base.mkdir(parents=True, exist_ok=True)
            self.diretorio_dados.mkdir(exist_ok=True)
            self.logs_dir.mkdir(exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erro Crítico", 
                f"Falha ao criar diretórios: {str(e)}\n"
                f"Verifique as permissões em: {self.diretorio_base}")

    def carregar_estoque(self):
        try:
            if self.estoque_path.exists():
                with open(self.estoque_path, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    self.produtos = {}
                    for codigo, info in dados.items():
                        self.produtos[codigo] = Produto(
                            codigo,
                            info.get("nome", ""),
                            info.get("quantidade", 0),
                            info.get("preco", 0.0),
                            info.get("novo", False),
                            info.get("seminovo", False),
                            info.get("categoria", "")
                        )
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar estoque: {str(e)}")
            self.produtos = {}

    def salvar_estoque(self) -> bool:
        try:
            dados = {
                codigo: {
                    "nome": produto.nome,
                    "quantidade": produto.quantidade,
                    "preco": produto.preco,
                    "novo": produto.novo,
                    "seminovo": produto.seminovo,
                    "categoria": produto.categoria
                } for codigo, produto in self.produtos.items()
            }
            with open(self.estoque_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar estoque: {str(e)}")
            return False

    def registrar_log_quantidades(self, produto):
        try:
            with open(self.log_quantidades_path, "a", encoding="utf-8") as f:
                status = "ESGOTADO" if produto.quantidade == 0 else f"Estoque: {produto.quantidade}"
                registro = f"{datetime.datetime.now()} - {produto.nome} ({produto.codigo}) - {status}\n"
                f.write(registro)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar log: {str(e)}")
            return False

    def gerar_log_produtos(self):
        try:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
            arquivo_log = self.logs_dir / f"log_produto_{data_atual}.txt"
            
            conteudo = """Pegamos seu usado como parte do pagamento. 📲🔄

Parcelamos em até 18x cartão ou em até 36x no boleto. 💳📄

"""
            produtos_por_categoria = {categoria: {subcat: [] for subcat in subcategorias} 
                                    for categoria, subcategorias in self.categorias.items()}

            for produto in self.produtos.values():
                if produto.quantidade <= 0:
                    continue
                
                if ":" in produto.categoria:
                    categoria, subcategoria = produto.categoria.split(":", 1)
                    categoria = categoria.strip().upper()
                    subcategoria = subcategoria.strip()
                    
                    if categoria in produtos_por_categoria:
                        for subcat_valida in produtos_por_categoria[categoria]:
                            if (subcat_valida.replace("|", "").replace(" ", "") == 
                                subcategoria.replace("|", "").replace(" ", "")):
                                produtos_por_categoria[categoria][subcat_valida].append(produto.nome)
                                break

            for categoria, subcategorias in produtos_por_categoria.items():
                if not any(subcategorias.values()):
                    continue
                    
                conteudo += f"⬇ {categoria} ⬇\n\n"
                for subcategoria, produtos in subcategorias.items():
                    if produtos:
                        conteudo += f"• {subcategoria}:\n"
                        conteudo += "\n".join(f"  - {produto}" for produto in produtos)
                        conteudo += "\n\n"

            if not any(any(subcats.values()) for subcats in produtos_por_categoria.values()):
                conteudo += "⚠ Nenhum produto cadastrado no sistema.\n"

            with open(arquivo_log, "w", encoding="utf-8") as f:
                f.write(conteudo)
            
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar log: {str(e)}")
            return False

    def cadastrar_produto(self, codigo: str, nome: str, quantidade: str, preco: str, novo: bool, seminovo: bool, categoria: str):
        if codigo in self.produtos:
            return False, "Produto já cadastrado!"
        try:
            quantidade_int = int(quantidade)
            preco_float = float(preco)
        except ValueError:
            return False, "Quantidade deve ser inteiro e preço deve ser número válido!"

        self.produtos[codigo] = Produto(codigo, nome, quantidade_int, preco_float, novo, seminovo, categoria)
        if self.salvar_estoque():
            return True, "Produto cadastrado com sucesso!"
        return False, "Erro ao salvar produto"

    def entrada_estoque(self, codigo: str, quantidade: str, responsavel: str):
        if codigo not in self.produtos:
            return False, "Produto não encontrado!"
        try:
            quantidade_int = int(quantidade)
        except ValueError:
            return False, "Quantidade deve ser um número inteiro!"

        self.produtos[codigo].quantidade += quantidade_int
        if self.salvar_estoque():
            return True, f"Entrada de {quantidade_int} unidades registrada para o produto {codigo}"
        return False, "Erro ao registrar entrada"

    def saida_estoque(self, codigo: str, quantidade: str, responsavel: str):
        if codigo not in self.produtos:
            return False, "Produto não encontrado!"
        try:
            quantidade_int = int(quantidade)
        except ValueError:
            return False, "Quantidade deve ser um número inteiro!"

        if self.produtos[codigo].quantidade < quantidade_int:
            return False, "Quantidade insuficiente em estoque!"

        self.produtos[codigo].quantidade -= quantidade_int
        if self.salvar_estoque():
            if self.produtos[codigo].quantidade == 0:
                self.registrar_log_quantidades(self.produtos[codigo])
            return True, f"Saída de {quantidade_int} unidades registrada para o produto {codigo}"
        return False, "Erro ao registrar saída"

    def listar_produtos(self):
        return list(self.produtos.values())
    
class LoginWindow:
    def __init__(self, root: tk.Tk, on_login_success):
        self.root = root
        self.on_login_success = on_login_success

        self.window = tk.Toplevel(root)
        self.window.title("Login")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        self.center_window()

        main_frame = ttk.Frame(self.window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        ttk.Label(main_frame, text="Senha:").pack(pady=(0, 5))
        self.senha_entry = ttk.Entry(main_frame, show="*")
        self.senha_entry.pack(pady=(0, 15))

        ttk.Button(main_frame, text="Entrar", command=self.verificar_login).pack(fill=tk.X)

        self.senha_correta = "1"

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def verificar_login(self):
        senha = self.senha_entry.get().strip()
        if senha == self.senha_correta:
            self.window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
            self.senha_entry.delete(0, 'end')
            self.senha_entry.focus()

class AplicativoEstoque:
    def __init__(self, root: tk.Tk):
        self.cor_fundo = "#1a1a1a"
        self.cor_texto = "#e0e0e0"
        self.cor_destaque = "#2d8ceb"
        self.cor_widgets = "#2d2d2d"
        self.cor_borda = "#404040"
        self.cor_tree = "#363636"
        self.cor_abas = "#333333" 
        
        self.root = root
        self._configurar_janela_principal()  
        self._configurar_tema()              
        self.sistema = SistemaEstoque()           
        self.show_login()

    def _configurar_tema(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.cor_abas_inativas = "#333333"   
        self.cor_abas_ativas = "#2d8ceb"      
        self.cor_borda_abas = "#555555"      
        self.cor_texto_abas = "#e0e0e0"
        self.cor_texto = "#ffffff"  
        self.cor_destaque = "#2d8ceb"  
        self.cor_widgets = "#2d2d2d"  
        
        self.style.configure('.', 
                       background=self.cor_fundo,
                       foreground=self.cor_texto,
                       font=('Arial', 10),
                       borderwidth=0)
    
        self.style.configure('TNotebook', 
                    background=self.cor_fundo,
                    borderwidth=0)
        
        self.style.configure('TNotebook.Tab', 
                        background=self.cor_abas_inativas,
                        foreground=self.cor_texto_abas,
                        borderwidth=1,
                        bordercolor=self.cor_borda_abas,
                        padding=[15, 5], 
                        font=('Arial', 10, 'bold'))
        
        self.style.map('TNotebook.Tab',
                    background=[('selected', self.cor_abas_ativas),
                            ('active', self.cor_abas_ativas),
                            ('!selected', self.cor_abas_inativas)],
                    foreground=[('selected', 'white'),
                            ('active', 'white'),
                            ('!selected', self.cor_texto_abas)],
                    relief=[('selected', 'raised'),
                        ('active', 'sunken'),
                        ('!selected', 'flat')],
                    lightcolor=[('selected', self.cor_abas_ativas)],
                    darkcolor=[('selected', self.cor_abas_ativas)])
            
        self.style.configure('TFrame', 
                           background=self.cor_fundo,
                           borderwidth=1,
                           relief='solid',
                           bordercolor=self.cor_borda)
        
        self.style.configure('TButton',
                           background=self.cor_widgets,
                           foreground=self.cor_texto,
                           borderwidth=1,
                           bordercolor=self.cor_borda,
                           focusthickness=0)
        self.style.map('TButton',
                     background=[('active', self.cor_destaque),
                                 ('pressed', self.cor_destaque)],
                     foreground=[('active', self.cor_texto),
                                 ('pressed', self.cor_texto)])
        
        self.style.configure('TEntry',
                           fieldbackground=self.cor_widgets,
                           bordercolor=self.cor_borda,
                           insertcolor=self.cor_texto,
                           lightcolor=self.cor_borda,
                           darkcolor=self.cor_borda)
        
        self.style.configure('TCombobox',
                       fieldbackground=self.cor_widgets,
                       background=self.cor_widgets,
                       foreground=self.cor_texto,  
                       selectbackground=self.cor_destaque,  
                       selectforeground='white',  
                       arrowcolor=self.cor_texto,  
                       bordercolor=self.cor_borda,
                       lightcolor=self.cor_borda,
                       darkcolor=self.cor_borda,
                       padding=5)  

        self.style.map('TCombobox',
                    fieldbackground=[('readonly', self.cor_widgets)],
                    background=[('readonly', self.cor_widgets)],
                    foreground=[('readonly', self.cor_texto)],
                    selectbackground=[('readonly', self.cor_destaque)],
                    selectforeground=[('readonly', 'white')])
            
        self.style.configure('Treeview',
                           background=self.cor_tree,
                           fieldbackground=self.cor_tree,
                           foreground=self.cor_texto,
                           borderwidth=0,
                           rowheight=30)
        self.style.configure('Treeview.Heading',
                           background=self.cor_borda,
                           foreground=self.cor_texto,
                           relief='flat',
                           borderwidth=1,
                           bordercolor=self.cor_borda)
        self.style.map('Treeview.Heading',
                     background=[('active', self.cor_destaque)])
        
        self.style.configure('Vertical.TScrollbar',
                           background=self.cor_widgets,
                           troughcolor=self.cor_fundo,
                           bordercolor=self.cor_borda)
        self.style.configure('Horizontal.TScrollbar',
                           background=self.cor_widgets,
                           troughcolor=self.cor_fundo,
                           bordercolor=self.cor_borda)

    def _configurar_janela_principal(self):
        self.root.title("Controle de Estoque")
        self.root.geometry("1100x750")
        self.root.configure(bg=self.cor_fundo)
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_login(self):
        self.root.withdraw()
        LoginWindow(self.root, self.init_ui)

    def init_ui(self):
        self.root.deiconify()
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.criar_aba_cadastro()
        self.criar_aba_movimentacao()
        self.criar_aba_consulta()
        self.atualizar_lista()

        self.style.theme_use('clam')  
        self.notebook.update_idletasks()

    def criar_aba_cadastro(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Cadastro")
        
        frame.columnconfigure(1, weight=1)
        
        campos = [
            ("Código:", 0, 'codigo_entry'),
            ("Nome:", 1, 'nome_entry'),
            ("Quantidade:", 2, 'quantidade_entry'),
            ("Preço:", 3, 'preco_entry')
        ]
        
        for texto, linha, nome in campos:
            lbl = ttk.Label(frame, text=texto)
            lbl.grid(row=linha, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(frame)
            entry.grid(row=linha, column=1, padx=5, pady=5, sticky='ew')
            setattr(self, nome, entry)

        lbl_categoria = ttk.Label(frame, text="Categoria:")
        lbl_categoria.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        
        self.categoria_var = tk.StringVar()
        self.categoria_combobox = ttk.Combobox(
            frame,
            textvariable=self.categoria_var,
            values=list(self.sistema.categorias.keys()),
            state='readonly',
            style='TCombobox'
        )
        self.categoria_combobox.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.categoria_combobox.set("Selecione")
        self.categoria_combobox.bind("<<ComboboxSelected>>", self.atualizar_subcategorias)

        self.lbl_subcategoria = ttk.Label(frame, text="Subcategoria:")
        self.lbl_subcategoria.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.lbl_subcategoria.grid_remove()
        
        self.subcategoria_var = tk.StringVar()
        self.subcategoria_combobox = ttk.Combobox(
            frame,
            textvariable=self.subcategoria_var,
            state='readonly',
            style='TCombobox'
        )
        self.subcategoria_combobox.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        self.subcategoria_combobox.grid_remove()

        self.lbl_armazenamento = ttk.Label(frame, text="Armazenamento:")
        self.lbl_armazenamento.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.lbl_armazenamento.grid_remove()
        
        self.armazenamento_var = tk.StringVar()
        self.armazenamento_combobox = ttk.Combobox(
            frame,
            textvariable=self.armazenamento_var,
            state='readonly',
            style='TCombobox'
        )
        self.armazenamento_combobox.grid(row=6, column=1, padx=5, pady=5, sticky='ew')
        self.armazenamento_combobox.grid_remove()

        self.novo_var = tk.BooleanVar()
        chk_novo = ttk.Checkbutton(frame, text="Novo", variable=self.novo_var)
        chk_novo.grid(row=7, column=0, padx=5, pady=5, sticky='w')
        
        self.seminovo_var = tk.BooleanVar()
        chk_seminovo = ttk.Checkbutton(frame, text="Semi-novo", variable=self.seminovo_var)
        chk_seminovo.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        self.btn_cadastrar = ttk.Button(frame, text="Cadastrar", command=self.cadastrar_produto)
        self.btn_cadastrar.grid(row=8, column=0, columnspan=2, pady=10, sticky='ew')

    def atualizar_subcategorias(self, event=None):
        self.subcategoria_var.set('')
        self.armazenamento_var.set('')
        
        categoria = self.categoria_var.get().strip().upper()
        
        self.subcategoria_combobox.grid_remove()
        self.lbl_subcategoria.grid_remove()
        self.armazenamento_combobox.grid_remove()
        self.lbl_armazenamento.grid_remove()

        if categoria in self.sistema.categorias:
            subcats = self.sistema.categorias[categoria]
            self.subcategoria_combobox['values'] = subcats
            self.subcategoria_combobox.set(subcats[0] if subcats else '')
            self.subcategoria_combobox.grid()
            self.lbl_subcategoria.grid()
            
            if categoria in self.sistema.armazenamentos:
                armazenamentos = self.sistema.armazenamentos[categoria]
                self.armazenamento_combobox['values'] = armazenamentos
                self.armazenamento_combobox.set(armazenamentos[0] if armazenamentos else '')
                self.armazenamento_combobox.grid()
                self.lbl_armazenamento.grid()

    def criar_aba_movimentacao(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Movimentação")
        
        entrada_frame = ttk.LabelFrame(frame, text=" Entrada no Estoque ")
        entrada_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._add_movimentacao_fields(entrada_frame, "entrada")
        
        ttk.Button(entrada_frame, text="Registrar Entrada", command=self.registrar_entrada
                  ).grid(row=3, column=0, columnspan=2, pady=5, sticky='ew')
        
        saida_frame = ttk.LabelFrame(frame, text=" Saída do Estoque ")
        saida_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self._add_movimentacao_fields(saida_frame, "saida")
        
        ttk.Button(saida_frame, text="Registrar Saída", command=self.registrar_saida
                  ).grid(row=3, column=0, columnspan=2, pady=5, sticky='ew')
        
        frame.columnconfigure(0, weight=1)

    def _add_movimentacao_fields(self, parent, prefix: str):
        campos = [
            ("Código:", f"{prefix}_codigo"),
            ("Quantidade:", f"{prefix}_quantidade"),
            ("Responsável:", f"{prefix}_responsavel")
        ]
        
        for i, (label_text, var_name) in enumerate(campos):
            lbl = ttk.Label(parent, text=label_text)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            
            entry = ttk.Entry(parent)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            setattr(self, var_name, entry)
        
        parent.columnconfigure(1, weight=1)

    def criar_aba_consulta(self):
        """Cria a aba de consulta de estoque com tabela dimensionada corretamente"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Consulta")
        
        container = ttk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(
            container,
            columns=("Codigo", "Nome", "Quantidade", "Preco", "Categoria","Armazenamento", "Novo", "SemiNovo"),
            show="headings",
            style='Treeview'
        )
        
        colunas = [
            ("Codigo", 120, 'center'),
            ("Nome", 250, 'w'),
            ("Quantidade", 100, 'center'),
            ("Preco", 150, 'e'),
            ("Categoria", 150, 'center'),
            ("Armazenamento", 100, 'center'),
            ("Novo", 80, 'center'),
            ("SemiNovo", 100, 'center')
        ]
        
        for heading, width, anchor in colunas:
            self.tree.heading(heading, text=heading)
            self.tree.column(heading, width=width, anchor=anchor, stretch=False)
        
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style='Vertical.TScrollbar')
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview, style='Horizontal.TScrollbar')
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5, padx=5)
        
        botoes = [
            ("Atualizar", self.atualizar_lista),
            ("Copiar Log", self.copiar_log_produtos),
            ("Excluir", self.excluir_produto),
            ("Editar Preço", self.abrir_edicao_preco)
        ]
        
        for texto, comando in botoes:
            btn = ttk.Button(
                btn_frame,
                text=texto,
                command=comando,
                style='TButton'
            )
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.tree.tag_configure('estoque_zero', background='#542626')
        self.tree.tag_configure('estoque_baixo', background='#4a3c1a')

    def cadastrar_produto(self):
        codigo = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()
        preco = self.preco_entry.get().strip()
        novo = self.novo_var.get()
        seminovo = self.seminovo_var.get()
        categoria_principal = self.categoria_var.get().upper() 
        subcategoria = self.subcategoria_var.get() if categoria_principal in self.sistema.categorias else ""

        if not all([codigo, nome, quantidade, preco]) or categoria_principal == "SELECIONE":
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        if categoria_principal in self.sistema.categorias and not subcategoria:
            messagebox.showerror("Erro", f"Selecione uma subcategoria para {categoria_principal}!")
            return

        try:
            quantidade_int = int(quantidade)
            preco_float = float(preco.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser inteiro e preço deve ser número válido!")
            return

        if categoria_principal in self.sistema.categorias:
            categoria_final = f"{categoria_principal}:{subcategoria}" 
        else:
            categoria_final = categoria_principal

        sucesso, mensagem = self.sistema.cadastrar_produto(
            codigo, nome, quantidade_int, preco_float, novo, seminovo, categoria_final
        )

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.codigo_entry.delete(0, tk.END)
            self.nome_entry.delete(0, tk.END)
            self.quantidade_entry.delete(0, tk.END)
            self.preco_entry.delete(0, tk.END)
            self.categoria_combobox.set("Selecione")
            self.subcategoria_var.set("")
            self.subcategoria_combobox.grid_remove()
            self.lbl_subcategoria.grid_remove()
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
            self.entrada_codigo.delete(0, 'end')
            self.entrada_quantidade.delete(0, 'end')
            self.entrada_responsavel.delete(0, 'end')
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
            self.saida_codigo.delete(0, 'end')
            self.saida_quantidade.delete(0, 'end')
            self.saida_responsavel.delete(0, 'end')
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

            armazenamento = "N/A"
            nome_completo = produto.nome
            
            for padrao in ["GB", "TB", "/"]:
                if padrao in nome_completo.upper():
                    partes = nome_completo.split()
                    if partes:
                        ultima_parte = partes[-1].upper()
                        if any(p in ultima_parte for p in ["GB", "TB", "/"]):
                            armazenamento = partes[-1]
                            nome_completo = " ".join(partes[:-1])
                            break
            
            categoria_exibicao = produto.categoria.split(":")[-1].strip()
            
            self.tree.insert('', 'end', values=(
                produto.codigo,
                nome_completo,
                produto.quantidade,
                f"R$ {produto.preco:.2f}",
                categoria_exibicao,
                armazenamento,
                "Sim" if produto.novo else "Não",
                "Sim" if produto.seminovo else "Não"
            ), tags=tags)

    def copiar_log_produtos(self):
        try:
            if self.sistema.gerar_log_produtos():
                data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
                arquivo_log = self.sistema.logs_dir / f"log_produto_{data_atual}.txt"
                
                with open(arquivo_log, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                self.root.clipboard_clear()
                self.root.clipboard_append(conteudo)
                messagebox.showinfo("Sucesso", "Log copiado para área de transferência!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao copiar log: {str(e)}")

    def excluir_produto(self):
        try:
            item_selecionado = self.tree.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione um produto na tabela!")
                return

            codigo = self.tree.item(item_selecionado, 'values')[0]
            if codigo not in self.sistema.produtos:
                messagebox.showerror("Erro", "Produto não encontrado!")
                self.atualizar_lista()
                return

            produto = self.sistema.produtos[codigo]
            confirmacao = messagebox.askyesno(
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir permanentemente?\n\n"
                f"Código: {codigo}\n"
                f"Nome: {produto.nome}\n"
                f"Quantidade: {produto.quantidade} unidades"
            )
            
            if confirmacao:
                del self.sistema.produtos[codigo]
                if self.sistema.salvar_estoque():
                    self.atualizar_lista()
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir: {str(e)}")
            self.atualizar_lista()

    def abrir_edicao_preco(self):
        try:
            item_selecionado = self.tree.selection()
            if not item_selecionado:
                messagebox.showwarning("Aviso", "Selecione um produto na tabela!")
                return

            codigo = self.tree.item(item_selecionado, 'values')[0]
            if codigo not in self.sistema.produtos:
                messagebox.showerror("Erro", "Produto não encontrado!")
                self.atualizar_lista()
                return

            produto = self.sistema.produtos[codigo]
            
            self.janela_edicao = tk.Toplevel(self.root)
            self.janela_edicao.title(f"Editar Preço - {produto.nome}")
            self.janela_edicao.geometry("300x150")
            
            frame_edicao = ttk.Frame(self.janela_edicao)
            frame_edicao.pack(padx=20, pady=20, fill='both', expand=True)
            
            ttk.Label(frame_edicao, text=f"Preço atual: R$ {produto.preco:.2f}").pack(pady=5)
            ttk.Label(frame_edicao, text="Novo preço:").pack()
            
            self.novo_preco = ttk.Entry(frame_edicao)
            self.novo_preco.pack(pady=5)
            self.novo_preco.insert(0, f"{produto.preco:.2f}")
            
            ttk.Button(
                frame_edicao,
                text="Atualizar",
                command=lambda: self.atualizar_preco(codigo)
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar: {str(e)}")

    def atualizar_preco(self, codigo):
        try:
            novo_preco = float(self.novo_preco.get().replace(',', '.'))
            self.sistema.produtos[codigo].preco = novo_preco
            if self.sistema.salvar_estoque():
                self.janela_edicao.destroy()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Preço atualizado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoEstoque(root)
    root.mainloop()