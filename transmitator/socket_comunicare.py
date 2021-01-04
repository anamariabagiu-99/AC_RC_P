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
            if(ta.Tahoe_Algoritm.stop_Thread):
                print('Am fost pornit de primire')
            # verific daca coada de pachete nu este vida
            if ( len(p_f.Thread_Prelucrare.coada_pachete) == 0) and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0 :
                # coada este vida si astept
                Thread_Trimitere.stare_trimitere.wait()

            # TODO partea de transmisie cu un anumit nr de pachete
            # trimit ceva pe sarma
            # de modificat DOAR pentru test
            #print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
            if len( p_f.Thread_Prelucrare.coada_pachete) and len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                # daca am in coada preiau din aceasta doar cate imi spune cwnd
                coada_trimis=[]
                # mai intai verific daca in coada nu sunt mai putine pachete decat dim
                if len(p_f.Thread_Prelucrare.coada_pachete) < ta.Tahoe_Algoritm.cwnd:
                    # le trimit pe toate
                    coada_trimis = p_f.Thread_Prelucrare.coada_pachete

                else:
                    # scot din coada doar cwnd pachete
                    #print('cwnd ='+ str(ta.Tahoe_Algoritm.cwnd))
                    for i in range (0, ta.Tahoe_Algoritm.cwnd):
                        p = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                        coada_trimis = coada_trimis+[p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate\
                            = ta.Tahoe_Algoritm.coada_pachete_neconfirmate+[p]
                    #print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
                    #print(coada_trimis)
                # si le pun in coada cu pachete neconfirmate
                #string = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                # trimit toate pachetele din coada de trimis
                for i in range(0, len(coada_trimis)):
                    string=coada_trimis.pop(0)
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                        (s_u.Socket_Utile.localIP, 1089))

            elif len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) != 0:
                print('Trimit din retransmise')
                coada_trimis = []
                # mai intai verific daca in coada nu sunt mai putine pachete decat dim
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) < ta.Tahoe_Algoritm.cwnd:
                    # le trimit pe toate
                    coada_trimis = ta.Tahoe_Algoritm.coada_pachete_retransmise

                else:
                    print('coada de retransmisie')
                    print(ta.Tahoe_Algoritm.coada_pachete_retransmise)
                    # scot din coada doar cwnd pachete
                    # print('cwnd ='+ str(ta.Tahoe_Algoritm.cwnd))
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                            = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                    # print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
                    # print(coada_trimis)
                # si le pun in coada cu pachete neconfirmate
                # string = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                # trimit toate pachetele din coada de trimis
                print(coada_trimis)
                for i in range(0, len(coada_trimis)):
                    string = coada_trimis.pop(0)
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                            (s_u.Socket_Utile.localIP, 1089))

                # ta.Tahoe_Algoritm.coada_pachete_retransmise=[]
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise):
                    ta.Tahoe_Algoritm.stop_Thread = False

                print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
            # eliberez lock
            Thread_Trimitere.stare_trimitere.release()


# thread pentru primirea de pe socket
class Thread_Primire(Thread):
    # variabila de conditie pentru primirea din socket
    stare_primire = Condition()
    coada_ACK=[]
    timp_asteptare=[0]
    ultima_ACK = [0, ' ']

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
                # preia data primita ca fiind string
                sir=str(data)
                sir = sir.split('%')
                sir = sir[1]
                # actualizez pe interfata
                self.interfata.update_label_ACK(sir)
                # pentru partea de ACK duplicat
                partea_ACK_duplicat(sir)
                # verific daca nu am retransmisie
                ta.Tahoe_Algoritm.trimiterea_rapida()
                #print(ta.Tahoe_Algoritm.stop_Thread)

                #print(Thread_Primire.ultima_ACK)
                # pun in coada de prelucrare
                Thread_Primire.coada_ACK=Thread_Primire.coada_ACK+ [sir]
                # dau lock thread-ul de prelucrare de ACK
                tpa.Thread_Prelucrare_ACK.stare_prelucrare_ACK.acquire()
                # il notific
                tpa.Thread_Prelucrare_ACK.stare_prelucrare_ACK.notify()
                # eliberez lock
                tpa.Thread_Prelucrare_ACK.stare_prelucrare_ACK.release()
                Thread_Primire.timp_asteptare.insert(0, contor)
                print('data= '+ sir )
            #print('contor=' +str(Thread_Primire.timp_asteptare[0]))

            # eliberez lock
            Thread_Primire.stare_primire.release()

def partea_ACK_duplicat(sir):
    print('Am intrat in ACK duplicat')
    # verific daca am primit de  mai multe ori confirmare pentru un pachet, incrementez
    # un contor
    if Thread_Primire.ultima_ACK[1]== sir:
        # daca aceasta exista deja, atunci incrementez contorul
        Thread_Primire.ultima_ACK[0] = Thread_Primire.ultima_ACK[0]+1
    else:
        # daca nu am introduc in coada si resetez contorul
        Thread_Primire.ultima_ACK[1] = sir
        Thread_Primire.ultima_ACK[0] = 0


def prelucrare_ACK(sir):
    # eu am sirul de caractere si scot numarul pachetului confirmat
    pass


