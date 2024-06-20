SIZEOF_REG = 64
SIZEOF_CAB = 4

def main() -> None:
    try:
        nome_arq = input("Digite o nome do arquivo: ")
        arq = open(nome_arq, 'rb')
    except FileNotFoundError as e:
        print(f"Erro: não foi encontrado o arquivo {nome_arq}")
    else:
        cab = arq.read(SIZEOF_CAB)
        total_reg = int.from_bytes(cab)
        
        rrn = int(input("Digite o rrn a ser lido: "))
        if rrn >= total_reg:
            raise ValueError("Valor invalido")
        
        offset = (rrn * SIZEOF_REG) + SIZEOF_CAB
        arq.seek(offset)

        buffer = arq.read(SIZEOF_REG)
        buffer = (buffer.decode()).rstrip('\0 ')

        contaCampo=1
        for campo in buffer.split('|')[0:-1]:
            print(f"Campo {contaCampo}: {campo} ")
            contaCampo+=1

        arq.close()

if __name__ == '__main__':
    main()