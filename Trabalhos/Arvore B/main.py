import sys
import struct
import io 
import os

ORDEM = 5
TAM_CAB = 4
TAM_REG = (12 * ORDEM)-4

class Pagina:
    def __init__(self) -> None:
        self.numChaves: int = 0
        self.chaves: list = [-1] * (ORDEM - 1)
        self.filhos: list = [-1] * (ORDEM)

def buscaNaArvore(chave, rrn):
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

def buscaNaPagina(chave, pag):
    pos = 0
    
    # Percorre as chaves na página até encontrar uma maior que a chave buscada ou até o final das chaves
    while pos < pag.numChaves and chave > pag.chaves[pos]:
        pos += 1
    
    # Verifica se a chave foi encontrada na posição 'pos'
    if pos < pag.numChaves and chave == pag.chaves[pos]:
        return True, pos
    else:
        return False, pos

def insereNaArvore(chave, rrnAtual):
    if rrnAtual == -1:  # Condição de parada da recursão
        chavePro = chave
        filhoDpro = -1
        return chavePro, filhoDpro, True
    else:
        # Leia a página armazenada em rrnAtual para pag
        pag = lePagina(rrnAtual)
        achou, pos = buscaNaPagina(chave, pag)

    if achou:
        raise ValueError("Chave duplicada")

    # Recursão para inserir na subárvore adequada
    chavePro, filhoDpro, promo = insereNaArvore(chave, pag.filhos[pos])
    
    if not promo:
        return -1, -1, False
    else:
        if pag.numChaves < ORDEM - 1:  # Existe espaço para inserir chavePro
            insereNaPagina(chavePro, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            return -1, -1, False
        else:
            chavePro, filhoDpro, pag, novapag = divide(chavePro, filhoDpro, pag)
            escrevePagina(rrnAtual, pag)
            escrevePagina(filhoDpro, novapag)
            return chavePro, filhoDpro, True

def insereNaPagina(chave, filhoD, pag):
    if pag.numChaves == ORDEM - 1:
        pag.filhos.append(-1)
        pag.chaves.append(-1)

    i = pag.numChaves
    
    # Move as chaves e filhos para a direita para criar espaço para a nova chave
    while i > 0 and chave < pag.chaves[i - 1]:
        pag.chaves[i] = pag.chaves[i - 1]
        pag.filhos[i + 1] = pag.filhos[i]
        i -= 1
    
    # Insere a nova chave e filhoD na posição correta
    pag.chaves[i] = chave
    pag.filhos[i + 1] = filhoD
    # Atualiza o número de chaves na página
    pag.numChaves += 1

def lePagina(rrn):
    # Calcula o byte-offset da página a partir do RRN
    byte_offset = (rrn * TAM_REG) + TAM_CAB
    # Move o ponteiro do arquivo para o byte-offset calculado
    with open('btree.dat', "rb") as arq:    
        arq.seek(byte_offset)    
        # Cria uma nova instância de Pagina
        pag = Pagina()
        # Ler o número de chaves
        pag.numChaves = struct.unpack('i', arq.read(4))[0]    
        pag.chaves = []
        for i in range(ORDEM - 1):
            chave = struct.unpack('i', arq.read(4))[0]
            pag.chaves.append(chave)
        
        pag.filhos = []
        for i in range(ORDEM):
            filho = struct.unpack('i', arq.read(4))[0]
            pag.filhos.append(filho)

        return pag


'''def escrevePagina(rrn, pag):
    with open("btree.dat", "rb+") as arq:
        byte_offset = (rrn * TAM_REG) + TAM_CAB
        arq.seek(byte_offset)
        # Escreve o número de chaves
        arq.write(struct.pack('i', pag.numChaves))
        
        # Escreve as chaves
        for chave in pag.chaves:
            arq.write(struct.pack('i', chave))
        
        # Escreve os filhos
        for filho in pag.filhos:
            arq.write(struct.pack('i', filho))

def divide(chave, filhoD, pag):
    # Insira chave e filhoD em pag usando a função insereNaPagina
    insereNaPagina(chave, filhoD, pag)
    # Calcule a posição do meio
    meio = ORDEM // 2
    # A chave promovida é a chave na posição do meio
    chavePro = pag.chaves[meio]
    # O RRN do filho direito promovido, que será o RRN da nova página
    filhoDpro = novo_rrn()
    
    # A página atual (pAtual) contém os elementos até o meio
    pAtual = Pagina()
    pAtual.chaves = pag.chaves[:meio]
    pAtual.filhos = pag.filhos[:meio + 1]
    
    # A nova página (pNova) contém os elementos a partir de meio+1
    pNova = Pagina()
    pNova.chaves = pag.chaves[meio + 1:]
    pNova.filhos = pag.filhos[meio + 1:]
    
    # Preencha as listas de chaves e filhos restantes com -1
    pAtual.chaves += [-1] * (ORDEM - 1 - len(pAtual.chaves))
    pAtual.filhos += [-1] * (ORDEM - len(pAtual.filhos))
    pNova.chaves += [-1] * (ORDEM - 1 - len(pNova.chaves))
    pNova.filhos += [-1] * (ORDEM - len(pNova.filhos))

    # Retorne a chave promovida, o RRN do filho direito, e as duas páginas
    return chavePro, filhoDpro, pAtual, pNova'''


def novo_rrn():
    with open("btree.dat", "r+b") as arq:
        arq.seek(0, os.SEEK_END)
        offset = arq.tell()
        rrn = (offset - TAM_CAB) // TAM_REG
        
    return rrn

'''def gerenciadorDeInsercao(raiz):
    chave = lerChave()
    while chave is not None:
        # Insere a chave na árvore e retorna a chave promovida, filho promovido e se houve promoção
        chavePro, filhoDpro, promoção = insereNaArvore(chave, raiz)
        if promoção:
            # Inicialize pNova como uma nova página
            pNova = Pagina()
            # Configure a nova página
            pNova.chaves[0] = chavePro     # nova chave raiz
            pNova.filhos[1] = filhoDpro    # filho direito promovido
            pNova.numChaves = 1            # incrementa o número de chaves
            # Escreva a nova página no arquivo da árvore-B
            rrn_pNova = novo_rrn()
            escrevePagina(rrn_pNova, pNova)
            # Atualize a raiz com o RRN da nova página
            raiz = rrn_pNova
            
        # Leia a próxima chave
        chave = lerChave()
    
    return raiz'''

def main():
    try:
        with open('btree.dat', "r+b") as arqArvb:
            # Leia o cabeçalho e armazene-o em raiz
            raiz_bytes = arqArvb.read(TAM_CAB)  # Assume que o cabeçalho tem TAM_CAB bytes
            raiz = struct.unpack('I', raiz_bytes)[0]  # Converte bytes para inteiro
    except:
        # O arquivo não existe, então crie um novo arquivo
        with open("btree.dat", "w+b") as arqArvb:
            # Define a raiz como 0 e escreve no cabeçalho
            raiz = 0
            arqArvb.write(struct.pack('I', raiz))  # Escreve o cabeçalho com TAM_CAB bytes            
            # Inicialize a página e escreva no arquivo
            pag = Pagina()
            pag_bytes = struct.pack('I', pag.numChaves)  # Número de chaves
            chaves_bytes = struct.pack('I' * (ORDEM - 1), *pag.chaves)  # Chaves
            filhos_bytes = struct.pack('I' * ORDEM, *pag.filhos)  # Filhos
            arqArvb.write(pag_bytes + chaves_bytes + filhos_bytes)

        # Gerencie a inserção
        raiz = gerenciadorDeInsercao(raiz)      
        # Abra o arquivo novamente para atualização
        with open("btree.dat", "r+b") as arqArvb:
            # Escreva a nova raiz no cabeçalho
            arqArvb.seek(0)
            arqArvb.write(struct.pack('I', raiz))

if __name__ == '__main__':
    main()
