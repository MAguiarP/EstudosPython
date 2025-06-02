import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pyopencl as cl
import numpy as np
import time

# Configurações
WIDTH, HEIGHT = 3840, 2160  # 4K
BLOCK_SIZE = 1.0
NUM_BLOCKS = 20  # total de blocos
NUM_PARTICLES = NUM_BLOCKS ** 3

EXPLOSION_ORIGIN = np.array([NUM_BLOCKS/2, NUM_BLOCKS/2, NUM_BLOCKS/2], dtype=np.float32)
EXPLOSION_RADIUS = 15.0
EXPLOSION_POWER = 50.0

# Inicializa pygame e OpenGL
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Explosão 3D com OpenCL e OpenGL")

glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, (0, 100, 100, 1))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

gluPerspective(45, WIDTH/HEIGHT, 0.1, 100.0)
glTranslatef(-NUM_BLOCKS/2, -NUM_BLOCKS/2, -60)

# Função para carregar textura simples
def load_texture():
    texture_surface = pygame.Surface((2,2))
    texture_surface.fill((200, 200, 200))
    pygame.draw.line(texture_surface, (100, 100, 100), (0,0), (1,1))
    pygame.draw.line(texture_surface, (100, 100, 100), (0,1), (1,0))
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 2, 2, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return texid

texture_id = load_texture()

# Função para desenhar um cubo com textura
def draw_block(x, y, z, size=BLOCK_SIZE):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    # Front face
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0); glVertex3f(x - size/2, y - size/2, z + size/2)
    glTexCoord2f(1, 0); glVertex3f(x + size/2, y - size/2, z + size/2)
    glTexCoord2f(1, 1); glVertex3f(x + size/2, y + size/2, z + size/2)
    glTexCoord2f(0, 1); glVertex3f(x - size/2, y + size/2, z + size/2)

    # Back face
    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0); glVertex3f(x - size/2, y + size/2, z - size/2)
    glTexCoord2f(1, 0); glVertex3f(x + size/2, y + size/2, z - size/2)
    glTexCoord2f(1, 1); glVertex3f(x + size/2, y - size/2, z - size/2)
    glTexCoord2f(0, 1); glVertex3f(x - size/2, y - size/2, z - size/2)

    # Left face
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(x - size/2, y - size/2, z - size/2)
    glTexCoord2f(1, 0); glVertex3f(x - size/2, y - size/2, z + size/2)
    glTexCoord2f(1, 1); glVertex3f(x - size/2, y + size/2, z + size/2)
    glTexCoord2f(0, 1); glVertex3f(x - size/2, y + size/2, z - size/2)

    # Right face
    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0); glVertex3f(x + size/2, y - size/2, z + size/2)
    glTexCoord2f(1, 0); glVertex3f(x + size/2, y - size/2, z - size/2)
    glTexCoord2f(1, 1); glVertex3f(x + size/2, y + size/2, z - size/2)
    glTexCoord2f(0, 1); glVertex3f(x + size/2, y + size/2, z + size/2)

    # Top face
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(x - size/2, y + size/2, z + size/2)
    glTexCoord2f(1, 0); glVertex3f(x + size/2, y + size/2, z + size/2)
    glTexCoord2f(1, 1); glVertex3f(x + size/2, y + size/2, z - size/2)
    glTexCoord2f(0, 1); glVertex3f(x - size/2, y + size/2, z - size/2)

    # Bottom face
    glNormal3f(0, -1, 0)
    glTexCoord2f(0, 0); glVertex3f(x - size/2, y - size/2, z - size/2)
    glTexCoord2f(1, 0); glVertex3f(x + size/2, y - size/2, z - size/2)
    glTexCoord2f(1, 1); glVertex3f(x + size/2, y - size/2, z + size/2)
    glTexCoord2f(0, 1); glVertex3f(x - size/2, y - size/2, z + size/2)
    glEnd()

# Setup OpenCL
platforms = cl.get_platforms()
platform = platforms[0]  # Seleciona o primeiro (AMD)
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

# OpenCL kernel para explosão
kernel_source = """
__kernel void explode(
    __global float4* pos,
    __global float4* vel,
    const float3 explosion_center,
    const float explosion_radius,
    const float explosion_power,
    const float delta_time)
{
    int i = get_global_id(0);
    float3 p = (float3)(pos[i].x, pos[i].y, pos[i].z);
    float3 dir = p - explosion_center;
    float dist = length(dir);
    if (dist < explosion_radius && dist > 0.0f)
    {
        float effect = (explosion_radius - dist) / explosion_radius;
        float3 force = normalize(dir) * effect * explosion_power;
        vel[i].xyz += force * delta_time;
    }
    // Atualiza posição pela velocidade
    pos[i].xyz += vel[i].xyz * delta_time;
}
"""

program = cl.Program(context, kernel_source).build()

# Inicializa posições e velocidades dos blocos
positions_np = np.zeros((NUM_PARTICLES, 4), dtype=np.float32)
velocities_np = np.zeros((NUM_PARTICLES, 4), dtype=np.float32)

index = 0
for x in range(NUM_BLOCKS):
    for y in range(NUM_BLOCKS):
        for z in range(NUM_BLOCKS):
            positions_np[index] = (x * BLOCK_SIZE, y * BLOCK_SIZE, z * BLOCK_SIZE, 0)
            velocities_np[index] = (0, 0, 0, 0)
            index += 1

mf = cl.mem_flags
pos_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=positions_np)
vel_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=velocities_np)

clock = pygame.time.Clock()

start_time = time.time()
simulation_time = 30.0  # segundos de simulação

running = True
while running:
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza kernel
    program.explode(queue, (NUM_PARTICLES,), None,
                   pos_buf, vel_buf,
                   cl.array.vec.make_float3(*EXPLOSION_ORIGIN),
                   np.float32(EXPLOSION_RADIUS),
                   np.float32(EXPLOSION_POWER),
                   np.float32(delta_time))
    queue.finish()

    # Lê dados da GPU para CPU para renderização
    cl.enqueue_copy(queue, positions_np, pos_buf)

    # Renderiza
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(20, 1, 0, 0)
    glRotatef(pygame.time.get_ticks() * 0.02, 0, 1, 0)

    for i in range(NUM_PARTICLES):
        pos = positions_np[i]
        draw_block(pos[0], pos[1], pos[2])

    glPopMatrix()
    pygame.display.flip()

    # Para simulação após 30 segundos
    if time.time() - start_time > simulation_time:
        running = False

pygame.quit()
