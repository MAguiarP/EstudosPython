#Uso de variável como contador
# Uso de variável como contador
# Inicializando o contador
contador = 0
# Loop para incrementar o contador
for i in range(10):
    contador += 1
# Exibindo o valor final do contador
print("Valor final do contador:", contador)
# Uso de variável como acumulador
# Inicializando o acumulador
acumulador = 0
# Loop para acumular valores
for i in range(1, 11):
    acumulador += i
# Exibindo o valor final do acumulador
print("Valor final do acumulador:", acumulador)
# Uso de variável como flag
# Inicializando a flag
flag = False
# Loop para verificar uma condição
for i in range(10):
    if i == 5:
        flag = True
        break
# Exibindo o estado da flag
print("Flag está ativa:", flag)
