from enum import Enum


class Note(Enum):
    DO = 0
    DO_diese = 1
    RE = 2
    RE_diese = 3
    Mi = 4
    FA = 5
    FA_diese = 6
    SOL = 7
    SOL_diese = 8
    LA = 9
    LA_diese = 10
    SI = 11

    @staticmethod
    def definir_note(numero_midi):
        return int(numero_midi % 12)

    def definir_octave(self, numero_midi):
        return int(numero_midi / 12 - 1)

    def hauteur_placement(self, numero_midi):
        diese = 0
        if self.value >= 10:
            diese = 5
        elif self.value >= 8:
            diese = 4
        elif self.value >= 6:
            diese = 3
        elif self.value >= 3:
            diese = 2
        elif self.value >= 1:
            diese = 1
        return 592 - (self.definir_octave(numero_midi) * 7 + self.value + 1 - diese) * 13

    def to_string(self, numero_midi):
        return str(self.definir_octave(numero_midi)) + " " + self.name
