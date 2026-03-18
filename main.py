from cliente import Cliente
from estoque import Estoque
import os
import time
resp="s"
def limpar():
    os.system("cls" if os.name=="nt" else "clear")
def animar_reticencias(texto):
    for _ in range(3):
        for pontos in range(4):  
            print(f"\r{texto}{'.' * pontos}   ", end="", flush=True)
            time.sleep(0.5)
    print()
class Main:
    def __init__(self):
        self.estoque=Estoque()
        self.cliente=Cliente(self.estoque)
        

#menu do sistema    
    def menu(self):
        while True:
            op=self.cliente.escolha()
            limpar()
            time.sleep(1)
            if op=="1":
                animar_reticencias("Processando compra")
                limpar()
                self.cliente.compra()
                input("\nPressione enter para continuar")
            if op=="2":
                animar_reticencias("Processando venda")
                limpar()
                self.cliente.venda()
                input("\nPressione enter para continuar")

            if op=="3":
                limpar()
                animar_reticencias("Consultando saldo")
                limpar()
                print(f"O saldo é {self.estoque.saldo}")
                input("\nPressione enter para continuar")
            if op=="4":
                limpar()
                animar_reticencias("Consultando estoque")
                print(f"A quantidade de ingressos no estoque é {self.estoque.quantidade}")
                input("\nPressione enter para continuar")
            if op=="5":
                limpar()
                animar_reticencias("Saindo")
                return
main=Main()
main.menu()


