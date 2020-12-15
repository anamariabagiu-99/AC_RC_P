from threading import Thread
from threading import Condition
import socket_com as s_c


class Prelucrare_date:
    @staticmethod
    def prelucrare(sir):
        # formatul pachetului este & nr& sir #suma#
        s=sir.split('&')
        # scot numarul pachetului, imi trebuie pentru partea de confirmare
        # a pachetelor
        nr_pachet=s[1]
        coada=[]
        s2=sir.split('#')
        # scot suma de control
        suma=s2[1]
        # scot sirul
        text=s[2]
        text=text.split('#')
        text=text[0]
        #ar trebui verificata suma
        suma_calculata=Prelucrare_date.suma_de_control(text)
        suma_pachet=Prelucrare_date.sir_number(suma)
        if(suma_calculata != suma_pachet):
            # TODO ce fac in cazul in care nu am primit corect
            print('Sume diferite')
        lista=[nr_pachet, text]
        return lista

    @staticmethod
    def suma_de_control(sir):
        suma = 0
        for c in sir:
            suma+= ord(c)
        return suma

    @staticmethod
    def sir_number(sir):
        nr =  0
        for c in sir :
            nr = nr*10 + int(c)
        #print(nr+1)
        return nr


class Thread_date(Thread):
    # variabila de conditie
    stare_date_primite=Condition()

    # constructorul clasei
    def __init__(self):
        # apelez constructorul din clasa parinte
        super(Thread_date, self).__init__()

    def run(self):
        # voi astepta
        while True:
            # primesc lock
            Thread_date.stare_date_primite.acquire()

            if len(s_c.Thread_Primire_Date.coada_pachete) == 0:
                # cat timp nu am pachete primite de prelucrat, astept
                Thread_date.stare_date_primite.wait()
            else:
                # scot primul pachet si il trimit la prelucrat
                sir = s_c.Thread_Primire_Date.coada_pachete.pop(0)
                print(sir)
                lista = Prelucrare_date.prelucrare(sir)
                # r il pun in coada pentru trimis confirmari
                print(lista[0])
                s_c.Thread_Trimitere_ACK.coada_ACK = s_c.Thread_Trimitere_ACK.coada_ACK+[lista[0]]

                # anunt threadul pentru trimiterea de ACK
                s_c.Thread_Trimitere_ACK.stare_ACK.acquire()
                s_c.Thread_Trimitere_ACK.stare_ACK.notify()
                s_c.Thread_Trimitere_ACK.stare_ACK.release()

            # eliberez lock
            Thread_date.stare_date_primite.release()