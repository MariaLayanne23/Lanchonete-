class TabelaHash:

    def __init__(self):
        self.tamanho = 10
        self.tabela = [[] for _ in range(self.tamanho)]

    # Calcula a posição do ingrediente na tabela
    def funcao_hash(self, chave):
        return sum(ord(letra) for letra in chave.lower()) % self.tamanho

    # Insere um ingrediente no estoque
    def inserir(self, ingrediente, quantidade):
        posicao = self.funcao_hash(ingrediente)

        for item in self.tabela[posicao]:
            if item[0] == ingrediente.lower():
                item[1] = quantidade
                print("Estoque atualizado!")
                return

        self.tabela[posicao].append([ingrediente.lower(), quantidade])
        print("Ingrediente cadastrado!")

    # Consulta um ingrediente
    def buscar(self, ingrediente):
        posicao = self.funcao_hash(ingrediente)

        for item in self.tabela[posicao]:
            if item[0] == ingrediente.lower():
                return item[1]

        return None

    # Remove um ingrediente do estoque
    def remover(self, ingrediente):
        posicao = self.funcao_hash(ingrediente)

        for item in self.tabela[posicao]:
            if item[0] == ingrediente.lower():
                self.tabela[posicao].remove(item)
                print("Ingrediente removido!")
                return

        print("Ingrediente não encontrado!")

    # Exibe todos os ingredientes cadastrados
    def exibir_estoque(self):
        print("\n===== ESTOQUE FASTLANCHE =====")

        for lista in self.tabela:
            for item in lista:
                print(f"Ingrediente: {item[0]} | Quantidade: {item[1]}")


    # Verifica ingredientes com estoque baixo
    def verificar_estoque_baixo(self, limite=5):
        print("\n===== ALERTA DE ESTOQUE =====")

        encontrou = False

        for lista in self.tabela:
            for item in lista:
                if item[1] <= limite:
                    print(f"ATENÇÃO: {item[0]} possui apenas {item[1]} unidades!")
                    encontrou = True

        if not encontrou:
            print("Todos os ingredientes possuem estoque suficiente!")


    # Calcula o consumo de ingredientes de um pedido
    def calcular_consumo(self, carrinho, receitas):

        consumo_total = {}

        for produto in carrinho:

            if produto not in receitas:
                continue

            ingredientes = receitas[produto]["ingredientes"]

            for ingrediente, quantidade in ingredientes.items():

                if ingrediente not in consumo_total:
                    consumo_total[ingrediente] = 0

                consumo_total[ingrediente] += quantidade

        return consumo_total
    
    # Verifica se existe estoque suficiente para o pedido
    def verificar_disponibilidade(self, consumo):

        for ingrediente, quantidade in consumo.items():

            estoque_atual = self.buscar(ingrediente)

            if estoque_atual is None:
                print(f"Ingrediente {ingrediente} não cadastrado!")
                return False

            if estoque_atual < quantidade:
                print(f"Estoque insuficiente de {ingrediente}!")
                print(f"Disponível: {estoque_atual} g")
                print(f"Necessário: {quantidade} g")
                return False

        return True


    # Desconta os ingredientes utilizados no pedido
    def baixar_estoque(self, consumo):

        if not self.verificar_disponibilidade(consumo):
            return False

        for ingrediente, quantidade in consumo.items():

            estoque_atual = self.buscar(ingrediente)

            nova_quantidade = estoque_atual - quantidade

            self.inserir(ingrediente, nova_quantidade)

        print("Estoque atualizado com sucesso!")
        return True


    # Verifica se algum ingrediente está com estoque baixo
    def verificar_estoque_baixo(self, limite=1000):

        print("\n===== ALERTA DE ESTOQUE =====")

        encontrou = False

        for lista in self.tabela:
            for item in lista:

                if item[1] <= limite:
                    print(
                        f"ATENÇÃO: {item[0]} possui "
                        f"apenas {item[1]} g em estoque!"
                    )
                    encontrou = True

        if not encontrou:
            print("Todos os ingredientes possuem estoque suficiente!")
