



# 🧾 Documentação — Sistema de Gerenciamento de Estoque

## 🚀 **Como executar o aplicativo**

Para utilizar o sistema, você tem **duas opções**:

* 🟢 **Executar o aplicativo compilado:**

  Rode o executável gerado na pasta `dist/app.exe`.

* 🧩 **Ou executar o código-fonte diretamente (requer Python e dependências):**

  ```bash
  python app.py
  ```

---

## 🏢 **Informações Gerais**

**Nome do Projeto:** Sistema de Gerenciamento de Estoque
**Desenvolvido por:** Samir David de Souza Santos Xavier
**Linguagem:** Python 3
**Interface:** Flet
**Banco de Dados:** SQLite
**Arquitetura:** Aplicação em 3 Camadas (Interface, Negócio e Dados)
**Objetivo:** Controlar o cadastro de produtos, registro de vendas e atualização automática de estoque.

---

## 🧱 **Arquitetura em 3 Camadas**

### 1. Camada de Interface (`interface.py`)

Responsável pela **interação com o usuário**.
Foi implementada utilizando o framework **Flet**, que oferece uma interface gráfica moderna e multiplataforma.

**Principais funções:**

* Exibir e manipular dados de produtos e vendas.
* Cadastrar novos produtos.
* Atualizar estoque automaticamente após uma venda.
* Impedir que uma venda seja registrada com quantidade superior ao estoque.
* Apresentar feedback visual com mensagens de sucesso ou erro.
* Visualizar histórico de vendas.

**Componentes visuais principais:**

* **Abas (Tabs):**

  * “Produtos” — cadastro e gerenciamento de estoque.
  * “Vendas” — registro e listagem de vendas.
* **Tabelas (DataTable):** exibição de produtos e vendas.
* **Campos de entrada (TextField, Dropdown).**
* **Botões (ElevatedButton, IconButton).**

---

### 2. Camada de Negócio (`negocio.py`)

Contém as **regras da aplicação** e realiza a comunicação entre a interface e o banco de dados.

**Classes principais:**

#### 🧩 Classe `Produto`

Responsável pelas operações CRUD da tabela de produtos.

| Método                                          | Descrição                                                                        |
| ----------------------------------------------- | -------------------------------------------------------------------------------- |
| `cadastrar(nome, descricao, preco, quantidade)` | Insere um novo produto, validando se o nome já existe.                           |
| `listar()`                                      | Retorna todos os produtos cadastrados.                                           |
| `ajustar_quantidade(id_produto, valor)`         | Altera a quantidade do produto (positivo para aumentar, negativo para diminuir). |
| `remover(id_produto)`                           | Exclui o produto do banco de dados.                                              |

---

#### 💰 Classe `Venda`

Gerencia as vendas e faz o controle de estoque associado.

| Método                                    | Descrição                                                   |
| ----------------------------------------- | ----------------------------------------------------------- |
| `registrar_venda(id_produto, quantidade)` | Registra uma venda, verificando se há estoque suficiente.   |
| `listar()`                                | Retorna o histórico completo de vendas com datas e valores. |

**Regras implementadas:**

* A venda **não é permitida** se a quantidade for maior que o estoque.
* Após uma venda, o estoque é automaticamente reduzido.

---

### 3. Camada de Dados (`BancoDeDados.py`)

Gerencia o **acesso e persistência dos dados** via **SQLite**, garantindo que todas as informações fiquem salvas localmente.

**Principais responsabilidades:**

* Criar o banco de dados e tabelas automaticamente, se não existirem.
* Executar comandos SQL (INSERT, SELECT, UPDATE, DELETE).
* Retornar os resultados em formato acessível para o código Python.

**Tabelas:**

#### 🗃️ `Produtos`

| Campo        | Tipo         | Descrição                        |
| ------------ | ------------ | -------------------------------- |
| `ID`         | INTEGER (PK) | Identificador único do produto   |
| `Nome`       | TEXT         | Nome do produto                  |
| `Descricao`  | TEXT         | Detalhes do produto              |
| `Preco`      | REAL         | Valor unitário                   |
| `Quantidade` | INTEGER      | Quantidade disponível no estoque |

#### 💸 `Vendas`

| Campo                | Tipo         | Descrição                        |
| -------------------- | ------------ | -------------------------------- |
| `id_venda`           | INTEGER (PK) | Identificador da venda           |
| `id_produto`         | INTEGER (FK) | Produto vendido                  |
| `Quantidade_vendida` | INTEGER      | Quantidade vendida               |
| `valor_total`        | REAL         | Valor total (preço * quantidade) |
| `data_venda`         | TEXT         | Data e hora da venda             |

---

## ⚙️ **Dependências do Projeto**

| Biblioteca  | Função                                  | Instalação               |
| ----------- | --------------------------------------- | ------------------------ |
| **flet**    | Criação da interface gráfica            | `pip install flet`       |
| **sqlite3** | Banco de dados local (nativo no Python) | *(já incluso no Python)* |
| **logging** | Registro de logs internos               | *(já incluso no Python)* |

Para instalar todas as dependências de uma vez:

```bash
pip install -r requirements.txt
```

---

## 💻 **Execução do Projeto**

1. **Ativar o ambiente virtual (opcional, mas recomendado):**

   ```bash
   .venv\Scripts\activate
   ```

2. **Rodar o aplicativo:**

   ```bash
   python interface.py
   ```

3. O sistema abrirá automaticamente no navegador ou em uma janela Flet.

💡 *Ou, simplesmente, execute o arquivo `dist/app.exe` se você já gerou o executável com o PyInstaller.*

---

## 🧮 **Fluxo de Funcionamento**

1. **Cadastro de Produto:**

   * Usuário insere nome, descrição, preço e quantidade.
   * O sistema valida campos e cria o registro no banco.

2. **Consulta e Atualização:**

   * A tabela mostra os produtos atuais com botões para aumentar/diminuir estoque.

3. **Venda:**

   * Usuário escolhe um produto e define quantidade.
   * Se a quantidade for maior que o estoque, a venda é rejeitada.
   * Caso contrário, o estoque é atualizado e a venda é registrada.

4. **Histórico:**

   * A aba “Vendas” mostra todas as transações, com data, valor e produto vendido.

---

## 🧠 **Regras de Negócio**

* Não é permitido cadastrar produtos com nomes duplicados.
* Não é permitido registrar vendas sem selecionar produto e quantidade.
* Não é permitido vender quantidade superior à disponível no estoque.
* Toda venda atualiza automaticamente o estoque.
* Todas as ações retornam feedback visual (mensagem na tela).

---

## 🎨 **Interface do Usuário**

* **Tema claro e minimalista** (pode ser alterado para escuro se desejar).
* **Abas:** Produtos e Vendas.
* **Feedback visual:** SnackBars coloridos para avisos e confirmações.
* **Tabelas responsivas:** adaptam-se à quantidade de registros.

---

## 🧾 **Arquivo `requirements.txt`**

Exemplo simples:

```
flet==0.28.3
```

Gerado automaticamente com:

```bash
pip freeze > requirements.txt
```

---

## 🔐 **Possíveis Extensões Futuras**

* Login de usuários com controle de acesso.
* Relatórios de vendas diárias/mensais.
* Exportação de dados em CSV ou PDF.
* Gráficos de desempenho com base nas vendas.
* Backup automático do banco de dados.

---

## 🧩 **Conclusão**

O sistema cumpre integralmente os requisitos de CRUD, persistência de dados e arquitetura modular.
A estrutura em 3 camadas garante **organização, manutenção fácil e escalabilidade**.
A integração com Flet proporciona uma interface moderna e intuitiva, adequada tanto para uso local quanto futuro deploy web.

---

📘 **Resumo Técnico:**

* Python 3.11+
* Flet 0.28.3
* SQLite nativo
* Arquitetura: Interface → Negócio → Dados
* Operações: Create, Read, Update, Delete (CRUD)
* Regras: Controle de estoque e validação de vendas

---


