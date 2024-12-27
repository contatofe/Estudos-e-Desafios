import py5

particles = []
num_particles = 30
center = (py5.width//2, py5.height//2)
step = py5.random(1,15)
trail_length = 1000
cols = 3
rows = 3

def setup():
    py5.size(800,800)
    py5.background(0,0,0)
    initialize_particles()
    
    
def initialize_particles():
    #Cria partículas em posições aleatórias.
    global particles
    particles.clear()
    for _ in range(num_particles):
        x = py5.random(py5.width)
        y = py5.random(py5.height)
        particles.append(Particle(x, y))
        
def draw():
    py5.fill(0, 30)  # Desenha um fundo semi-transparente para "desbotar" os rastros
    py5.no_stroke()
    for col in range(cols):  # Loop para colunas
        for row in range(rows):  # Loop para linhas
            # Dimensões dos círculos
            circle_width = py5.width // cols
            circle_height = py5.height // rows

            # Deslocamento para centralizar
            offset_x = (py5.width - cols * circle_width) // 2
            offset_y = (py5.height - rows * circle_height) // 2

            # Coordenadas dos círculos]
            x = offset_x + col * circle_width + circle_width // 2
            y = offset_y + row * circle_height + circle_height // 2

            py5.ellipse(x, y, circle_width, circle_height)

    for particle in particles:
        particle.move()
        particle.draw()
        
def key_pressed():
    #Salva ao pressionar s e limpa ao pressionar barra de espaço
    if py5.key == 's':
        py5.save_frame('###.png')
    elif py5.key == ' ':
        particles.clear()
        initialize_particles()
        

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.history = []

    def move(self):
        #Move a partícula em direção ao centro com um pouco de aleatoriedade.
        target_x = py5.width//2
        target_y = py5.height//2

        # Direção para o centro
        dx = (target_x - self.x) * 0.01
        dy = (target_y - self.y) * 0.01

        # Adiciona movimento aleatório
        self.x += dx + py5.random(-step*2, step*2)
        self.y += dy + py5.random(-step*2, step*2)

        # Salva a posição no histórico
        self.history.append((self.x, self.y))

        # Limita o comprimento do histórico
        if len(self.history) > trail_length:
            self.history.pop(0)
            
    def draw(self):
        #Desenha a partícula e seu rastro.
        py5.no_fill()
        py5.stroke_weight(0.1)
        py5.stroke(57, 255, 20, 50)
        py5.begin_shape()
        for x, y in self.history:
            py5.vertex(x, y)
        py5.end_shape()
        
py5.run_sketch()
