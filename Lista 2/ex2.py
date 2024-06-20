def main():
    print("Contador de bytes e linhas")
    nome_arq = input("Digite o nome do arquivo a ser lido: ")
    try:
        with open(nome_arq, 'rb') as arq:
            nlinhas = 0
            nbytes = 0
            c = arq.read(1)
            while c:
                if c == 'b\n':
                    nlinhas += 1
                nbytes += 1
                c = arq.read(1)
            
            nlinhas += 1
            
            print(f"O arquivo contém {nlinhas} linhas e {nbytes} bytes.")
            
    except OSError as e:
        print(f"Erro: {e}")
        
if __name__ == '__main__':
    main()