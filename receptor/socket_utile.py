
import socket
import interfata_grafica as i_g
import socket_com as s_c

class Socket_Utile:
    localIP = "127.0.0.1"
    localPort = 20001
    bufferSize = 1024
    UDPServerSocket = None
    flag = False

    @staticmethod
    def initializare():
        # anunt threadurile ca pot sa isi inceapa treaba
        # sa nu apasa de mai multe ori pe start
        if Socket_Utile.flag == True:
            exit
        # setez flagul
        Socket_Utile.flag=True
        # realizez conexiunea pe socket
        Socket_Utile.UDPServerSocket = socket.socket(family=socket.AF_INET,
                                                     type=socket.SOCK_DGRAM)
        # fac bind
        s = i_g.InterfataGrafica.port[0]
        # 1089
        Socket_Utile.UDPServerSocket.bind((Socket_Utile.localIP, s))

        # dau drumul la threadul de primire a datelor
        s_c.Thread_Primire_Date.stare_primire_date.acquire()
        s_c.Thread_Primire_Date.stare_primire_date.notify()
        s_c.Thread_Primire_Date.stare_primire_date.release()

        # dau lock si pentru threadul de trimitere
        s_c.Thread_Trimitere_ACK.stare_ACK.acquire()
        s_c.Thread_Trimitere_ACK.stare_ACK.notify()
        s_c.Thread_Trimitere_ACK.stare_ACK.release()



