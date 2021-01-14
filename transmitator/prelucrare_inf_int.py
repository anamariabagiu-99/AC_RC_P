from tkinter import messagebox
import interfata_grafica  as i_g


class prelucrare_inf_int:
    @staticmethod
    def validare_port(sir):
        # sirul care va reprezenta nr portului trebuie sa fie alcatuit doar '
        # din cifre, iar prima cifra dif de 0
        if sir[0] == '0':
            s = 'Numarul portului nu trebuie sa inceapa cu cifra 0.'
            messagebox.showinfo('Eroare', s)
            return False
        # verific sa fie alcatuit doar din cifre
        for x in sir:
            if not (x >= '0' and x <= '9'):
                s = 'Numarul portului  trebuie sa fie alcatuit doar din cifre.'
                messagebox.showinfo('Eroare', s)
                return False
        # in cazul in care nu am iesit pe niciuna din conditiile de mai sus
        return True

    @staticmethod
    def alcatuit_cifre(sir):
        # fct ce verifica ca un sir sa fie alcatuit doar din cifre
        for x in sir:
            if not (x >= '0' and x <= '9'):
                return False
        return True

    @staticmethod
    def numar(sir):
        # fct care face transformarea din sir in nr intreg
        nr = 0
        for x in sir:
            # aplic formula de la matematica
            nr = nr*10 + int(x)
        return nr