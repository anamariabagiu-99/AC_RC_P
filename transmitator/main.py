
from interfata_grafica import *
from prelucrare_fisiere import*
from socket_comunicare import *
from Thread_Prelucrare_ACK import *
from socket_utile_c import *

if __name__ == '__main__':
    # instantiez gui
    r = InterfataGrafica()
    # instantiez thread-urile
    t_trimitere = Thread_Trimitere()
    t_primire = Thread_Primire(r)
    t_prelucrare_ACK=Thread_Prelucrare_ACK()
    t_citire = Thread_Prelucrare()
    # le pornesc
    t_citire.start()
    t_trimitere.start()
    t_primire.start()
    t_prelucrare_ACK.start()

    #rulez bucla pentru gui
    r.start_interface()

    # dau join la threaduri
    t_citire.join()
    t_trimitere.join()
    t_primire.join()
    t_prelucrare_ACK.join()


    



