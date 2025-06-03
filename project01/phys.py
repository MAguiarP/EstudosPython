import pyopencl as cl
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import time
import math

# Configurações
WIDTH, HEIGHT = 1200, 900
SIM_DURATION = 20.0  # segundos
IMPACT_TIME = 5.0    # tempo até impacto (queda)
PARTICLES = 5000     # partículas totais (1 gota + respingo)

# Inicializa GLFW
if not glfw.init():
    raise Exception("Falha ao inicializar GLFW")

window = glfw.create_window(WIDTH, HEIGHT, "Simulação Gota de Chuva 3D", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar janela GLFW")

glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glPointSize(3)

# Setup OpenCL
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

# Kernel OpenCL para física
kernel_code = """
__kernel void simulate_rain(
    __global float3* positions,
    __global float3* velocities,
    __global float4* colors,
    __global float* lifetimes,
    float dt,
    int total_particles,
    int impact_occurred
) {
    int gid = get_global_id(0);
    if (gid >= total_particles) return;

    const float gravity = -9.8f;
    const float damping = 0.99f;

    if (gid == 0 && impact_occurred == 0) {
        // Gota caindo
        velocities[gid].y += gravity * dt;
        positions[gid] += velocities[gid] * dt;

        if (positions[gid].y <= 0.0f) {
            positions[gid].y = 0.0f;
            // Impacto ocorreu (flag fora do kernel)
        }
    } else if (impact_occurred == 1 && gid > 0) {
        if (lifetimes[gid] > 0.0f) {
            velocities[gid].y += gravity * dt * 0.3f;
            positions[gid] += velocities[gid] * dt;

            velocities[gid] *= damping;

            if (positions[gid].y < 0.0f) {
                positions[gid].y = 0.0f;
                velocities[gid].y = -velocities[gid].y * 0.4f;
            }

            lifetimes[gid] -= dt;

            float alpha = lifetimes[gid] * 0.5f;
            if (alpha < 0.0f) alpha = 0.0f;

            colors[gid].w = alpha;

            // Mudança sutil de cor na evaporação
            colors[gid].x = 0.2f + (1.0f - alpha) * 0.3f;
            colors[gid].z = 1.0f - (1.0f - alpha) * 0.5f;
        }
    }
}
"""

program = cl.Program(context, kernel_code).build()

# Buffers host
positions = np.zeros((PARTICLES, 3), dtype=np.float32)
velocities = np.zeros((PARTICLES, 3), dtype=np.float32)
colors = np.zeros((PARTICLES, 4), dtype=np.float32)
lifetimes = np.zeros(PARTICLES, dtype=np.float32)

# Inicializa gota principal
positions[0] = [0.0, 10.0, 0.0]
velocities[0] = [0.0, -1.0, 0.0]
colors[0] = [0.2, 0.4, 1.0, 1.0]
lifetimes[0] = SIM_DURATION

# Cria buffers OpenCL
cl_positions = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=positions)
cl_velocities = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=velocities)
cl_colors = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=colors)
cl_lifetimes = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=lifetimes)

# Função para carregar textura
def load_texture(path):
    img = Image.open(path).convert("RGBA")
    img_data = np.array(img)
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex

try:
    texture_id = load_texture("water_texture.png")  # Substitua pelo seu arquivo
except Exception:
    texture_id = None

# Variáveis para controle
impact_occurred = 0
start_time = time.time()
camera_angle = 0.0

# Função para inicializar partículas de respingo após impacto
def init_splash_particles():
    for i in range(1, PARTICLES):
        angle = 2 * math.pi * (i % 360) / 360.0
        speed = 2.0 + (i % 100) * 0.02
        dir_x = math.cos(angle)
        dir_y = abs(math.sin(angle))
        dir_z = math.sin(angle)

        positions[i] = [0.0, 0.0, 0.0]
        velocities[i] = [dir_x * speed, dir_y * speed * 2.0, dir_z * speed]
        colors[i] = [0.2, 0.4, 1.0, 1.0]
        lifetimes[i] = 2.0 + (i % 100) * 0.01

    # Atualiza buffers OpenCL
    cl.enqueue_copy(queue, cl_positions, positions)
    cl.enqueue_copy(queue, cl_velocities, velocities)
    cl.enqueue_copy(queue, cl_colors, colors)
    cl.enqueue_copy(queue, cl_lifetimes, lifetimes)
    queue.finish()

# Renderização
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Posiciona câmera em círculo
    cam_x = 15 * math.sin(camera_angle)
    cam_z = 15 * math.cos(camera_angle)
    gluLookAt(cam_x, 5.0, cam_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Desenha chão
    glColor4f(0.3, 0.3, 0.4, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-20.0, 0.0, -20.0)
    glVertex3f(-20.0, 0.0,  20.0)
    glVertex3f( 20.0, 0.0,  20.0)
    glVertex3f( 20.0, 0.0, -20.0)
    glEnd()

    # Partículas
    if texture_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
    else:
        glDisable(GL_TEXTURE_2D)

    glBegin(GL_POINTS)
    for i in range(PARTICLES):
        if lifetimes[i] > 0.0:
            glColor4fv(colors[i])
            glVertex3fv(positions[i])
    glEnd()

    if texture_id:
        glDisable(GL_TEXTURE_2D)

# Loop principal
while not glfw.window_should_close(window):
    current_time = time.time() - start_time
    dt = 0.016  # Aproximadamente 60 FPS

    if current_time >= SIM_DURATION:
        break

    # Detecta impacto e inicializa respingo
    if impact_occurred == 0 and positions[0][1] <= 0.0:
        impact_occurred = 1
        init_splash_particles()

    # Atualiza física com OpenCL
    program.simulate_rain(
        queue, (PARTICLES,), None,
        cl_positions, cl_velocities, cl_colors, cl_lifetimes,
        np.float32(dt),
        np.int32(PARTICLES),
        np.int32(impact_occurred)
    )

    # Copia dados atualizados de volta para renderização
    cl.enqueue_copy(queue, positions, cl_positions)
    cl.enqueue_copy(queue, colors, cl_colors)
    cl.enqueue_copy(queue, lifetimes, cl_lifetimes)

    camera_angle += 0.002

    render()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
