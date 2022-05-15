import mido
import threading


class AcquereurNote:

    def __init__(self, notali_object):
        self._midi_input = None
        self._midi_output = None
        self._notali = notali_object

    def acquerir_note(self):
        #  Boucle d'acquisition et d'affichage des messages envoyés par VMPK,

        with self._midi_input as inport:  # connexion VMPK-Out à RtMidi-In

            for msg in inport:  # passe contenu 'inport' à 'msg'
                self._midi_output.send(msg)  # envoie contenu 'msg' à RtMidi-Out vers PC-speaker
                self._notali.notifier(msg.note, msg.type == "note_on")

    def lancer_processus(self):
        processus_piano = threading.Thread(target=self.acquerir_note, daemon=True)
        processus_piano.start()

    def set_midi_in(self, port_in):
        if self._midi_input is not None:
            self._midi_input.close()

        self._midi_input = mido.open_input(port_in)

    def set_midi_out(self, port_out):
        if self._midi_output is not None:
            self._midi_output.close()

        self._midi_output = mido.open_output(port_out)
