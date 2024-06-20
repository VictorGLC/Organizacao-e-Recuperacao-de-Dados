def leia_reg(arq) -> str:
    try:
        tam = int.from_bytes(arq.read(2))
        if tam > 0:
            s = arq.read(tam)
            return s.decode()
        return ''
    except OSError as e:
        print(f'Erro leia_reg: {e}')


def main() -> None:
    try:
        nome_arq = input("Digite o nome do arquivo a ser aberto: ")
        arq = open(nome_arq, 'rb')
    except FileNotFoundError as e:
        print(f"Erro: não foi encontrado o arquivo {nome_arq}")
    else:
        chave = input("Insira o sobrenome a ser buscado: ")
        achou = False
        
        reg = leia_reg(arq)
        while reg and achou == False:
            sobrenome = reg.split(sep='|')[0]

            if sobrenome == chave:
                achou = True
            else:
                reg = leia_reg(arq)
        if achou:
            reg = reg.split(sep="|")
            contaCampo = 1

            for campos in reg[0:-1]:
                print(f"Campo {contaCampo}: {campos}")
                contaCampo+=1
        else:
            print("Registro não encontrado")
        
        arq.close()



if __name__ == "__main__":
    main()