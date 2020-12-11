
import random
import pygame


# Define umas cor
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
CINZA = (170, 170, 170)
MARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
ARCO_IRIS = (random.randint(1,225),random.randint(1,225),random.randint(1,225))

# constancias
QUADRADOS = 8
LADO_TELA = 80
EPILEPSIA = False
PECAS = 3


class Tabuleiro:
    def __init__(self, quadrados):
        self.quadrados = quadrados
        self.tabuleiro = []
        for j in range(self.quadrados):
            linhas = []
            for i in range(self.quadrados):
                casa  = 'vazio'
                linhas.append(casa)
            self.tabuleiro.append(linhas)
        self.posicionar()


    def posicionar(self):
        self.selecionado = []
        self.turno = random.choice(("vermelho","preto"))


        for y in range(PECAS):      #Intercalandaço
            for x in range(QUADRADOS):
                if (x+y) % 2 == 0: self.tabuleiro[y][x] = "vermelho"

        for y in range(QUADRADOS-PECAS, QUADRADOS):
            for x in range(QUADRADOS):
                if (x+y) % 2 == 0: self.tabuleiro[y][x] = "preto" #


    def capturaPossivel(self, diagonais, diagonaisParalelas, ReiLegitimo = False):

        for i in range(2):
            try:
                if diagonais[i] != 'vazio' and diagonais[i] != self.turno and \
                diagonaisParalelas[i] == 'vazio':
                    return True
            except: return False

        return False



    def pegaRato(self, mouseX, mouseY):     #(Get the mouse)


        if len(self.selecionado) == 0:  #Peça tocada, peça jogada
            if self.tabuleiro[mouseX][mouseY] == self.turno:
                 self.selecionado = [mouseX, mouseY]
                 print("Selecionou X",  mouseX, " Y",mouseY)    #Selecionar

        elif self.tabuleiro[mouseX][mouseY] == self.turno:print('Peça tocada é peça jogada')


        elif self.tabuleiro[mouseX][mouseY] == 'vazio' and  (mouseX + mouseY) % 2 == 0:

            if abs(mouseX - self.selecionado[0]) == 1: #MOVER NORMAL


                    if   mouseX == self.selecionado[0] + 1 and  mouseY != self.selecionado[1] and self.turno == "vermelho" or \
                    mouseX == self.selecionado[0] - 1 and  mouseY != self.selecionado[1] and self.turno == "preto":

                        self.tabuleiro[mouseX][mouseY] = self.turno
                        self.tabuleiro[self.selecionado[0]][self.selecionado[1]]  = 'vazio'
                        self.selecionado = []
                        self.trocaTurno(self.turno)





            elif mouseX - self.selecionado[0] == -2 and self.turno == "preto"  or \
                mouseX - self.selecionado[0] == +2 and self.turno == "vermelho" :         #CAPTURAR





                velocidade = 1 if self.turno == 'vermelho' else -1
                capy = - 1 if  mouseY > self.selecionado[1] else  + 1       #Da direita ou esquerda


                if self.tabuleiro[self.selecionado[0] + velocidade][capy + mouseY] != self.turno and    \
                 self.tabuleiro[self.selecionado[0] + velocidade][capy + mouseY] != 'vazio':

                 self.tabuleiro[self.selecionado[0]][self.selecionado[1]]  = 'vazio'
                 self.tabuleiro[mouseX][mouseY] = self.turno
                 self.tabuleiro[self.selecionado[0] + velocidade][capy + mouseY] = 'vazio'
                 self.selecionado = []
                 print(self.turno , 'capturou\n')

                try:

                    diagonais = [self.tabuleiro[velocidade + mouseX][mouseY - 1] , self.tabuleiro[mouseX + velocidade][1 + mouseY]]
                    diagonaisParalelas = [self.tabuleiro[(velocidade * 2)+ mouseX ][mouseY - 2] , self.tabuleiro[mouseX + (velocidade * 2)][2 + mouseY]]
                    if self.capturaPossivel(diagonais[0],diagonaisParalelas ):
                        print('Bela jogada amigão, você pode capturar aquela peça ali ')
                        self.trocaTurno(self.turno)


                except:
                    None

                self.trocaTurno(self.turno)



    def trocaTurno(self, turnoAtual):
        if turnoAtual == "vermelho": self.turno = "preto"
        else: self.turno = "vermelho"



    def desenhar(self, scrn):
        tamY = 0
        metade = LADO_TELA // 2
        raio = ( metade*8)//10
        raio2 =  metade//2
        raio3 =  metade//4
        for y in range(self.quadrados):
            tamX = 0
            for x in range(self.quadrados):

                if self.tabuleiro[y][x] == 'vazio':
                    if EPILEPSIA: pygame.draw.rect(scrn, (random.randint(1,225),random.randint(1,225),random.randint(1,225)) ,[tamX, tamY, LADO_TELA, LADO_TELA])
                    else:
                        if (x + y)% 2 == 0 :pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                        else :pygame.draw.rect(scrn, BRANCO, [tamX, tamY, LADO_TELA, LADO_TELA])

                elif self.tabuleiro[y][x] == "vermelho":
                    pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                    pygame.draw.circle(scrn, VERMELHO, [tamX+ metade,tamY+ metade], raio)

                elif self.tabuleiro[y][x] == "preto":
                    pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                    pygame.draw.circle(scrn, PRETO, [tamX+ metade,tamY+ metade], raio)
#
#                elif self.tabuleiro[y][x] == 'ReiVermelho':
#                    pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
#                    pygame.draw.circle(scrn, VERMELHO, [tamX+ metade,tamY+ metade], raio)
#                    pygame.draw.circle(scrn, CINZA, [tamX+ metade,tamY+ metade], raio2)
#                    pygame.draw.circle(scrn, VERMELHO, [tamX+ metade,tamY+ metade], raio3)
#
#                elif self.tabuleiro[y][x] == 'ReiPreto':
#
#                   pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
#                   pygame.draw.circle(scrn, PRETO, [tamX+ metade,tamY+ metade], raio)
#                   pygame.draw.circle(scrn, CINZA, [tamX+ metade,tamY+ metade], raio2)
#                   pygame.draw.circle(scrn, PRETO, [tamX+ metade,tamY+ metade], raio3)
                else:

                    pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                tamX += LADO_TELA
            tamY += LADO_TELA
        if len(self.selecionado) > 0:
            tamX = self.selecionado[1] *LADO_TELA
            tamY = self.selecionado[0] *LADO_TELA
            pygame.draw.circle(scrn, MARELO, [tamX +  metade, tamY +  metade], raio)



def main():
    pygame.init()


    tam = (QUADRADOS*LADO_TELA, QUADRADOS*LADO_TELA)
    tela = pygame.display.set_mode(tam)

    #width, height = tela.get_size()


    tabuleiro = Tabuleiro(QUADRADOS)
    clock = pygame.time.Clock()


    terminou = False
    while not terminou:

        pygame.display.set_caption("Turno do "+ tabuleiro.turno)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: terminou = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()

                tabuleiro.pegaRato(mpos[1]//LADO_TELA, mpos[0]//LADO_TELA)


        tela.fill(BRANCO)
        tabuleiro.desenhar(tela)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

##  É Por meio deste testamento em que eu relato a insalubridade da natureza humana
##  onde incotaveis anos de liberdade e juventude são disperdiçados atraz de linhas metaforicas
##  Peço perdão a aqueles que depositaram sua confiança em mim, pois no dia de hoje, mais uma vez
##  sucumbo perante meus pecados e promessas falsas
##
##
##  Nossa eu sou filho da puta mesmo em
##  Vai tomanocu desde as 4 da tarde fazendo isso e não to nem na metade
##  pqp se fosse o valanhdro já teria feito 3 desses
##  Ah vai toma no cu
##  Valandro pilantra
##
##
##

main()
