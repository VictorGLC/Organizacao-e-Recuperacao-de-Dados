import sys

def cria_nomes_arq(args) -> tuple[str, str]:
    nome_atual = args[1]
    nome_novo = nome_atual.rstrip('.txt')
    opcao = args[2]

    if opcao == '-wl':
        nome_novo += '_linux.txt'
    elif opcao == '-lw':
        nome_novo += '_windows.txt'
    return nome_atual, nome_novo

def main(nargs, args) -> None:
    if nargs != 3:
        raise Exception(f'Número incorreto de argumentos. Modo de uso:\n$ {args[0]} nome_arq -wl|-lw')
    if args[2] != '-wl' and args[2] != '-lw':
        raise Exception(f'O argumento {args[2]} é inválido. Modo de uso:\n$ {args[0]} nome_arq -wl|-lw')
    
    nome_atual, nome_novo = cria_nomes_arq(args)
    try:
        arq_atual = open(nome_atual, 'rb')
        arq_novo = open(nome_novo, 'wb')
        c = arq_atual.read(1)

        # windows p/ linux
        if args[2] == '-wl':
            while c:
                if int.from_bytes(c) != 13: # verifica se é != \r
                    arq_novo.write(c)
                c = arq_atual.read(1)

        # linux p/ windows
        else:
            while c:
                if int.from_bytes(c) == 10: # verifica se é \n
                    arq_novo.write((13).to_bytes(1)) # escreve \r
                arq_novo.write(c)
                c = arq_atual.read(1)

        arq_atual.close()
        arq_novo.close()
    except OSError as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)