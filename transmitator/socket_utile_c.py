import socket
import socket_comunicare as s_c

class Socket_Utile:
    localIP = "127.0.0.1"
    localPort = 20001
    bufferSize = 1024 # dimensiune port
    UDPServerSocket = None
    flag = False # flag care imi spune daca conexiunea la socket
                # a fost realizata sau nu

    @staticmethod
    def initializare():
        #verific sa nu fie apasat de mai multe ori butonul de Start
        if(Socket_Utile.flag == True):
            # daca se intampla asta, ies din functie
            exit
        # am modificat starea flag-ului
        Socket_Utile.flag = True
        # creez socket-ul

        Socket_Utile.UDPServerSocket = socket.socket(family=socket.AF_INET,
                                        type=socket.SOCK_DGRAM)
        # fac bind
        Socket_Utile.UDPServerSocket.bind((Socket_Utile.localIP, Socket_Utile.localPort))

        #  anunt thread-ul de primire ca poate sa isi inceapa treaba
        s_c.Thread_Primire.stare_primire.acquire()
        s_c.Thread_Primire.stare_primire.notify()
        s_c.Thread_Primire.stare_primire.release()

        #  anunt thread-ul de trimitere ca poate sa isi inceapa treaba
        s_c.Thread_Trimitere.stare_trimitere.acquire()
        s_c.Thread_Trimitere.stare_trimitere.notify()
        # eliberare lock
        s_c.Thread_Trimitere.stare_trimitere.release()



