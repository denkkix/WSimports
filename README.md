# 🏬 Controle de Estoque - WSImports

Sistema completo de gerenciamento de estoque para lojas de eletrônicos e celulares, com interface intuitiva e relatórios automáticos.

## 🔐 Acesso ao Sistema
- **Login seguro** com tela de autenticação
- **Senha padrão**: `1` (modificável no código-fonte)
- Interface moderna com tema escuro

## ✨ Funcionalidades Principais

### 📝 Cadastro de Produtos
- **Sistema de categorias completo**:
  - 🍎 Apple (13 subcategorias)
  - 📱 Xiaomi (24 subcategorias)
  - ⚙️ Samsung/Motorola/Realme
  - 🎮 Video Games
- **Detalhes do produto**:
  - Código único
  - Nome completo
  - Quantidade em estoque
  - Preço unitário
  - Armazenamento (variável por categoria)
  - Status (Novo/Semi-novo)

### 🔄 Movimentação de Estoque
- **Entradas**:
  - Adição de novos itens
  - Aumento de quantidade existente
- **Saídas**:
  - Controle de vendas
  - Baixa automática no estoque
- **Registro de responsável** por cada movimentação

### 🔍 Consulta e Gestão
- **Tabela interativa** com:
  - Destaque visual para estoque baixo
  - Códigos de cores:
    - 🔴 Vermelho = Esgotado
    - 🟡 Amarelo = Estoque baixo (<5 unidades)
- **Filtros** por categoria/marca
- **Edição rápida** de preços
- **Exclusão segura** de itens

### 📊 Relatórios Automáticos
- **Log diário** formatado para divulgação:
  - Lista organizada por categorias
  - Pronto para copiar (Ctrl+C)
- **Histórico** de movimentações
- **Backup automático** em JSON

## 🛠 Tecnologias Utilizadas
| Tecnologia | Finalidade |
|------------|------------|
| Python 3.x | Lógica principal |
| Tkinter | Interface gráfica |
| JSON | Armazenamento de dados |
| Pathlib | Manipulação de arquivos |
| Datetime | Registro temporal |

## ⚙️ Instalação e Uso
1. **Pré-requisitos**:
   ```bash
   Python 3.8+
2. **Execução**:
   ```bash
    git clone https://github.com/seuusuario/controle-estoque-techcell.git
    cd controle-estoque-techcell
    python controlwLogin.py
3. **Primeiro uso**:
  - O sistema criará automaticamente a estrutura de pastas
  - Use a senha padrão 1 para o primeiro acesso

## 📂 Estrutura de Arquivos
  ```
   ControleEstoqueData/
    ├── dados/
    │ └── estoque.json
    └── logs/
    ├── log_quantidades.txt
    └── log_produto_AAAA-MM-DD.txt
  ```
## 🎨 Personalização
### O sistema permite fácil modificação de:

 - Cores do tema

 - Categorias e subcategorias

 - Opções de armazenamento

## 🤝 Como Contribuir
- Contribuições são bem-vindas! Siga os passos:

- Faça um Fork

- Crie uma Branch (git checkout -b feature/nova-feature)

- Commit suas mudanças (git commit -m 'Adiciona nova feature')

- Push para a Branch (git push origin feature/nova-feature)

- Abra um Pull Request

Desenvolvido com ❤️ por Denki
