import pgzrun
import random # import de biblioteca
import socket # trabalha com conexões de rede
import select 

WIDTH = 800
HEIGHT = 600

# Estado Jogo
estado_jogo = 'menu' 
vida = 3
score_pink = 0 
score_green = 0
cont = 0
intervalo = 0
game_over = False

# Cria um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
# Associe (Bind) o socket a uma porta
server_address = ('<IP DO SERVIDOR>', 8080) # server conectado a um localhost
sock.bind(server_address)
print('starting up on {} port {}'.format(*server_address))


# lista de estrelas
stars = []  
imgs = ['star', 'star_bronze', 'star_silver'] 

# Peixe rosa
fishpink = Actor ('fishpink') 
fishpink.x = 750 # começar na esquerda
fishpink.y = 500

# Peixe Verde
fishgreen = Actor ('fishgreen')  
fishgreen.x = 50 # começar na direita
fishgreen.y = 500

# Inimigo 
inimigo = Actor ('piranha_down')
inimigo.x = random.randint(20,700)
inimigo.y = 0


for img in imgs:
    star = Actor(img) # adiciona o ator star
    star.x = random.randint(20,780) # fazer aparecer em lugares randoms 
    star.y = random.randint(0,200)
    stars.append(star)

# Fundos e menu + botão play
background = Actor ('teste1') 
fundo2 = Actor ('fundo2')
play_button = Actor ('play_button') 
play_button.x = 400
play_button.y = 370

# reset para quando o jogo for iniciado == correção de quando o o botão de play precionada, o jogo não parar de funcionar
def reset_jogo():
    global estado_jogo, score_green, score_pink, stars, vida, cont, intervalo, game_overm, sock

    game_over = False
    vida = 3
    score_pink = 0
    score_green = 0
    cont = 0
    intervalo = 0
    stars = []

    for img in imgs:
        star = Actor(img)
        star.x = random.randint (20, 780)
        star.y = random.randint (20, 200)
        stars.append(star)

# teste para dectar os cliques com o mouse
# def on_mouse_down(pos):
    # global estado_jogo

    # if estado_jogo == 'menu' and play_button.collidepoint(pos):
        # estado_jogo = 'jogando'
        # reset_jogo() # reseta o jogo
   # elif estado_jogo == 'game_over':
       # estado_jogo = 'menu'

# Sock 
def recebe():
    global sock # variavel global

    # Use select para esperar até 0.1 segundos por dados
    ready = select.select([sock], [], [], 0.01)

    if ready[0]:
        # Leia os dados do socket
        data, addr = sock.recvfrom(1)
        # converte bytes em string
        return data.decode("utf-8")

def update(): # loop
    global estado_jogo, score_pink, score_green, stars, vida, cont, intervalo, game_over, sock 

    comando = recebe()

    if estado_jogo == 'menu':
        if comando == 'i':
            print ('Iniciando jogo...')
            estado_jogo = 'jogando'

    # Peixe Rosa
    if estado_jogo == 'jogando':
       if keyboard.right:
          fishpink.x += 5.2
          fishpink.image = 'fishpink_right' 
       elif keyboard.left:
          fishpink.x -= 5.2
          fishpink.image = 'fishpink'
    
    if comando == 'd':
        fishgreen.x = fishgreen.x + 5.2
    if  comando == 'a':
        fishgreen.x = fishgreen.x - 5.2
    if comando == 'i': # aguardo de inicialização
        print ('O jogo está iniciando.... ')
        estado_jogo = 'jogando'
        reset_jogo()


    # Borda infinita - Pink
    if fishpink.x > WIDTH:
        fishpink.x = 0
    elif fishpink.x < 0:
        fishpink.x = WIDTH

    # Borda infinita - Green
    if fishgreen.x > WIDTH:
        fishgreen.x = 0
    elif fishgreen.x < 0:
        fishgreen.x = WIDTH

    # star se move a cada update
    for star in stars:
        star.y += 1.7 
        if star.colliderect(fishpink): # quando colisão, star volta para posição inicial
            score_pink += 1  # pontuação rosa
            star.y = 0
            star.x = random.randint (20, 780)  # toda vez que ocorre a colisão, star reaparece em uma nova posição
        if star.colliderect(fishgreen):
            score_green += 1 # pontuação verde
            star.y = 0
            star.x = random.randint (20, 780)
        if star.y > 600:
            star.y = 0
            star.x = random.randint (20,780)
            vida -= 1 # perde 1 de vida
            if vida == 0:
                estado_jogo = 'game_over' # tela de game over


    inimigo.y = inimigo.y + 3 
    if inimigo.y > 600:
        inimigo.y = 0
        inimigo.x = random.randint(20, 780) 
    if inimigo.colliderect(fishgreen): # para o verde caso o inimigo
        score_green = max (0, score_green -1) # evita o score negativado
        # fishgreen.x += 10
        inimigo.y = 0

        inimigo.x = random.randint(20, 780)
    if inimigo.colliderect(fishpink): # para o rosa caso o inimigo
        score_pink = max (0, score_pink -1)
        # fishpink.x += 10
        inimigo.y = 0
        inimigo.x = random.randint(20, 780) 
    
    # Os peixes quando se colidem andam 10 pixels (uma espécie de parede)
    if fishpink.colliderect(fishgreen):
        fishgreen.x += 10
        fishpink.x -+ 10

    if cont < len(imgs)and intervalo % 100 == 0: 
        star = Actor(imgs[cont])
        star.x = random.randint(20, 780)
        star.y = 0
        stars.append(star)
        cont +=1
        intervalo +=1
    else:
        intervalo +=1

def fecha():
    global sock
    # Fechar socket
    print('closing socket')
    sock.close()

def draw():
    screen.clear()  
    if estado_jogo == 'menu': # se tela do jogo = mostra o que tem na tela de menu
        fundo2.draw()
        play_button.draw()
        screen.draw.text('Aguardando o segundo jogando começar...', center=(400, 250), fontsize=35, color='white')
    elif estado_jogo == 'jogando': # se estiver jogando...
        background.draw()
        fishpink.draw()
        fishgreen.draw()
        inimigo.draw()
        for star in stars:
            star.draw()
        screen.draw.text('Rosa: ' + str(score_pink), (710,550), color=(255,255,255), fontsize=30)
        screen.draw.text('Verde: ' + str(score_green), (10,550), color=(255,255,255), fontsize=30)
        screen.draw.text('Vidas: ' + str(vida), (10,10), color=(255,255,255), fontsize=30)
        screen.draw.text('Maria Luiza Lima', (620,10), color=(255,255,255), fontsize=25)
        screen.draw.text('RA: 1430962421004', (620,30), color=(255,255,255), fontsize=25)
    elif estado_jogo == 'game_over': # se o jogador perder...
        screen.draw.text ('GAMER OVER!', (300, 250), color=(255,255,255), fontsize=60)
        screen.draw.text ('Rosa: ' + str(score_pink), (340, 300), color=(255,255,255), fontsize=60)
        screen.draw.text ('Verde: ' + str(score_green), (340, 350), color=(255,255,255), fontsize=60)


pgzrun.go() # deve ser a última linha