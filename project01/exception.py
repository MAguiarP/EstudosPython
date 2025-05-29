while True:
    try:
        nr = int(input("Digite um número: "))
        s = nr * 3
        print(s)
        q = 12 / s
        print(q)
        break
    except ValueError:
        print("Entre com um número válido.")