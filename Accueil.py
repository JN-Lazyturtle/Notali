import pygame
import mido

port_in = 'init'
port_out = 'init'


# la fonction renvoi la liste des ports ainsi que la liste des rects sur lesquels on peut cliquer
# (qui corresponds au texte des ports affichés)
def afficher_ports(screen, height):
    hauteur_in = 10
    hauteur_out = height / 2 + 10
    # creation textes
    police = pygame.font.SysFont('Comic Sans MS', 20)
    texte_ports_midi_in = police.render("ports midi IN : ", True, (0, 0, 0))
    texte_ports_midi_out = police.render("ports midi out : ", True, (0, 0, 0))
    screen.blit(texte_ports_midi_in, (10, hauteur_in - 5))
    screen.blit(texte_ports_midi_out, (10, hauteur_out - 5))
    ports_in = mido.get_input_names()
    ports_out = mido.get_output_names()
    rect_in = []
    rect_out = []

    decal = 25
    for port in ports_in:
        texte = police.render(port, True, (0, 0, 0))
        rect = texte.get_rect()
        rect.x = 10
        rect.y = hauteur_in + decal
        screen.blit(texte, rect)
        rect_in.append(rect)
        decal += 25

    decal = 25

    for port in ports_out:
        texte = police.render(port, True, (0, 0, 0))
        rect = texte.get_rect()
        rect.x = 10
        rect.y = hauteur_out + decal
        screen.blit(texte, rect)
        rect_out.append(rect)
        decal += 25

    return ports_in, rect_in, ports_out, rect_out


# on initialise les ports midi aux premiers ports in et out qu'on trouve, si on en trouve
def initialiser_ports_midi():
    ports_in = mido.get_input_names()
    ports_out = mido.get_output_names()
    if len(ports_in) != 0:
        port_in = ports_in[0]
    if len(ports_out) != 0:
        port_out = ports_out[0]

    return [port_in, port_out]


def afficher(screen, width, height, police):
    global port_in, port_out
    ports = initialiser_ports_midi()
    port_in = ports[0]
    port_out = ports[1]

    # import bouton pour lancer la partie
    play_button = pygame.image.load("img/bouton_demarrer.png")
    play_button = pygame.transform.scale(play_button, (400, 100))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = 600
    play_button_rect.y = 450
    # bouton settings
    bouton_settings = pygame.image.load("img/bouton.png")
    bouton_settings = pygame.transform.scale(bouton_settings, (250, 50))
    bouton_settings_rect = bouton_settings.get_rect()
    bouton_settings_rect.x = 675
    bouton_settings_rect.y = 600
    # volet settings
    volet_ports_midi = pygame.image.load("img/bouton.png")
    volet_ports_midi = pygame.transform.scale(volet_ports_midi, (width/2.7, height))
    volet_ports_midi_rect = volet_ports_midi.get_rect()
    volet_ports_midi_rect.x = 0
    volet_ports_midi_rect.y = 0
    # alert 0 ports in
    volet_alert = pygame.image.load("img/bouton.png")
    volet_alert = pygame.transform.scale(volet_alert, (width / 2, height/10))
    volet_alert_rect = volet_alert.get_rect()
    volet_alert_rect.x = width/3
    volet_alert_rect.y = 0


    # Ajout fond d'écran/ load : charger une image a un chemin spécifique
    background = pygame.image.load("img/fond_accueil.jpg")

    texte_ports_midi = police.render("choisir les ports midi", True, (0, 0, 0))
    texte_alert = police.render("attention vous n'avez pas de port midi-in !", True, (0, 0, 0))
    texte_alert2 = police.render("cela ne pourra pas marcher", True, (0, 0, 0))

    volet_ports_midi_ouvert = False
    running = True
    un = True
    while running:

        # screen.blit : ajouter une image à un endroit spécifique de la fenêtre (largeur, hauteur)
        screen.blit(background, (0, -20))

        if volet_ports_midi_ouvert:
            screen.blit(volet_ports_midi, volet_ports_midi_rect)

        if len(mido.get_input_names()) == 0:
            screen.blit(volet_alert, volet_alert_rect)
            volet_alert.blit(texte_alert, (75, 10))
            volet_alert.blit(texte_alert2, (130, 35))

        # Appliquer image bouton
        screen.blit(play_button, play_button_rect)
        screen.blit(bouton_settings, bouton_settings_rect)
        bouton_settings.blit(texte_ports_midi, (25, 10))

        # mettre à jour la fenêtre
        pygame.display.flip()

        # si le joueur ferme la fenêtre
        for event in pygame.event.get():
            # que l'evènement est fermeture de fenetre
            if event.type == pygame.QUIT:
                return ['quitter']


            # le joueur appuie sur jouer
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    running = False
                    return ['Notali', port_in, port_out]

                if bouton_settings_rect.collidepoint(event.pos):
                    volet_ports_midi_ouvert = not volet_ports_midi_ouvert

                # quand le volet des ports midi est activé, alors on capture les clique sur les noms des ports
                if volet_ports_midi_ouvert:
                    liste_ports = afficher_ports(volet_ports_midi, height)
                    i = 0
                    for rect_port in liste_ports[1]:
                        if rect_port.collidepoint(event.pos):
                            port_in = liste_ports[0][i]
                        i += 1

                    i = 0
                    for rect_port in liste_ports[3]:
                        if rect_port.collidepoint(event.pos):
                            port_out = liste_ports[2][i]
                        i += 1


def set_port_in(midi_in):
    global port_in
    port_in = midi_in


def set_port_out(midi_out):
    global port_out
    port_out = midi_out