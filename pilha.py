from typing import List, Any

class Pilha:
    # Inicializa a pilha com 4 elementos vazios e o topo com -1
    def __init__(self) -> None:
        self.__elem: List[int] = [-1,-1,-1,-1]
        self.__topo = -1

    # Verifica se a pilha está vazia
    def pilha_vazia(self) -> bool:
        return self.__topo == -1

    # Verifica se a pilha está cheia
    def pilha_cheia(self) -> bool:
        return self.__topo == 3
    
    # Retorna a quantidade de elementos na pilha
    def quantidade_elementos(self) -> int:
        return self.__topo + 1

    # Retorna o elemento do topo da pilha
    def elemento_do_topo(self) -> int:
        if not self.pilha_vazia():
            return self.__elem[self.__topo]
        else:
            raise ValueError('Erro: Pilha Vazia')
    
    # Empilha um elemento na pilha
    def empilha(self, x: int) -> None:
        if not self.pilha_cheia():
            self.__topo +=1 
            self.__elem[self.__topo] = x

    # Desempilha um elemento da pilha    
    def desempilha(self) -> Any:
        if not self.pilha_vazia():
            x = self.__elem[self.__topo]
            self.__elem[self.__topo] = -1
            self.__topo -= 1
            return x

    # Retorna uma lista com os elementos da pilha
    def get_elementos(self) -> List[int]:
        return self.__elem