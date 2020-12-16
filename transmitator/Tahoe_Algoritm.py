

class Tahoe_Algoritm:
    '''def __init__(self, x, y):
        self.prag=x # dimenisiunea maxima pana la care
                    # creste cwnd
        self.cwnd=0 # nu am trimis inca niciun pachet
        # pachetele trimise dar care inca nu au primit confirmare
        self.coada_pachete_neconfirmate=[]'''
    prag=10
    cwnd=1
    coada_pachete_neconfirmate=[]
    @staticmethod
    def slow_start():
        # daca nu am atins pragul cresc exp
        if Tahoe_Algoritm.cwnd <  Tahoe_Algoritm.prag:
            Tahoe_Algoritm.cwnd = Tahoe_Algoritm.cwnd * 2
        else:
            # am depasit pragul cresc liniar
            Tahoe_Algoritm.cwnd = Tahoe_Algoritm.cwnd + 1