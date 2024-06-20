SIZEOF_REG = 64
SIZEOF_CAB = 4
CAMPOS = ['Sobrenome: ', 'Nome: ', 'Endereco: ', 'Cidade: ', 'Estado: ', 'CEP: ']

''' Função auxiliar que imprime o menu e le a opcao do usuario '''
def menu() -> int:
    print('\n\n\t PROGRAMA PARA INSERCAO E ALTERACAO DE REGISTROS')
    print('\n\nSuas opcoes sao:\n')
    print('\t1. Inserir um novo registro')
    print('\t2. Buscar um registro por RRN para alteracoes')
    print('\t3. Terminar o programa\n')
    opcao = int(input('Digite o numero da sua opcao: '))
    return opcao

''' Função auxiliar que le campos de registro e retorna um registro de bytes com tam_reg em bytes'''
def le_campos() -> bytes:
    
    buffer = ''
    for string in CAMPOS:
        campo = input(string)
        buffer += campo + '|'
    buffer = buffer.encode()
    buffer = buffer.ljust(SIZEOF_REG, b'\0')
    return buffer

'''  Função auxiliar que le o registro de um determinado rrn e o imprime'''
def le_reg_e_mostra(rrn, arq) -> None:
    try:
        offset = (rrn * SIZEOF_REG) + SIZEOF_CAB
        arq.seek(offset)

        buffer = (arq.read(SIZEOF_REG)).decode()
        buffer = buffer.rstrip('\0')
        
        print('Conteudo do registro: ')
        i = 0
        for campo in buffer.split('|'):
            if campo:
                print(f'\t{CAMPOS[i]} {campo}')
            i+=1
    except OSError as e:
        print(f"Erro: {e}")

''' Função auxiliar que imprime e le a opcao sobre alterar o registro'''
def modifica_reg() -> bool:
    print('Deseja modificar este registro?')
    resp = input('Responda S ou N e pressione <Enter>: ').casefold()
    if resp == 's':
        return True
    else:
        return False

def main() -> None:
    nomeArq = input('Digite o nome do arquivo a ser aberto: ')
    try:
        try:
            arq = open(nomeArq, 'r+b')
            # leia o cabeçalho e decodifique-o
            cab = arq.read(SIZEOF_CAB)
            totalReg = int.from_bytes(cab)
        except FileNotFoundError:
            arq = open(nomeArq, 'w+b')
            # inicialize o cabeçalho e grave-o
            totalReg = 0
            cab = totalReg.to_bytes(SIZEOF_CAB)
            arq.write(cab)
    
        print("Programa para insercao e alteração de registros\nSuas opcoes sao:\n")
        print("1.Inserir um novo registro\n2.Buscar um registro por RRN para alteracoes\n3.Terminar o programa")
        
        opcao = int(input("Digite o numero de suas escolha: "))

        while opcao != 3:
            if opcao == 1:
                print("Digite os dados do novo registro: ")
                reg = le_campos()
                offset = (totalReg * SIZEOF_REG) + SIZEOF_CAB
                arq.seek(offset)
                arq.write(reg)
                totalReg += 1
            
            elif opcao == 2:
                rrn = int(input("Digite o rrn a ser buscado: "))
                if rrn > totalReg:
                    print("\nRRN invalido... Voltando para o menu")
                else: 
                    le_reg_e_mostra(rrn, arq)
                    
                    if modifica_reg():
                        print('Digite os dados do novo registro:\n')
                        reg = le_campos()
                        offset = rrn * SIZEOF_REG + SIZEOF_CAB
                        arq.seek(offset)
                        arq.write(reg)
            opcao = menu()
        arq.seek(0)
        arq.write(totalReg.to_bytes(SIZEOF_CAB))
        arq.close()
    except OSError as e:
        print(f"Erro: {e}")
            
if __name__ == '__main__':
    main()