import socket_comunicare as s_c
import prelucrare_fisiere as p_f

class Tahoe_Algoritm:
    prag = 30
    cwnd=1
    coada_pachete_neconfirmate=[]
    timp_asteptare=15
    stop_Thread=False
    coada_pachete_retransmise=[]
    coada_ut_conf = ['1']

    @staticmethod
    def slow_start():
        # daca nu am atins pragul cresc exp
        if Tahoe_Algoritm.cwnd < Tahoe_Algoritm.prag:
            Tahoe_Algoritm.cwnd = Tahoe_Algoritm.cwnd * 2
        else:
            # am depasit pragul cresc liniar
            Tahoe_Algoritm.cwnd = Tahoe_Algoritm.cwnd + 1

    @staticmethod
    def trimiterea_rapida():
        print('Am intrat in trimitere')
        print('timp_asteptare='+str(s_c.Thread_Primire.timp_asteptare[0]))
        print(s_c.Thread_Primire.ultima_ACK)
        # verfic conditiile pentru existenta congestie
        if (s_c.Thread_Primire.timp_asteptare[0]> Tahoe_Algoritm.timp_asteptare) or (s_c.Thread_Primire.ultima_ACK[0] == 3):
            # am detectat congestia
            # modific timpul de asteptare
            print('Am intrat in if')
            s_c.Thread_Primire.timp_asteptare.insert(0, 0)
            # modific pragul
            # verfic daca cwnd>1
            if( Tahoe_Algoritm.cwnd > 1 ):
                Tahoe_Algoritm.prag = Tahoe_Algoritm.cwnd / 2
            # modific dimensiunea ferestrei de congestie
            Tahoe_Algoritm.cwnd = 1
            print("Tahoe_Algoritm.cwnd "+ str(Tahoe_Algoritm.cwnd))
            print("Tahoe_Algoritm.prag " + str(Tahoe_Algoritm.prag))

            # Tahoe_Algoritm.coada_pachete_retransmise = Tahoe_Algoritm.coada_pachete_retransmise + Tahoe_Algoritm.coada_ut_conf
            if(len(Tahoe_Algoritm.coada_pachete_neconfirmate) == 1):
                k = Tahoe_Algoritm.coada_pachete_neconfirmate.pop(0)
                Tahoe_Algoritm.coada_pachete_retransmise.append(k)

            if(len(Tahoe_Algoritm.coada_pachete_neconfirmate)):
                for x in (0, len(Tahoe_Algoritm.coada_pachete_neconfirmate)):
                    k=Tahoe_Algoritm.coada_pachete_neconfirmate.pop(0)
                    Tahoe_Algoritm.coada_pachete_retransmise.append(k)

            Tahoe_Algoritm.coada_pachete_neconfirmate = []
            Tahoe_Algoritm.stop_Thread = True
            # resetez datele din coada
            s_c.Thread_Primire.ultima_ACK[0] = 0
            s_c.Thread_Primire.ultima_ACK[1] = ' '
            print('retransmisie')
            print(Tahoe_Algoritm.coada_pachete_retransmise)
            print(Tahoe_Algoritm.cwnd)
            #print(s_c.Thread_Primire.ultima_ACK)
            return True

        # in cazul in care nu am detectat congestia
        Tahoe_Algoritm.stop_Thread = False
        return False



