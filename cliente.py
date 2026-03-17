from estoque import Estoque
class Cliente:
    def __init__(self):
        self.desejado=int(input("Quantos ingressos vc quer comprar/vender"))
        self.preco=self.desejado*int(input("Qual valor do ingresso"))

    def venda(self):
        while True:
            if self.estoque.quantidade<self.desejado:
                print("Quantidade desejada nao tem no estoque")
                continue 
            self.estoque.quantidade-=self.desejado
            self.estoque.saldo-=self.preco
            print("Venda efetuada")
            print(f"Vendemos {self.desejado} por {self.preco}")
            resp=input("Deseja continuar comprando? s/n: ")
            if resp=="n":
                return
    def compra(self):
        while True:
            if self.estoque.saldo<self.preco:
                print("Falta de saldo")
                continue 
            self.estoque.quantidade+=self.desejado
            self.estoque.saldo+=self.preco
            print("Compra efetuada")
            print(f"Compramos {self.desejado} por {self.preco}")
            resp1=input("Deseja continuar comprando? s/n: ")
            if resp1=="n":
                return


            

