from threading import Thread
from threading import Condition
import socket_com  as s_c
import interfata_grafica as i_g
import time
import random


class Prelucrare_date:
    f =0
    @staticmethod
    def prelucrare(sir):
        # verific daca nu am un pachet de start sau de stop
        if sir[2] =='*':
            s = sir.split('*')
            # verific daca de tip start/stop
            if Prelucrare_date.siruri_egale(s[1],'START' ):
                # deschid fisierul
                Prelucrare_date.f = open(s[2], "a")
            elif Prelucrare_date.siruri_egale(s[1],'STOP' ):
                Prelucrare_date.f.close()
            return []
        else:
            # formatul pachetului este & nr& sir #suma#
            s=sir.split('&')
            # scot numarul pachetului, imi trebuie pentru partea de confirmare
            # a pachetelor
            nr_pachet=s[1]
            print("nr din fct de prelucrare")
            print(s)
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
            # scriu in fisier
            Prelucrare_date.f.write(text)
            suma_pachet=Prelucrare_date.sir_number(suma)
            if(suma_calculata != suma_pachet):
                # TODO ce fac in cazul in care nu am primit corect
                print('Sume diferite')
            lista=[nr_pachet]
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

    @staticmethod
    def trimit_sau_nu():
        # scot probabiliatea introdusa
        p=i_g.InterfataGrafica.probabilitatea[0]
        print('p=' +str(i_g.InterfataGrafica.probabilitatea) )
        # generez aleator un nr
        nr=random.random()
        # verific unde se situeaza acesta fata de probabilitatea
        # introdusa de utilizator
        if nr < p :
            # trimit confirmare
            print(nr)
            print('trimit')
            return False
        else:
            print(nr)
            print(' nu trimit')
            return True

    @staticmethod
    def siruri_egale(s1, s2):
        if len(s1) != len(s2):
            return False
        for i in (0, len(s1) - 1):
            if s1[i] != s2[i]:
                return False
        return True

    @staticmethod
    def nr_pachet(sir):
        print(sir[2])
        if(sir[2]=='*'):
            print(sir[0])
            s = sir.split('*')
            print(s)
            if (Prelucrare_date.siruri_egale(s[1],'START' ) ):
                return 'deschis : '+ s[2]
            elif (Prelucrare_date.siruri_egale(s[1],'STOP' ) ):
                return 'inchis :'+ s[2]
        else:
            s = sir.split('&')
            print(s)
            # scot numarul pachetului, imi trebuie pentru partea de confirmare
            # a pachetelor
            nr_pachet = s[1]
            return nr_pachet

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
                print("PRELUCREZ SIRUL "+ sir)
                lista = Prelucrare_date.prelucrare(sir)
                if(len(lista)):
                # r il pun in coada pentru trimis confirmari
                #print(lista[0])
                    s_c.Thread_Trimitere_ACK.coada_ACK = s_c.Thread_Trimitere_ACK.coada_ACK+lista

                    # anunt threadul pentru trimiterea de ACK
                    s_c.Thread_Trimitere_ACK.stare_ACK.acquire()
                    s_c.Thread_Trimitere_ACK.stare_ACK.notify()
                    s_c.Thread_Trimitere_ACK.stare_ACK.release()

            # eliberez lock
            Thread_date.stare_date_primite.release()