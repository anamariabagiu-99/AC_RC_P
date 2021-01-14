import Design as d
import text as t
import prelucrare_inf_int as p_i
from prelucrare_fisiere import *
from socket_utile_c import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class InterfataGrafica:
    port = [0, 0] # coada in care voi pune porturile introduse de utilizator
    def __init__(self):
        #creez fereastra
        self.i = Tk()
        #aleg designul pentru interfata
        self.design_win()
        #creez butoanele
        self.design_button()
        # eticheta titlul si subtitlul
        self.eticheta_titlu = Label(self.i, text=t.my_text.start, bg=d.Design.eticheta_titlu,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 50, 'bold')
                                    )
        self.eticheta_subtitlul = Label(self.i, text=t.my_text.t, bg=d.Design.eticheta_titlu,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 30, 'bold')
                                    )
        # eticheta port, in care voi afisa portul pe care comunic
        self.e_port_sursa = Label(self.i, text='Port sursa', bg=d.Design.culoarea_back,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 20, 'bold'))
        self.e_port_s =  Entry(self.i , bg=d.Design.culoarea_back,
                       fg=d.Design.culoare_scris,
                       font=('Arial', 20, 'bold')
                       )
        self.e_port_destinatie = Label(self.i, text='Port destinatie', bg=d.Design.culoarea_back,
                                  fg=d.Design.culoare_scris,
                                  font=('Arial', 20, 'bold'))
        self.e_port_d = Entry(self.i, bg=d.Design.culoarea_back,
                              fg=d.Design.culoare_scris,
                              font=('Arial', 20, 'bold')
                              )

        # butonul pentru rasfoire, alegerea fisierului ce va fi trimis
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
                                      fg='black',
                                      font=('Arial', 14, 'bold'))
        self.inchis = Radiobutton(self.i, text="Conexiune inchisa!", variable=self.var,
                                   value=2, bg=d.Design.culoarea_back,
                                   fg='black',
                                   font=('Arial', 14, 'bold'))
        # conexiunea este initial inchisa
        self.var.set(2)

        # creez casetele in care voi afisa informatiile despre pachete
        # inf fisiere deschise
        self.label_text_box = Label(self.i, text = 'Informatii fisiere deschise:', bg=d.Design.culoarea_back,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        self.label_text_inf = Label(self.i, text = 'Informatii ACK primite:', bg=d.Design.culoarea_back,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        # informatii ACK primite
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
        self.i.title("Emitator") # setez titlul
        self.i.geometry("800x800")   # setez dimenisiunea
        self.i.configure(bg=d.Design.culoarea_back) # setez culoare bck

    def plasare_gui(self):
        # plasez elementele create pe gui
        self.eticheta_titlu.place(x=100, y=10)
        self.eticheta_subtitlul.place(x=250, y=80)
        self.e_port_sursa.place(x=100, y=125)
        self.e_port_s.place(x=300, y=125)
        self.e_port_destinatie.place(x=100, y=175)
        self.e_port_d.place(x=300, y=175)
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

        #setez coordonatele
        self.start.place(x=100, y=740)
        self.stop.place(x=475, y=740)

    def call_start(self):
        self.var.set(1) # setez conex pe deschisa
        # scot valorile porturilor si le validez
        p1 = self.e_port_s.get()
        # validez
        if p_i.prelucrare_inf_int.validare_port(p1):
            # il transform in numar
            nr1 = p_i.prelucrare_inf_int.numar(p1)
            # il adaug in coada
            InterfataGrafica.port[0] = nr1
        else:
            self.e_port_s.delete(0, END)
            return
        # procedez la fel si pentru portul destinatie
        p2 = self.e_port_d.get()
        if p_i.prelucrare_inf_int.validare_port(p2):
            nr2 = p_i.prelucrare_inf_int.numar(p2)
            InterfataGrafica.port[1] = nr2
        else:
            self.e_port_d.delete(0, END)
            return

        Socket_Utile.initializare()

    def call_stop(self):
        self.var.set(2)
        s_u.Socket_Utile.UDPServerSocket.shutdown()

    def start_interface(self):
        # bucla pentru interfata
        # functia pentru primirea pachetelor este blocanta
        # si atunci aceasta trebuie apelata la inf

        self.i.mainloop()

    def browse(self, k, y):
        x = Button(self.i, text='Rasfoire',fg='black', bg='skyblue',
                   width=15, height=2, command=lambda: self.file_opener())
        x.place(x=k, y=y)
        return x

    def file_opener(self):
        # deschidere fisier din calea specificata de mine
        input = filedialog.askopenfile(initialdir="/home/ana/Desktop/Retele_de_calculatoare_Proiect/cod/fisiere/")
        # daca am selectat ceva
        if input:
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

