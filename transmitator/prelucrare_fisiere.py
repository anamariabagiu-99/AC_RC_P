from threading import Thread
from threading import Condition
import  socket_comunicare as s_c
import socket_utile_c as s_u


class Prelucrare_fisier:
    @staticmethod
    def citire_fisier(cale):
        # deschid fisierul in format rb
        c = open(cale, "rb")
        # citesc continutul fisierului
        text = c.read()
        # il afisez doar pentru test, DE SCOS
        # print(text)
        # inchid fisierul
        c.close()
        # returnez fisierul citit
        return text

    @staticmethod
    def impachetare_continut(sir):
        #modalitatea in care va fi impartit textul si cum va fi
        #el transmis pe socket
        # TODO vector de pachete
        vector=["ana", "are", "mere"] # pentru test DE SCOS
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
                # TODO partea de prelucrare vector
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



