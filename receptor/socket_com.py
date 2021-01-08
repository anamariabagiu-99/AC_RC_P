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
    am_t_d = False

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
                # daca am primit din nou ultimul pachet, nu il mai fac duplicat
                if Thread_Trimitere_ACK.ultima_ACK[0] != Thread_Trimitere_ACK.coada_ACK[0]:
                    self.ACK_netrimise()
                # in cazul in care nu am blocat trimiterea ACK, trimit pe socket
                print("coada ACK de trimis")
                print(Thread_Trimitere_ACK.coada_ACK)
                if(len(Thread_Trimitere_ACK.coada_ACK) and not(Thread_Trimitere_ACK.trimit_ACK) ):
                    print("Trimit normal")
                    string = Thread_Trimitere_ACK.coada_ACK.pop(0)
                    sir = string
                    print("Trimit "+ sir)
                    string='%'+string +'%'
                    s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                            (s_u.Socket_Utile.localIP, 20001))
                    # actualizez ultima ACK
                    Thread_Trimitere_ACK.ultima_ACK.insert(0 , string)
                    self.i.update_label_ACK(sir)
                else:
                    # trimit patru copii pentru ultima ACK, pentru cazul in carea m blocat trimiterea
                    '''if Thread_Trimitere_ACK.coada_index[0] < 4:
                        print("Trimit cele 4 ACK DUPLICATE")
                        string = Thread_Trimitere_ACK.ultima_ACK[0]
                        print("TRIMIT "+ string)
                        sir = string
                        string = '%' + string + '%'
                        s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                                (s_u.Socket_Utile.localIP, 20001))
                        # actualizez contorul
                        Thread_Trimitere_ACK.coada_index[0] = Thread_Trimitere_ACK.coada_index[0] + 1
                        self.i.update_label_ACK(sir)

                    else:
                        # am terminat de trimis copiile si las coada de ACK vida
                        Thread_Trimitere_ACK.coada_ACK=[]
                        Thread_Trimitere_ACK.coada_index[0] = 0
                        print("am terminat cu duplicatele")
                        print(' Din thread trimitere coada de pachete arata :')
                        print(Thread_Primire_Date.coada_pachete)
                        self.i.update_label_ACK("AM TERMINAT DE TRIMIS COPIILE")
                        Thread_Primire_Date.coada_pachete = []'''
                    Thread_Trimitere_ACK.am_t_d = True
                    string = Thread_Trimitere_ACK.ultima_ACK[0]
                    sir = string
                    string = '%' + string + '%'
                    for i in range(0, 4):
                        print("TRIMIT " + string)
                        s_u.Socket_Utile.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                                (s_u.Socket_Utile.localIP, 20001))
                        # actualizez contorul
                        Thread_Trimitere_ACK.coada_index[0] = Thread_Trimitere_ACK.coada_index[0] + 1
                        self.i.update_label_ACK(sir)
                    Thread_Trimitere_ACK.coada_ACK = []
                    Thread_Primire_Date.coada_pachete = []
                    Thread_Trimitere_ACK.am_t_d = False

                        # eliberez lock'''
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
            print(Thread_Trimitere_ACK.trimit_ACK)
            if Thread_Trimitere_ACK.trimit_ACK:
                # daca am oprit trimiterea ACK, mut tot in coada de ACK netrimise
                # pun si ultima ACK trimis
                print("TRIMIT CERERE DUPLICAT PENTRU "+Thread_Trimitere_ACK.coada_ACK [0])
                Thread_Trimitere_ACK.ultima_ACK [0] = Thread_Trimitere_ACK.coada_ACK [0]
                print("am blocat trimiterea")
                Thread_Primire_Date.coada_pachete =[]




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
                # daca am blocata trimiterea, verific daca pot sa deblochez trimiterea
                if (Thread_Trimitere_ACK.trimit_ACK):
                    self.deblocare_trimitere(str(data))
                #pun in coada inf citite din socket
                Thread_Primire_Date.coada_pachete.append(str(data))
                print("AM PRIMIT "+ str(data))

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

                sir = p_d.Prelucrare_date.nr_pachet(str(data))
                self.interfata.update_label_packet(sir)
            Thread_Primire_Date.stare_primire_date.release()

    def deblocare_trimitere(self, sir ):
        print('am intrat in fct de deblocare')
        Thread_Trimitere_ACK.trimit_ACK = False
        print(' Din fct de deblocare coada de pachete arata :')
        print(Thread_Primire_Date.coada_pachete)
        print(Thread_Trimitere_ACK.trimit_ACK)
        print("coada ACK")
        print(Thread_Trimitere_ACK.coada_ACK)
        # parcurg lista pentru care nu am trimis inapoi ACK
        # si daca primesc un pachet care se afla in aceasta lista, deblochez
        # procesul de trimitere a pachetelor






# TODO revezi partea aceasta de cod

