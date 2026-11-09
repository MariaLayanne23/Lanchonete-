# Classe que representa cada elemento da lista
class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


# Classe que controla a lista encadeada
class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    # Adiciona um elemento no final da lista
    def inserir(self, dado):
        novo_no = No(dado)

        if self.inicio is None:
            self.inicio = novo_no
        else:
            atual = self.inicio

            while atual.proximo is not None:
                atual = atual.proximo

            atual.proximo = novo_no

        self.tamanho += 1

    # Exibe todos os elementos
    def exibir(self):
        if self.inicio is None:
            print("Histórico vazio.")
            return

        atual = self.inicio

        while atual is not None:
            pedido = atual.dado

            print(f"\nPedido #{pedido['id']}")
            print(f"Itens: {', '.join(pedido['itens'])}")
            print(f"Total: R$ {pedido['total']:.2f}")
            print(f"Status: {pedido['status']}")

            atual = atual.proximo

    # Busca um pedido pelo identificador
    def buscar(self, identificador):
        atual = self.inicio

        while atual is not None:
            if atual.dado["id"] == identificador:
                return atual.dado

            atual = atual.proximo

        return None
