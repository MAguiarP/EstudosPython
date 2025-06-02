try:
    # Bloco 1: código que pode gerar exceção
    x = 1 / 0
except ZeroDivisionError:
    # Bloco tratador para ZeroDivisionError
    print("Tratamento de divisão por zero")
except Exception as e:
    # Bloco tratador para outras exceções
    print(f"Outra exceção capturada: {e}")
else:
    # Bloco 2 – executado caso nenhuma exceção seja levantada
    print("Nenhuma exceção ocorreu")
finally:
    # Bloco 3 – executado independente do que ocorrer
    print("Finalizando o bloco try/except")

# Instrução fora do try/except
print("Código fora do bloco try/except")