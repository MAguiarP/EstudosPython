import os
import time
import random
import keyboard
from collections import deque

class CarrinhoGame:
    def __init__(self):
        self.width = 40
        self.height = 20
        self.carro_pos = self.width // 2
        self.obstaculos = deque()
        self.explosoes = []
        self.score = 0
        self.vidas = 3
        self.game_over = False
        self.speed = 0.1
        self.velocidade_carro = 0
        self.max_velocidade = 5
        self.aceleracao = 0.5
        self.frame_count = 0
        self.road_offset = 0
        self.car_sprites = ["  ____  ", 
                          " /|_||_\\`.__", 
                          "(   _    _ _\\", 
                          "=`-(_)--(_)-' "]
        self.obstaculo_sprites = ["  /\\  ", 
                                 " /  \\ ", 
                                 "/____\\", 
                                 " |||| "]
        self.explosao_sprites = ["  **  ", 
                                " **** ", 
                                " **** ", 
                                "  **  "]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_road(self):
        print("+" + "-" * self.width + "+")
        for y in range(self.height):
            # Efeito de movimento da estrada
            road_pattern = ["|"] + [" "]*self.width + ["|"]
            
            # Linhas da estrada
            for x in range(self.width):
                if (x + self.road_offset) % 8 == 0 and y % 2 == 0:
                    road_pattern[x+1] = "."
            
            # Adicionar obstáculos
            for obs_x, obs_y, _ in self.obstaculos:
                if obs_y <= y < obs_y + 4 and 0 <= obs_x < self.width:
                    for i, line in enumerate(self.obstaculo_sprites):
                        if y == obs_y + i:
                            for j, char in enumerate(line):
                                pos = obs_x + j
                                if 0 <= pos < self.width:
                                    road_pattern[pos+1] = char
            
            # Adicionar explosões
            for exp_x, exp_y, exp_frame in self.explosoes:
                if exp_y <= y < exp_y + 4 and 0 <= exp_x < self.width:
                    for i, line in enumerate(self.explosao_sprites):
                        if y == exp_y + i:
                            for j, char in enumerate(line):
                                pos = exp_x + j
                                if 0 <= pos < self.width:
                                    road_pattern[pos+1] = char
            
            # Adicionar carro
            if self.height - 4 <= y < self.height:
                car_line = y - (self.height - 4)
                if 0 <= car_line < len(self.car_sprites):
                    for j, char in enumerate(self.car_sprites[car_line]):
                        pos = self.carro_pos + j - 3
                        if 0 <= pos < self.width:
                            if road_pattern[pos+1] not in [' ', '.']:
                                # Colisão detectada
                                if not any(obs for obs in self.obstaculos if obs[0] <= pos < obs[0]+6 and obs[1] <= y < obs[1]+4):
                                    self.explosoes.append((pos, y, 0))
                            road_pattern[pos+1] = char
            
            print("".join(road_pattern))
        print("+" + "-" * self.width + "+")

    def draw(self):
        self.clear_screen()
        print(f"Score: {self.score} | Vidas: {'♥' * self.vidas}")
        print(f"Velocidade: {'▮' * int(self.velocidade_carro)}")
        self.draw_road()
        print("Controles: ← → para acelerar, ↑ ↓ para manter velocidade, ESC para sair")

    def update(self):
        self.frame_count += 1
        self.road_offset = (self.road_offset + 1) % 8
        
        # Atualizar física do carro
        if keyboard.is_pressed('right'):
            self.velocidade_carro = min(self.velocidade_carro + self.aceleracao, self.max_velocidade)
        elif keyboard.is_pressed('left'):
            self.velocidade_carro = max(self.velocidade_carro - self.aceleracao, -self.max_velocidade)
        else:
            # Fricção natural
            if self.velocidade_carro > 0:
                self.velocidade_carro = max(0, self.velocidade_carro - 0.2)
            elif self.velocidade_carro < 0:
                self.velocidade_carro = min(0, self.velocidade_carro + 0.2)
        
        # Mover carro
        new_pos = self.carro_pos + int(self.velocidade_carro)
        self.carro_pos = max(3, min(self.width - 4, new_pos))
        
        # Mover obstáculos
        for i in range(len(self.obstaculos)):
            x, y, tipo = self.obstaculos[i]
            self.obstaculos[i] = (x, y + 2, tipo)
        
        # Remover obstáculos que saíram da tela
        while self.obstaculos and self.obstaculos[0][1] > self.height:
            self.obstaculos.popleft()
            self.score += 10
        
        # Adicionar novos obstáculos
        if random.random() < 0.1:
            x = random.randint(0, self.width - 6)
            tipo = random.choice([0, 1, 1, 1])  # 0 é um obstáculo especial
            self.obstaculos.append((x, -4, tipo))
        
        # Atualizar explosões
        self.explosoes = [(x, y, frame+1) for (x, y, frame) in self.explosoes if frame < 5]
        
        # Verificar colisões
        car_rect = (self.carro_pos - 3, self.height - 4, 6, 4)
        for obs_x, obs_y, _ in self.obstaculos:
            obs_rect = (obs_x, obs_y, 6, 4)
            if self.check_collision(car_rect, obs_rect):
                self.vidas -= 1
                self.explosoes.append((obs_x, obs_y, 0))
                # Remover o obstáculo colidido
                self.obstaculos = deque(obs for obs in self.obstaculos if obs[0] != obs_x or obs[1] != obs_y)
                if self.vidas <= 0:
                    self.game_over = True
                break
        
        # Aumentar dificuldade
        if self.score % 100 == 0:
            self.speed = max(0.05, self.speed * 0.95)

    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

    def run(self):
        try:
            while not self.game_over:
                start_time = time.time()
                
                self.update()
                self.draw()
                
                if keyboard.is_pressed('esc'):
                    self.game_over = True
                
                # Controle de FPS
                elapsed = time.time() - start_time
                time.sleep(max(0, self.speed - elapsed))
            
            self.clear_screen()
            print("╔════════════════════════╗")
            print("║       GAME OVER!       ║")
            print(f"║   Score final: {self.score:<5}   ║")
            print("╚════════════════════════╝")
            print("\nPressione qualquer tecla para sair...")
            keyboard.read_key()
            
        except KeyboardInterrupt:
            print("\nJogo encerrado pelo usuário.")

if __name__ == "__main__":
    game = CarrinhoGame()
    game.run()