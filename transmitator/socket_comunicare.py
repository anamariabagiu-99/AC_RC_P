import socket
from socket_utile_c import *
from threading import Thread
from threading import Condition
import prelucrare_fisiere as p_f
import socket_utile_c as s_u
import sys
import select
import interfata_grafica as ig
def receive_fct():
    contor = 0
    running=1
    while running:
        # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
        # Stabilim un timeout de 1 secunda
        r, _, _ = select.select([s_u.Socket_Utile.UDPServerSocket], [], [], 1)
        if not r:
        	contor = contor + 1
        else:
            data, address = s_u.Socket_Utile.UDPServerSocket.recvfrom(1024)
            print("S-a receptionat ", str(data), " de la ", address)
            print("Contor= ", contor)


# thread pentru trimiterea pe socket
class Thread_Comunicare(Thread):
    # variabila de conditie pentru comunicarea prin socket
    stare_comunicare=Condition()

    def __init__(self):
        # apelez constructorul din clasa parinte
        super(Thread_Comunicare, self).__init__()

    def run(self):
        # astept
        while True:
            # primesc lock
                Thread_Comunicare.stare_comunicare.acquire()
            # verific daca coada de pachete nu este vida
                if len(p_f.Thread_Prelucrare.coada_pachete) == 0:
                    # coada este vida si astept
                    Thread_Comunicare.stare_comunicare.wait()
                # TODO partea de transmisie cu un anumit nr de pachete
                # trimit ceva pe sarma
                # de modificat DOAR pentru test
                string = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                        ( s_u.Socket_Utile.localIP, 1089))
                # eliberez lock
                Thread_Comunicare.stare_comunicare.release()


