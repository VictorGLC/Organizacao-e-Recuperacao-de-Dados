import sys
import struct
import io
import os

ORDEM = 5
TAM_CAB = 4
TAM_PAG = (12 * ORDEM)-4
ARQ_DADOS = 'dados/games20.dat'

class Pagina:
    def __init__(self) -> None:
        self.numChaves: int = 0
        self.chaves: list = [-1] * (ORDEM - 1)
        self.offsets: list = [-1] * (ORDEM - 1)
        self.filhos: list = [-1] * (ORDEM)

# funcoes auxiliares
def escreveRaiz(raiz: int) -> None:
    with open('btree.dat', 'r+b') as arq:
        arq.seek(0)
        arq.write(struct.pack('<i', raiz))

def retornaRaiz() -> int: 
    with open('btree.dat', 'r+b') as arq:
        arq.seek(0)
        raiz = struct.unpack('<i', arq.read(4))[0]
    return raiz

def buscaNaArvore(chave: int, rrn: int) -> tuple[bool, int, int]:
    if rrn == -1:  # Condição de parada de recursão
        return False, -1, -1
    else:
        # Leia a página armazenada no rrn para pag
        pag = lePagina(rrn)
        # Busca na página
        achou, pos = buscaNaPagina(chave, pag)
        # POS recebe a posição em que CHAVE ocorre em PAG ou deveria ocorrer se estivesse em PAG
        if achou:
            return True, rrn, pos
        else:
            # Busque na página filha
            return buscaNaArvore(chave, pag.filhos[pos])

def buscaNaPagina(chave: int, pag: Pagina) -> tuple[bool, int]:
    pos = 0

    # Percorre as chaves na página até encontrar uma maior que a chave buscada ou até o final das chaves
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos += 1
    
    # Verifica se a chave foi encontrada na posição 'pos'
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos
    else:
        return False, pos

def insereNaArvore(chave: int, byteOffset: int, rrnAtual: int) -> tuple[int, int, int, bool]:
    if rrnAtual == -1:  # Condição de parada da recursão
        chavePro = chave
        filhoDpro = -1
        return chavePro, byteOffset, filhoDpro, True
    else:
        # Leia a página armazenada em rrnAtual para pag
        pag = lePagina(rrnAtual)
        achou, pos = buscaNaPagina(chave, pag)

    if achou:
        raise ValueError("Chave duplicada")

    # Recursão para inserir na subárvore adequada
    chavePro, byteOffset, filhoDpro, promo = insereNaArvore(chave, byteOffset, pag.filhos[pos])
    if not promo:
        return -1, -1, -1, False
    else:
        if pag.numChaves < ORDEM - 1:  # Existe espaço para inserir chavePro
            insereNaPagina(chavePro, byteOffset, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            return -1, -1, -1, False
        else:
            chavePro, filhoDpro, pag, novapag, byteOffsetPro = divide(chavePro, byteOffset, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            escrevePagina(novoRrn(), novapag)
            return chavePro, byteOffsetPro, filhoDpro, True

def insereNaPagina(chave: int, byteOffset: int, filhoD: int, pag: Pagina) -> None:
    if pag.numChaves == ORDEM - 1:
        pag.filhos.append(-1)
        pag.chaves.append(-1)
        pag.offsets.append(-1)
  
    i = pag.numChaves
    # Move as chaves e filhos para a direita para criar espaço para a nova chave
    while i > 0 and chave < pag.chaves[i - 1]:
        pag.chaves[i] = pag.chaves[i - 1]
        pag.offsets[i] = pag.offsets[i - 1]
        pag.filhos[i + 1] = pag.filhos[i]
        i -= 1
    
    # Insere a nova chave e filhoD na posição correta
    pag.chaves[i] = chave
    pag.offsets[i] = byteOffset
    pag.filhos[i + 1] = filhoD
    # Atualiza o número de chaves na página
    pag.numChaves += 1
  

def lePagina(rrn: int) -> Pagina:
    # Calcula o byte-byteOffset da página a partir do RRN
    byteOffset = (rrn * TAM_PAG) + TAM_CAB
    # Move o ponteiro do arquivo para o byte-byteOffset calculado
    with open('btree.dat', "rb") as arq:    
        arq.seek(byteOffset)    
        # Cria uma nova instância de Pagina
        pag = Pagina()
        # Ler o número de chaves
        pag.numChaves = struct.unpack('<i', arq.read(4))[0]
        pag.chaves = []
        for _ in range(ORDEM - 1):
            chave = struct.unpack('<i', arq.read(4))[0]
            pag.chaves.append(chave)
        
        pag.offsets = []
        for _ in range(ORDEM - 1):
            byteOffset = struct.unpack('<i', arq.read(4))[0]
            pag.offsets.append(byteOffset)

        pag.filhos = []
        for _ in range(ORDEM):
            filho = struct.unpack('<i', arq.read(4))[0]
            pag.filhos.append(filho)

        return pag

def escrevePagina(rrn: int, pag: Pagina):
    with open("btree.dat", "r+b") as arq:
        byteOffset = (rrn * TAM_PAG) + TAM_CAB
        arq.seek(0)
        arq.seek(byteOffset)
        # Escreve o número de chaves
        arq.write(struct.pack(f'<i{ORDEM - 1}i{ORDEM-1}i{ORDEM}i', pag.numChaves, *pag.chaves, *pag.offsets, *pag.filhos))

def divide(chave: int, byteOffset: int, filhoD: int, pag: Pagina) -> tuple[int, int, Pagina, Pagina, int]:
    # Insira chave e filhoD em pag usando a função insereNaPagina
    insereNaPagina(chave, byteOffset, filhoD, pag)
    # Calcule a posição do meio
    meio = ORDEM // 2
    # A chave promovida é a chave na posição do meio
    chavePro = pag.chaves[meio]
    byteOffsetPro = pag.offsets[meio]
    # O RRN do filho direito promovido, que será o RRN da nova página
    filhoDpro = novoRrn()
    
    # A página atual (pAtual) contém os elementos até o meio
    pAtual = Pagina()
    pAtual.numChaves = meio
    pAtual.chaves = pag.chaves[:meio]
    pAtual.offsets = pag.offsets[:meio]
    pAtual.filhos = pag.filhos[:meio + 1]
    
    # A nova página (pNova) contém os elementos a partir de meio+1
    pNova = Pagina()
    pNova.numChaves = ORDEM - meio - 1
    pNova.chaves = pag.chaves[meio + 1:]
    pNova.offsets = pag.offsets[meio + 1:]
    pNova.filhos = pag.filhos[meio + 1:]
    
    # Preencha as listas de chaves, filhos e offsets de pAtual com -1
    pAtual.chaves += [-1] * (ORDEM - 1 - len(pAtual.chaves))
    pAtual.filhos += [-1] * (ORDEM - len(pAtual.filhos))
    pAtual.offsets += [-1] * (ORDEM - 1 - len(pAtual.offsets))

    # Preencha as listas de chaves, filhos e offsets de pNova com -1
    pNova.chaves += [-1] * (ORDEM - 1 - len(pNova.chaves))
    pNova.filhos += [-1] * (ORDEM - len(pNova.filhos))
    pNova.offsets += [-1] * (ORDEM - 1 - len(pNova.offsets))
    # Retorne a chave promovida, o RRN do filho direito, e as duas páginas
    return chavePro, filhoDpro, pAtual, pNova, byteOffsetPro


def novoRrn() -> int:
    with open("btree.dat", "r+b") as arq:
        arq.seek(0, os.SEEK_END)
        byteOffset = arq.tell()
        rrn = (byteOffset - TAM_CAB) // TAM_PAG
        
    return rrn

def gerenciadorDeInsercao(chave: int, offset: int) -> None:
    raiz = retornaRaiz()
    chavePro, byteOffsetPro, filhoDpro, promocao = insereNaArvore(chave, offset, raiz)

    if promocao:
        # Inicialize pNova como uma nova página
        pNova = Pagina()
        # Configure a nova página
        pNova.chaves[0] = chavePro     # nova chave raiz
        pNova.filhos[0] = raiz
        pNova.filhos[1] = filhoDpro    # filho direito promovido
        pNova.offsets[0] = byteOffsetPro
        pNova.numChaves = 1            # incrementa o número de chaves
        # Escreva a nova página no arquivo da árvore-B
        raiz = novoRrn()
        
        # Atualize a raiz com o RRN da nova página
        escrevePagina(raiz, pNova)
        escreveRaiz(raiz)
    
def criaIndice() -> None:

    iniciaIndice()
    i = 0
    chave, byteOffset = lerChave(i)
    while chave is not None:
        i+=1
        gerenciadorDeInsercao(chave, byteOffset)
        chave, byteOffset = lerChave(i)

    print('O indice btree.dat foi criado com sucesso!')

def iniciaIndice() -> None:
     with open('btree.dat', 'wb') as arq:
        raiz = 0
        arq.write(struct.pack('<i', raiz))
        pag = Pagina()
        arq.write(struct.pack('<i', pag.numChaves))
        arq.write(struct.pack(f'<{ORDEM - 1}i', *pag.chaves))
        arq.write(struct.pack(f'<{ORDEM -1}i', *pag.offsets))
        arq.write(struct.pack(f'<{ORDEM}i', *pag.filhos))

def buscaChave(chave: int, arqDados: io.BufferedIOBase) -> None:
    raiz = retornaRaiz()
    achou, rrn, pos = buscaNaArvore(chave, raiz)
    if achou:
        pag = lePagina(rrn)
        byteOffset = pag.offsets[pos]
        arqDados.seek(0)
        arqDados.seek(byteOffset)
        tamReg = struct.unpack('<h', arqDados.read(2))[0]
        reg = arqDados.read(tamReg).decode()

        print(f'Busca pelo registro de chave "{chave}"')
        print(reg + f' ({tamReg} bytes - offset {byteOffset})\n')
    else:
        print(f'Busca pelo registro de chave "{chave}"')
        print("Erro: registro não encontrado!\n")

def insereChave(registro: str, arqDados: io.BufferedIOBase) -> None:
    tamReg = len(registro)
    chave = int(registro.split("|")[0])
    raiz = retornaRaiz()
    achou, _, _ = buscaNaArvore(chave, raiz)
    if achou:
        print(f'Inserção do registro de chave "{chave}"')
        print(f'Erro: chave "{chave}" já existente\n')
    else:
        arqDados.seek(0, 2)
        byteOffset = arqDados.tell()
        arqDados.write(struct.pack('<h', tamReg))
        arqDados.write(registro.encode())

        arqDados.seek(0)
        numRegs = struct.unpack('<i', arqDados.read(TAM_CAB))[0]

        arqDados.seek(0)
        arqDados.write(struct.pack('<i', numRegs+1))

        gerenciadorDeInsercao(chave, byteOffset)
        print(f'Inserção do registro de chave "{chave}"')
        print(registro + f' ({tamReg} bytes - offset {byteOffset})\n')        

def executaOperacoes(arqDados: io.BufferedIOBase, arquivo_operacoes: io.BufferedIOBase) -> None:
    with open(arquivo_operacoes, 'r') as arq_operacoes:
        for linha in arq_operacoes:
            operacao = linha[0]
            conteudo = linha[1:].strip()
            chave = int(conteudo.split("|")[0])

            if operacao == 'i':
                insereChave(conteudo, arqDados)
            elif operacao == 'b':
                buscaChave(chave, arqDados)
            else:
                raise Exception('Operação inválida')
            arqDados.seek(0)

    print(f'As operações do arquivo "{arquivo_operacoes}" foram executadas com sucesso!')

def lerTodasPaginas(arq: io.BufferedIOBase) -> list[Pagina]:
    paginas = []
    while True:
        # Ler uma página
        pag = Pagina()
        data = arq.read(TAM_PAG)

        if len(data) < TAM_PAG:
            break

        # Ler o número de chaves
        pag.numChaves = struct.unpack('<i', data[0:4])[0]
        
        # Ler as chaves
        pag.chaves = list(struct.unpack(f'{ORDEM - 1}i', data[4:4 + (ORDEM - 1) * 4]))
        
        # Ler os byteOffsets
        pag.offsets = list(struct.unpack(f'{ORDEM - 1}i', data[4 + (ORDEM - 1) * 4: 4 + 2 * (ORDEM - 1) * 4]))
        
        # Ler os filhos
        pag.filhos = list(struct.unpack(f'{ORDEM}i', data[4 + 2 * (ORDEM - 1) * 4:]))
        
        paginas.append(pag)
    
    return paginas

def imprimeArvore() -> None:
    with open('btree.dat', 'rb') as arq:
        raiz = struct.unpack('<i', arq.read(TAM_CAB))[0]
        paginas = lerTodasPaginas(arq)
        for i in range(len(paginas)):
            if raiz == i:
                print('- - - - - - - - - - Raiz  - - - - - - - - - -')
                print(f'Pagina {i}:')
                print('numChaves:', paginas[i].numChaves)
                print(f'Chaves: {paginas[i].chaves}')
                print(f'Offsets: {paginas[i].offsets}')
                print(f'Filhos: {paginas[i].filhos}')
                print('- - - - - - - - - - - - - - - - - - - - - - -\n')
            else:
                print(f'Pagina {i}:')
                print('numChaves:', paginas[i].numChaves)
                print(f'Chaves: {paginas[i].chaves}')
                print(f'Offsets: {paginas[i].offsets}')
                print(f'Filhos: {paginas[i].filhos}\n')
        print('O índice "btree.dat" foi impresso com sucesso!')

def registrosDados() -> tuple[int, int]:
    with open(ARQ_DADOS, 'rb') as arqDados:
        pares = []
        arqDados.seek(0)
        num_registros = struct.unpack('<i', arqDados.read(TAM_CAB))[0]
        byteOffset = TAM_CAB
        for i in range(num_registros):
            tam = struct.unpack('<h', arqDados.read(2))[0]
            chave = int(arqDados.read(tam).decode().split("|")[0])
            pares.append((chave, byteOffset))
            byteOffset += tam + 2
    return pares

def lerChave(indice: int) -> tuple[int, int]:
    pares = registrosDados()

    if indice < len(pares):
        chave = pares[indice][0]
        byteOffset = pares[indice][1]
        return chave, byteOffset
    
    return None, None


def main(nargs: int, args: list[str]) -> None:
    try:
        arqDados = open(ARQ_DADOS, "r+b")
    except FileNotFoundError:
        print(f"Erro ao abrir o arquivo de dados: {ARQ_DADOS}")
    else:
        modo_uso = f"Modo de uso: $ {args[0]} -c\n$ {args[0]} -e caminho_arq_operacoes\n$ {args[0]} -p\n"

        if nargs > 1  and nargs < 4:
            flag = args[1]

            if flag == '-c':
                criaIndice()
            elif flag == '-e':
                arquivo_operacoes = args[2]
                executaOperacoes(arqDados, arquivo_operacoes)
            elif flag == '-p':
                imprimeArvore()
            else:
                raise Exception(f"Flag {flag} inválida.\n{modo_uso}")
        else:
            raise Exception(f"Número incorreto de argumentos.\n{modo_uso}")
        
        arqDados.close()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
