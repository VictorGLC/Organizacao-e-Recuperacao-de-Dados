import io

def main():
    nome_arq: str = input("Digite o nome do arquivo: ")
    try:    
        arq = open(nome_arq, 'w+b')
        
        campo: str = input("Digite o sobrenome:\n>>> ")
        while campo:
            buffer: str = ''
            buffer += campo + '|'
            for i in range(5):
                campo = input("Digite o próximo campo:\n>>> ")
                buffer = buffer + campo + '|'
            
            buffer = buffer.encode()
            tam: int = len(buffer)
            
            tam = tam.to_bytes(2)
            arq.write(tam)
            arq.write(buffer)
            
            campo = input("Digite o sobrenome:\n>>>")
        
        arq.close()    
    except FileNotFoundError:
        print(f"Error: não foi possível abrir o arquivo {nome_arq}")
    
if __name__ == '__main__':
    main()