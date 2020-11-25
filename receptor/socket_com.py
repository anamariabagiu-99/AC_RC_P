import select
import socket_utile as s_u
from threading import Thread
from threading import Condition
import prelucrare_date as  p_d


# thread pentru trimiterea pe socket

class Thread_Trimitere_ACK(Thread):
    # variabila de cond ce o sa imi spuna cand incep sa trimit
    stare_ACK=Condition()
    coada_ACK=[]

    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Trimitere_ACK, self).__init__()
        self.i=interfata

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Trimitere_ACK.stare_ACK.acquire()
            # cat timp nu am ACK in coada de trimis, astept
            if len(Thread_Trimitere_ACK.coada_ACK) == 0:
                Thread_Trimitere_ACK.stare_ACK.wait()
            # daca am in coada, scot si trimit pe socket
            if len(Thread_Trimitere_ACK.coada_ACK):
                string = Thread_Trimitere_ACK.coada_ACK.pop(0)
                s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                        (s_u.Socket_Utile.localIP, 20001))
                # TODO de pus pachetul corespunzator
                self.i.update_label_ACK("1")
                # eliberez lock


class Thread_Primire_Date(Thread):
    # variabila de conditie pentru primirea de pachete
    stare_primire_date=Condition()
    coada_pachete=[]

    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Primire_Date, self).__init__()

        self.interfata = interfata

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Primire_Date.stare_primire_date.acquire()

            # verific daca s-a apasat pe start
            if not s_u.Socket_Utile.flag:
                # astept
                Thread_Primire_Date.stare_primire_date.wait()
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptia
            r, _, _ = select.select([s_u.Socket_Utile.UDPServerSocket], [], [], 1)

            # scot date de pe socket
            if r:
                data, address = s_u.Socket_Utile.UDPServerSocket.recvfrom(s_u.Socket_Utile.bufferSize)
                #pun in coada inf citite din socket
                Thread_Primire_Date.coada_pachete.append(str(data))
                # TODO prelucrarea pachetelor si afisarea a ceva mai mic pe interfata
                # anunt thread-ul pentru prelucrarea inf
                p_d.Thread_date.stare_date_primite.acquire()
                p_d.Thread_date.stare_date_primite.notify()
                p_d.Thread_date.stare_date_primite.release()

                # actualizez inf de pe interfata
                self.interfata.update_label_packet(str(data))
            Thread_Primire_Date.stare_primire_date.release()


