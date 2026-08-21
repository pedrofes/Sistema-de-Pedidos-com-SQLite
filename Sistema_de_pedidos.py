import sqlite3


def cadastrar_cliente():
    nome_cliente = input('Digite o nome do cliente que deseja cadastrar: ').strip()
    email = input('Digite o e-mail do cliente que está sendo cadastrado no sistema: ').strip()

    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT * FROM clientes WHERE email=?;
    ''', (email,))

    nome_busca = cursor.fetchone()

    if nome_busca:
        print('O e-mail em questão já consta como cadastrado no sistema.')
        conexao.close()
        return

    cursor.execute('''
        INSERT INTO clientes (nome, email)
        VALUES (?, ?)
    ''', (nome_cliente, email))

    conexao.commit()
    conexao.close()
    print('Cliente cadastrado no sistema.')


def listar_clientes():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT * FROM clientes;
    ''')

    clientes_cadastrados = cursor.fetchall()

    if clientes_cadastrados:
        for cliente in clientes_cadastrados:
            print(f'ID: {cliente[0]} - Cliente: {cliente[1]} - E-mail: {cliente[2]}')
    else:
        print('Nenhum cliente cadastrado no banco de dados.')

    conexao.close()


def cadastrar_produto():
    nome = input('Digite o nome do produto que deseja cadastrar: ').strip()

    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT * FROM produtos WHERE nome=?;
    ''', (nome,))

    produto_cadastrado = cursor.fetchone()

    if produto_cadastrado:
        estoque = int(input('Digite quantas unidades do produto você está cadastrando no estoque: ').strip())
        nova_quantidade = estoque + produto_cadastrado[3]

        cursor.execute('''
            UPDATE produtos SET estoque=? WHERE nome=?;
        ''', (nova_quantidade, produto_cadastrado[1]))

        conexao.commit()
        print('Produto já cadastrado no estoque, quantidade disponível atualizada.')

    else:
        preco = float(input('Digite o preço da unidade do produto que está sendo cadastrado: ').strip())
        estoque = int(input('Digite quantas unidades do produto deseja cadastrar no estoque: ').strip())

        cursor.execute('''
            INSERT INTO produtos (nome, preco, estoque) VALUES (?,?,?);
        ''', (nome, preco, estoque))

        conexao.commit()
        print('Cadastro do produto realizado com sucesso!')

    conexao.close()


def listar_produtos():

    conexao = sqlite3.connect('estoque.db')

    cursor = conexao.cursor()

    cursor.execute('''
    SELECT * FROM produtos;
    ''')

    produtos_cadastrados = cursor.fetchall()

    if produtos_cadastrados:

        for produto in produtos_cadastrados:
            print(f'Produto: {produto[1]} cadastrado com o código: {produto[0]}. Unidades em estoque: {produto[3]}. Preço por unidade: R$ {produto[2]}.')

    else:
        print('Nenhum produto cadastrado em estoque.')


    conexao.close()


def buscar_produto():

    conexao = sqlite3.connect('estoque.db')

    cursor = conexao.cursor()

    print('Para buscar um produto por número do código id, digite 1.')
    print('Para buscar um produto por nome, digite 2.')

    try:
        opção = int(input('Digite o número de sua opcao: ').strip())

    except ValueError:
        print('Digite apenas números.')
        conexao.close()
        return

    if opção == 1:

        try:

            codigo = int(input('Digite o código do produto que você está buscando: ').strip())

            cursor.execute('''
            SELECT * FROM produtos WHERE id=?;
            ''',(codigo,))


            produto_busca = cursor.fetchone()

            if produto_busca:
                print(f'O produto: {produto_busca[1]}, de id: {produto_busca[0]} foi encontrado no cadastro do estoque com {produto_busca[3]} unidades disponíveis. Preço por unidade de {produto_busca[2]}.')

            else:
                print('Nenhum produto com esse código de id foi encontrado no estoque.')

        except ValueError:
            print('Digie apenas um número das opções disponíveis.')

    elif opção == 2:
        nome_busca = input('Digite o nome do produto que está buscando no cadastrado: ').strip()

        cursor.execute('''
        SELECT * FROM produtos WHERE nome=?;
        ''', (nome_busca,)
        )

        produto_encontrado = cursor.fetchone()

        if produto_encontrado:
            print(f'O produto: {produto_encontrado[1]}, de id: {produto_encontrado[0]} foi encontrado no cadastro do estoque com {produto_encontrado[3]} unidades disponíveis. Preço por unidade de {produto_encontrado[2]}.')


        else:
            print('Nenhum produto com este nome foi encontrado no cadastro do estoque.')


    else:
        print('Digite apenas o número de uma das opções disponíveis, 1 ou 2.')


    conexao.close()


def realizar_pedido():
    conexao = sqlite3.connect('estoque.db')

    cursor = conexao.cursor()

    nome_cliente = input('Digite o nome do cliente: ').strip()
    nome_produto = input('Digite o nome do produto que deseja pedir: ').strip()

    cursor.execute('''
    SELECT * FROM clientes WHERE nome = ?; ''',
    (nome_cliente,))

    cliente_encontrado = cursor.fetchone()


    if cliente_encontrado:

        print('Cliente encontrado no sistema de cadastros.')
        print('Verificando estoque do produto.')

        cursor.execute('''
        SELECT * FROM produtos WHERE nome = ?; ''',
        (nome_produto,))

        produto_selecionado = cursor.fetchone()

        if produto_selecionado:
            print(f'Produto encontrado no estoque')
            try: 
                quantidade = int(input('Digite quantas unidades do produto deseja em números: ').strip())
            except ValueError:
                print('Digite apenas números.')
                conexao.close()
                return

            if quantidade <= 0:
                print('Digite um número maior do que 0.')
                conexao.close()
                return

            if produto_selecionado[3] >= quantidade:
                print(f'A quantidade disponível em estoque é suficiente para realizar o pedido.')

                cursor.execute(
                '''INSERT INTO pedidos (cliente_id, produto_id, quantidade) VALUES (?,?,?) ''', (cliente_encontrado[0], produto_selecionado[0], quantidade) )

                print(f'Pedido realizado com sucesso!')

                nova_quantidade_estoque = produto_selecionado[3] - quantidade

                cursor.execute('''
                UPDATE produtos SET estoque=? WHERE nome=?;
                ''', (nova_quantidade_estoque, produto_selecionado[1]))

                conexao.commit()

                print('Dados do estoque atualizados!')
                print('Obrigado pela compra!')

                conexao.close()
                return

            else:
                print(f'A quantidade disponível em estoque não é suficiente para o pedido. Atualmente, contamos com {produto_selecionado[3]} unidades do produto {produto_selecionado[1]}.')
                conexao.close()
                return

        else:
            print('Nenhum produto com esse nome está cadastrado no estoque.')
            conexao.close()

    else:
        print('Cliente não encontrado no cadastrado. Por gentileza, realize primeiro seu cadastro no sistema.')
        conexao.close()

def listar_pedidos():
    conexao = sqlite3.connect('estoque.db')

    cursor = conexao.cursor()

    cursor.execute(
    '''SELECT pedidos.id, clientes.nome, produtos.nome, pedidos.quantidade
    FROM pedidos
    JOIN clientes
    ON pedidos.cliente_id = clientes.id
    JOIN produtos
    ON pedidos.produto_id = produtos.id;
    ''')

    pedidos = cursor.fetchall()

    if pedidos:
        for pedido in pedidos:
            print(f'Código do pedido {pedido[0]} - Cliente do pedido: {pedido[1]} - Nome do produto: {pedido[2]} - Unidades adquiridas: {pedido[3]}.')
        print('Estes são todos os pedidos registrados no estoque.')
    else:
        print('Nenhum pedido cadastrado no sistema.')

    conexao.close()

def atualizar_estoque():

    conexao = sqlite3.connect('estoque.db')

    cursor = conexao.cursor()

    cursor.execute('''
    SELECT * FROM produtos;'''
    )

    produtos_em_estoque = cursor.fetchall()

    if produtos_em_estoque:
        nome_do_produto = input('Digite o nome do produto que deseja atualizar os dados: ').strip()

        cursor.execute('''
            SELECT * FROM produtos WHERE nome=?;
            ''', (nome_do_produto,)
            )

        produto_encontrado = cursor.fetchone()

        if produto_encontrado:

            try:
                opcao = int(input('Se você deseja alterar o preço do produto, digite 1. Se você deseja alterar a quantidade disponível em estoque (unidades), digite 2. Se deseja alterar as duas informações, digite 3: '))

                if opcao == 1:
                    try:
                        novo_preco = float(input('Digite o novo preço que deseja definir para o produto: ').strip())
                    except ValueError:
                        print('Digite apenas números.')
                        conexao.close()
                        return

                    if novo_preco < 0:
                        print('Digite um valor maior ou igual a zero para o produto.')
                        conexao.close()
                        return

                    cursor.execute('''
                    UPDATE produtos SET preco=? WHERE nome=?;
                    ''',(novo_preco, produto_encontrado[1]))

                    conexao.commit()
                    print('Alteração realizada com sucesso.')
                    print(f'O novo preço do produto {produto_encontrado[1]} é de R$ {novo_preco}.')
                    conexao.close()
                    return

                elif opcao == 2:
                    try:
                        quantidade = int(input('Digite a nova quantidade do produto disponível no estoque em unidades: ').strip())
                                                
                    except ValueError:
                        print('Digite apenas números.')
                        conexao.close()
                        return

                    if quantidade <0:
                        print('Digite apena um número maior ou igual a 0.')
                        conexao.close()
                        return

                    cursor.execute('''
                        UPDATE produtos SET estoque=? WHERE nome=?;
                        ''',(quantidade, produto_encontrado[1]))

                    conexao.commit()

                    print('Alteração realizada com sucesso.')
                    print(f'O {produto_encontrado[1]} conta com {quantidade} unidades disponíveis em estoque no momento.')
                    conexao.close()
                    return

                elif opcao == 3:

                    try:
                        novo_preco = float(input('Digite o novo preço do produto: ').strip())
                    except ValueError:
                        print('Digite apenas números.')
                        conexao.close()
                        return

                    if novo_preco < 0:
                        print('Digite um valor maior ou igual a zero para o preço.')
                        conexao.close()
                        return

                    try:
                        quantidade = int(input('Digite a nova quantidade do produto disponível no estoque em unidades: ').strip())
                                                
                    except ValueError:
                        print('Digite apenas números.')
                        conexao.close()
                        return

                    if quantidade <0:
                        print('Digite apena um número maior ou igual a 0.')
                        conexao.close()
                        return

                    cursor.execute('''
                    UPDATE produtos SET preco=?, estoque=? WHERE nome=?; 
                    ''', (novo_preco, quantidade, produto_encontrado[1]))

                    conexao.commit()
                    print('Atualização realizada com sucesso!')
                    print(f'Produto: {produto_encontrado[1]} - Preço por unidade: {novo_preco} - Unidades disponíveis no estoque: {quantidade}.')
                    conexao.close()

                else:
                    print('Digite apenas uma opção de 1 a 3.')
                    conexao.close()
                    return

            except ValueError:
                print('Digite apenas números.')
                conexao.close()
        else:
            print('Nenhum produto encontrado no sistema com esse nome.')
            conexao.close()
            return

    else:
        print('Nenhum produto cadastrado em estoque atualmente.')
        conexao.close()


def cancelar_pedido():
    try:
        id_remocao = int(input('Digite o id do pedido que deseja cancelar: ').strip())
    except ValueError:
        print('Digite apenas números.')
        return

    conexao = sqlite3.connect('estoque.db')

    cursor = conexao.cursor()

    cursor.execute('''
    SELECT * FROM pedidos WHERE id=?;
    ''',(id_remocao,))

    pedido_encontrado = cursor.fetchone()

    if pedido_encontrado:

        cursor.execute('''
        DELETE FROM pedidos WHERE id=?;
        ''', (id_remocao,))

        cursor.execute('''
        SELECT * FROM produtos WHERE id=?;
        ''',(pedido_encontrado[2],))

        produto_atualizar = cursor.fetchone()

        nova_quantidade = pedido_encontrado[3] + produto_atualizar[3]

        cursor.execute('''
        UPDATE produtos SET estoque=? WHERE id=?;
        ''', (nova_quantidade,produto_atualizar[0]))

        conexao.commit()
        print('Pedido cancelado!')

        conexao.close()

    else:
        print('O pedido em questão não está registrado no sistema.')
        conexao.close()
        return

def encerrar_programa():
    print('Encerrando programa.')
    return False


def menu():
    while True:
        print('==== Menu do Sistema de Pedidos ====')
        print('Confira as opções abaixo:')
        print('1. Cadastrar cliente')
        print('2. Listar clientes')
        print('3. Cadastrar produto')
        print('4. Listar produtos')
        print('5. Buscar produto')
        print('6. Realizar pedido')
        print('7. Listar pedidos')
        print('8. Atualizar estoque')
        print('9. Cancelar pedido')
        print('10. Encerrar programa\n')

        try:
            opcao = input('Digite o número da opção que deseja acessar: ').strip()
            opcao = int(opcao)
        except ValueError:
            print('Digite apenas números.')
            continue

        if opcao == 1:
            cadastrar_cliente()
        elif opcao == 2:
            listar_clientes()
        elif opcao == 3:
            cadastrar_produto()
        elif opcao == 4:
            listar_produtos()
        elif opcao == 5:
            buscar_produto()
        elif opcao == 6:
            realizar_pedido()
        elif opcao == 7:
            listar_pedidos()
        elif opcao == 8:
            atualizar_estoque()
        elif opcao == 9:
            cancelar_pedido()
        elif opcao == 10:
            encerrar_programa()
            print('Programa encerrado.')
            break
        else:
            print('Digite apenas o número de uma das opções apresentadas pelo sistema.')


menu()