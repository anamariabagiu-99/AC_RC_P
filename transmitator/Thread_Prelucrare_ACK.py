import socket_comunicare as sc
import Tahoe_Algoritm as ta
from threading import Thread
from threading import Condition

# creez o clasa care sa imi fac prelucrarea ACK

class Thread_Prelucrare_ACK(Thread):
    stare_prelucrare_ACK = Condition() # var de cond pentru sincronizare thread

    def __init__(self):
        # apelez constructorul din clada parinte
        super(Thread_Prelucrare_ACK, self).__init__()

    def run(self):
        # rulez thread-ul la infinit
        while 1:
            # primesc lock
            Thread_Prelucrare_ACK.stare_prelucrare_ACK.acquire()
            # astept cat timp coada de ACK e goala
            if len(sc.Thread_Primire.coada_ACK) == 0:
                Thread_Prelucrare_ACK.stare_prelucrare_ACK.wait()
            # daca am in coada prelucrez
            else:
              # scot din coada sirul
                sir = sc.Thread_Primire.coada_ACK.pop(0)
                # ar trebui sa parcurg coada de pachete neconfirmate si sa il scot pe cel pentru
                # care am primit ack
                for i in range(0, len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)):
                    # scot pachetul de pe pozitia i
                    c = ta.Tahoe_Algoritm.coada_pachete_neconfirmate[i]
                    # scot numarul pachetului
                    nr = c.split('&')
                    nr = nr[1]
                    # compar cele 2 siruri
                    if (siruri_egale(nr, sir)):
                        # daca cele 2 siruri sunt egale, atunci scot din coada pachetul pt
                        # acesta primit confirmare
                        p=ta.Tahoe_Algoritm.coada_pachete_neconfirmate.pop(i)
                        # actualizez si ultima ACK primita
                        ta.Tahoe_Algoritm.coada_ut_conf[0] = p
                        break
                # verific daca nu mai am nimic in coada de pachete trimise, dar inca neconfirmate
                if(len( ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0):
                    # daca nu mai, am pot sa cresc dimensiunea ferestrei de congestie
                    ta.Tahoe_Algoritm.slow_start()
            Thread_Prelucrare_ACK.stare_prelucrare_ACK.release()



def siruri_egale(s1, s2):
    # verific daca cele 2 siruri au lungimi egale
    if(len(s1)!=len(s2)):
        # in caz contrar inseamna ca ele nu pot fi identice
        return False
    # parcurg cele 2 siruri si verific daca sunt la fel
    for c in range (0, len(s1)):
        if s1[c]!= s2[c]:
            # cele 2 siruri au simboluri diferite pe aceeasi pozitie-> nu sunt egale
            return False
    # sirurile sunt identice
    return True