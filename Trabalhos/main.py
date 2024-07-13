import sys
import io
import os

SIZEOF_CAB = 4 # tamanho em bytes do cabeçalho do registro
SIZEOF_TAM_REG = 2 # tamanho em bytes que precede cada registro
SIZEOF_LED_PTR = 4 # tamanho em bytes do ponteiro da led
CARACTER_REMOCAO = '*' # caracter lógico de remoção do registro
NUM_BYTES_MIN = 15 # tamanho minimo de bytes para inserção na led

# percorre todos os elementos adicionados na led
def percorre_led(arq: io.TextIOWrapper) -> bool:
    ponteiros = []
    pont = le_cab(arq)
    while pont != -1:
        arq.seek(os.SEEK_SET)
        arq.seek(pont)

        tam = int.from_bytes(arq.read(SIZEOF_TAM_REG))
        arq.seek(os.SEEK_CUR, 1)

        elem = (pont, tam)
        ponteiros.append(elem)

        pont = int.from_bytes(arq.read(SIZEOF_LED_PTR), signed=True)

    return ponteiros

# imprime os elementos da led
def imprime_led(arq: io.TextIOWrapper):
    ponteiros = percorre_led(arq)

    str = "LED -> "
    for elem in  ponteiros:
        str += f"[offset: {elem[0]}, tam: {elem[1]}] -> "
    str += "[offset: -1]"
    print(str)
    print(f"Total: {len(ponteiros)} espaços disponiveis")

# insere novo registro de jogo no fim do arquivo
def insere_jogo(arq: io.TextIOWrapper, conteudo: str) -> None:
    arq.seek(os.SEEK_SET, os.SEEK_END)
    chave = conteudo.split("|")[0]
    buffer = conteudo.encode()

    tam = len(buffer).to_bytes(SIZEOF_TAM_REG)
    arq.write(tam)
    arq.write(buffer)

    print(f"Inserção do registro de chave \"{chave}\" ({len(conteudo)} bytes)\nLocal: fim do arquivo.\n")

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
def le_cab(arq: io.TextIOWrapper):
    arq.seek(os.SEEK_SET)
    cab = int.from_bytes(arq.read(SIZEOF_CAB), signed=True)
    arq.seek(os.SEEK_SET)

    return cab

# procura a chave no arquivo, se existir, faz a remoção lógica do registro
def remove_jogo(arq: io.TextIOWrapper, chave: str) -> None:
    reg, tam, offset, achou = busca(arq, chave)
    cab = le_cab(arq)
    print(f"Remoção do registro de chave \"{chave}\"")

    if achou:
        arq.seek(offset)
        tam_reg_remocao = int.from_bytes(arq.read(SIZEOF_TAM_REG))
        arq.write(CARACTER_REMOCAO.encode())

        arq.write(cab.to_bytes(4, signed=True))
        arq.seek(0)
        arq.write(offset.to_bytes(4, signed=True))

        print(f"Registro removido! ({tam} bytes)\nLocal: offset = {offset} bytes (0x{offset:04x})\n")
    else:
        print("Erro: registro não encontrado\n")

# busca o id no registro e retorna uma tupla com o reg, tamanho, offset e achou
def busca(arq: io.TextIOWrapper, chave: str) -> tuple[str, int, int, bool]:
    arq.seek(SIZEOF_CAB)
    achou = False
    offset = SIZEOF_CAB
    reg, tam = leia_reg(arq)
    while reg and not achou:
        chave_reg = reg.split('|')[0]

        if chave_reg == chave:
            achou = True
        else:
            offset = offset + SIZEOF_TAM_REG + tam  # atualiza o offset
            reg, tam = leia_reg(arq)

    return reg, tam, offset, achou

# busca o registro e o imprime
def busca_jogo(arq: io.TextIOWrapper, chave: str) -> None:
    reg, tam, offset, achou = busca(arq, chave)

    print(f"Busca pelo registro de chave \"{chave}\"")
    if achou:
        print(f"{reg} ({tam} bytes)\nLocal: offset = {offset} bytes\n")
    else:
        print("Erro: registro não encontrado!\n")

# le cada linha do arquivo de operacoes e executa a operaçao determinada
def operacoes(arq: io.TextIOWrapper, caminho_operacoes: str) -> None:
    with open(caminho_operacoes, 'r') as arq_operacoes:
        for linha in arq_operacoes:
            operacao = linha[0]
            conteudo = linha[1:].strip() # Remove espaços em branco
            chave = conteudo.split('|')[0] 

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
        arq = open('dados.dat', 'r+b')
    except FileNotFoundError:
        print(f"Erro: não foi possivel encontrar o arquivo: dados.dat")
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