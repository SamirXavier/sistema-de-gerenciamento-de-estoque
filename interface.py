import flet as ft
from negocio import Produto, Venda


def main(page: ft.Page):
    page.title = "Sistema de Gerenciamento de Estoque"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "adaptive"

    # Instâncias da camada de negócio
    produto_negocio = Produto()
    venda_negocio = Venda()

    # ========== CAMPOS PRODUTO ==========
    nome_input = ft.TextField(label="Nome do Produto", width=250)
    descricao_input = ft.TextField(label="Descrição", width=400, multiline=True)
    preco_input = ft.TextField(label="Preço (R$)", width=150)
    quantidade_input = ft.TextField(label="Quantidade", width=150)

    # ========== CAMPOS VENDA ==========
    produto_dropdown = ft.Dropdown(label="Produto", width=250)
    quantidade_venda_input = ft.TextField(label="Quantidade Vendida", width=150)

    # ========== TABELAS ==========
    tabela_produtos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Preço")),
            ft.DataColumn(ft.Text("Quantidade")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    tabela_vendas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Venda")),
            ft.DataColumn(ft.Text("Produto")),
            ft.DataColumn(ft.Text("Qtd. Vendida")),
            ft.DataColumn(ft.Text("Valor Total")),
            ft.DataColumn(ft.Text("Data")),
        ],
        rows=[]
    )

    # ========== FUNÇÕES AUXILIARES ==========
    def mostrar_mensagem(msg, cor="blue"):
        page.snack_bar = ft.SnackBar(ft.Text(msg, color="white"), bgcolor=cor, open=True)
        page.update()

    def atualizar_tabela_produtos(e=None):
        tabela_produtos.rows.clear()
        lista = produto_negocio.listar()
        produto_dropdown.options.clear()

        for p in lista:
            pid = p["ID"]
            produto_dropdown.options.append(ft.dropdown.Option(f'{pid} - {p["Nome"]}'))

            def remover(pid=pid):
                resultado = produto_negocio.remover(pid)
                mostrar_mensagem(resultado, "green" if "sucesso" in resultado else "red")
                atualizar_tabela_produtos()

            def aumentar(pid=pid):
                resultado = produto_negocio.ajustar_quantidade(pid, +1)
                mostrar_mensagem(resultado, "green" if "sucesso" in resultado else "red")
                atualizar_tabela_produtos()

            def diminuir(pid=pid):
                resultado = produto_negocio.ajustar_quantidade(pid, -1)
                mostrar_mensagem(resultado, "green" if "sucesso" in resultado else "red")
                atualizar_tabela_produtos()

            tabela_produtos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p["ID"]))),
                        ft.DataCell(ft.Text(p["Nome"])),
                        ft.DataCell(ft.Text(p["Descricao"])),
                        ft.DataCell(ft.Text(f'R$ {p["Preco"]:.2f}')),
                        ft.DataCell(ft.Text(str(p["Quantidade"]))),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.Icons.ADD, icon_color="green", tooltip="Aumentar", on_click=lambda e, pid=pid: aumentar(pid)),
                                    ft.IconButton(icon=ft.Icons.REMOVE, icon_color="orange", tooltip="Diminuir", on_click=lambda e, pid=pid: diminuir(pid)),
                                    ft.IconButton(icon=ft.Icons.DELETE_FOREVER, icon_color="red", tooltip="Excluir", on_click=lambda e, pid=pid: remover(pid)),
                                ]
                            )
                        ),
                    ]
                )
            )

        page.update()

    def atualizar_tabela_vendas(e=None):
        tabela_vendas.rows.clear()
        lista = venda_negocio.listar()
        produtos = {p["ID"]: p["Nome"] for p in produto_negocio.listar()}

        for v in lista:
            pid = v["id_produto"]
            tabela_vendas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(v["id_venda"]))),
                        ft.DataCell(ft.Text(produtos.get(pid, "Desconhecido"))),
                        ft.DataCell(ft.Text(str(v["Quantidade_vendida"]))),
                        ft.DataCell(ft.Text(f'R$ {v["valor_total"]:.2f}')),
                        ft.DataCell(ft.Text(v["data_venda"])),
                    ]
                )
            )

        page.update()

    def cadastrar_produto(e):
        nome = nome_input.value.strip()
        descricao = descricao_input.value.strip()
        preco = preco_input.value.strip()
        quantidade = quantidade_input.value.strip()

        if not nome or not descricao or not preco or not quantidade:
            mostrar_mensagem("Preencha todos os campos!", "red")
            return

        try:
            preco = float(preco)
            quantidade = int(quantidade)
        except ValueError:
            mostrar_mensagem("Preço e quantidade devem ser numéricos!", "red")
            return

        resultado = produto_negocio.cadastrar(nome, descricao, preco, quantidade)
        mostrar_mensagem(resultado, "green" if "sucesso" in resultado else "red")
        atualizar_tabela_produtos()

        nome_input.value = ""
        descricao_input.value = ""
        preco_input.value = ""
        quantidade_input.value = ""
        page.update()

    def registrar_venda(e):
        if not produto_dropdown.value or not quantidade_venda_input.value:
            mostrar_mensagem("Selecione um produto e informe a quantidade!", "red")
            return

        try:
            id_produto = int(produto_dropdown.value.split(" - ")[0])
            quantidade_vendida = int(quantidade_venda_input.value)
        except ValueError:
            mostrar_mensagem("Quantidade deve ser numérica!", "red")
            return

        resultado = venda_negocio.registrar_venda(id_produto, quantidade_vendida)
        if "erro" in resultado:
            mostrar_mensagem(resultado, "red")
        else:
            mostrar_mensagem(resultado, "green")
            atualizar_tabela_produtos()
            atualizar_tabela_vendas()

        quantidade_venda_input.value = ""
        page.update()

    # ========== BOTÕES ==========
    cadastrar_btn = ft.ElevatedButton("Cadastrar Produto", on_click=cadastrar_produto)
    atualizar_btn = ft.ElevatedButton("Atualizar Produtos", on_click=atualizar_tabela_produtos)
    registrar_venda_btn = ft.ElevatedButton("Registrar Venda", on_click=registrar_venda)

    # ========== TELAS ==========
    aba_produtos = ft.Column(
        [
            ft.Text("📦 Cadastro de Produtos", size=22, weight="bold"),
            ft.Row([nome_input, preco_input, quantidade_input]),
            descricao_input,
            ft.Row([cadastrar_btn, atualizar_btn]),
            ft.Divider(),
            ft.Text("Produtos Cadastrados", size=18, weight="bold"),
            tabela_produtos,
        ]
    )

    aba_vendas = ft.Column(
        [
            ft.Text("💰 Registro de Vendas", size=22, weight="bold"),
            ft.Row([produto_dropdown, quantidade_venda_input, registrar_venda_btn]),
            ft.Divider(),
            ft.Text("Histórico de Vendas", size=18, weight="bold"),
            tabela_vendas,
        ]
    )

    abas = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Produtos", icon=ft.Icons.STORE, content=aba_produtos),
            ft.Tab(text="Vendas", icon=ft.Icons.SHOPPING_CART, content=aba_vendas),
        ],
        expand=1,
    )

    page.add(abas)

    atualizar_tabela_produtos()
    atualizar_tabela_vendas()


# Execução do app
ft.app(target=main)
