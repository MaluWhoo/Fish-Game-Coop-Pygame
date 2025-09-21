# Implementando o Cliente

import time
import pgzrun
import socket # trabalha com conexões de rede

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8080)

# fundo meno + botão play
background = Actor('teste1')  
fundo_menu = Actor('fundo2')  

# Estado do jogo
estado_jogo = 'menu'  # Variável para definir o estado do jogo

def envia(message):
    try:
        # Send data
        sent = sock.sendto(message, server_address)
    except:
        print("ERRO")

def update():
    global estado_jogo # Colocar as telas de fundo

    inicialização = b'i'
    esquerda = b'a'
    direita = b'd'

    if keyboard.a:
        envia(esquerda)
    if keyboard.d:
        envia(direita)

    ## 'i'  para iniciar funcionando
    if keyboard.i:
        envia(inicialização)
        estado_jogo = 'aguardando' ## muda esperando a confirmação 

    if keyboard.q:
        fecha()

def draw():
    screen.clear()

    # Desenha o fundo do menu ou do jogo, dependendo do estado
    if estado_jogo == 'menu':
        fundo_menu.draw()
        screen.draw.text("Jogador 2", center=(400, 100), fontsize=50, color="white")
        screen.draw.text("Pressione 'i' para iniciar", center=(400, 300), fontsize=40, color="white")
        screen.draw.text("Use 'a' e 'd' para mover", center=(400, 350), fontsize=30, color="white")
        screen.draw.text("Pressione 'q' para sair", center=(400, 400), fontsize=30, color="black")
    elif estado_jogo == 'jogando':
        background.draw()
        screen.draw.text("Pressione 'q' para sair", (10, 10), fontsize=25, color="red")

def fecha():
    global sock
    # Fechar socket
    print('Closing Socket')
    sock.close()
    sys.exist() # Fecha o promp quando Q apertado

pgzrun.go() # ultima linha