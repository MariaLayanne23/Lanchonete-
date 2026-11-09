from receitas import receitas


menu = {
    nome: dados["preco"]
    for nome, dados in receitas.items()
}


def exibir_cardapio():
    print("\n===== CARDÁPIO FASTLANCHE =====")

    for produto, preco in menu.items():
        print(f"{produto}: R$ {preco:.2f}")


def montar_pedido():
    carrinho = []

    while True:
        exibir_cardapio()

        produto_digitado = input(
            "\nDigite o lanche desejado (ou 'q' para finalizar): "
        ).strip().lower()

        if produto_digitado == "q":
            break

        produto_encontrado = None

        for nome in menu:
            if nome.lower() == produto_digitado:
                produto_encontrado = nome
                break

        if produto_encontrado is not None:
            carrinho.append(produto_encontrado)
            print(f"{produto_encontrado} adicionado ao carrinho!")
        else:
            print("Produto não encontrado. Tente novamente.")

    total = 0

    print("\n===== SEU CARRINHO =====")

    if not carrinho:
        print("Nenhum produto selecionado.")

    for produto in carrinho:
        preco = menu[produto]
        print(f"{produto}: R$ {preco:.2f}")
        total += preco

    print(f"\nTotal do pedido: R$ {total:.2f}")

    return carrinho, total
