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
    trimit_ACK=False # pentru partea de pierdere a pachetelor
    coada_nu_ACK=[]
    ultima_ACK=['%0%']
    coada_index = [0]

    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Trimitere_ACK, self).__init__()
        self.i=interfata

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Trimitere_ACK.stare_ACK.acquire()
            # verific daca nu am setat flagul pentru duplicat
            '''if ( Thread_Trimitere_ACK.trimit_ACK):
                # daca da, trimit ACK duplicat
                string = Thread_Trimitere_ACK.ultima_ACK[0]
                s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                        (s_u.Socket_Utile.localIP, 20001))
                self.i.update_label_ACK(string)'''


            # cat timp nu am ACK in coada de trimis, astept
            if len(Thread_Trimitere_ACK.coada_ACK) == 0:
                Thread_Trimitere_ACK.stare_ACK.wait()
            # daca am in coada, scot si trimit pe socket
            if len(Thread_Trimitere_ACK.coada_ACK):
                self.ACK_netrimise()
                # in cazul in care nu am blocat trimiterea ACK, trimit pe socket
                if(len(Thread_Trimitere_ACK.coada_ACK) and Thread_Trimitere_ACK.coada_ACK[0]!='*'):
                    string = Thread_Trimitere_ACK.coada_ACK.pop(0)
                    string='%'+string +'%'
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                            (s_u.Socket_Utile.localIP, 20001))
                    # TODO de pus pachetul corespunzator
                    Thread_Trimitere_ACK.ultima_ACK.insert(0,string )
                    self.i.update_label_ACK(string)
                else:
                    if Thread_Trimitere_ACK.coada_index[0] <=  4:
                        string = Thread_Trimitere_ACK.ultima_ACK[0]
                        s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                                (s_u.Socket_Utile.localIP, 20001))

                        self.i.update_label_ACK(string)
                        Thread_Trimitere_ACK.coada_index[0] = Thread_Trimitere_ACK.coada_index[0] + 1
                    else:
                        Thread_Trimitere_ACK.coada_ACK=[]


                    # salvez ACK ca fiind ultimul ACK trimis
                    #Thread_Trimitere_ACK.ultima_ACK.insert(0, string)

                # eliberez lock
                Thread_Trimitere_ACK.stare_ACK.release()

    # functie pentru ACK netrimise
    def ACK_netrimise(self):
        # verific daca flagul este setat pe TRUE, pentru a stii daca la un moment dat
        # i-am schimbat valoarea si opresc trimiterea ACK
        if  not(Thread_Trimitere_ACK.trimit_ACK):
            # daca nu e oprita, arunc cu banul
            Thread_Trimitere_ACK.trimit_ACK=p_d.Prelucrare_date.trimit_sau_nu()
            # daca deja am hotarat ca nu mai trimit pachete,
            # nu mai apelez functia
        if Thread_Trimitere_ACK.trimit_ACK:
            # daca am oprit trimiterea ACK, mut tot in coada de ACk netrimise
            for i in (0, len(Thread_Trimitere_ACK.coada_ACK)-1):
                if(Thread_Trimitere_ACK.coada_ACK):
                    x=Thread_Trimitere_ACK.coada_ACK[i]
                    # fac asta pentru a putea trimite ACK
                    Thread_Trimitere_ACK.coada_ACK[i]='*'
                    Thread_Trimitere_ACK.coada_nu_ACK.append(x)
            print('AM MUTAT TOT!!!!!!!!!!!')

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
                # verific daca pot sa deblochez trimiterea
                self.deblocare_trimitere()
                print(Thread_Trimitere_ACK.trimit_ACK)
                # self.deblocare_trimitere()
                # TODO prelucrarea pachetelor si afisarea a ceva mai mic pe interfata
                # anunt thread-ul pentru prelucrarea inf
                p_d.Thread_date.stare_date_primite.acquire()
                p_d.Thread_date.stare_date_primite.notify()
                p_d.Thread_date.stare_date_primite.release()
                # TODO aici nu este ok, nu pot sa modific astea cum vreau eu, tre sa gasesc
                # o alta cale de sincronizare

                # actualizez inf de pe interfata
                self.interfata.update_label_packet(str(data))
            Thread_Primire_Date.stare_primire_date.release()

    def deblocare_trimitere(self):
        print('am intrat in fct de deblocare')
        # parcurg lista pentru care nu am trimis inapoi ACK
        # si daca primesc un pachet care se afla in aceasta lista, deblochez
        # procesul de trimitere a pachetelor
        for x in  Thread_Primire_Date.coada_pachete:
            # aplic procesul de despachetare a datelor
            l=p_d.Prelucrare_date.prelucrare(x)
            # parcurg lista de ACK netrimise
            for y in Thread_Trimitere_ACK.coada_nu_ACK:
                # daca gasesc pachetul acolo, insemna ca am trimis din nou si
                # trebuie sa modific starea trimiterii
                s=y.split('%')
                s=s[0]
                print(s)
                if l[0]==s:
                    Thread_Trimitere_ACK.trimit_ACK = False




