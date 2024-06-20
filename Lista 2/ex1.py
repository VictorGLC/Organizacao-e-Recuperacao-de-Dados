import sys

''' 
    'sys.stdin' designa a entrada padrão em python.
    Esse descritor foi utilizado para fazer a leitura da stdin
    caractere por caractere, fazendo com que a função ficasse
    mais parecida com o programa do slide 
'''
def main() -> None:
    nomeArq = input('Digite o nome do arquivo a ser criado: ')
    try:
        with open(nomeArq, 'w') as saida:
            c = sys.stdin.read(1)
            while c != '\n':
                saida.write(c)
                c = sys.stdin.read(1)
    except OSError as e:
        print(f'Erro main: {e}')


if __name__ == '__main__':
    main()