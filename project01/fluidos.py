import pybullet as p
import pybullet_data
import numpy as np
import matplotlib.pyplot as plt
import time

def ballistic_simulation():
    # Configuração da simulação
    p.connect(p.GUI)  # Modo visualização gráfica
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    
    # Parâmetros da simulação
    bullet_mass = 0.008  # 8g para 9mm
    bullet_radius = 0.009  # 9mm de diâmetro
    iron_thickness = 0.005  # 5mm de espessura
    impact_velocity = 360  # m/s (velocidade típica de 9mm)
    
    # Criar plano de ferro fundido
    iron_plate = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.1, 0.1, iron_thickness/2])
    iron_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.1, 0.1, iron_thickness/2], rgbaColor=[0.5, 0.5, 0.5, 1])
    iron_body = p.createMultiBody(baseMass=0, baseCollisionShape=iron_plate, baseVisualShape=iron_visual, basePosition=[0, 0, 0])
    
    # Criar projétil 9mm
    bullet_shape = p.createCollisionShape(p.GEOM_SPHERE, radius=bullet_radius)
    bullet_visual = p.createVisualShape(p.GEOM_SPHERE, radius=bullet_radius, rgbaColor=[0.8, 0.2, 0.2, 1])
    bullet_body = p.createMultiBody(baseMass=bullet_mass, baseCollisionShape=bullet_shape, 
                                   baseVisualShape=bullet_visual, basePosition=[-0.2, 0, 0])
    
    # Aplicar velocidade inicial
    p.resetBaseVelocity(bullet_body, linearVelocity=[impact_velocity, 0, 0])
    
    # Propriedades dos materiais
    p.changeDynamics(iron_body, -1, restitution=0.1, lateralFriction=0.5)
    p.changeDynamics(bullet_body, -1, restitution=0.3, lateralFriction=0.1)
    
    # Configurar câmera
    p.resetDebugVisualizerCamera(cameraDistance=0.5, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0, 0, 0])
    
    # Dados para plotagem
    time_steps = []
    bullet_positions = []
    bullet_velocities = []
    penetration_depths = []
    
    # Simulação em tempo real com visualização
    print("Iniciando simulação balística...")
    start_time = time.time()
    
    for i in range(500):
        p.stepSimulation()
        time.sleep(1./240.)  # Taxa de atualização
        
        # Coletar dados
        pos, _ = p.getBasePositionAndOrientation(bullet_body)
        vel, _ = p.getBaseVelocity(bullet_body)
        
        time_steps.append(i * (1./240.))
        bullet_positions.append(pos[0])
        bullet_velocities.append(np.linalg.norm(vel))
        
        # Verificar penetração
        if -bullet_radius < pos[0] < bullet_radius:
            penetration_depths.append(max(0, bullet_radius - abs(pos[0])))
        else:
            penetration_depths.append(0)
        
        if i % 50 == 0:
            print(f"Tempo: {time_steps[-1]:.3f}s | Posição X: {pos[0]:.4f}m | Velocidade: {np.linalg.norm(vel):.1f}m/s")
    
    print(f"Simulação concluída em {time.time()-start_time:.2f} segundos")
    
    # Visualização dos resultados
    plt.figure(figsize=(15, 8))
    
    # Posição vs Tempo
    plt.subplot(2, 2, 1)
    plt.plot(time_steps, bullet_positions, 'r-')
    plt.axvline(x=bullet_radius/impact_velocity, color='k', linestyle='--')
    plt.axhline(y=bullet_radius, color='k', linestyle='--')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição X (m)')
    plt.title('Trajetória do Projétil')
    
    # Velocidade vs Tempo
    plt.subplot(2, 2, 2)
    plt.plot(time_steps, bullet_velocities, 'b-')
    plt.axvline(x=bullet_radius/impact_velocity, color='k', linestyle='--')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Velocidade (m/s)')
    plt.title('Decaimento de Velocidade')
    
    # Profundidade de penetração
    plt.subplot(2, 2, 3)
    plt.plot(time_steps, penetration_depths, 'g-')
    plt.axvline(x=bullet_radius/impact_velocity, color='k', linestyle='--')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Penetração (m)')
    plt.title('Profundidade de Penetração')
    
    # Energia cinética
    plt.subplot(2, 2, 4)
    kinetic_energy = [0.5 * bullet_mass * v**2 for v in bullet_velocities]
    plt.plot(time_steps, kinetic_energy, 'm-')
    plt.axvline(x=bullet_radius/impact_velocity, color='k', linestyle='--')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Energia (J)')
    plt.title('Energia Cinética do Projétil')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ballistic_simulation()