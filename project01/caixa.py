# Caixa de supermercado simples
# Preços unitários dos produtos
preco_arroz = 5.50
preco_feijao = 7.20
preco_macarrao = 4.00
preco_leite = 3.80

print("Bem-vindo ao caixa do supermercado!\n")

# Solicita a quantidade de cada produto
try:
	qtd_arroz = int(input("Quantidade de pacotes de arroz (R$ 5.50 cada): "))
	qtd_feijao = int(input("Quantidade de pacotes de feijão (R$ 7.20 cada): "))
	qtd_macarrao = int(input("Quantidade de pacotes de macarrão (R$ 4.00 cada): "))
	qtd_leite = int(input("Quantidade de caixas de leite (R$ 3.80 cada): "))
except EOFError:
	# Valores padrão para ambientes sem entrada de dados
	qtd_arroz = 1
	qtd_feijao = 1
	qtd_macarrao = 1
	qtd_leite = 1
	print("Entrada não disponível. Usando valores padrão: 1 para cada produto.")

# Calcula o total de cada produto
total_arroz = qtd_arroz * preco_arroz
total_feijao = qtd_feijao * preco_feijao
total_macarrao = qtd_macarrao * preco_macarrao
total_leite = qtd_leite * preco_leite

# Calcula o total geral
total_compra = total_arroz + total_feijao + total_macarrao + total_leite

# Exibe o resultado
print("\nResumo da compra:")
print(f"Arroz: {qtd_arroz} x R$ {preco_arroz:.2f} = R$ {total_arroz:.2f}")
print(f"Feijão: {qtd_feijao} x R$ {preco_feijao:.2f} = R$ {total_feijao:.2f}")
print(f"Macarrão: {qtd_macarrao} x R$ {preco_macarrao:.2f} = R$ {total_macarrao:.2f}")
print(f"Leite: {qtd_leite} x R$ {preco_leite:.2f} = R$ {total_leite:.2f}")
print(f"\nTotal da compra: R$ {total_compra:.2f}")

