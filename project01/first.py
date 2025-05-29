print("hello world")

#Como você deve ter percebido, o que a função print() recebeu entre parênteses foi uma string. Ou seja,
#poderíamos ter passado para ela uma string já definida. Veja no exemplo! 
s = "Hello World"
print(s)

#Também poderíamos ter passado como parâmetro uma variável já definida,
# A função print() vai trabalhar com o valor dessa variável.
num = 10
print(num)

#Entrada de dados com a função Input()
#Quando o programador quiser que o usuário entre com algum valor, ele deverá exibir na tela o seu pedido.
# Em C, é necessário utilizar a função printf() para escrever a solicitação ao usuário e a função scanf()
#  para receber a entrada e armazenar em uma variável. Em Python, é possível utilizar a função input().
#  Ela tanto exibe na tela o pedido, como permite que o valor informado pelo usuário seja armazenado em uma variável do seu programa
nome = input('Entre com seu Nome: ')
print(nome)
#A linha 1 fará com que a frase Entre com seu nome: seja exibida no console, mas a execução do programa fica travada até que o usuário aperte [ENTER] no teclado. 
# Tudo o que foi digitado até o [ENTER] vai ser armazenado na variável nome. A linha 2 fará a exibição do conteúdo da variável nome. 

#Perceba que a função input() trata tudo o que for digitado pelo usuário como uma string, armazenando na variável designada pelo programador para isso. 
# Mesmo que o usuário entre com apenas uma letra ou um número, isso será armazenado como uma string na variável.
num = input('Entre com um inteiro: ')
print(type(num))


#A função eval() recebe uma string, mas trata como um valor numérico.

s = '1+2'
x=type(s)
y=eval(s)
print(' x = ' , x)
print(' y = ' , y)

#Mesmo tendo recebido a string ‘1+2’ como parâmetro, a função eval() efetuou a soma de 1 com 2.
# Observe que confirmamos que s é uma string com a instrução type(s). Para tratar a entrada do usuário como um número e, com isso, realizar operações algébricas,
# por exemplo, é necessário utilizar a função eval() em conjunto com a input().

num = eval(input('Entre com um número: '))
num = num + 10
print('O número informado foi: ', num)
#A função eval() é muito útil quando o programador precisa receber uma expressão matemática do usuário e realizar o cálculo dessa expressão.
 