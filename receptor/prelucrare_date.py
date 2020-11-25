from threading import Thread
from threading import Condition
import socket_com as s_c


class Prelucrare_date:
    @staticmethod
    def prelucrare(sir):
        # TODO prelucrarea pachetelor care vin pe socket
        # TODO coada pentru ACK
        coada=["ana", "are", "mere"]
        print(sir)
        return coada


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
                r = Prelucrare_date.prelucrare(sir)
                # r il pun in coada pentru trimis confirmari
                s_c.Thread_Trimitere_ACK.coada_ACK = s_c.Thread_Trimitere_ACK.coada_ACK+r

                # anunt threadul pentru trimiterea de ACK
                s_c.Thread_Trimitere_ACK.stare_ACK.acquire()
                s_c.Thread_Trimitere_ACK.stare_ACK.notify()
                s_c.Thread_Trimitere_ACK.stare_ACK.release()

            # eliberez lock
            Thread_date.stare_date_primite.release()