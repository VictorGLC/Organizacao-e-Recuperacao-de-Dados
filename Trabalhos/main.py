import sys
import io
import os

SIZEOF_CAB = 4 # tamanho em bytes do cabeçalho do registro
SIZEOF_TAM_REG = 2 # tamanho em bytes que precede cada registro
SIZEOF_LED_PTR = 4 # tamanho em bytes do ponteiro da led
CARACTER_REMOCAO = '*' # caracter lógico de remoção do registro
CARACTER_SOBRA = "." # caracter para simbolizar fragmentacao interna e/ou sobra
SEPARADOR = "|" # caracter para indicar o separador entre os campos do registro
NUM_BYTES_MIN = 15 # tamanho minimo de bytes para inserção na led
NUM_CAMPOS = 6 # numero de campos padrao do registro
ARQ_DADOS = 'dados.dat' # nome do arquivo utilizado como base de dados

# le um registro e retorna uma tupla com a string do registro e seu tamanho em bytes.
def leia_reg(arq: io.TextIOWrapper) -> tuple[str, int]:
    tam = int.from_bytes(arq.read(SIZEOF_TAM_REG))

    if tam > 0:
        reg = arq.read(tam)
        if reg[0:1] == CARACTER_REMOCAO.encode():
            return '*', tam
        
        return reg.decode(), tam
    return '', None

# retorna o valor da cabeça da led armazenada no cabeçalho.
def leia_cabecalho(arq: io.TextIOWrapper) -> int:
    arq.seek(os.SEEK_SET)
    cab = int.from_bytes(arq.read(SIZEOF_CAB), signed=True)
    arq.seek(os.SEEK_SET)

    return cab

# imprime os elementos da led
def imprime_led(arq: io.TextIOWrapper) -> None:
    ponteiros = percorre_led(arq)

    str = "LED -> "
    for elem in  ponteiros:
        str += f"[offset: {elem[0]}, tam: {elem[1]}] -> "
    str += "[offset: -1]"
    print(str)
    print(f"Total: {len(ponteiros)} espaços disponiveis")

# percorre todos os elementos adicionados na led e retorna uma lista de tuplas com offset e tamanho do registro removido.
def percorre_led(arq: io.TextIOWrapper) -> list[tuple[int, int]]:
    ponteiros = []
    offset = leia_cabecalho(arq)

    while offset != -1:
        arq.seek(offset, os.SEEK_SET)

        tam = int.from_bytes(arq.read(SIZEOF_TAM_REG))
        arq.seek(1, os.SEEK_CUR)

        elem = (offset, tam)
        ponteiros.append(elem)

        offset = int.from_bytes(arq.read(SIZEOF_LED_PTR), signed=True)

    return ponteiros

# retorna o primeiro indice do offset cujo tamanho seja maior que o tamanho do registro excluido.
def indice_led(arq: io.TextIOWrapper, tam_reg_removido: int) -> tuple[int, list]:
    ponteiros = percorre_led(arq)
    for i in range(len(ponteiros)):
        if tam_reg_removido > ponteiros[i][1]:
            if i == 0:
                return i, ponteiros
            
            return i-1, ponteiros
    return -1, ponteiros

# adiciona e ordena o offset na led no formato worst-fit.
def ordena_led(arq: io.TextIOWrapper, offset: int) -> None:
    arq.seek(offset, os.SEEK_SET)
    tam_reg_removido = int.from_bytes(arq.read(SIZEOF_TAM_REG))
    indice, ponteiros = indice_led(arq, tam_reg_removido)
    maior_tam_led = ponteiros[0][1]
    antecessor_reg_removido = ponteiros[indice][0]

    if tam_reg_removido > maior_tam_led: # se o tam do registro deletado for o maior, adiciona na cabeça da led
        cab = leia_cabecalho(arq)
        arq.write(offset.to_bytes(SIZEOF_LED_PTR, signed=True))

        arq.seek(offset, os.SEEK_SET)
        arq.read(SIZEOF_TAM_REG)
        arq.write(CARACTER_REMOCAO.encode())
        arq.write(cab.to_bytes(4, signed=True))
    else:
        arq.seek(antecessor_reg_removido, os.SEEK_SET)
        arq.seek(SIZEOF_TAM_REG+len(CARACTER_REMOCAO), os.SEEK_CUR)
        antecessor_offset = int.from_bytes(arq.read(SIZEOF_LED_PTR)) # le o ponteiro do offset maior que o reg removido.

        arq.seek(antecessor_reg_removido, os.SEEK_SET)
        arq.seek(SIZEOF_TAM_REG+len(CARACTER_REMOCAO), os.SEEK_CUR)
        arq.write(offset.to_bytes(SIZEOF_LED_PTR, signed=True)) # escreve o offset do reg removido no seu antecessor de tamanho
        
        arq.seek(offset, os.SEEK_SET)
        arq.seek(SIZEOF_TAM_REG, os.SEEK_CUR)
        arq.write(CARACTER_REMOCAO.encode())
        arq.write(antecessor_offset.to_bytes(SIZEOF_LED_PTR)) # escreve no offset do reg removido o offset de seu antecessor

# remove a cabeca e aponta para o proximo maior elemento da led
def remove_cabeca_led(arq: io.TextIOWrapper) -> None:
    offset_cab = leia_cabecalho(arq)
    arq.seek(offset_cab)
    arq.seek(SIZEOF_TAM_REG+len(CARACTER_REMOCAO), os.SEEK_CUR)
    nova_cab = int.from_bytes(arq.read(SIZEOF_LED_PTR))
    arq.seek(os.SEEK_SET)
    arq.write(nova_cab.to_bytes(SIZEOF_LED_PTR))
    arq.seek(os.SEEK_SET)

# faz o tratamento da sobra, se a sobra for do tamanho minimo de bytes permitido.
def trata_sobra(arq: io.TextIOWrapper, sobra: int, offset_sobra: int) -> None:
    sobra = sobra - SIZEOF_TAM_REG
    tam_sobra_byte = sobra.to_bytes(SIZEOF_TAM_REG)
    
    arq.write(tam_sobra_byte)
    for _ in range(sobra):
        arq.write(CARACTER_SOBRA.encode())
    
    remove(arq, leia_cabecalho(arq), offset_sobra)

# faz uma inserção no offset da cabeça da led
def inserir_led(arq: io.TextIOWrapper, conteudo: str, offset_cabeca: int, tamanho_cabeca: int) -> int:
    remove_cabeca_led(arq)

    arq.seek(offset_cabeca, os.SEEK_SET)
    buffer = conteudo.encode()
    tam_reg = len(buffer).to_bytes(SIZEOF_TAM_REG)

    sobra = tamanho_cabeca - len(buffer)
    offset_sobra = offset_cabeca + SIZEOF_TAM_REG + len(buffer)
    if sobra >= NUM_BYTES_MIN:
        arq.write(tam_reg)
        arq.write(buffer)
        trata_sobra(arq, sobra, offset_sobra)
        return sobra - SIZEOF_TAM_REG
    else:
        sobra_arq = len(buffer) + sobra
        arq.write(sobra_arq.to_bytes(SIZEOF_TAM_REG))
        arq.write(buffer)
        for _ in range(sobra):
            arq.write(CARACTER_SOBRA.encode())

        return sobra

    
# faz uma inserção no final do arquivo
def inserir_fim(arq: io.TextIOWrapper, conteudo: str) -> None:
    arq.seek(os.SEEK_SET, os.SEEK_END)
    buffer = conteudo.encode()

    tam = len(buffer).to_bytes(SIZEOF_TAM_REG)
    arq.write(tam)
    arq.write(buffer)

# insere novo registro de jogo no fim do arquivo ou na cabeça da led se o espaço for o suficiente.
def insere_jogo(arq: io.TextIOWrapper, conteudo: str) -> None:
    led = percorre_led(arq)
    chave = conteudo.split(SEPARADOR)[0]
    insercao_registro = f"Inserção do registro de chave \"{chave}\" ({len(conteudo)} bytes)"

    if led and led[0][1] >= len(conteudo):
        offset_cabeca = led[0][0]
        tamanho_cabeca = led[0][1]

        sobra = inserir_led(arq, conteudo, offset_cabeca, tamanho_cabeca)
        sobra_reutilizada = f"(Sobra de {sobra} bytes)" if sobra > NUM_BYTES_MIN  else ""
        tamanho_reutilizado = f"Tamanho do espaço reutilizado: {tamanho_cabeca} bytes {sobra_reutilizada}"
        local = f"offset: {offset_cabeca} bytes (0x{offset_cabeca:04x})"

        print(f"{insercao_registro}\n{tamanho_reutilizado}\nLocal: {local}\n")
    else:
        inserir_fim(arq, conteudo)
        print(f"{insercao_registro}\nLocal: fim do arquivo.\n")

# remove o registro e o adiciona na led
def remove(arq: io.TextIOWrapper, cabeca: int, offset: int):
    if cabeca == -1: # se a led estiver vazia adiciona na cabeça da LED
        arq.write(offset.to_bytes(SIZEOF_LED_PTR, signed=True))

        arq.seek(offset, os.SEEK_SET)
        arq.seek(SIZEOF_TAM_REG, os.SEEK_CUR)
        arq.write(CARACTER_REMOCAO.encode())
        arq.write(cabeca.to_bytes(SIZEOF_LED_PTR, signed=True))
    else: # caso contrario, ordena a LED
        ordena_led(arq, offset)

# procura a chave no arquivo, se existir, faz a remoção lógica do registro
def remove_jogo(arq: io.TextIOWrapper, chave: str) -> None:
    _, tam, offset, achou = busca(arq, chave)
    cab = leia_cabecalho(arq)
    print(f"Remoção do registro de chave \"{chave}\"")

    if achou:
        remove(arq, cab, offset)
        print(f"Registro removido! ({tam} bytes)\nLocal: offset = {offset} bytes (0x{offset:04x})\n")
    else:
        print("Erro: registro não encontrado\n")

# busca o registro e o imprime
def busca_jogo(arq: io.TextIOWrapper, chave: str) -> None:
    reg, tam, offset, achou = busca(arq, chave)

    print(f"Busca pelo registro de chave \"{chave}\"")
    if achou:
        print(f"{reg} ({tam} bytes)\nLocal: offset = {offset} bytes\n")
    else:
        print("Erro: registro não encontrado!\n")

# busca o id no registro e retorna uma tupla com o reg, tamanho, offset e achou
def busca(arq: io.TextIOWrapper, chave: str) -> tuple[str, int, int, bool]:
    arq.seek(SIZEOF_CAB)
    achou = False
    offset = SIZEOF_CAB
    reg, tam = leia_reg(arq)
    while reg and not achou:
        chave_reg = reg.split(SEPARADOR)[0]
        if chave_reg == chave:
            achou = True
            campos = reg.split(SEPARADOR)
            
            if len(campos) > NUM_CAMPOS:
                reg = SEPARADOR.join(campos[:-1])
                tam = tam - len(campos[-1])
        else:
            offset = offset + SIZEOF_TAM_REG + tam  # atualiza o offset
            reg, tam = leia_reg(arq)

    return reg, tam, offset, achou

# le cada linha do arquivo de operacoes e executa a operaçao determinada
def operacoes(arq: io.TextIOWrapper, caminho_operacoes: str) -> None:
    with open(caminho_operacoes, 'r') as arq_operacoes:
        for linha in arq_operacoes:
            operacao = linha[0]
            conteudo = linha[1:].strip() # Remove espaços em branco
            chave = conteudo.split(SEPARADOR)[0] 

            if operacao == 'b':
                busca_jogo(arq, chave)
            elif operacao == 'i':
                insere_jogo(arq, conteudo) 
            elif operacao == 'r':
                remove_jogo(arq, chave)

            arq.seek(os.SEEK_SET)

# inicializa arquivo de operacoes
def inicializa_arq_operacoes(arq: io.TextIOWrapper, caminho_operacoes: str) -> None:
    try:
        operacoes(arq, caminho_operacoes)
    except FileNotFoundError:
        print(f"Erro: O arquivo de operações {caminho_operacoes} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao abrir o arquivo: {e}")

def main(nargs: int, args: list[str]) -> None:
    try:
        arq = open(ARQ_DADOS, 'r+b')
    except FileNotFoundError:
        print(f"Erro: não foi possivel encontrar o arquivo: {ARQ_DADOS}")
    else:
        modo_uso = f"Modo de uso:\n$ {args[0]} -e nome_arq\n$ {args[0]} -p"
        
        if nargs > 1 and nargs < 4:
            flag = args[1]
        
            if flag == '-e':
                caminho_operacoes = args[2]
                inicializa_arq_operacoes(arq, caminho_operacoes)
            elif flag == '-p':
                imprime_led(arq)
            else:
                raise Exception(f"Flag {flag} inválida.\n{modo_uso}")
        else:
            raise Exception(f"Número incorreto de argumentos.\n{modo_uso}")

        arq.close()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)