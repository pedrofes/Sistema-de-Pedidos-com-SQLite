# Sistema de Pedidos com SQLite

## Sobre o projeto

O projeto em questão é um sistema de pedidos baseado em Python e SQLite. O sistema foi desenvolvido como parte de um esquema de estudos para integração de Python com banco de dados. Este é o terceiro projeto dessa trilha com foco na integração com bancos de dados.

Desta vez, foram introduzidos os conceitos de chave primária, chave estrangeira e relacionamento entre tabelas. Neste sistema, é possível cadastrar clientes, produtos e pedidos, bem como visualizar informações, realizar atualizações e deletar registros por meio do cancelamento de pedidos.

## Funcionalidades

- Cadastrar cliente
- Listar clientes
- Cadastrar produto
- Listar produtos
- Buscar produto
- Realizar pedido
- Listar pedidos
- Atualizar estoque
- Cancelar pedido
- Encerrar o programa

## Tecnologias utilizadas

- Python
- SQLite

## Conceitos praticados

- Integração entre Python e SQLite
- Chave primária e chave estrangeira
- Relacionamento entre tabelas
- Criação e manipulação de banco de dados
- Operações SQL com `SELECT`, `INSERT`, `JOIN`, `DELETE` e `UPDATE`
- Consultas parametrizadas
- Uso de `fetchone()` e `fetchall()`
- Persistência e gerenciamento de dados
- Validação de entradas e tratamento de erros em Python
- Atualização de dados relacionados entre diferentes tabelas

## Estrutura do banco de dados

As tabelas do banco de dados estão estruturadas da seguinte forma (base dos comandos SQL):

```sql
TABLE clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)

TABLE produtos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
)

TABLE pedidos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
```

### Tabela `clientes`

A tabela `clientes` registra os dados dos clientes cadastrados no sistema. Estes incluem:

- ID do cliente
- Nome do cliente
- E-mail do cliente, que deve ser único no sistema

### Tabela `produtos`

A tabela `produtos` registra os dados referentes aos produtos cadastrados no sistema. Estes incluem:

- ID do produto
- Nome do produto
- Preço do produto
- Quantidade de unidades disponíveis em estoque

### Tabela `pedidos`

A tabela `pedidos` registra os pedidos realizados no sistema e estabelece o relacionamento entre clientes e produtos. Estes incluem:

- ID do pedido
- ID do cliente responsável pelo pedido
- ID do produto relacionado ao pedido
- Quantidade de unidades solicitadas

As colunas `cliente_id` e `produto_id` são chaves estrangeiras que relacionam a tabela `pedidos` às tabelas `clientes` e `produtos`, respectivamente.

## Como executar

É necessário ter o Python instalado no computador.

Baixe o projeto e primeiro execute o arquivo `criar_banco.py` para criar o banco de dados `estoque.db` e as tabelas utilizadas pelo sistema.

Em seguida, execute o arquivo `sistema_de_pedidos.py`.

O sistema conta com execução simples. O usuário deve selecionar uma das opções numéricas disponíveis no menu, que vão de 1 a 10.

## Status do projeto

Projeto finalizado.

Tempo de desenvolvimento: 1 dia.

## Autor

Pedro Fonseca Esperidião Silva