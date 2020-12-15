

import random
import pygame
import pygame_menu


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



    def posicionar(self):           #Criação
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



    def reconhecerLegitimidade(self, pedraJogando):             #Statico, testa criação de dama

        monarca = "ReiPreto" if pedraJogando == 'preto' else "ReiVermelho"
        palacio = 0 if pedraJogando == 'preto' else (QUADRADOS - 1)

        for casa in range(QUADRADOS):
            if self.tabuleiro[palacio][casa] == pedraJogando:
                 self.tabuleiro[palacio][casa] = monarca





    def superMovimentar(self, pedraSelecionada,casaClicada): #Anda com a dama
        valido = True
        LadoDaGuerra = "Rei" + str(self.turno).capitalize()
        Direita = 1 if pedraSelecionada[1] < casaClicada[1] else -1
        Subindo  = -1 if pedraSelecionada[0] >  casaClicada[0] else 1



        diagY = pedraSelecionada[1] - casaClicada[1]
        diagX = pedraSelecionada[0] - casaClicada[0]
        if  abs(diagY) == abs(diagX):

            for i in range(abs(diagX)):

                try:

                    pec = self.tabuleiro[pedraSelecionada[0] + (Subindo * i)][pedraSelecionada[1] + (Direita * i)]
                    pecPlus = self.tabuleiro[pedraSelecionada[0] + ((Subindo * 2) * i)][pedraSelecionada[1] + ((Direita * 2)* i)]

                    if i == 0: None
                    elif pec == 'vazio':None
                    elif pecPlus == 'vazio' and not pec == self.turno : self.tabuleiro[pedraSelecionada[0] + (Subindo * i)][pedraSelecionada[1] + (Direita * i)] = 'vazio'
                    elif pecPlus == self.turno: valido = False
                    else:
                         self.tabuleiro[pedraSelecionada[0]][pedraSelecionada[1]] = LadoDaGuerra
                         valido = False


                except: None

            if valido:
                self.tabuleiro[pedraSelecionada[0]][pedraSelecionada[1]] = 'vazio'
                self.tabuleiro[casaClicada[0]][casaClicada[1]] = LadoDaGuerra
                self.selecionado = []
                self.trocaTurno(self.turno)




    def caminhar(self, mouseX, mouseY):
        if   mouseX == self.selecionado[0] + 1 and  mouseY != self.selecionado[1] and self.turno == "vermelho" or \
        mouseX == self.selecionado[0] - 1 and  mouseY != self.selecionado[1] and self.turno == "preto":

            self.tabuleiro[mouseX][mouseY] = self.turno
            self.tabuleiro[self.selecionado[0]][self.selecionado[1]]  = 'vazio'

            self.trocaTurno(self.turno)
            self.reconhecerLegitimidade(self.turno)



    def capturamento(self, mouseX, mouseY):

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
                        self.reconhecerLegitimidade(self.turno)



    def pegaRato(self, mouseX, mouseY):     #(Get the mouse)


        if len(self.selecionado) == 0 :  #Peça tocada, peça jogada

            if self.tabuleiro[mouseX][mouseY] == self.turno or self.tabuleiro[mouseX][mouseY] == "Rei" + str(self.turno).capitalize():  #Validar Seleção
                 self.selecionado = [mouseX, mouseY]
                 print("Selecionou X",  mouseX, " Y",mouseY)                                                                            #Selecionar


        elif self.tabuleiro[mouseX][mouseY] == self.turno:print('Peça tocada é peça jogada')

        elif self.tabuleiro[mouseX][mouseY] == 'vazio' and  (mouseX + mouseY) % 2 == 0:


            if self.tabuleiro[self.selecionado[0]][self.selecionado[1]] == "Rei" + str(self.turno).capitalize():    #Movimentar como dama

                self.superMovimentar(self.selecionado, [mouseX ,mouseY])


            elif abs(mouseX - self.selecionado[0]) == 1:                                                            #Movimentar como peça genérica
                self.caminhar(mouseX, mouseY)


            elif mouseX - self.selecionado[0] == -2 and self.turno == "preto"  or \
                mouseX - self.selecionado[0] == +2 and self.turno == "vermelho" :                                      #Verifica e captura

                self.capturamento(mouseX,mouseY)




    def trocaTurno(self, turnoAtual):
        if turnoAtual == "vermelho": self.turno = "preto"
        else: self.turno = "vermelho"
        self.selecionado = []



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

                elif self.tabuleiro[y][x] == 'ReiVermelho':
                    pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                    pygame.draw.circle(scrn, VERMELHO, [tamX+ metade,tamY+ metade], raio)
                    pygame.draw.circle(scrn, BRANCO, [tamX+ metade,tamY+ metade], raio2)
                    pygame.draw.circle(scrn, VERMELHO, [tamX+ metade,tamY+ metade], raio3)

                elif self.tabuleiro[y][x] == 'ReiPreto':

                   pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                   pygame.draw.circle(scrn, PRETO, [tamX+ metade,tamY+ metade], raio)
                   pygame.draw.circle(scrn, MARELO, [tamX+ metade,tamY+ metade], raio2)
                   pygame.draw.circle(scrn, PRETO, [tamX+ metade,tamY+ metade], raio3)
                else:

                    pygame.draw.rect(scrn, CINZA, [tamX, tamY, LADO_TELA, LADO_TELA])
                tamX += LADO_TELA
            tamY += LADO_TELA
        if len(self.selecionado) > 0:
            tamX = self.selecionado[1] *LADO_TELA
            tamY = self.selecionado[0] *LADO_TELA
            pygame.draw.circle(scrn, MARELO, [tamX +  metade, tamY +  metade], raio)
            if self.tabuleiro[self.selecionado[0]][self.selecionado[1]][0] == 'R':
                pygame.draw.circle(scrn, BRANCO, [tamX +  metade, tamY +  metade], raio2)
                pygame.draw.circle(scrn, MARELO, [tamX +  metade, tamY +  metade], raio3)




def main():
    pygame.init()
    tabuleiro = Tabuleiro(QUADRADOS)
    clock = pygame.time.Clock()

    tam = (QUADRADOS*LADO_TELA, QUADRADOS*LADO_TELA)
    tela = pygame.display.set_mode(tam)


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
