from threading import Thread
from threading import Condition
import  socket_comunicare as s_c
import socket_utile_c as s_u


class Prelucrare_fisier:
    # setez dimenisiunea unui pachet
    dim_pachet=15
    # coada pentru siruri
    coada_siruri=[]
    numar_pachet=0
    nr_pachet=1
    @staticmethod
    def citire_fisier(cale):
        # deschid fisierul in format rb
        c = open(cale)
        # citesc continutul fisierului
        text = c.read()
        # il afisez doar pentru test, DE SCOS
        #print(text)
        # inchid fisierul
        c.close()
        # apelez functia pentru spargerea fisierului in bucatele mai mici
        Prelucrare_fisier.spargere_fisier(sir=text)
        # returnez fisierul citit
        return text

    @staticmethod
    def spargere_fisier(sir):
        # despart continutul fisierului in bucatele micute
        pas=Prelucrare_fisier.dim_pachet
        # parcurg sirul cu pas si pun in coada
        coada_siruri = []
        for i in range(pas, len(sir)+pas, pas):
            s=sir[i-pas:i]
            #print(s)
            # pun in coada de sir semi prelucrat
            coada_siruri.append(s)
        #apelez functia pentru impachetarea datelor
        return coada_siruri

    @staticmethod
    def suma_control(sir):
        # calculez suma de control a sirului
        suma=0
        for c in sir:
            suma=suma + ord(c)
        return suma


    @staticmethod
    def impachetare_continut(sir):
        # mai intai sparg continutul fisierului in siruri micute
        coada_siruri=Prelucrare_fisier.spargere_fisier(sir)
        # coada in care vor fi puse sirurile prelucrate
        vector=[]
        # &nr_pachet& sir #suma control#
        # parcurg toate elementele din coada

        for s in coada_siruri:
            suma=Prelucrare_fisier.suma_control(s)
            sir='&'+str(Prelucrare_fisier.nr_pachet)+'&'+s+'#'+str(suma)+'#'
            Prelucrare_fisier.nr_pachet=Prelucrare_fisier.nr_pachet+1
            vector.append(sir)
        print(Prelucrare_fisier.nr_pachet)
        return vector



class Thread_Prelucrare(Thread):
    # creez o variabila de conditie pentru sincronizarea thread-ului de citire
    stare_citire = Condition()
    coada_fisiere = []
    coada_pachete = []

    def __init__(self):
        # apelez constructor din clasa parinte
        super(Thread_Prelucrare, self).__init__()

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Prelucrare.stare_citire.acquire()
            # astept cat coada e vida
            if len(Thread_Prelucrare.coada_fisiere) == 0:
                Thread_Prelucrare.stare_citire.wait()
            # prelucrez urmatorul elem din coada
            if len(Thread_Prelucrare.coada_fisiere):
                sir=Prelucrare_fisier.citire_fisier(Thread_Prelucrare.coada_fisiere.pop(0))

                pachete=Prelucrare_fisier.impachetare_continut(sir)
                # pun in coada de pachete
                Thread_Prelucrare.coada_pachete = Thread_Prelucrare.coada_pachete + pachete

                if s_u.Socket_Utile.flag:
                    #  anunt thread-ul de trimitere ca poate sa isi inceapa treaba
                    s_c.Thread_Trimitere.stare_trimitere.acquire()
                    s_c.Thread_Trimitere.stare_trimitere.notify()
                    # eliberare lock
                    s_c.Thread_Trimitere.stare_trimitere.release()

            Thread_Prelucrare.stare_citire.release()



