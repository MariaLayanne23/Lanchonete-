class Pilha:

    def __init__(self):
        self.itens = []

    # Adiciona uma ação no topo da pilha
    def empilhar(self, item):
        self.itens.append(item)

    # Remove e retorna a última ação
    def desempilhar(self):
        if self.esta_vazia():
            return None

        return self.itens.pop()

    # Verifica se a pilha está vazia
    def esta_vazia(self):
        return len(self.itens) == 0

    # Exibe as ações armazenadas
    def exibir(self):
        if self.esta_vazia():
            print("Nenhuma ação registrada.")
            return

        print("\n===== HISTÓRICO DE AÇÕES =====")

        for acao in reversed(self.itens):
            print(
                f"Pedido #{acao['id']} | "
                f"{acao['anterior']} -> {acao['novo']}"
            )
