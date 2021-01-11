from tkinter import *
from tkinter import messagebox

import Design as d
import prelucrare_interfata as p_i
import socket_com as s_c
import socket_utile as s_u
import text as t


class InterfataGrafica:
    probabilitatea = [] # prob va fi citita din interfata grafica
    port = [0, 0] # portul va fi introdus de utilizator
    def __init__(self):
        #creez fereastra
        self.i = Tk()
        #aleg designul pentru interfata
        self.design_win()
        # eticheta titlul
        self.eticheta_titlu = Label(self.i, text=t.my_text.start, bg=d.Design.eticheta_titlu,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 50, 'bold')
                                    )
        # eticheta subtitulul
        self.eticheta_subtitlul = Label(self.i, text=t.my_text.t, bg=d.Design.eticheta_titlu,
                                        fg=d.Design.culoare_scris,
                                        font=('Arial', 30, 'bold')
                                        )
        # eticheta port
        self.e_port_sursa = Label(self.i, text='Port sursa', bg=d.Design.culoarea_back,
                                  fg=d.Design.culoare_scris,
                                  font=('Arial', 20, 'bold'))
        self.e_port_s = Entry(self.i, bg=d.Design.culoarea_back,
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
        # pentru prob la care se pierd pachetele
        self.label_p =  Label(self.i, text='Introduceti probabilitatea de forma a/b', bg=d.Design.culoarea_back,
                            fg=d.Design.culoare_scris,
                            font=('Arial', 20, 'bold'))
        self.p = Entry(self.i , bg=d.Design.culoarea_back,
                       fg=d.Design.culoare_scris,
                       font=('Arial', 20, 'bold')
                       )
        #creez butoanele
        self.design_button()
        # un radiobutton care sa imi spuna cum este conexiunea cu socketul
        # inchisa sau deschisa
        self.var = IntVar()  # variabila care o sa spuna cum este conexiunea
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
        # casetele text pentru afisarea inf despre pachete
        self.label_text_box = Label(self.i, text='Informatii pachete primite:', bg=d.Design.culoarea_back,
                                    fg=d.Design.culoare_scris,
                                    font=('Arial', 20, 'bold'))
        self.label_text_inf = Label(self.i, text='Informatii ACK trimise:', bg=d.Design.culoarea_back,
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
        self.plasare_gui()

    def design_win(self):
        # setez titlul
        self.i.title("Receptor")
        # setez dimenisiunea
        self.i.geometry("800x800")
        # setez culoare bck
        self.i.configure(bg=d.Design.culoarea_back)

    def plasare_gui(self):
        # fct pentru plasarea pe gui
        self.eticheta_titlu.place(x=100, y=10)
        self.eticheta_subtitlul.place(x=250, y=80)
        self.e_port_sursa.place(x=100, y=125)
        self.e_port_s.place(x=300, y=125)
        self.e_port_destinatie.place(x=100, y=175)
        self.e_port_d.place(x=300, y=175)
        self.label_p.place(x=30, y=225)
        self.p.place(x=525, y=225)
        self.deschis.place(x=100, y=700)
        self.inchis.place(x=475, y=700)
        self.label_text_box.place(x=50, y=275)
        self.text_box.place(x=50, y=310)
        self.label_text_inf.place(x=425, y=275)
        self.text_inf.place(x=425, y=310)

    def design_button(self):
        #butonul de start
        # trebuie sa adaug o comanda pentru a incepe transmiterea
        self.start = Button(self.i, text='Deschire conexiune', fg=d.Design.culoare_scris,
                            bg=d.Design.culoare_butoane, width=20, height=2,
                            command=self.partea_de_start)

        #butonul pentru inchiderea interfetei
        self.stop = Button(self.i, text='Inchidere conexiune',
                          fg=d.Design.culoare_scris, bg=d.Design.culoare_butoane,
                           width=20, height=2,command=self.call_stop)

        #setez coordonatele
        self.start.place(x=100, y=740)
        self.stop.place(x=475, y=740)

    def start_interface(self):
        #bucla pentru interfata
        self.i.mainloop()


    #functiile pentru update ale casetelor text
    def update_label_packet(self, text):
        self.text_box.insert(END, 'Pachet <-'+text+'\n')

    def update_label_ACK(self, nr):
        self.text_inf.insert(END, 'ACK -> '+nr+'\n')

    # fct de callback a butonului de start
    def partea_de_start(self):
        # scot de pe interfata probabilitatea
        sir = self.p.get()
        # validez probabilitatea introdusa de utilizator
        if not (p_i.prelucrare_inf_int.prelucrare_prob(sir)):
            self.p.delete(0, END)
            return
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

     # pun numarul portului in coada cores
        self.var.set(1) # setez conexiunea ca fiind deschisa
        # creez legatura cu socketul
        s_u.Socket_Utile.initializare()

    def call_stop(self):
        # fct de callback a butonului de stop
        # setez valoarea butonului radio ca fiind inchis
        self.var.set(2)


# functii pentru afisarea de inf din meniu
    def meniu_help(self):
        messagebox.showinfo(title="Ajutor", message=t.my_text.help)

    def meniu_about(self):
        messagebox.showinfo(title="Despre", message=t.my_text.despre)



