
from interfata_grafica import *
from prelucrare_fisiere import*
from socket_comunicare import *
from socket_utile_c import *

if __name__ == '__main__':
    t_citire=Thread_Prelucrare()
    t_comunicare = Thread_Comunicare()
    t_citire.start()
    t_comunicare.start()

    r=InterfataGrafica()
    r.start_interface()

    #citire(r.path)
    



