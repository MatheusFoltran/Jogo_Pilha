#Jogo de Gerenciamento de Pilhas

from pilha import Pilha
from copy import deepcopy
from random import shuffle

#Faz a lista de pilhas do jogo
def lista_de_pilhas(n: int) -> list[Pilha]:
    pilha = Pilha()
    b: int = n + 2
    list_pilhas: list[Pilha] = []
    while b > 0:
        list_pilhas.append(deepcopy(pilha))
        b -= 1
    return list_pilhas

#Gera os números que serão sorteados nas pilhas
def lista_de_inteiros(n: int) -> list[int]:
    lista: list = []
    for c in range(0, 4):
        for d in range(1, n+1):
            lista.append(d)
    shuffle(lista)
    return lista

#Verifica se o jogo foi finalizado(se o jogador venceu)
def vencedor(lista_de_pilhas: list[Pilha]) -> bool:
    a = deepcopy(lista_de_pilhas)
    x = True
    for b in a:
        if b.quantidade_elementos() < 4 and b.quantidade_elementos() > 0:
            x = False
        else:
            while b.quantidade_elementos() > 1 and x == True:
                d = b.desempilha()
                c = b.elemento_do_topo()
                if c != d:
                    x = False
    return x

#Enche as pilhas com os números sorteados
def enche_lista_de_pilhas(list_int: list[int], list_pilhas: list[Pilha]) -> list[Pilha]:
    
    # Preenche as pilhas com a configuração atual
    contador = 0
    for c in range(len(list_pilhas) - 2):  # Exclui as duas últimas pilhas
        for d in range(4):  # Cada pilha recebe 4 elementos
            list_pilhas[c].empilha(list_int[contador])
            contador += 1
    
    # Se a configuração for vencedora, embaralha e recomeça
    if vencedor(list_pilhas):
        for pilha in list_pilhas:
            while not pilha.pilha_vazia():
                pilha.desempilha()
        shuffle(list_int)
        return enche_lista_de_pilhas(list_int, list_pilhas)
    else:
        return list_pilhas   
        
#Define as jogadas e suas condições, se uma das condições não for atendida a jogada não é feita
def jogada(lista_de_pilhas: list[Pilha], pilha1_posição: int, pilha2_posição: int) -> list[Pilha]:
    pilha1 = lista_de_pilhas[pilha1_posição]
    pilha2 = lista_de_pilhas[pilha2_posição]
    if not pilha1.pilha_vazia():
        if not pilha2.pilha_cheia():
            if not pilha2.pilha_vazia() and not pilha1.elemento_do_topo() == pilha2.elemento_do_topo():
                return False, 'Elementos do topo são diferentes'
            else:
                pilha2.empilha(pilha1.elemento_do_topo())
                pilha1.desempilha()
                return True, 'Jogada realizada com sucesso'
        else:
            return False, 'Pilha de destino cheia'
    else:
        return False, 'Pilha de origem vazia'