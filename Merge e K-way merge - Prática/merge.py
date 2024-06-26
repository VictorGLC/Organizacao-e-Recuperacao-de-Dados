import io
# CONSTANTES
VALOR_BAIXO = ''
VALOR_ALTO = '~'

def inicialize() -> tuple[str, str, io.TextIOWrapper, io.TextIOWrapper, io.TextIOWrapper, bool]:
    ant1 = VALOR_BAIXO
    ant2 = VALOR_BAIXO
    try:
        lista1 = open('listas/lista1.txt', 'r')
        lista2 = open('listas/lista2.txt', 'r')
        saida = open(input("Digite o nome do arquivo de saida: "), 'w')
        existem_mais_nomes = True
    except OSError as e:
        print(f"Erro: {e}")

    return ant1, ant2, lista1, lista2, saida, existem_mais_nomes

def leia_nome(lista: io.TextIOWrapper, nome_ant: str, nome_ant_outra_lista: str, existem_mais_nomes: bool) -> tuple[str, str, bool]:
    nome = lista.readline()

    if not nome:
        if nome_ant_outra_lista == VALOR_ALTO:
            existem_mais_nomes = False
        else:
            nome = VALOR_ALTO
    else:
        if nome <= nome_ant:
            raise Exception('Erro de sequência')
    nome_ant = nome
    
    return nome, nome_ant, existem_mais_nomes

def merge() -> None:
    nome1_ant, nome2_ant, lista1, lista2, saida, existem_mais_nomes = inicialize()
    nome1, nome1_ant, existem_mais_nomes = leia_nome(lista1, nome1_ant, nome2_ant, existem_mais_nomes)
    nome2, nome2_ant, existem_mais_nomes = leia_nome(lista2, nome2_ant, nome1_ant, existem_mais_nomes)

    while existem_mais_nomes:
        if nome1 < nome2:
            saida.write(nome1)
            nome1, nome1_ant, existem_mais_nomes = leia_nome(lista1, nome1_ant, nome2_ant, existem_mais_nomes)
        
        elif nome1 > nome2:
            saida.write(nome2)
            nome2, nome2_ant, existem_mais_nomes = leia_nome(lista2, nome2_ant, nome1_ant, existem_mais_nomes)
        
        else:
            saida.write(nome1)
            nome1, nome1_ant, existem_mais_nomes = leia_nome(lista1, nome1_ant, nome2_ant, existem_mais_nomes)
            nome2, nome2_ant, existem_mais_nomes = leia_nome(lista2, nome2_ant, nome1_ant, existem_mais_nomes)

    lista1.close()
    lista2.close()
    saida.close()

if __name__ == '__main__':
    merge()