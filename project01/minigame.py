import pygame
import sys
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker com Power-Ups")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN]

# Jogador
paddle_width = 100
paddle_height = 20
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 40
paddle_speed = 8
original_paddle_width = paddle_width

# Bola
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5 * random.choice([-1, 1])
ball_dy = -5
original_ball_speed = 5

# Power-ups
powerups = []
powerup_types = [
    {"color": GREEN, "type": "big_paddle", "duration": 500},
    {"color": RED, "type": "small_paddle", "duration": 500},
    {"color": BLUE, "type": "slow_ball", "duration": 500},
    {"color": YELLOW, "type": "fast_ball", "duration": 500}
]
active_powerups = []
powerup_size = 20
powerup_speed = 3

# Tijolos
brick_width = 75
brick_height = 30
bricks = []
bricks_broken = 0
brick_health = 10

for row in range(5):
    for col in range(WIDTH // brick_width):
        bricks.append({
            'x': col * brick_width,
            'y': row * brick_height + 50,
            'width': brick_width,
            'height': brick_height,
            'color': random.choice(COLORS),
            'health': brick_health,  # Vida do tijolo
            'crack_stage': 0,  # Estágio de rachadura (0-9)
            'visible': True
        })

# Pontuação e texto
score = 0
font = pygame.font.Font(None, 36)

def spawn_powerup(x, y):
    if random.random() < 0.3:  # 30% de chance de dropar power-up
        powerup = random.choice(powerup_types)
        powerups.append({
            'x': x,
            'y': y,
            'width': powerup_size,
            'height': powerup_size,
            'color': powerup['color'],
            'type': powerup['type'],
            'duration': powerup['duration']
        })

def apply_powerup(powerup):
    global paddle_width, ball_dx, ball_dy

    if powerup['type'] == "big_paddle":
        paddle_width = 150
    elif powerup['type'] == "small_paddle":
        paddle_width = 50
    elif powerup['type'] == "slow_ball":
        # Prevent ball_dx or ball_dy from becoming zero
        ball_dx = ball_dx * 0.5 if abs(ball_dx * 0.5) >= 1 else (1 if ball_dx > 0 else -1)
        ball_dy = ball_dy * 0.5 if abs(ball_dy * 0.5) >= 1 else (1 if ball_dy > 0 else -1)
    elif powerup['type'] == "fast_ball":
        ball_dx = ball_dx * 1.5 if abs(ball_dx * 1.5) <= 20 else (20 if ball_dx > 0 else -20)
        ball_dy = ball_dy * 1.5 if abs(ball_dy * 1.5) <= 20 else (20 if ball_dy > 0 else -20)

    active_powerups.append(powerup.copy())
def reset_powerups():
    global paddle_width, ball_dx, ball_dy
    paddle_width = original_paddle_width
    # Avoid zero division or zero speed
    ball_dx = original_ball_speed * (1 if ball_dx > 0 else -1)
    ball_dy = original_ball_speed * (1 if ball_dy > 0 else -1)
    ball_dy = original_ball_speed * (1 if ball_dy > 0 else -1)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Controles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed
    
    # Movimento da bola
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Colisão com as paredes
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_dx *= -1
    if ball_y <= ball_radius:
        ball_dy *= -1
    
    # Colisão com a plataforma
    if (paddle_x < ball_x < paddle_x + paddle_width and
        paddle_y < ball_y + ball_radius < paddle_y + paddle_height):
        ball_dy *= -1
        # Efeito de rebatimento diferente conforme a posição
        relative_intersect = (ball_x - (paddle_x + paddle_width/2)) / (paddle_width/2)
        ball_dx = relative_intersect * 7
    
    # Colisão com tijolos
    for brick in bricks:
        if brick['visible']:
            if (brick['x'] < ball_x < brick['x'] + brick['width'] and
                brick['y'] < ball_y < brick['y'] + brick['height']):
                
                brick['health'] -= 1
                brick['crack_stage'] = 9 - brick['health']  # Atualiza estágio da rachadura
                
                if brick['health'] <= 0:
                    brick['visible'] = False
                    bricks_broken += 1
                    if bricks_broken % 10 == 0:
                        spawn_powerup(brick['x'] + brick['width']//2, brick['y'] + brick['height']//2)
                
                ball_dy *= -1
                score += 1  # Pontua menor por acerto
                break
    
    # Movimento e coleta de power-ups
    for powerup in powerups[:]:
        powerup['y'] += powerup_speed
        
        # Colisão com a plataforma
        if (paddle_x < powerup['x'] < paddle_x + paddle_width and
            paddle_y < powerup['y'] + powerup['height'] < paddle_y + paddle_height):
            apply_powerup(powerup)
            powerups.remove(powerup)
        # Saiu da tela
        elif powerup['y'] > HEIGHT:
            powerups.remove(powerup)
    
    # Atualizar power-ups ativos
    for powerup in active_powerups[:]:
        powerup['duration'] -= 1
        if powerup['duration'] <= 0:
            active_powerups.remove(powerup)
            reset_powerups()
    
    # Verifica se a bola caiu
    if ball_y > HEIGHT:
        # Reinicia a bola
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = original_ball_speed * random.choice([-1, 1])
        ball_dy = -original_ball_speed
        score = max(0, score - 5)
        reset_powerups()
    
    # Verifica vitória
    if all(not brick['visible'] for brick in bricks):
        text = font.render("PARABÉNS! VOCÊ VENCEU!", True, WHITE)
        screen.blit(text, (WIDTH//2 - 180, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    
    # Desenha tudo
    screen.fill(BLACK)
    
    # Desenha tijolos
    for brick in bricks:
        if brick['visible']:
            # Desenha o tijolo
            pygame.draw.rect(screen, brick['color'], 
                            (brick['x'], brick['y'], brick['width'], brick['height']))
            
            # Desenha contorno preto
            pygame.draw.rect(screen, BLACK, 
                            (brick['x'], brick['y'], brick['width'], brick['height']), 2)
            
            # Desenha rachaduras conforme o dano
            if brick['crack_stage'] > 0:
                crack_color = (max(0, 255 - brick['crack_stage']*25), 
                              max(0, 255 - brick['crack_stage']*25), 
                              max(0, 255 - brick['crack_stage']*25))
                
                # Linhas de rachadura
                for i in range(brick['crack_stage']):
                    start_pos = (brick['x'] + random.randint(5, brick['width']-5), 
                                brick['y'] + random.randint(5, brick['height']-5))
                    end_pos = (start_pos[0] + random.randint(-10, 10), 
                              start_pos[1] + random.randint(-10, 10))
                    pygame.draw.line(screen, crack_color, start_pos, end_pos, 1)
    
    # Desenha plataforma
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # Desenha bola
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
    
    # Mostra pontuação e power-ups ativos
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Mostra power-ups ativos
    for i, powerup in enumerate(active_powerups):
        pygame.draw.rect(screen, powerup['color'], (10 + i*30, 50, 25, 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()