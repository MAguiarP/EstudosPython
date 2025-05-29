print('{:4},{:5}'.format(10, 100))
#


#O padrão de alinhamento dos valores é à direita do espaço reservado para a impressão da variável.
print('{:8.5}'.format(10/3))

#Impressão de sequências
seq = [0, 1, 2, 3, 4, 5]
print(seq)


#Para imprimir uma substring, por exemplo, basta utilizar os colchetes para indicar o intervalo de índices que deve ser impresso.
#  Vale lembrar que o primeiro caractere da string é indexado como 0.
print(seq[1:4])  # Imprime os elementos de índice 1 a 3
#Impressão de tuplas
tup = (1, 2, 3, 4, 5)
print(tup)
#Para imprimir uma tupla, basta utilizar a função print diretamente.
#Impressão de dicionários
d = {'a': 1, 'b': 2, 'c': 3}
print(d)
#Para imprimir um dicionário, basta utilizar a função print diretamente.
#Impressão de conjuntos
s = {1, 2, 3, 4, 5}
print(s)
#Para imprimir um conjunto, basta utilizar a função print diretamente.
#Impressão de listas
l = [1, 2, 3, 4, 5]
print(l)
#Para imprimir uma lista, basta utilizar a função print diretamente.
#Impressão de strings
s = "Hello, World!"
print(s)
#Para imprimir uma string, basta utilizar a função print diretamente.
#Impressão de valores com formatação
#Para imprimir valores com formatação, podemos utilizar o método format() da string.
print('O valor de pi é {:.2f}'.format(3.14159))
#Impressão de valores com formatação avançada
print('O valor de pi é {0:.2f} e o valor de e é {1:.2f}'.format(3.14159, 2.71828))
#Impressão de valores com formatação avançada utilizando f-strings (Python 3.6+)
print(f'O valor de pi é {3.14159:.2f} e o valor de e é {2.71828:.2f}')
