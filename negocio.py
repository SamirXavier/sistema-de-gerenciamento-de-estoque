# negocio.py
from BancoDeDados import BancoDeDados as BancoDados
from typing import List, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Estoque:
    def __init__(self, nome_bd: str = 'DadosProdutos.sqlite'):
        self.bd = BancoDados(nome_bd)
        self.bd.criar_tabelas()


class Produto(Estoque):
    def __init__(self, nome_bd: str = 'DadosProdutos.sqlite'):
        super().__init__(nome_bd)

    # Create
    def cadastrar(self, nome: str, descricao: str, preco: float, quantidade: int) -> str:
        nome = nome.strip()
        descricao = descricao.strip()

        # Validações simples
        if not nome:
            return "erro: nome é obrigatório"
        if preco < 0:
            return "erro: preço deve ser >= 0"
        if quantidade < 0:
            return "erro: quantidade deve ser >= 0"

        # Verifica duplicidade por nome
        if self.bd.produto_existe(nome):
            return "erro: o produto já existe"

        # Insere
        self.bd.inserir_produto(nome, descricao, preco, quantidade)
        return "produto cadastrado com sucesso"

    # Read (listar todos)
    def listar(self) -> List[Dict]:
        """
        Retorna lista de produtos (cada produto é um dict).
        Se ocorrer erro retorna lista vazia.
        """
        try:
            return self.bd.listar_produtos() or []
        except Exception as e:
            logging.error(f"Erro ao listar produtos no negócio: {e}")
            return []

    # Auxiliar: buscar por ID
    def buscar_por_id(self, id_produto: int) -> Optional[Dict]:
        produtos = self.listar()
        for p in produtos:
            # chave pode ser 'ID' ou 'Id' dependendo do DB; ajustamos para 'ID'
            if int(p.get('ID', p.get('Id', p.get('id', 0)))) == int(id_produto):
                return p
        return None

    # Update (completo: altera todos os campos)
    def atualizar(self, id_produto: int, nome: str, descricao: str, preco: float, quantidade: int) -> str:
        # Verifica existência
        produto = self.buscar_por_id(id_produto)
        if not produto:
            return "erro: produto não encontrado"

        nome = nome.strip()
        descricao = descricao.strip()
        if not nome:
            return "erro: nome é obrigatório"
        if preco < 0:
            return "erro: preço deve ser >= 0"
        if quantidade < 0:
            return "erro: quantidade deve ser >= 0"

        try:
            self.bd.alterar_produto(id_produto, nome, descricao, preco, quantidade)
            return "produto atualizado com sucesso"
        except Exception as e:
            logging.error(f"Erro ao atualizar produto: {e}")
            return "erro: falha ao atualizar produto"

    # Update de quantidade (ajuste incremental: delta pode ser negativo para diminuir)
    def ajustar_quantidade(self, id_produto: int, delta: int) -> str:
        produto = self.buscar_por_id(id_produto)
        if not produto:
            return "erro: produto não encontrado"

        nova_qnt = int(produto['Quantidade']) + int(delta)
        if nova_qnt < 0:
            return "erro: quantidade resultante não pode ser negativa"

        try:
            # Reaproveita alterar_produto (é necessário passar todos os campos)
            self.bd.alterar_produto(
                id_produto,
                produto['Nome'],
                produto['Descricao'],
                float(produto['Preco']),
                nova_qnt
            )
            return "quantidade atualizada com sucesso"
        except Exception as e:
            logging.error(f"Erro ao ajustar quantidade: {e}")
            return "erro: falha ao ajustar quantidade"

    # Delete
    def remover(self, id_produto: int) -> str:
        produto = self.buscar_por_id(id_produto)
        if not produto:
            return "erro: produto não encontrado"

        try:
            self.bd.excluir_produto(id_produto)
            return "produto removido com sucesso"
        except Exception as e:
            logging.error(f"Erro ao remover produto: {e}")
            return "erro: falha ao remover produto"


class Venda(Estoque):
    def __init__(self, nome_bd: str = 'DadosProdutos.sqlite'):
        super().__init__(nome_bd)

    # Registrar venda (diminui o estoque automaticamente)
    def registrar_venda(self, id_produto: int, quantidade_vendida: int, valor_total: Optional[float] = None) -> str:
        # validações
        if quantidade_vendida <= 0:
            return "erro: quantidade vendida deve ser maior que zero"

        # busca produto
        produto = Produto(self.bd.nomeBD).buscar_por_id(id_produto)
        if not produto:
            return "erro: produto não encontrado"

        estoque_atual = int(produto['Quantidade'])
        if quantidade_vendida > estoque_atual:
            return "erro: quantidade vendida maior que o estoque disponível"

        # se o valor_total não foi fornecido, calcula a partir do preço
        if valor_total is None:
            valor_total = float(produto['Preco']) * quantidade_vendida

        try:
            # registra venda
            self.bd.registrar_venda(id_produto, quantidade_vendida, float(valor_total))
            # decrementa estoque: reutiliza Produto.ajustar_quantidade com delta negativo
            p = Produto(self.bd.nomeBD)
            ajuste = p.ajustar_quantidade(id_produto, -int(quantidade_vendida))
            # verificar se ajuste foi bem-sucedido
            if "sucesso" not in ajuste:
                # caso o ajuste falhe, registrar um log e avisar (ideal: rollback em transação)
                logging.error(f"Venda registrada mas falha ao ajustar estoque: {ajuste}")
                return "aviso: venda registrada, mas falha ao ajustar estoque"
            return "venda registrada com sucesso"
        except Exception as e:
            logging.error(f"Erro ao registrar venda: {e}")
            return "erro: falha ao registrar venda"

    # listar vendas
    def listar(self) -> List[Dict]:
        try:
            return self.bd.listar_vendas() or []
        except Exception as e:
            logging.error(f"Erro ao listar vendas: {e}")
            return []

    # remover venda (nota: não repõe estoque automaticamente aqui)
    def remover_venda(self, id_venda: int) -> str:
        try:
            self.bd.excluir_venda(id_venda)
            return "venda removida com sucesso"
        except Exception as e:
            logging.error(f"Erro ao remover venda: {e}")
            return "erro: falha ao remover venda"

    # atualizar venda (atenção: não atualiza automaticamente o estoque aqui)
    def atualizar_venda(self, id_venda: int, id_produto: int, quantidade_vendida: int, valor_total: float) -> str:
        try:
            self.bd.alterar_venda(id_venda, id_produto, quantidade_vendida, valor_total)
            return "venda atualizada com sucesso"
        except Exception as e:
            logging.error(f"Erro ao atualizar venda: {e}")
            return "erro: falha ao atualizar venda"


# --- Uso rápido de teste (apenas se executar o arquivo diretamente) ---
if __name__ == "__main__":
    p = Produto()
    v = Venda()

    print("Cadastrando produto de teste:", p.cadastrar("teste", "descrição", 10.0, 5))
    print("Lista de produtos:", p.listar())
    prod = p.listar()[0] if p.listar() else None
    if prod:
        pid = prod['ID']
        print("Ajustar quantidade (-2):", p.ajustar_quantidade(pid, -2))
        print("Registrar venda (2):", v.registrar_venda(pid, 2))
        print("Produtos após venda:", p.listar())
