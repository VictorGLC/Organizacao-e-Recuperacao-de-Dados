import io

def main():
    nome_arq: str = input("Digite o nome do arquivo:\n>>> ")

    try:
        arq = open(nome_arq, 'w')
        sobrenome: str = input("Digite o sobrenome ou <ENTER> para sair:\n>>> ")
        
        while sobrenome:
            nome: str = input("Digite o nome:\n>>> ")
            endereco: str = input("Digite o endereço:\n>>> ")
            cidade: str = input("Digite a cidade:\n>>> ")
            estado: str = input("Digite o estado:\n>>> ")
            cep: str = input("Digite o cep:\n>>> ")
            
            arq.write(sobrenome)
            arq.write('|')
            arq.write(nome)
            arq.write('|')
            arq.write(endereco)
            arq.write('|')
            arq.write(cidade)
            arq.write('|')
            arq.write(estado)
            arq.write('|')
            arq.write(cep)
            arq.write('|')
            
            sobrenome = input("Digite o sobrenome ou <ENTER> para sair:\n>>> ")
            

        arq.close()
    except FileNotFoundError:
        print(f'Erro: Não foi possível abrir o arquivo {nome_arq}')
    except:
        print(f'Erro: Não foi possível escrever no arquivo {nome_arq}')
        
if __name__ == '__main__':
    main()