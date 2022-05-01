import mido
import threading
from Note import Note

midi_in = ""
midi_out = ""

tab_on_off = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False, False, False, False, False,
              False
              ]

tab_notes_on = []


def acquerir_note():
    global tab_on_off

    #  Boucle d'acquisition et d'affichage des messages envoyés par VMPK,

    outport = mido.open_output(midi_out)  # connexion RtMidi-Out à Synth-In
    with mido.open_input(midi_in) as inport:  # connexion VMPK-Out à RtMidi-In

        for msg in inport:  # passe contenu 'inport' à 'msg'
            # print("Humain: ", msg.note)  # affiche contenu 'msg' Humain à l'écran
            # print("  Bytes:", msg.bytes())  # affiche contenu 'msg' Bytes décimal à l'écran
            outport.send(msg)  # envoie contenu 'msg' à RtMidi-Out vers PC-speaker
            # print(msg.channel)
            tab_on_off[msg.note] = msg.type == "note_on"
            update_notes_on()


def lancer_processus(port_in, port_out):
    global midi_in
    global midi_out
    midi_in = port_in
    midi_out = port_out
    processus_piano = threading.Thread(target=acquerir_note, daemon=True)
    processus_piano.start()


def update_notes_on():
    tab_notes_on.clear()
    for num_note in range(21, 109):
        if tab_on_off[num_note]:
            tab_notes_on.append(num_note)   #les notes ne sont plus instancié ici, cela renvoie un tableau de num midi



def get_notes_on():
    return tab_notes_on
