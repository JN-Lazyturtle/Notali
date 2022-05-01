import pygame
import Acquéreur_note
import Metronome
from Gamme import Gamme
from Note import Note


class Notali:

    def __init__(self, screen, police):
        self._screen = screen
        self._police = police
        self._tab_note_on = []

    def afficher(self):
        # hauteurNoteLa0_clefFa = 592
        tab_notes_on = []
        input_actif = False

        # chargement background et note
        portee = pygame.image.load("img/fond_portee.jpg")
        note_simple = pygame.image.load("img/notesimple.png")
        barre = pygame.image.load("img/barre.png")
        diese = pygame.image.load("img/diese.png")
        bemol = pygame.image.load("img/bemol.png")
        cote = pygame.image.load("img/back_bouton.jpg")
        cote = pygame.transform.scale(cote, (300, 630))

        # creation des boutons
        bouton_metronome = pygame.image.load("img/bouton.png")
        bouton_metronome = pygame.transform.scale(bouton_metronome, (250, 50))
        bouton_metronome_rect = bouton_metronome.get_rect()
        bouton_metronome_rect.x = 780
        bouton_metronome_rect.y = 150
        input_metronome = pygame.image.load("img/bouton.png")
        input_metronome = pygame.transform.scale(bouton_metronome, (150, 50))
        input_metronome_rect = input_metronome.get_rect()
        input_metronome_rect.x = 780
        input_metronome_rect.y = 250
        ok_input = pygame.image.load("img/bouton.png")
        ok_input = pygame.transform.scale(bouton_metronome, (50, 50))
        ok_input_rect = ok_input.get_rect()
        ok_input_rect.x = 970
        ok_input_rect.y = 250

        # texte et texte des boutons
        texte2 = self._police.render("Appuie sur une touche de ton clavier :)", 1, (0, 0, 0))
        texte_tonalite = self._police.render("Tonalité :", 1, (0, 0, 0))
        texte_metronome = self._police.render("METRONOME", 1, (0, 0, 0))
        texte_ok_input = self._police.render('OK', True, (0, 0, 0))
        texte_input_metronome = self._police.render("entrez un chiffre en bpm", 1, (0, 0, 0))
        user_texte = '120'

        # initialisation de l'armure
        choix_gamme = 8

        running = True

        # boucle d'affichage
        while running:

            tab_notes_on = Acquéreur_note.get_notes_on()

            pygame.draw.rect(self._screen, pygame.Color('black'), input_metronome_rect)

            # texte à update
            texte_affichage = self._police.render("Affichage", 1, (0, 0, 0))
            user_texte_metronome = self._police.render(user_texte, True, (0, 0, 0))

            # affichage/superposition des images/textes
            self._screen.fill((255, 255, 255))
            self._screen.blit(portee, (0, 100))
            self._screen.blit(texte2, (400, 20))

            self._screen.blit(cote, (763, 50))
            self._screen.blit(texte_affichage, (790, 85))
            self._screen.blit(texte_tonalite, (790, 350))
            self._screen.blit(bouton_metronome, bouton_metronome_rect)
            self._screen.blit(texte_metronome, (bouton_metronome_rect.x + 60, bouton_metronome_rect.y + 10))
            self._screen.blit(input_metronome, input_metronome_rect)
            self._screen.blit(texte_input_metronome, (input_metronome_rect.x + 10, input_metronome_rect.y - 30))
            self._screen.blit(user_texte_metronome, (input_metronome_rect.x + 20, input_metronome_rect.y + 10))
            self._screen.blit(ok_input, ok_input_rect)
            self._screen.blit(texte_ok_input, (ok_input_rect.x + 10, ok_input_rect.y + 10))

            # Armure
            armure = Gamme(choix_gamme)
            texte_gamme = self._police.render(armure.name, 1, (0, 0, 0))
            self._screen.blit(texte_gamme, (900, 350))
            nb_symbol = armure.nb_alteration()
            symbol = diese
            if nb_symbol > 0:
                if armure.value < 8:
                    symbol = bemol
                position_x = 100
                for i in range(nb_symbol):
                    midi = armure.affichage_sol(i)
                    note_armure = Note(Note.definir_note(midi))
                    self._screen.blit(symbol, (position_x, note_armure.hauteur_placement(midi)))
                    midi = armure.affichage_fa(i)
                    note_armure = Note(Note.definir_note(midi))
                    self._screen.blit(symbol, (position_x, note_armure.hauteur_placement(midi)))
                    position_x += 25

            # notes
            note_precedente = None
            nb_note_decale = 0
            for note_midi in tab_notes_on:

                note = Note(Note.definir_note(note_midi))
                # bloc pour décaler une note en cas d'accord serré : si une note se trouve à moins de 1 ou deux cran d'écart
                # c'est soit la même note en dièse, soit la note juste au dessus, dans tout les cas on la décale pour éviter
                # qu'elles se chevauchent
                position_x = 350
                if note_precedente is not None:
                    if note.value - note_precedente.value <= 2 \
                            or note.value - note_precedente.value <= 3 and len(note.name) > 3:
                        nb_note_decale += 1
                        position_x += 50 * nb_note_decale

                placement = note.hauteur_placement(note_midi)
                note_affichee = note_simple
                self._screen.blit(note_affichee, (position_x, placement))

                # affiche un dièse si note est dièse et non intégrée dans la gamme
                if len(note.name) > 3:
                    if not armure.note_alteree(note):
                        self._screen.blit(symbol, (position_x - 40, placement))

                # affiche une barre de portée si note hors de la portée
                if note_midi < 41:
                    placement = 371
                    difference = int((40 - note_midi + 3) / 3)
                    for i in range(difference):
                        self._screen.blit(barre, (position_x, placement))
                        placement += 26
                if note_midi > 80:
                    placement = 59
                    difference = int((note_midi - 81 + 3) / 3)
                    for i in range(difference):
                        self._screen.blit(barre, (position_x, placement))
                        placement -= 26
                if note_midi == 60:
                    self._screen.blit(barre, (position_x, placement))

                # affiche le nom de la note
                texte = self._police.render(note.to_string(note_midi), 1, (0, 0, 0))
                self._screen.blit(texte, (position_x, 650))
                note_precedente = note

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if choix_gamme < 15:
                        if event.key == pygame.K_d:
                            choix_gamme += 1
                    if choix_gamme > 1:
                        if event.key == pygame.K_b:
                            choix_gamme -= 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        Metronome.mute_demute()

                elif event.type == pygame.QUIT:
                    return ['quitter']

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    input_actif = False

                    if bouton_metronome_rect.collidepoint(event.pos):
                        Metronome.mute_demute()

                    elif input_metronome_rect.collidepoint(event.pos):
                        input_actif = True
                        user_texte = ""

                    elif ok_input_rect.collidepoint(event.pos):
                        Metronome.changer_bpm(int(user_texte))

                if event.type == pygame.KEYDOWN:
                    if input_actif:
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
                            user_texte = user_texte[:-1]
                        # unicode stock la valeur de la touche frappé
                        else:
                            user_texte += event.unicode
