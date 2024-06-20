import io

def leia_campo(arq: io.TextIOWrapper) -> str:
    campo: str = ''
    c: str = arq.read(1)
    while c and c != '|':
        campo = campo + c
        c = arq.read(1)
    return campo    

def main():
    nome_arq: str = input("Digite o nome do arquivo:\n>>> ")
    try:
        arq = open(nome_arq, 'r')
        
    except FileNotFoundError as e:
        print(f"Error: o arquivo {nome_arq} não foi encontrado")
    else:
        contaCampo: int = 1
        campo: str = leia_campo(arq)
        
        while campo:
            print(f"Campo #{contaCampo}: {campo}")
            contaCampo += 1
            campo = leia_campo(arq)
        
        arq.close()

if __name__ == '__main__':
    main()