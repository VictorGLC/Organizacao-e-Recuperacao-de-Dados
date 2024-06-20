
# Programa 1

## Implemente o pseudocódigo `escreve_campos`

- O programa `escreve_campos` lê dados de pessoas repetidamente até que se digite um sobrenome “vazio”
  - Sobrenome, Nome, Endereço, Cidade, Estado e CEP

- Os dados de cada pessoa devem ser gravados em um arquivo texto como uma sequência de campos de tamanho variável delimitados por `|`

Exemplo de saída:

```
Silva|Alan|RuaTiete 123|Maringa|PR|87100|
Flores|Andre|Rua Braga 34|Sarandi|PR|87111|
...
```


## Pseudocódigo `escreve_campos`

```
PROGRAMA: escreve_campos
  receba o nome do arquivo a ser criado na string NOME_ARQ
  abra o arquivo NOME_ARQ para escrita com o nome lógico SAIDA
  receba o sobrenome na string SOBRENOME
  enquanto SOBRENOME for diferente de string vazia faça
    receba nome, endereço, cidade, estado e cep nas strings NOME, ENDERECO, CIDADE, ESTADO e CEP, respectivamente
    escreva a string SOBRENOME no arquivo SAIDA
    escreva a string ‘|’ no arquivo SAIDA
    escreva a string NOME no arquivo SAIDA
    escreva a string ‘|’ no arquivo SAIDA
    escreva a string ENDERECO no arquivo SAIDA
    escreva a string ‘|’ no arquivo SAIDA
    escreva a string CIDADE no arquivo SAIDA
    escreva a string ‘|’ no arquivo SAIDA
    escreva a string ESTADO no arquivo SAIDA
    escreva a string ‘|’ no arquivo SAIDA
    escreva a string CEP no arquivo SAIDA
    escreva a string ‘|’ no arquivo SAIDA
    receba o próximo sobrenome na string SOBRENOME
  feche SAIDA
fim PROGRAMA
```

# Programa 2

## Implemente o pseudocódigo `le_campos`

- O programa `le_campos` lê os dados gravados no arquivo texto criado pelo programa `escreve_campos`.
- Os campos devem ser lidos do arquivo um a um e apresentados em tela.

## Pseudocódigo `le_campos`

```
PROGRAMA: le_campos
  receba o nome do arquivo na string NOME_ARQ
  abra o arquivo NOME_ARQ para leitura com o nome lógico ENTRADA
  se o arquivo não foi aberto, termine o programa
  chame a função leia_campo(ENTRADA) e armazene o retorno em CAMPO
  enquanto CAMPO for diferente de string vazia faça
    escreva a string CAMPO na tela
    chame leia_campo(ENTRADA) e armazene o retorno em CAMPO
  feche ENTRADA
fim PROGRAMA

FUNÇÃO: leia_campo(ENTRADA)
  inicialize a string CAMPO como vazia
  leia um caractere de ENTRADA e armazene na string C
  enquanto C diferente de string vazia e C diferente de ‘|’ faça
    concatene a string C na string CAMPO
    leia um caractere de ENTRADA e armazene na string C
  retorne CAMPO
fim FUNÇÃO
```

# Programa 3

## Implemente o pseudocódigo `escreve_registros`

- Assim como o `escreve_campos`, o `escreve_registros` lê dados de pessoas repetidamente até que se digite um sobrenome “vazio”.
- Para cada pessoa lida, os dados são gravados em um arquivo binário como um registro de tamanho variável com indicação de tamanho no início do registro e campos delimitados por `|`.

## Pseudocódigo `escreve_registros`

```
PROGRAMA: escreve_registros
  receba o nome do arquivo na string NOME_ARQ
  abra o arquivo NOME_ARQ para escrita binária com o nome lógico SAIDA
  receba o sobrenome na string CAMPO
  enquanto CAMPO for diferente de string vazia faça
    inicialize a string BUFFER como vazia
    concatene as strings CAMPO e ‘|’ em BUFFER
    para cada campo faça
      receba o campo na string CAMPO
      concatene as strings CAMPO e ‘|’ em BUFFER
    converta a string BUFFER para o tipo binário
    # utilize a função encode() da classe str
    armazene o comprimento string BUFFER no inteiro TAM
    converta TAM para um binário de 2 bytes
    # utilize a função to_bytes(2) da classe int
    escreva a variável TAM no arquivo SAIDA
    escreva a variável BUFFER no arquivo SAIDA
    receba o próximo sobrenome na string CAMPO
  feche SAIDA
fim PROGRAMA
```

# Programa 4

## Implemente o pseudocódigo `le_registros`

- O programa `le_registros` lê os dados gravados no arquivo criado pelo programa `escreve_registros`.
- Os registros devem ser lidos do arquivo um a um e apresentados em tela.

## Pseudocódigo `le_registros`

```
PROGRAMA: le_registros
  receba o nome do arquivo na string NOME_ARQ
  abra NOME_ARQ para leitura binária com o nome lógico ENTRADA
  se o arquivo não foi aberto, termine o programa
  chame a função leia_reg(ENTRADA) e armazene o retorno em BUFFER
  enquanto BUFFER for diferente de string vazia faça
    converta BUFFER para uma LISTA de campos
    # utilize a função split(sep='|') da classe str
    para cada CAMPO em LISTA faça
      escreva CAMPO na tela
    chame leia_reg(ENTRADA) e armazene o retorno em BUFFER
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
