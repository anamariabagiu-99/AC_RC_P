
from interfata_grafica import *
from prelucrare_fisiere import*
from socket_comunicare import *
from socket_utile_c import *

if __name__ == '__main__':
    r = InterfataGrafica()

    t_citire = Thread_Prelucrare()
    t_trimitere = Thread_Trimitere()
    t_primire = Thread_Primire(r)
    t_citire.start()
    t_trimitere.start()
    t_primire.start()

    r.start_interface()

    t_citire.join()
    t_trimitere.join()
    t_primire.join()


    



