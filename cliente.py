import time
from estoque import Estoque
import estoque
import os
def limpar():
    os.system("cls" if os.name=="nt" else "clear")
def animar_reticencias(texto):
    for _ in range(3):
        for pontos in range(4):  
            print(f"\r{texto}{'.' * pontos}   ", end="", flush=True)
            time.sleep(0.5)
    print()
class Cliente:
    def __init__(self,estoque):
        self.estoque=estoque
        
        
    def escolha(self):
        print("-----------------Menu------------------")
        print("Bem vindo à loja de ingressos")
        print(f"Nosso estoque tem {self.estoque.quantidade} ingressos e o saldo é {self.estoque.saldo} reais")
        print("1-Comprar")
        print("2-Vender")
        print("3-Consultar saldo")
        print("4-Consultar quantidade no estoque")
        print("5-Sair")
        return input("Escolha uma opção: ")
        
    def venda(self):
        while True:
            print("Estoque tem ",self.estoque.quantidade," ingressos e o saldo é ",self.estoque.saldo," reais")
            print("Venda de ingressos")
            self.desejado=int(input("Informe a quantidade de ingressos que deseja vender "))
            self.preco=self.desejado*int(input("Informe o valor que deseja receber por cada ingresso "))
            if self.estoque.saldo<self.preco:
                print("Saldo insuficiente para realizar a venda")
                return False
            self.estoque.quantidade+=self.desejado
            self.estoque.saldo-=self.preco
            animar_reticencias("Processando venda")
            print("Venda efetuada")
            time.sleep(1)   
            print(f"Voce vendeu {self.desejado} ingressos por {self.preco} reais")
            resp=input("Deseja continuar vendendo? s/n: ")
            time.sleep(1)
            limpar()
            if resp=="n":
                return
    def compra(self):
        while True:
            print("Estoque tem ",self.estoque.quantidade," ingressos e o saldo é ",self.estoque.saldo," reais")
            print("Compra de ingressos" )
            self.desejado=int(input("Informe a quantidade de ingressos que deseja comprar "))
            self.preco=self.desejado*int(input("Informe o valor que deseja pagar por cada ingresso "))
            if self.estoque.quantidade<self.desejado:
                print("Falta de estoque") 
                return False
            self.estoque.quantidade-=self.desejado
            self.estoque.saldo+=self.preco
            animar_reticencias("Processando compra")
            time.sleep(3)
            print("Compra efetuada")
            time.sleep(1)
            print(f"Voce comprou {self.desejado} ingressos por {self.preco} reais")
            resp1=input("Deseja continuar comprando? s/n: ")
            time.sleep(1)
            limpar()
            if resp1=="n":
                return True


            

