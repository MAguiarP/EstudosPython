from word2number import w2n

def traduzir_para_ingles(texto):
    traducoes = {
        'trinta': 'thirty',
        'quarenta': 'forty',
        'cinquenta': 'fifty',
        'vinte': 'twenty',
        'dez': 'ten',
        'onze': 'eleven',
        'doze': 'twelve'
        # Adicione mais traduções conforme necessário
    }
    return traducoes.get(texto, texto)

while True:  # Loop infinito
    print("\nDigite 'sair' para encerrar o programa")
    texto = input("Digite um número por extenso (ex: trinta): ").strip().lower()
    
    if texto == 'sair':
        print("Encerrando o programa...")
        break  # Sai do loop
    
    # Primeiro tenta em português
    try:
        numero = w2n.word_to_num(texto)
        print(f"Você digitou '{texto}', que corresponde a: {numero}")
    except:
        # Se falhar, tenta traduzir para inglês
        texto_en = traduzir_para_ingles(texto)
        try:
            numero = w2n.word_to_num(texto_en)
            print(f"Você digitou '{texto}', que corresponde a: {numero}")
        except:
            print(f"Não consegui reconhecer '{texto}' como número")