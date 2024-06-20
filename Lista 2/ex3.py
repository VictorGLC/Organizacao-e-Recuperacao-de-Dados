def remove_espaco(entrada, saida):
    cAnterior = ''
    cAtual = entrada.read(1)
    while cAtual:
        if not (cAnterior == ' ' and cAtual == ' '):
            saida.write(cAtual)
        cAnterior = cAtual
        cAtual = entrada.read(1)
        
def main():
    print("Removedor de espaços repetidos")
    nomeEntrada = input("Digite o nome do arquivo de entrada: ")
    nomeSaida = input("Digite o nome do arquivo de saida: ")
    
    try:
        entrada = open(nomeEntrada, 'r')
        saida = open(nomeSaida, 'w')
        remove_espaco(entrada, saida)
        entrada.close()
        saida.close()
    except OSError as e:
        print(f"Erro: não foi possivel abrir o arquivo: {e}")

if __name__ == '__main__':
    main()