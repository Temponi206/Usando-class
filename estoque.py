import os
import time
def limpar():
    os.system("cls" if os.name=="nt" else "clear")
class Estoque:
    def __init__(self):
        qtd=int(input("Informe a quantidade de ingressos no estoque "))
        limpar()
        sal=int(input("Informe o valor em caixa da loja "))
        limpar()
        self.quantidade=qtd
        self.saldo=sal
        
