import pygame
import Accueil
from Notali import Notali
import Acquéreur_note
import Metronome

pygame.init()

size = width, height = 1080, 720
pygame.display.set_caption("Notali")
pygame_icon = pygame.image.load('img/icone.png')
pygame.display.set_icon(pygame_icon)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

# creation style du texte
police = pygame.font.SysFont('Comic Sans MS', 20)

notali = Notali(screen, police)
ports = Accueil.initialiser_ports_midi()
Acquéreur_note.lancer_processus(ports[0], ports[1])
Metronome.lancer([120])

action = ['accueil']
while len(action) > 0 and action[0] != 'quitter':
    if action[0] == 'accueil':
        action = Accueil.afficher(screen, width, height, police)

    if action[0] == 'Notali':
        action = notali.afficher()
        Metronome.mute()

pygame.quit()