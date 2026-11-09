from collections  import deque
from threading import Thread, Lock
import time
from estruturas.lista_encadeada import ListaEncadeada
from estruturas.pilha import Pilha
from estruturas.tabela_hash import TabelaHash
from receitas import receitas

# Tabela Hash para controle de estoque
estoque = TabelaHash()

# Estoque inicial em gramas (5 kg de cada ingrediente)
estoque.inserir("Carne", 100)
estoque.inserir("Frango", 5000)
estoque.inserir("Bacon", 5000)

historico_acoes = Pilha()

fila_pedidos = deque()

# Histórico de pedidos concluídos
pedidos_concluidos = ListaEncadeada()

proximo_id = 1
preparo_ativo = False

# 3 minutos por lanche (180 segundos)
TEMPO_POR_ITEM = 10

# Controle de acesso à fila
trava = Lock()


def registrar_pedido(carrinho, total):
    global proximo_id, preparo_ativo

    if not carrinho:
        print("Pedido não registrado: carrinho vazio.")
        return

    consumo = estoque.calcular_consumo(carrinho, receitas)

    iniciar_automaticamente = False

    with trava:

        # Verifica e desconta o estoque
        if not estoque.baixar_estoque(consumo):
            print("\nPedido não registrado por falta de ingredientes.")
            return

        pedido = {
            "id": proximo_id,
            "itens": carrinho.copy(),
            "total": total,
            "status": "Aguardando preparo",
            "tempo": len(carrinho) * TEMPO_POR_ITEM,
            "consumo": consumo
        }

        fila_pedidos.append(pedido)

        print(f"\nPedido #{proximo_id} registrado com sucesso!")
        print(f"Total: R$ {total:.2f}")
        print(f"Tempo estimado: {pedido['tempo']} segundos")

        print("\nIngredientes utilizados:")

        for ingrediente, quantidade in consumo.items():
            print(f"{ingrediente}: {quantidade} g")

        if not preparo_ativo:
            preparo_ativo = True
            iniciar_automaticamente = True

        proximo_id += 1

    if iniciar_automaticamente:
        Thread(target=processar_fila, daemon=True).start()


def processar_fila():
    global preparo_ativo

    while True:

        with trava:
            if not fila_pedidos:
                preparo_ativo = False
                return

            pedido = fila_pedidos[0]
            pedido["status"] = "Em preparo"

            tempo = pedido["tempo"]

            print(f"\nPedido #{pedido['id']} começou a ser preparado!")
            print(f"Tempo estimado: {pedido['tempo']} segundos")

        # Simula o tempo de preparo
        time.sleep(tempo)

        with trava:
            pedido["status"] = "Pronto"

            pedidos_concluidos.inserir(pedido) #conecta esse nó ao histórico encadeado.
            fila_pedidos.popleft()

            print(f"\nPedido #{pedido['id']} está pronto!")
            print("Pedido removido da fila de preparo.")


def consultar_pedido():

    print("\n===== PEDIDOS NA FILA =====")

    with trava:

        if not fila_pedidos:
            print("Não existem pedidos aguardando.")
        else:
            for pedido in fila_pedidos:
                print(f"\nPedido #{pedido['id']}")
                print(f"Itens: {', '.join(pedido['itens'])}")
                print(f"Total: R$ {pedido['total']:.2f}")
                print(f"Status: {pedido['status']}")
                print(f"Tempo estimado: {pedido['tempo']} segundos")

        print("\n===== PEDIDOS CONCLUÍDOS =====")

        pedidos_concluidos.exibir()


def gerenciar_estoque():

    while True:
        print("\n===== GERENCIAMENTO DE ESTOQUE =====")
        print("1 - Consultar estoque completo")
        print("2 - Consultar ingrediente")
        print("3 - Repor ingrediente")
        print("4 - Verificar estoque baixo")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":

            with trava:
                estoque.exibir_estoque()

        elif opcao == "2":

            ingrediente = input("Nome do ingrediente: ").strip()

            with trava:
                quantidade = estoque.buscar(ingrediente)

                if quantidade is None:
                    print("Ingrediente não encontrado!")
                else:
                    print(f"\nIngrediente: {ingrediente}")
                    print(f"Quantidade: {quantidade} g")
                    print(f"Quantidade: {quantidade / 1000:.2f} kg")

        elif opcao == "3":

            ingrediente = input("Ingrediente para reposição: ").strip()

            try:
                quantidade = float(
                    input("Quantidade recebida: ").replace(",", ".")
                )

                unidade = input("Unidade (kg ou g): ").strip().lower()

                if quantidade <= 0:
                    print("Informe uma quantidade maior que zero!")

                elif unidade not in ["kg", "g"]:
                    print("Unidade inválida! Utilize kg ou g.")

                else:
                    if unidade == "kg":
                        quantidade *= 1000

                    with trava:
                        quantidade_atual = estoque.buscar(ingrediente)

                        if quantidade_atual is None:
                            print("Ingrediente não cadastrado!")
                        else:
                            nova_quantidade = quantidade_atual + quantidade

                            estoque.inserir(
                                ingrediente,
                                nova_quantidade
                            )

                            print("\nReposição realizada!")
                            print(
                                f"Novo estoque: {nova_quantidade:.0f} g"
                            )
                            print(
                                f"Equivalente a: "
                                f"{nova_quantidade / 1000:.2f} kg"
                            )

            except ValueError:
                print("Digite uma quantidade numérica válida!")

        elif opcao == "4":

            with trava:
                estoque.verificar_estoque_baixo()

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")

def alterar_status(identificador, novo_status):

    with trava:

        pedido = pedidos_concluidos.buscar(identificador)

        if pedido is None:
            print("Pedido não encontrado no histórico.")
            return

        status_anterior = pedido["status"]

        # Registra a ação antes de modificar
        acao = {
            "id": identificador,
            "anterior": status_anterior,
            "novo": novo_status
        }

        historico_acoes.empilhar(acao)

        pedido["status"] = novo_status

        print(f"\nStatus do pedido #{identificador} alterado!")
        print(f"Anterior: {status_anterior}")
        print(f"Novo: {novo_status}")


def desfazer_ultima_acao():

    with trava:

        if historico_acoes.esta_vazia():
            print("\nNão existem ações para desfazer.")
            return

        acao = historico_acoes.desempilhar()

        pedido = pedidos_concluidos.buscar(acao["id"])

        if pedido is not None:
            pedido["status"] = acao["anterior"]

            print(f"\nAlteração do pedido #{acao['id']} desfeita!")
            print(f"Status restaurado: {acao['anterior']}")


def consultar_historico_acoes():
    historico_acoes.exibir()
