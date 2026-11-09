from cardapio import exibir_cardapio, montar_pedido
from pedidos import (
    registrar_pedido,
    consultar_pedido,
    alterar_status,
    desfazer_ultima_acao,
    consultar_historico_acoes,
    gerenciar_estoque
)

def exibir_menu():
    print("\n===== FASTLANCHE =====")
    print("1 - Ver cardápio")
    print("2 - Montar pedido")
    print("3 - Consultar pedidos")
    print("4 - Consultar rotas")
    print("5 - Relatórios e estatísticas")
    print("6 - Alterar status de pedido concluído")
    print("7 - Desfazer última alteração")
    print("8 - Consultar histórico de ações")
    print("9 - Gerenciar estoque")
    print("0 - Sair")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: \n").strip()

        if opcao == "1":
            exibir_cardapio()

        elif opcao == "2":
            carrinho, total= montar_pedido()
            registrar_pedido(carrinho, total)

        elif opcao == "3":
            consultar_pedido()

        elif opcao == "4":
            print("Consulta de rotas em desenvolvimento.")

        elif opcao == "5":
            print("Relatórios em desenvolvimento.")
        
        elif opcao == "6":
            identificador = int(input("Número do pedido: "))
            novo_status = input("Novo status: ")
            alterar_status(identificador, novo_status)

        elif opcao == "7":
            desfazer_ultima_acao()

        elif opcao == "8":
            consultar_historico_acoes()
        
        elif opcao == "9":
            gerenciar_estoque()

        elif opcao == "0":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
