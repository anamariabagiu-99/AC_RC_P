from prelucrare_fisiere import *
from socket_utile_c import *
from threading import Condition
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket_comunicare as s_c


class InterfataGrafica:
    def __init__(self):
        #creez fereastra
        self.i = Tk()

        #aleg designul pentru interfata
        self.design_win()

        #creez butoanele
        self.design_button()

        #casetele text
        self.text_box=self.text_box_create(30, 300)
        self.text_inf=self.text_box_create(480, 300)

        #etichetele
        self.label_text_box=self.create_label("Informatii fisiere deschise", 50,270 )
        self.label_text_inf=self.create_label("Informatii ACK primite", 500, 270)

        #eticheta port
        self.label_port=self.create_label("Port", 10, 40)
        self.port=Label(self.i,text="text", bg='steelblue', font=('verdana', 15) ).place(x=65, y=40)

        #butonul de broswe
        self.label_file = self.create_label("Pentru a alege fisierul folositi bu"
                                            "tonul", 50, 150)
        self.browse_button=self.browse(500, 150)
        # il folosesc pentru a scoate calea spre fisiere
        self.cale= ""

        # folosesc o variabile contor in care sa retin nr de fisiere deschise
        self.contor=0




    def design_win(self):
        # setez titlul
        self.i.title("Sender")
        # setez dimenisiunea
        self.i.geometry("900x900")
        # setez culoare bck
        self.i.configure(bg="lightseagreen")

    def design_button(self):
        # butonul de start, am o comanda pentru a incepe transmiterea
        self.start = Button(self.i, text='Start', fg='black', bg='cornflowerblue', width=15, height=2,
                            command=Socket_Utile.initializare)

        # butonul pentru inchiderea interfetei
        self.stop = Button(self.i, text='Stop', fg='black', bg='cornflowerblue', width=15, height=2, command=self.i.destroy)

        #setez coordonatele
        self.start.place(x=250, y=840)
        self.stop.place(x=500, y=840)

    def start_interface(self):
        # bucla pentru interfata
        if(s_u.Socket_Utile.flag ):
            s_c.receive_fct()
        self.i.mainloop()


    def browse(self, k, y):
        x = Button(self.i, text='Rasfoire',fg='black', bg='cyan',
                   width=15, height=2, command=lambda: self.file_opener())
        x.place(x=k, y=y)
        return x

    def file_opener(self):
        # deschidere fisier
        input = filedialog.askopenfile(initialdir=".")
        # salvez calea fisierului
        self.cale=input.name
        # acord lock
        Thread_Prelucrare.stare_citire.acquire()
        # pun in coada calea fisierului
        Thread_Prelucrare.coada_fisiere.append(input.name)
        # notific thread-ul pentru prelucrarea fisierului
        Thread_Prelucrare.stare_citire.notify()
        # eliberez lock
        Thread_Prelucrare.stare_citire.release()
        # incrementez numarul de fisiere deschise
        self.contor=self.contor+1

        # daca deschid mai mult de 3  fisiere si nu am facut conexiunea
        # cu socket-ul dau un mesaj de eroare
        if(Socket_Utile.flag == False and self.contor>=3):
            messagebox.showinfo(title="Start", message="Apasati START pentru "
                                                       "a deschide conexiunea cu socketul")

        # cand deschid un fisier fac update la inf de pe caseta text
        self.update_label_open_file(input.name)


    def text_box_create(self, x, y):
        #creez caseta text
        text_box=Text(self.i, width=50, height=30, bg='lightskyblue')
        text_box.place(x=x, y=y)
        return text_box



    def create_label(self, text, x, y):
        #creez etichete
        l1=Label(self.i, text=text, bg='lightseagreen', font=('verdana', 15) )
        l1.place(x=x, y=y)
        return l1

    # functiile pentru update ale casetelor text
    def update_label_open_file(self, text):
        self.text_box.insert(END, 'Am deschis fisierul \t'+text+'\n\n')

    def update_label_ACK(self, nr):
        self.text_inf.insert(END, '\n\n Am primit ACK pentru pachetul \t'+nr)

    def stop_button(self):
        s_u.Socket_Utile.UDPServerSocket.shutdown()

