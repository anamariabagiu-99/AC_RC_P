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
        for x in sir:
            if not (x >= '0' and x <= '9'):
                return False
        return True

    @staticmethod
    def numar(sir, nr=None):
        nr = 0
        for x in sir:
            nr = nr*10 + int(x)
        return nr

    @staticmethod
    def prelucrare_prob(sir):
        # interfata trebuie sa aiba forma nr1/nr2
        lista = sir.split('/')
        if len(lista) == 1:
            s = 'Probabilitatea trebuie sa aiba forma nr1/nr2.'
            messagebox.showinfo('Eroare', s)
        # cele 2 siruri sa fie alcatuite doar din cifre
        if not prelucrare_inf_int.alcatuit_cifre(lista[0]) or not prelucrare_inf_int.alcatuit_cifre(lista[1]):
            s = 'a si b trebuie sa fie alcatuite doar din cifre.'
            messagebox.showinfo('Eroare', s)
            return False
        # valoarea calculata sa fie subunitara
        nr1 = prelucrare_inf_int.numar(lista[0], 0)
        nr2 = prelucrare_inf_int.numar(lista[1], 0)
        p = nr1 /nr2
        if(p > 1):
            s =' Probilitatea trebuie sa fie subunitara pentru asta a < b.'
            messagebox.showinfo('Eroare', s)
            return False
        i_g.InterfataGrafica.probabilitatea.append(p)
        return True