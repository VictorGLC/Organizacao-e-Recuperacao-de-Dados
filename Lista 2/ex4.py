def remove_comentario(entrada, saida):
    aspas = False
    c = entrada.read(1)
    while c:
        # Verifica se as aspas estao abertas
        if c == '\'':
            aspas = not aspas
            
        # Verifica se c esta lendo '#'
        if c == '#':
            # Se as aspas estiver fechado, é um comentario
            if not aspas:
                # Percorre o comentario até o final da linha
                while c and c != '\n':
                    c = entrada.read(1)
                    
                # Escreve '\n' se c nao for vazio
                if c:
                    saida.write(c)
            # Se estiver aberta, é um comentario
            else:
                saida.write(c)
        # Se não for '#' escreve normalmente
        else:
            saida.write(c)
        c = entrada.read(1)
         
def main():
    print("Removedor de comentário em python")
    nome_arq = input("Digite o nome do arquivo de entrada: ")
    nome_saida = input("Digite o nome do arquivo de saida: ")
    try:
        entrada = open(nome_arq, 'r')
        saida = open(nome_saida, 'w')
    
        remove_comentario(entrada, saida)
        
        entrada.close()
        saida.close()
    except OSError as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    main()