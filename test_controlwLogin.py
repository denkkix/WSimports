import unittest
from pathlib import Path
import shutil
import datetime
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from controlwLogin import SistemaEstoque

class TestSistemaEstoque(unittest.TestCase):
    def setUp(self):
        # Configura ambiente de teste isolado
        self.temp_dir = Path("test_temp_dir")
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir()
        self.dados_dir = self.temp_dir / "dados"
        self.logs_dir = self.temp_dir / "logs"
        self.dados_dir.mkdir()
        self.logs_dir.mkdir()

        # Configura sistema com paths de teste
        self.sistema = SistemaEstoque()
        self.sistema.diretorio_base = self.temp_dir
        self.sistema.diretorio_dados = self.dados_dir
        self.sistema.logs_dir = self.logs_dir
        self.sistema.estoque_path = self.dados_dir / "estoque.json"
        self.sistema.log_quantidades_path = self.logs_dir / "log_quantidades.txt"

    def tearDown(self):
        # Limpeza completa
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_cadastrar_produto(self):
        # Teste de cadastro válido
        sucesso, mensagem = self.sistema.cadastrar_produto(
            "TEST001", 
            "FONE XIAOMI REDMI BUDS 4", 
            "5", 
            "199.99", 
            True, 
            False, 
            "XIAOMI:FONE"
        )
        self.assertTrue(sucesso, f"Falha no cadastro: {mensagem}")
        self.assertIn("TEST001", self.sistema.produtos)
        
        # Teste de duplicação
        sucesso, mensagem = self.sistema.cadastrar_produto(
            "TEST001", 
            "FONE XIAOMI", 
            "5", 
            "199.99", 
            True, 
            False, 
            "XIAOMI:FONE"
        )
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Produto já cadastrado!")

    def test_entrada_estoque(self):
        # Configuração inicial
        self.sistema.cadastrar_produto("TEST002", "CABO USB", "10", "29.90", False, True, "XIAOMI:ACESSÓRIOS")
        
        # Entrada válida
        sucesso, mensagem = self.sistema.entrada_estoque("TEST002", "5", "FUNC001")
        self.assertTrue(sucesso)
        self.assertEqual(self.sistema.produtos["TEST002"].quantidade, 15)
        
        # Produto não existe
        sucesso, mensagem = self.sistema.entrada_estoque("INVALIDO", "5", "FUNC001")
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Produto não encontrado!")

    def test_saida_estoque(self):
        # Configuração
        self.sistema.cadastrar_produto("TEST003", "CARREGADOR", "8", "89.90", True, False, "XIAOMI:ACESSÓRIOS")
        
        # Saída válida
        sucesso, mensagem = self.sistema.saida_estoque("TEST003", "3", "FUNC002")
        self.assertTrue(sucesso)
        self.assertEqual(self.sistema.produtos["TEST003"].quantidade, 5)
        
        # Estoque insuficiente
        sucesso, mensagem = self.sistema.saida_estoque("TEST003", "10", "FUNC002")
        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Quantidade insuficiente em estoque!")

    def test_registrar_log_quantidades(self):
        # Configura produto com estoque zero
        self.sistema.cadastrar_produto("LOG001", "CASE CELULAR", "0", "49.90", False, True, "XIAOMI:ACESSÓRIOS")
        
        # Limpa log existente
        if self.sistema.log_quantidades_path.exists():
            self.sistema.log_quantidades_path.unlink()
        
        # Gera log
        produto = self.sistema.produtos["LOG001"]
        self.assertTrue(self.sistema.registrar_log_quantidades(produto))
        
        # Verifica conteúdo
        with open(self.sistema.log_quantidades_path, "r", encoding="utf-8") as f:
            log_content = f.read()
        self.assertIn("ESGOTADO", log_content)
        self.assertIn("LOG001", log_content)

    def test_salvar_e_carregar_estoque(self):
        # Limpa estoque atual
        self.sistema.produtos = {}
        
        # Cadastra novos produtos
        self.sistema.cadastrar_produto("SAVE001", "TELA PROTETORA REDMI", "20", "19.90", True, False, "XIAOMI:ACESSÓRIOS")
        self.sistema.cadastrar_produto("SAVE002", "PELÍCULA VIDRO NOTE 12", "15", "24.90", True, False, "XIAOMI:ACESSÓRIOS")
        
        # Salva estoque
        self.assertTrue(self.sistema.salvar_estoque())
        
        # Verifica se arquivo foi criado
        self.assertTrue(self.sistema.estoque_path.exists())
        
        # Cria novo sistema com mesmos paths
        novo_sistema = SistemaEstoque()
        novo_sistema.diretorio_base = self.temp_dir
        novo_sistema.diretorio_dados = self.dados_dir
        novo_sistema.logs_dir = self.logs_dir
        novo_sistema.estoque_path = self.dados_dir / "estoque.json"
        
        # Carrega estoque
        novo_sistema.carregar_estoque()
        
        # Verifica dados
        self.assertIn("SAVE001", novo_sistema.produtos)
        self.assertEqual(novo_sistema.produtos["SAVE001"].nome, "TELA PROTETORA REDMI")
        self.assertIn("SAVE002", novo_sistema.produtos)
        self.assertEqual(novo_sistema.produtos["SAVE002"].quantidade, 15)

    def test_gerar_log_produtos(self):
        # 1. Limpeza completa do estoque
        self.sistema.produtos = {}
        
        # 2. Cadastro de produtos usando apenas categorias válidas
        produtos_teste = [
            # Produto na subcategoria FONE (válida)
            ("FONE-001", "FONE XIAOMI BUDS 4", "5", "199.90", "XIAOMI:FONE"),
            # Produto na subcategoria REDMI 12 (válida)
            ("CEL-001", "XIAOMI REDMI 12", "3", "1299.90", "XIAOMI:REDMI 12"),
            # Produto com estoque zero não deve aparecer
            ("TAB-001", "XIAOMI REDMI PAD", "0", "1999.90", "XIAOMI:REDMI PAD")  
        ]
        
        for cod, nome, qtd, preco, cat in produtos_teste:
            self.sistema.cadastrar_produto(cod, nome, qtd, preco, True, False, cat)
        
        # 3. Geração do log
        self.assertTrue(self.sistema.gerar_log_produtos())
        
        # 4. Verificação do arquivo
        log_file = self.logs_dir / f"log_produto_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        self.assertTrue(log_file.exists())
        
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 5. Verificações essenciais
        print("\nConteúdo do log gerado:\n", content)  # Para debug
        
        # Verifica se produtos aparecem nas subcategorias corretas
        self.assertIn("FONE XIAOMI BUDS 4", content)
        self.assertIn("XIAOMI REDMI 12", content)
        self.assertNotIn("XIAOMI REDMI PAD", content)  # Não deve aparecer (estoque zero)
        
        # Verifica estrutura das categorias
        self.assertIn("• FONE:", content)
        self.assertIn("• REDMI 12:", content)
        self.assertIn("⬇ XIAOMI ⬇", content)

if __name__ == "__main__":
    unittest.main()