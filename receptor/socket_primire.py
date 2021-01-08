import select
import socket_utile as s_u
from threading import Thread
from threading import Condition
import prelucrare_date as  p_d
import socket_trimitere_ACK as s_t


class Thread_Primire_Date(Thread):
    # variabila de conditie pentru primirea de pachete
    stare_primire_date=Condition()
    # coada in care voi pune pachetele primite pe socket
    coada_pachete=[]

    # constructorul clasei
    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Primire_Date, self).__init__()
        self.interfata = interfata

    # fct de run a thread
    def run(self):
        # astept la infinit
        while True:
            # primesc lock
            Thread_Primire_Date.stare_primire_date.acquire()
            # verific daca s-a apasat pe start
            if not s_u.Socket_Utile.flag:
                # astept cat inca conexiunea nu a fost deschisa
                Thread_Primire_Date.stare_primire_date.wait()
            # Apelam la functia sistem IO -select- pentru a verifca
            # daca socket-ul are date in bufferul de receptia
            r, _, _ = select.select([s_u.Socket_Utile.UDPServerSocket], [], [], 1)
            # daca am date le prelucrez
            if r:
                # scot inf din r
                data, address = s_u.Socket_Utile.UDPServerSocket.recvfrom(s_u.Socket_Utile.bufferSize)
                # verific daca am blocata trimiterea si o deblochez
                if s_t.Thread_Trimitere_ACK.trimit_ACK :
                    self.deblocare()
                # apoi prelucrez inf primite
                    # pun in coada inf citite din socket
                Thread_Primire_Date.coada_pachete.append(str(data))
                # anunt thread-ul pentru prelucrarea inf
                p_d.Thread_date.stare_date_primite.acquire()
                p_d.Thread_date.stare_date_primite.notify()
                p_d.Thread_date.stare_date_primite.release()
                # actualizez inf pe gui
                self.interfata.update_label_packet(str(data))
            # eliberez resursele
            Thread_Primire_Date.stare_primire_date.release()


    def deblocare(self):
        # fct pentru deblocarea trimiterii ACK, dupa ce am trimis duplicate
        print('Am intrat in fct de deblocare.')
        s_t.Thread_Trimitere_ACK.trimit_ACK = False