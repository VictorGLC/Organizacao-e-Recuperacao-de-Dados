from sys import argv
import io

# CONSTANTES
VALOR_BAIXO = ''
VALOR_ALTO = '~'
# VAR GLOBAL
numEOF = 0

def inicialize(caminho: str, numListas: int) -> tuple[list[str], list[str], list[io.TextIOWrapper], io.TextIOWrapper, bool]:
    anteriores = [VALOR_BAIXO] * numListas
    nomes = [VALOR_BAIXO] * numListas
    listas = [None] * numListas
    for i in range(numListas):
        nomeArq = f'{caminho}/lista{i}.txt'
        listas[i] = open(nomeArq, 'r')

    saida = open('saida.txt', 'w')
    return anteriores, nomes, listas, saida, True

def finalize(listas: list[io.TextIOWrapper], saida: io.TextIOWrapper, numListas: int) -> None:
    for i in range(numListas):
        listas[i].close()
    saida.close()

def leia_nome(lista: io.TextIOWrapper, nome_ant: str, existem_mais_nomes: bool, numListas: int) -> tuple[str, str, bool]:
    global numEOF
    nome = lista.readline()
    if not nome: # se não tiver mais nomes para ler
        nome = VALOR_ALTO
        numEOF += 1
        if numEOF == numListas:
            existem_mais_nomes = False
    else:
        if nome <= nome_ant:
            raise Exception(f'Erro de sequência {lista.name} -> {nome}')
    return nome, nome, existem_mais_nomes

def kwaymerge(caminho: str, numListas: int) -> None:
    try:
        anteriores, nomes, listas, saida, existem_mais_nomes = inicialize(caminho, numListas)

        for i in range(numListas):
            nomes[i], anteriores[i], existem_mais_nomes = leia_nome(listas[i], anteriores[i], existem_mais_nomes, numListas)
    
        while existem_mais_nomes:
            menor = 0
            for i in range(numListas): # encontra o indice do menor elemento em *nomes*
                if nomes[i] < nomes[menor]: 
                    menor = i

            saida.write(nomes[menor])
            # substitui nomes[menor] e anteriores[menor] pelo proximo nome que esta em *listas[menor]* que é um arquivo .txt de nomes
            nomes[menor], anteriores[menor], existem_mais_nomes = leia_nome(listas[menor], anteriores[menor], existem_mais_nomes, numListas) 
        finalize(listas, saida, numListas)
    except Exception as e:
        print(f"Erro: {e}")

def main() -> None:
    modo_de_uso = f'Modo de uso:\n $ {argv[0]} caminho_listas numListas'
    if len(argv) < 3:
        raise TypeError('Número incorreto de argumentos!', modo_de_uso)
    kwaymerge(argv[1], int(argv[2]))

if __name__ == '__main__':
    main()