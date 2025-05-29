


# Passo 1: Definir a função imprimir_dados
def imprimir_dados(numero, texto):
    print("Dentro da funcao:")
    print("Número vinculado ao parametro 'numero':", numero)
    print("Texto vinculado ao parametro 'texto':", texto)

# Passo 2: Chamar a função imprimir_dados com dois argumentos
# Fornecer um número e uma string como argumentos
numero_exemplo = 42
texto_exemplo = "Python e incrivel!"
# Chamar a função imprimir_dados com os valores fornecidos
print("Fora da funcao:")
print("Número antes da chamada da funcao:", numero_exemplo)
print("Texto antes da chamada da funcao:", texto_exemplo)
imprimir_dados(numero_exemplo, texto_exemplo)
print("Fora da funcao apos a chamada:")
print("Numero apos a chamada da funcao:", numero_exemplo)
print("Texto apos a chamada da funcao:", texto_exemplo)