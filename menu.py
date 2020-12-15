import pygame
import pygame_menu
import os
import game
comecou = False


caminho = os.path.join(os.getcwd(), "bg.jpg")
pygame.init()
surface = pygame.display.set_mode((1000, 700))

def tamanho(value, Tamanho):
    game.QUADRADOS = int(value[0])
    if value[1] == 1: game.LADO_TELA = 60
    print


def epilepis(value, EPILEPSIA):
    if value[1] == 1 : game.EPILEPSIA = True


def boot():
    game.main()
    pygame_menu.events.EXIT


menu = pygame_menu.Menu(700, 1000, 'Damas',
                       theme=pygame_menu.themes.THEME_BLUE)


menu.add_label('Guilherme Rebllatto & Vitor kruger')
menu.add_image(caminho, scale=(0.45, 0.45), scale_smooth=True)
menu.add_button('Começar', boot)
menu.add_selector('Psicodélico ', [('Não', False), ('Sim', True)], onchange= epilepis)
menu.add_selector('Tamanho ', [('8', 8), ('12',12)], onchange= tamanho)
menu.add_button('Começar', boot)



while not comecou:
    menu.mainloop(surface)
