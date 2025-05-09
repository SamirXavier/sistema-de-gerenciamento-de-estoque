import sqlite3
import logging


# Configuração do logging
# O arquivo de log será criado no mesmo diretório do script
logging.basicConfig(
    filename='app.log',      # Arquivo onde os logs serão salvos
    level=logging.INFO,      # Nível mínimo de mensagens que serão registradas
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class BancoDeDados:
    def __init__(self,nomeBD):
        self.nomeBD = nomeBD
        self.conexaoBD = None
        self.cursor = None
    
    
    def conectar(self):
        # método para conectar ao banco de dados SQLite
        # se o banco de dados não existir, ele será criado    
        try:
            # cria conexão com o Banco de Dados
            self.conexaoBD = sqlite3.connect(self.nomeBD)
            # cria cursor para executar comandos SQL
            self.cursor = self.conexaoBD.cursor()
            # Ativa o suporte a chaves estrangeiras
            self.cursor.execute("PRAGMA foreign_keys = ON")   
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
        finally:
            logging.info("Conexão com o banco de dados estabelecida com sucesso.")
    
    # método para desconectar do banco de dados SQLite
    # fecha a conexão e o cursor, se estiverem abertos
    def desconectar(self):
        if self.conexaoBD:
            try:
                self.conexaoBD.close()
                logging.info("Conexão com o banco de dados fechada.")
            except sqlite3.Error as e:
                logging.error(f"Erro ao fechar a conexão com o banco de dados: {e}")
            finally:
                self.conexaoBD = None
                self.cursor = None
        else:
            logging.warning("Tentativa de desconectar sem uma conexão ativa.")
    
    #funcao para criar as tabelas Produtos e Vendas no banco de dados
    # as tabelas serão criadas se não existirem/    
    def criar_tabelas(self):
        #cria tabela de clientes e produtos
        
        #conecta ao banco de dados
        self.conectar()
        
        # executa comandos SQL para criar as tabelas no banco de dados
        try:
            comando ="""
                CREATE TABLE IF NOT EXISTS Produtos (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nome TEXT NOT NULL,
                    Descricao TEXT NOT NULL,
                    Preco REAL NOT NULL CHECK (Preco >= 0),
                    Quantidade INTEGER NOT NULL CHECK (Quantidade >= 0)
                );
                CREATE TABLE IF NOT EXISTS Vendas (
                    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_produto INTEGER,
                    Quantidade_vendida INTEGER NOT NULL CHECK (Quantidade_vendida >= 0),
                    data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    valor_total REAL NOT NULL CHECK (valor_total >= 0),
                    FOREIGN KEY (id_produto) REFERENCES Produtos(ID)
                );
                """
            self.cursor.execute(comando)
            logging.info("Tabelas criadas com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar as tabelas: {e}")
        finally:
            self.desconectar()
    
    
    
    
#                                                                                     # \_______________________________________/ #                                                                       #
#---------------------------------------------------------------------------------------|operaçoes de produtos no banco de dados|-------------------------------------------------------------------------#
#                                                                                     # |_______________________________________| #                                                                       #
    
    
    
    # funçao para inserir um novo produto na tabela Produtos
    # os parâmetros são: nome, descricao, preco e quantidade
    def inserir_produto(self, nome, descricao, preco, quantidade):
       
        try:
            # conecta ao banco de dados
            self.conectar()
            
            # verifica se o preco e a quantidade sao maiores que zero
            if preco < 0 or quantidade < 0:
                raise ValueError("Preço e quantidade devem ser valores positivos.")

            # executa comando SQL para inserir um novo produto na tabela Produtos
            # os valores são passados como parâmetros para evitar SQL Injection
            comando = """
                INSERT INTO Produtos (Nome, Descricao, Preco, Quantidade)
                VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(comando,(nome, descricao, preco, quantidade))
            # confirma inclusão do produto no banco de dados
            self.conexaoBD.commit()
            logging.info(f"Produto '{nome}' inserido com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao inserir o produto: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()
    
    # função para listar todos os produtos na tabela Produtos
    def listar_produtos(self):
        try:
            # conecta ao banco de dados
            self.conectar()
            
            # executa comando sql para selecionar todos osprodutos na tabela produtos
            comando ='''
                select * from Produtos;
            '''
            self.cursor.execute(comando)
            # busca todos os produtos na tabela Produtos
            dados_produtos = self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao listar os produtos: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()
            return dados_produtos
            

    
    
    
    
    # funçao para editar um produto na tabela Produtos
    def alterar_produto(self, ID, nome, descricao, preco, quantidade):
        try:
            # conecta ao banco de dados
            self.conectar()
            
            # verifica se o preco e a quantidade sao maiores que zero
            if preco < 0 or quantidade < 0:
                raise ValueError("Preço e quantidade devem ser valores positivos.")

            # executa comando SQL para alterar um produto na tabela Produtos
            # os valores são passados como parâmetros para evitar SQL Injection
            comando = """
                UPDATE Produtos
                SET Nome = ?, Descricao = ?, Preco = ?, Quantidade = ?
                WHERE ID = ?
            """
            self.cursor.execute(comando,(nome, descricao, preco, quantidade, ID))
            # confirma alteração do produto no banco de dados
            self.conexaoBD.commit()
            logging.info(f"Produto '{nome}' alterado com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao alterar o produto: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()
    
    
    # função para excluir um produto na tabela Produtos
    def excluir_produto(self, ID):
        try:
            # conecta ao banco de dados
            self.conectar()

            # executa comando sql para excluir um produto na tabela produtos
            comando = '''
                DELETE FROM Produtos WHERE ID = ?;
            '''
            # o ID do produto a ser excluído é passado como parâmetro para evitar SQL Injection
            self.cursor.execute(comando, (ID,))
            
            if self.cursor.rowcount == 0:
                logging.warning(f"Nenhum produto com ID {ID} foi encontrado.")
            else:
                # confirma exclusão do produto no banco de dados
                self.conexaoBD.commit()
                logging.info(f"Produto com ID {ID} excluído com sucesso.")
            
        except sqlite3.Error as e:
            logging.error(f"Erro ao excluir o produto: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()
    
#                                                                                     # \_______________________________________/ #                                                                       #
#---------------------------------------------------------------------------------------| operaçoes de vendas no banco de dados |-------------------------------------------------------------------------#
#                                                                                     # |_______________________________________| #                                                                       #
    # função para registrar uma venda na tabela Vendas
    # os parâmetros são: id_produto, quantidade_vendida e valor_total
    def resgistrar_venda(self, id_produto, quantidade_vendida, valor_total):
        try:
            # conecta ao banco de dados
            self.conectar()

            # verifica se a quantidade vendida e o valor total sao maiores que zero
            if quantidade_vendida < 0 or valor_total < 0:
                raise ValueError("Quantidade vendida e valor total devem ser valores positivos.")
            
            comando = '''
                INSERT INTO Vendas (id_produto, Quantidade_vendida, valor_total)
                VALUES (?, ?, ?);
            '''
            self.cursor.execute(comando, (id_produto, quantidade_vendida, valor_total))
            # confirma inclusão da venda no banco de dados
            self.conexaoBD.commit()
            logging.info(f"Venda registrada com sucesso. ID do produto: {id_produto}, Quantidade vendida: {quantidade_vendida}, Valor total: {valor_total}.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao registrar a venda: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()
    
    # funçao para listar todas as vendas na tabela Vendas
    def listar_vendas(self):
        try:
            # conecta ao banco de dados
            self.conectar()
            
            # executa comando sql para selecionar todas as vendas na tabela vendas
            comando = '''
                SELECT * FROM Vendas;
            '''
            self.cursor.execute(comando)
            # busca todas as vendas na tabela Vendas
            dados_vendas = self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao listar as vendas: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()
            return dados_vendas
        

    # funçao para editar uma venda na tabela Vendas
    
    def alterar_venda(self, id_venda, id_produto, quantidade_vendida, valor_total):
        try:
            # conecta ao banco de dados
            self.conectar()
            
            # verifica se a quantidade vendida e o valor total sao maiores que zero
            if quantidade_vendida < 0 or valor_total < 0:
                raise ValueError("Quantidade vendida e valor total devem ser valores positivos.")

            # executa comando SQL para alterar uma venda na tabela Vendas
            # os valores são passados como parâmetros para evitar SQL Injection
            
            comando = '''
                UPDATE Vendas
                SET id_produto = ?, Quantidade_vendida = ?, valor_total = ?
                WHERE id_venda = ?;
            '''
            self.cursor.execute(comando, (id_produto, quantidade_vendida, valor_total, id_venda))
            # confirma alteração da venda no banco de dados
            self.conexaoBD.commit()
            logging.info(f"Venda com ID {id_venda} alterada com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao alterar a venda: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()

            
    # funçao para excluir uma venda na tabela Vendas
    
    def excluir_venda(self, id_venda):
        try:
            # conecta ao banco de dados
            self.conectar()

            # executa comando sql para excluir uma venda na tabela vendas
            comando = '''
                DELETE FROM Vendas WHERE id_venda = ?;
            '''
            # o ID da venda a ser excluída é passado como parâmetro para evitar SQL Injection
            self.cursor.execute(comando, (id_venda,))
            
            if self.cursor.rowcount == 0:
                logging.warning(f"Nenhuma venda com ID {id_venda} foi encontrada.")
            else:
                logging.info(f"Venda com ID {id_venda} excluída com sucesso.")
            # confirma exclusão da venda no banco de dados
            self.conexaoBD.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao excluir a venda: {e}")
        finally:
            # desconecta do banco de dados
            self.desconectar()       
    
 
            