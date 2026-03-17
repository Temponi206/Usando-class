from cliente import Cliente
from estoque import Estoque
resp="s"
class Main:
    def __init__(self):
        self.estoque=Estoque()
        self.cliente=Cliente()


    def menu(self):
        resp=input("Deseja fazer alguma operação s/n? ")
        while resp!="n":
            print("1-Comprar")
            print("2-Vender")
            print("3-Consultar saldo")
            print("4-Consultar quantidade no estoque")
            op=input("Digite a opçao que deseja")
            if op=="1":
                self.cliente.compra()
            if op=="2":
                self.cliente.venda()
            if op=="3":
                print(f"O saldo é {self.estoque.saldo}")
            if op=="4":
                print(f"A quantidade de ingressos no estoque é {self.estoque.quantidade}")
main=Main()
main.menu()


