from enum import Enum


class Gamme(Enum):
    DO_diese = 15
    FA_diese = 14
    SI = 13
    MI = 12
    LA = 11
    RE = 10
    SOL = 9
    DO = 8
    FA = 7
    SI_bemol = 6
    MI_bemol = 5
    LA_bemol = 4
    RE_bemol = 3
    SOL_bemol = 2
    DO_bemol = 1

    def liste_alterations(self):
        alteration = []
        # altération en dièse
        if self.value > 8:  # Sol maj
            alteration.append("FA_diese")
            if self.value > 9:  # Ré maj
                alteration.append("DO_diese")
                if self.value > 10:  # La maj
                    alteration.append("SOL_diese")
                    if self.value > 11:  # Mi maj
                        alteration.append("RE_diese")
                        if self.value > 12:  # Si maj
                            alteration.append("LA_diese")
                            if self.value > 13:  # Fa maj
                                alteration.append("MI_diese")
                                if self.value > 14:  # Do maj
                                    alteration.append("SI_diese")
        # altération en bémol
        if self.value < 8:  # Si
            alteration.append("SI_bemol")
            if self.value < 7:  # Mi
                alteration.append("MI_diese")
                if self.value < 6:  # La
                    alteration.append("LA_diese")
                    if self.value < 5:  # Re
                        alteration.append("RE_diese")
                        if self.value < 4:  # Sol
                            alteration.append("SOL_diese")
                            if self.value < 3:  # Do
                                alteration.append("DO_diese")
                                if self.value < 2:  # Fa
                                    alteration.append("FA_diese")
        return alteration

    def affichage_sol(self, nombre):
        if self.value > 8:
            note_armure = [78, 73, 80, 75, 70, 76, 71]  #ok
        else:
            note_armure = [71, 76, 70, 75, 68, 73, 66]  #ok
        return note_armure[nombre]

    def affichage_fa(self, nombre):
        if self.value > 8:
            note_armure = [54, 49, 56, 51, 46, 52, 47]  #ok
        else:
            note_armure = [47, 52, 46, 51, 44, 49, 42]  #ok
        return note_armure[nombre]

    def nb_alteration(self):
        return len(self.liste_alterations())

    def note_alteree(self, note):
        if note.name in self.liste_alterations():
            return True
        return False
