
 
# Simulando o status do sensor (True = ligado, False = desligado)
sensor_ligado = True  # Altere para False para testar o status desligado

# Função para verificar o status do sensor
def verificar_sensor(status):
    if status:
        return "Sensor está LIGADO"
    else:
        return "Sensor está DESLIGADO"

# Verificando e exibindo o status
status_sensor = verificar_sensor(sensor_ligado)
print(status_sensor)

# Versão que pergunta ao usuário
entrada = input("O sensor está ligado? (s/n): ").lower()
sensor_ligado = entrada == 's'

print("Sensor está LIGADO" if sensor_ligado else "Sensor está DESLIGADO")