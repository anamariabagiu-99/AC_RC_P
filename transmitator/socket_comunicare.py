import socket
from socket_utile_c import *
from threading import Thread
from threading import Condition
import prelucrare_fisiere as p_f
import socket_utile_c as s_u
import sys
import select
import interfata_grafica as ig
import Tahoe_Algoritm as ta

# thread pentru trimiterea pe socket
class Thread_Trimitere(Thread):
    # variabila de conditie pentru comunicarea prin socket
    stare_trimitere = Condition()

    def __init__(self):
        # apelez constructorul din clasa parinte
        super(Thread_Trimitere, self).__init__()

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Trimitere.stare_trimitere.acquire()
            # verific daca coada de pachete nu este vida
            if len(p_f.Thread_Prelucrare.coada_pachete) == 0:
                # coada este vida si astept
                Thread_Trimitere.stare_trimitere.wait()
            # TODO partea de transmisie cu un anumit nr de pachete
            # trimit ceva pe sarma
            # de modificat DOAR pentru test
            if len( p_f.Thread_Prelucrare.coada_pachete):
                # daca am in coada
                string = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                        (s_u.Socket_Utile.localIP, 1089))
            # eliberez lock
            Thread_Trimitere.stare_trimitere.release()


# thread pentru primirea de pe socket
class Thread_Primire(Thread):
    # variabila de conditie pentru primirea din socket
    stare_primire = Condition()

    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Primire, self).__init__()

        self.interfata = interfata

    def run(self):
        contor = 0
        while True:
            # primesc lock
            Thread_Primire.stare_primire.acquire()

            # verific daca s-a apasat pe butonul de start
            if not s_u.Socket_Utile.flag:
                # nu s-a apasat inca butonul de start si astept
                Thread_Primire.stare_primire.wait()

            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([s_u.Socket_Utile.UDPServerSocket], [], [], 1)
            if not r:
                contor = contor + 1
            else:
                data, address = s_u.Socket_Utile.UDPServerSocket.recvfrom(s_u.Socket_Utile.bufferSize)
                print("S-a receptionat ", str(data), " de la ", address)
                self.interfata.update_label_ACK(str(data))
                print("Contor= ", contor)

            # eliberez lock
            Thread_Primire.stare_primire.release()
