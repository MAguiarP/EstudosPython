numero_inteiro = int(input("Digite um número inteiro: "))
numero_flutuante = float(input("Digite um número de ponto flutuante: "))
valor_booleano = input("Digite um valor booleano (True ou False): ")

valor_booleano = valor_booleano.lower()  # Converte para minúsculas para garantir que seja reconhecido como booleano
valor_booleano = valor_booleano == "true"  # Converte para tipo bool

print("\nValores convertidos:")
print(f"- Número inteiro: {numero_inteiro} (tipo: {type(numero_inteiro).__name__})")
print(f"- Número de ponto flutuante: {numero_flutuante} (tipo: {type(numero_flutuante).__name__})")
print(f"- Valor booleano: {valor_booleano} (tipo: {type(valor_booleano).__name__})")