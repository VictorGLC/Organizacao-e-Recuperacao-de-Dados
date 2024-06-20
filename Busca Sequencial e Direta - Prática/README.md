
# Programa 1: busca_seq

## Implemente o pseudocódigo `busca_seq`

- O programa `busca_seq` faz uma busca sequencial em um arquivo de registros de tamanho variável no formato gravado pelo programa `escreve_registros`.
- O programa solicita o nome do arquivo a ser pesquisado e um sobrenome como chave primária de busca.
- Se o registro correspondente for encontrado, o mesmo deve ser apresentado em tela, caso contrário, imprime “Registro não encontrado”.

## Pseudocódigo `busca_seq`

```
PROGRAMA: busca_seq
  receba o nome do arquivo a ser aberto em NOME_ARQ
  abra NOME_ARQ para leitura binária e chame-o ENTRADA
  Se NOME_ARQ não existir, termine o programa
  receba o sobrenome a ser buscado em CHAVE
  inicialize ACHOU com falso
  chame a função leia_reg(ENTRADA) e armazene o retorno em REG
  enquanto REG for diferente de vazio e não ACHOU faça
    faça SOBRENOME receber o 1o campo de REG
    # sobrenome = reg.split(sep='|')[0]
    se SOBRENOME é igual a CHAVE então
      ACHOU recebe verdadeiro
    senão
      chame leia_reg(ENTRADA) e armazene em REG
  se ACHOU então
    # Lembre-se que reg.split(sep='|') retorna
    uma lista com os campos contidos em REG
    para cada CAMPO em REG faça
      escreva CAMPO na tela
  senão
    imprima uma mensagem de erro
  feche ENTRADA
fim PROGRAMA

FUNÇÃO: leia_reg(ENTRADA)
  leia 2 bytes do arquivo ENTRADA e armazene em TAM
  converta TAM para inteiro
  # utilize a função int.from_bytes(TAM)
  se TAM > 0 então
    leia TAM bytes do arquivo ENTRADA e armazene em BUFFER
    converta BUFFER para o tipo string
    # utilize a função decode() da classe bytes
    retorne BUFFER
  senão
    retorne ''
fim FUNÇÃO
```

# Programa 2: busca_rrn

## Implemente o pseudocódigo `busca_rrn`

- O programa `busca_rrn` faz uma busca direta em um arquivo de registros de tamanho fixo.
- Usaremos registros de 64 bytes com campos de tamanho variável e sobras preenchidas com `\0`.
- O arquivo inicia com um cabeçalho de 4 bytes que armazena o total de registros do arquivo.

## Pseudocódigo `busca_rrn`

```
PROGRAMA: busca_rrn
  receba o nome do arquivo a ser aberto em NOME_ARQ
  abra NOME_ARQ para leitura binária e chame-o ENTRADA
  Se NOME_ARQ não existir, termine o programa
  leia 4 bytes de ENTRADA e armazene de CAB
  Converta CAB para inteiro e armazene em TOTAL_REG
  # utilize o método int.from_bytes() para converter CAB
  receba o RRN do registro a ser lido
  se RRN >= TOTAL_REG então
    imprima uma mensagem de erro e termine
  calcule o OFFSET de leitura /* RRN * 64 + 4 */
  faça seek para OFFSET
  leia o registro e decodifique-o em REG
  # utilize o método decode() para decodificar REG
  # Lembre-se que reg.split(sep='|') retorna
  uma lista com os campos contidos em REG
  para cada CAMPO em REG faça
    escreva CAMPO na tela
  feche ENTRADA
fim PROGRAMA
```

# Programa 3: busca_e_atualiza

## Implemente o pseudocódigo `busca_e_atualiza`

- O programa `busca_e_atualiza` permite que:
  - Se abra um arquivo existente (ou se crie, caso não exista).
  - Se insira novos registros (sempre no final do arquivo).
  - Se busque um registro pelo seu RRN para alterações (busca e possível regravação do registro).
- O programa utiliza registros de tamanho fixo com campos de tamanho variável, preenchendo as sobras com `\0`.

## Pseudocódigo `busca_e_atualiza`

```
PROGRAMA: busca_e_atualiza
  receba o nome do arquivo em NOME_ARQ
  abra o arquivo NOME_ARQ para L/E e chame-o de ARQ # ‘r+b’
  se o arquivo NOME_ARQ não existir então
    crie e abra NOME_ARQ para L/E com o nome lógico ARQ # ‘w+b’
    faça TOTAL_REG = 0 e escreva-o em ARQ com 4 bytes
  senão
    leia o cabeçalho de ARQ e armazene-o em TOTAL_REG
  receba a escolha do usuário em OPCAO #(1)inserir (2)buscar (3)sair
  enquanto (OPCAO < 3) faça
    se OPCAO == 1:
      receba todos os campos do registro e concatene em REG
      codifique e preencha REG até 64b
      # use encode() para codificar e ljust(64, b’\0’) para preencher
      calcule o OFFSET de gravação # TOTAL_REG * 64 + 4
      faça seek para OFFSET e escreva REG em ARQ
      incremente TOTAL_REG
    senão se OPCAO == 2:
      receba o RRN
      se RRN >= TOTAL_REG então
        imprima mensagem de erro
      senão
        calcule o OFFSET de leitura # RRN * 64 + 4
        faça seek para OFFSET
        leia o registro REG e mostre-o na tela
        receba a opção sobre uma possível alteração em ALTERAR
        se ALTERAR então
          receba todos os campos do registro e concatene em REG
          codifique e preencha REG até 64b
          faça seek para OFFSET e escreva REG em ARQ
    receba a escolha do usuário em OPCAO
  faça seek para o início de ARQ
  escreva TOTAL_REG em ARQ com 4 bytes
  feche ARQ
fim PROGRAMA
```
