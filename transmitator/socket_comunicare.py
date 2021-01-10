from threading import Thread
from threading import Condition
import prelucrare_fisiere as p_f
import socket_utile_c as s_u
import select
import Tahoe_Algoritm as ta
import Thread_Prelucrare_ACK as tpa

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
            coada_trimis = [] # coada in care voi pune pachetele de trimis
                # daca cele doua cozi din care pot lua pachete spre a fi trimise sunt
                # vide astept
            if (len(p_f.Thread_Prelucrare.coada_pachete) == 0) and len(
                        ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                Thread_Trimitere.stare_trimitere.wait()
            # daca nu am elemente in coada de retransmisie si toate pachetele trimise
            # au primit ACK, trimit din coada de pachete
            if len(p_f.Thread_Prelucrare.coada_pachete) and len(
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(
                        ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                # scot primul pachet si verific daca este de tip start/ stop
                p = p_f.Thread_Prelucrare.coada_pachete [0]
                # daca da, il trimit direct, fara sa ma uit la cwnd si fara sa il pun in coada
                if p[0] == '*':
                    # il scot din coada
                    s = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                    # trimit
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(s.encode('utf-8')),
                                                            (s_u.Socket_Utile.localIP, 1089))
                    # daca am in coada preiau din aceasta doar cate imi spune cwnd

                    # mai intai verific daca in coada nu sunt mai putine pachete decat dim
                if len(p_f.Thread_Prelucrare.coada_pachete) < ta.Tahoe_Algoritm.cwnd:
                    print('cazul in care am mai putine')
                            # le trimit pe toate
                    for i in range(0, len(p_f.Thread_Prelucrare.coada_pachete)):
                        # verific sa nu fie pachetul de start sau stop
                        if (p_f.Thread_Prelucrare.coada_pachete[0][0] !='*'):
                            # le scot din coada de pachete
                            p = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                            # le adaug in coada de trimis si in coada de pachete neconfirmate
                            coada_trimis = coada_trimis + [p]
                            ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                                        = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                else:
                            # scot din coada doar cwnd pachete
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        # verific sa nu fie pachetul de start sau stop
                        if (p_f.Thread_Prelucrare.coada_pachete[0][0] != '*'):
                            # la fel le scot din coada de pachete, le pun in coada de trimis
                            # si in cea de pachete neconfirmate
                            p = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                            coada_trimis = coada_trimis + [p]
                            ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                                        = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                    # parcurg fiecare element din coada de trimis
                for i in range(0, len(coada_trimis)):
                    # scot din coada
                    string = coada_trimis.pop(0)
                    print("Am trimis " + string)
                    # trimit pe socket
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                                (s_u.Socket_Utile.localIP, 1089))
            # in cazul in care am elemente in coada de retransmisie si pachetele deja trimise
            # au primit ACK, trimit pachetele din coada de retransmisie
            elif len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) != 0:
                print('Trimit din retransmise')
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 1:
                    # trimit direct
                    p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                    coada_trimis = coada_trimis + [p]
                    ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                        = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) < ta.Tahoe_Algoritm.cwnd:
                     print('cazul in care am mai putine')
            # le trimit pe toate
                     for i in range(0,len(ta.Tahoe_Algoritm.coada_pachete_retransmise)):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                            = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                else:
                    print('coada de retransmisie')
                    print(ta.Tahoe_Algoritm.coada_pachete_retransmise)
                    # scot din coada doar cwnd pachete
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                            = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                print("coada de trimis")
                print(coada_trimis)
                for i in range(0, len(coada_trimis)):
                    string = coada_trimis.pop(0)
                    print("Am trimis " + string)
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                            (s_u.Socket_Utile.localIP, 1089))

                # ta.Tahoe_Algoritm.coada_pachete_retransmise=[]
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) ==0:
                    ta.Tahoe_Algoritm.stop_Thread = False

                print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
                # eliberez lock


            Thread_Trimitere.stare_trimitere.release()



# thread pentru primirea de pe socket
class Thread_Primire(Thread):
    stare_primire = Condition()  # variabila de conditie pentru primirea din socket
    coada_ACK = [] # coada de ACK primite
    timp_asteptare = [0] # timpul de asteptare
    ultima_ACK = [0, ' '] # retin ultima ACK primit si un contor pentru aceasta

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
                # incrementez un contor care sa imi spuna cat am asteptat pana am primit ceva
                contor = contor + 1
            else:
                # primesc ceva pe socket
                data, address = s_u.Socket_Utile.UDPServerSocket.recvfrom(s_u.Socket_Utile.bufferSize)
                # preia data primita ca fiind string
                sir=str(data)
                # prelucrez informatia, tiind cont de formatul ei de pe socket
                sir = sir.split('%')
                sir = sir[1]
                # actualizez pe interfata
                self.interfata.update_label_ACK(sir)
                # pentru partea de ACK duplicat
                partea_ACK_duplicat(sir)
                # verific daca nu am retransmisie
                # TODO AICI AM MODIFICAT
                if not ta.Tahoe_Algoritm.trimiterea_rapida():
                # pun in coada de prelucrare
                    Thread_Primire.coada_ACK=Thread_Primire.coada_ACK + [sir]
                    # dau lock thread-ul de prelucrare de ACK
                    tpa.Thread_Prelucrare_ACK.stare_prelucrare_ACK.acquire()
                    # il notific
                    tpa.Thread_Prelucrare_ACK.stare_prelucrare_ACK.notify()
                    # eliberez lock
                    tpa.Thread_Prelucrare_ACK.stare_prelucrare_ACK.release()
                # resetez contorul de timp
                Thread_Primire.timp_asteptare.insert(0, contor)
                print('data= '+ sir )

            # eliberez lock
            Thread_Primire.stare_primire.release()

def partea_ACK_duplicat(sir):
    print('Am intrat in ACK duplicat')
    # verific daca am primit de  mai multe ori confirmare pentru un pachet, incrementez
    # un contor
    if p_f.Prelucrare_fisier.siruri_egale(Thread_Primire.ultima_ACK[1], sir):
        # daca aceasta exista deja, atunci incrementez contorul
        Thread_Primire.ultima_ACK[0] = Thread_Primire.ultima_ACK[0]+1
    else:
        # daca nu am introduc in coada si resetez contorul
        Thread_Primire.ultima_ACK[1] = sir
        Thread_Primire.ultima_ACK[0] = 0



