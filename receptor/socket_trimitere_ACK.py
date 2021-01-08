import select
import socket_utile as s_u
from threading import Thread
from threading import Condition
import prelucrare_date as  p_d
import socket_primire as s_p


class Thread_Trimitere_ACK(Thread):

    # variabila de conditie care imi va spune starea threadului
    stare_ACK = Condition()
    coada_ACK = [] # coada in care voi pune ACK de trimis
    trimit_ACK = False # un flag care imi va spune daca trimit sau nu ACK
    coada_nu_ACK = [] # coada cu pachetele pentru care nu trimit ACK
    ultima_ACK = [] # ultima ACK trimis
    coada_index = [0] # coada care imi va spune de cate ori am trimis ACk

    #constructorul
    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Trimitere_ACK, self).__init__()
        self.i = interfata

    def run(self):
        # astept la infinit
        while True:
            # primesc lock
            Thread_Trimitere_ACK.stare_ACK.acquire()
            # astept cat timp nu am in coada de trimis
            if len(Thread_Trimitere_ACK.coada_ACK) == 0:
                Thread_Trimitere_ACK.stare_ACK.wait()
            # daca am in coada, scot si trimit pe socket
            if len(Thread_Trimitere_ACK.coada_ACK) :
                # daca am facut un pachet duplicat sa nu il fac la inf
                if Thread_Trimitere_ACK.ultima_ACK[0] != Thread_Trimitere_ACK.coada_ACK[0]:
                    self.ACK_netrimise()

                # verific daca nu am blocat trimiterea
                if (len(Thread_Trimitere_ACK.coada_ACK) and not (Thread_Trimitere_ACK.trimit_ACK) ):
                    string = Thread_Trimitere_ACK.coada_ACK.pop(0)
                    sir = string
                    string = '%' + string + '%'
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                    (s_u.Socket_Utile.localIP, 20001))
                    # actualizez ultima ACK
                    Thread_Trimitere_ACK.ultima_ACK.insert(0, sir)
                    self.i.update_label_ACK(string)
                else:
                    # in cazul in care am blocat trimiterea, trimit 4 copii ale ultimei ACK
                    if Thread_Trimitere_ACK.coada_index[0] < 4:
                        # extrag detaliile pentru ultima ACK
                        string = Thread_Trimitere_ACK.ultima_ACK[0]
                        # impachetez conform formatului stabilit
                        string = '%' + string + '%'
                        # trimit pe socket
                        s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                                (s_u.Socket_Utile.localIP, 20001))
                        # actualizez inf pe interfata
                        self.i.update_label_ACK(string)
                        # actualizez contorul
                        Thread_Trimitere_ACK.coada_index[0] = Thread_Trimitere_ACK.coada_index[0] + 1
                    else:
                        # am terminat de trimis copiile si las coada de ACK vida
                        Thread_Trimitere_ACK.coada_ACK = []
                        # actualizez contorul
                        Thread_Trimitere_ACK.coada_index[0] = 0
                        # eliberez lock
            Thread_Trimitere_ACK.stare_ACK.release()

    def ACK_netrimise(self):
        # fct care imi va spune daca trimit sau nu ACK
        # verific daca nu am blocata deja trimiterea
        if not(Thread_Trimitere_ACK.trimit_ACK):
            # daca nu e, verific daca poate fi blocata
            Thread_Trimitere_ACK.trimit_ACK = p_d.Prelucrare_date.trimit_sau_nu()
        if Thread_Trimitere_ACK.trimit_ACK:
            print('Am blocat trimiterea')
            # eliberez coada de pachete primite, pentru ca vor fi retransmise
            s_p.Thread_Primire_Date.coada_pachete = []


