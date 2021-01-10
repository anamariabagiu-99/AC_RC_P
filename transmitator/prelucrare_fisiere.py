from threading import Thread
from threading import Condition

import  socket_comunicare as s_c
import socket_utile_c as s_u


class Prelucrare_fisier:
    dim_pachet = 2 # setez dimenisiunea unui pachet
    coada_siruri = []  # coada pentru siruri
    numar_pachet=0 # contor pentru impachetare
    nr_pachet=1

    @staticmethod
    def citire_fisier(cale):
        c = open(cale) # deschid fisierul in format rb
        text = c.read()  # citesc continutul fisierulul
        c.close() # inchid fisierul
        # apelez functia pentru spargerea fisierului in bucatele mai mici
        Prelucrare_fisier.spargere_fisier(sir=text)
        # returnez fisierul citit
        return text

    @staticmethod
    def spargere_fisier(sir):
        # despart continutul fisierului in bucatele micute
        pas = Prelucrare_fisier.dim_pachet
        # parcurg sirul cu pas si pun in coada
        coada_siruri = [] # pun primul elem din coada calea
        # parcurg sirul, retin cate pas simboluri
        for i in range(pas, len(sir)+pas, pas):
            s = sir[i-pas:i] # scot pas simboluri
            coada_siruri.append(s) # pun in coada de sir semi prelucrat
        return coada_siruri

    @staticmethod
    def suma_control(sir):
        # calculez suma de control a sirului
        suma=0
        # parcurg sirul si adun la suma codul ascii al fiecarei litere
        for c in sir:
            suma=suma + ord(c)
        return suma

    @staticmethod
    def impachetare_continut(sir):
        # mai intai sparg continutul fisierului in siruri micute
        coada_siruri=Prelucrare_fisier.spargere_fisier(sir)
        # coada in care vor fi puse sirurile prelucrate
        vector=[]
        # forma pachetului:&nr_pachet& sir #suma control#
        # parcurg toate elementele din coada

        for s in coada_siruri:
            # calculez suma de control
            suma=Prelucrare_fisier.suma_control(s)
            # realizez impachetarea conform conventiei de mai sus
            sir='&'+str(Prelucrare_fisier.nr_pachet)+'&'+s+'#'+str(suma)+'#'
            # incrementez contorul pentru numarul de pachete
            Prelucrare_fisier.nr_pachet=Prelucrare_fisier.nr_pachet+1
            # adaug in coada de pachete
            vector.append(sir)
        # returnez coada cu sirurile prelucrate
        return vector

    @staticmethod
    def pachet_start_stop(sir, f):
        # fct pentru primul si ultimul pachet
        nume_f = sir.split('/') # despart calea pentru a scoate numele fisierului
        nume_f = nume_f[-1] # scot numele fisierului
        # hotarasc daca pachetul este de start sau de stop
        if f == 1:
            # impachetam pachetul de start
            s = '*START*'+ nume_f
        else:
            # impachetez pachetul de stop
            s = '*STOP*'+ nume_f
        # returnez sirul prelucrat corespunzator
        return s

    @staticmethod
    def siruri_egale(s1, s2):
        # verific daca cele 2 siruri au lungimi egale
        if (len(s1) != len(s2)):
            # in caz contrar inseamna ca ele nu pot fi identice
            return False
        # parcurg cele 2 siruri si verific daca sunt la fel
        for c in range(0, len(s1)):
            if s1[c] != s2[c]:
                # cele 2 siruri au simboluri diferite pe aceeasi pozitie-> nu sunt egale
                return False
        # sirurile sunt identice
        return True



class Thread_Prelucrare(Thread):
    # creez o variabila de conditie pentru sincronizarea thread-ului de citire
    stare_citire = Condition()
    coada_fisiere = [] # coada ce ca contine caile catre fisierele de citit
    coada_pachete = [] # coada ce va contine continutul fisierelor prelucrate

    def __init__(self):
        # apelez constructor din clasa parinte
        super(Thread_Prelucrare, self).__init__()

    # metoda run
    def run(self):
        # astept la infinit
        while True:
            # primesc lock
            Thread_Prelucrare.stare_citire.acquire()
            # astept cat coada e vida
            if len(Thread_Prelucrare.coada_fisiere) == 0:
                Thread_Prelucrare.stare_citire.wait()
            # daca in coada se adauga un fisier pornesc imediat sa il prelucrez
            if len(Thread_Prelucrare.coada_fisiere):
                # scot din coada prima cale spre un fisier
                cale =Thread_Prelucrare.coada_fisiere.pop(0)
                # retin calea pentru impachetarea pachetelor de start si stop
                sir=Prelucrare_fisier.citire_fisier(cale)
                # prelucrez si pun in coada pachetul de start
                s = Prelucrare_fisier.pachet_start_stop(cale, 1)
                # adaug pachetul de start
                Thread_Prelucrare.coada_pachete = Thread_Prelucrare.coada_pachete + [s]
                # prelucrez continutul fisierului
                pachete=Prelucrare_fisier.impachetare_continut(sir)
                # pun in coada de pachete
                Thread_Prelucrare.coada_pachete = Thread_Prelucrare.coada_pachete + pachete
                # dupa ce am pus toate pachetele corespunzatoare, adaug pachetul de stop
                s = Prelucrare_fisier.pachet_start_stop(cale, 2)
                # adaug pachetul de stop
                Thread_Prelucrare.coada_pachete = Thread_Prelucrare.coada_pachete + [s]
                # verific daca am conexiunea pe socket deschisa
                if s_u.Socket_Utile.flag:
                    #  anunt thread-ul de trimitere ca poate sa isi inceapa treaba
                    s_c.Thread_Trimitere.stare_trimitere.acquire()
                    s_c.Thread_Trimitere.stare_trimitere.notify()
                    # eliberare lock
                    s_c.Thread_Trimitere.stare_trimitere.release()
            # eliberare lock
            Thread_Prelucrare.stare_citire.release()



