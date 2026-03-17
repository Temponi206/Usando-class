from estoque import Estoque
class Cliente:
    def __init__(self):
        self.desejado=10
        self.estoque=Estoque()
        
        
    def venda(self):
        if self.estoque.quantidade<self.desejado:
            return "Quantidade desejada nao tem no estoque"
        return "Venda Realizada"

cliente=Cliente()
print(cliente.venda())