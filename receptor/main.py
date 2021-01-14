from interfata_grafica import *
from socket_com import *
from prelucrare_date import *


def main():
    # instantiez gui

    r = InterfataGrafica()
    # creez thread-urile
    t_trimire_ACK = Thread_Trimitere_ACK(r)
    t_primire_date = Thread_Primire_Date(r)
    t_prelucrare = Thread_date()

    # dau drumul la thread-uri
    t_prelucrare.start()
    t_primire_date.start()
    t_trimire_ACK.start()

    # bucla pentru interfata grafica
    r.start_interface()

    # opresc threadurile
    t_prelucrare.join()

    t_trimire_ACK.join()

if __name__ == '__main__':
    main()
