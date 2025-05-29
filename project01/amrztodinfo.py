#armazenamento de dados do usuário
while True:
    try:
        idade = int(input("Digite sua idade: "))
        if idade <= 0:
            raise ValueError("A idade deve ser um número positivo.")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}. Por favor, Digite Idade.")

nome = input("Digite seu nome: ")
# Exibir dados do usuário
print(f"Nome: {nome}, Idade: {idade} anos")

# Entrada de dados com tratamento de exceção
while True:
    try:
        altura = float(input("Digite sua altura em metros: "))
        if altura <= 0:
            raise ValueError("A altura deve ser um número positivo.")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}. Por favor, Digite Altura.")
        # exibir todos os dados do usuário
print(f"Nome: {nome}, Idade: {idade} anos, Altura: {altura:.2f} metros")