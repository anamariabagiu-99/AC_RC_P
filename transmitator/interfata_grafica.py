import Design as d
import text as t

from prelucrare_fisiere import *
from socket_utile_c import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class InterfataGrafica:
    def __init__(self):
        #creez fereastra
        self.i = Tk()
        #aleg designul pentru interfata
        self.design_win()
        #creez butoanele
        self.design_button()
        # eticheta titlul
        self.eticheta_titlu = Label(self.i, text=t.my_text.start, bg=d.Design.eticheta_titlu,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 50, 'bold')
                                    )
        self.eticheta_subtitlul = Label(self.i, text=t.my_text.t, bg=d.Design.eticheta_titlu,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 30, 'bold')
                                    )
        # eticheta port
        self.e_port = Label(self.i, text='Port', bg=d.Design.culoarea_back,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 20, 'bold'))
        self.e_port_i = Label(self.i, text=Socket_Utile.localPort, bg=d.Design. culoare_port,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        # butonul pentru rasfoire
        self.fisier =  Label(self.i, text = 'Alegeti un fisier folosind butonul ', bg=d.Design.culoarea_back,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        self.browse_button = self.browse(500, 225)

        #butoanele de stop si start
        self.design_button()
        # un radiobutton care sa imi spuna cum este conexiunea cu socketul
        # inchisa sau deschisa
        self.var = IntVar() # variabila care o sa spuna cum este conexiunea
        self.deschis = Radiobutton(self.i, text="Conexiune deschisa!", variable=self.var,
                                      value=1, bg=d.Design.culoarea_back,
                                      fg=d.Design.culoare_scris,
                                      font=('Arial', 14, 'bold'))
        self.inchis = Radiobutton(self.i, text="Conexiune inchisa!", variable=self.var,
                                   value=2, bg=d.Design.culoarea_back,
                                   fg=d.Design.culoare_scris,
                                   font=('Arial', 14, 'bold'))
        # conexiunea este initial inchisa
        self.var.set(2)

        # creez casetele in care voi afisa informatiile despre pachete
        self.label_text_box = Label(self.i, text = 'Informatii fisiere deschise:', bg=d.Design.culoarea_back,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        self.label_text_inf = Label(self.i, text = 'Informatii ACK primite:', bg=d.Design.culoarea_back,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        self.text_box = Text(self.i, bg=d.Design.culoare_inf,
                            fg=d.Design.culoare_scris_inf,
                            font=('Arial', 15, 'bold'),
                             width=30, height=15)
        self.text_inf = Text(self.i, bg=d.Design.culoare_inf,
                            fg=d.Design.culoare_scris_inf,
                            font=('Arial', 15, 'bold'),
                             width=30, height=15)
        # creez meniu
        self.meniu = Menu(self.i)
        self.filemenu = Menu(self.meniu)
        self.filemenu.add_command(label='Despre', command=self.meniu_about)
        self.filemenu.add_command(label='Ajutor', command=self.meniu_help)
        self.meniu.add_cascade(label="Meniu", menu=self.filemenu)
        self.meniu.config(bg=d.Design.back_meniu)
        self.i.config(menu=self.meniu)

        # plasez elementele pe gui
        self.plasare_gui()
        # contor pentru numarul de fisiere deschise
        self.contor = 0


    def design_win(self):
        # setez titlul
        self.i.title("Emitator")
        # setez dimenisiunea
        self.i.geometry("800x800")
        # setez culoare bck
        self.i.configure(bg=d.Design.culoarea_back)

    def plasare_gui(self):
        # plasez elementele create pe gui
        self.eticheta_titlu.place(x=100, y=10)
        self.eticheta_subtitlul.place(x=250, y=100)
        self.e_port.place(x=100, y=175)
        self.e_port_i.place(x=200, y=175)
        self.fisier.place(x=75, y=225)
        self.deschis.place(x=100, y=700)
        self.inchis.place(x=475, y=700)
        self.label_text_box.place(x=50, y=275)
        self.text_box.place(x=50, y=310)
        self.label_text_inf.place(x=425, y=275)
        self.text_inf.place(x = 425, y = 310)

    def design_button(self):
        # butonul de start, am o comanda pentru a incepe transmiterea
        self.start = Button(self.i, text='Deschire conexiune', fg=d.Design.culoare_scris,
                            bg=d.Design.culoare_butoane, width=20, height=2,
                            command=self.call_start)

        # butonul pentru inchiderea interfetei
        self.stop = Button(self.i, text='Inchidere conexiune',
                          fg=d.Design.culoare_scris, bg=d.Design.culoare_butoane,
                           width=20, height=2,command=self.call_stop)
        # TODO de verificat daca nu exista ceva pentru inchiderea conexiunii

        #setez coordonatele
        self.start.place(x=100, y=740)
        self.stop.place(x=475, y=740)

    def call_start(self):
        self.var.set(1)
        Socket_Utile.initializare()

    def call_stop(self):
        self.var.set(2)
        s_u.Socket_Utile.UDPServerSocket.shutdown()

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
        input = filedialog.askopenfile(initialdir="/home/ana/Desktop/Retele_de_calculatoare_Proiect/cod/fisiere/")
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

    # functiile pentru update ale casetelor text
    def update_label_open_file(self, text):
        self.text_box.insert(END, 'Fisier deschis: \t'+text+'\n')

    def update_label_ACK(self, nr):
        self.text_inf.insert(END, 'ACK <-'+nr+'\n')

    # functii pentru afisarea de inf din meniu
    def meniu_help(self):
        messagebox.showinfo(title="Ajutor", message=t.my_text.help)

    def meniu_about(self):
        messagebox.showinfo(title="Despre", message=t.my_text.despre)

