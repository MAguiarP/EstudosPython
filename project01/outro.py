preco_arroz = 10
preco_feijao = 20
preco_macarrao = 12

quantidade_arroz = int(input("Digite a quantidade de arroz: "))
quantidade_feijao = int(input("Digite a quantidade de feijão: "))
quantidade_macarrao = int(input("Digite a quantidade de macarrão: "))

total_compra = (preco_arroz * quantidade_arroz) + (preco_feijao * quantidade_feijao) + (preco_macarrao * quantidade_macarrao)
print("O total da sua compra é: R$", total_compra)

