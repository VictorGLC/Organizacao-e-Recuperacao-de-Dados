import io

def leia_reg(arq: io.TextIOWrapper) -> str:
    tam = arq.read(2)
    tam = int.from_bytes(tam)

    if tam > 0:
        buffer = arq.read(tam)

        return buffer.decode()
    else:
        return ''

def main():
    nome_arq: str = input("Digite o nome do arquivo: ")
    try:
        arq = open(nome_arq, 'rb')
    except FileNotFoundError:
        print(f"Error: não foi possivel abrir o arquivo {nome_arq}")
    else:
        buffer: str = leia_reg(arq)
        
        contaRegistro: int = 1
        while buffer:
            if buffer and buffer[-1] == '|':
                buffer = buffer[:-1]  # Remove o último '|' se ele existir
            
            contaCampo: int = 0
            campos: list[str] = buffer.split('|')
            print(f"Registro #{contaRegistro} (Tam: {len(buffer)+1})")
            for campo in campos:
                contaCampo += 1
                print(f"Campo #{contaCampo}: {campo}")

            print("\n")
            contaRegistro += 1
            buffer = leia_reg(arq)
            
        arq.close()
    
if __name__ == '__main__':
    main()