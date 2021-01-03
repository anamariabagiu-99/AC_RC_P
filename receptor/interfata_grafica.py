from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import socket_utile as s_u

class InterfataGrafica:
    probabilitatea = []
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

        #etchetele
        self.label_text_box=self.create_label("Informatii pachete primite", 50,270 )
        self.label_text_inf=self.create_label("Informatii ACK trimise", 500, 270)

        #eticheta port
        self.label_port=self.create_label("Port", 10, 40)
        self.port=Label(self.i,text="text", bg='orchid', font=('verdana', 15) ).place(x=65, y=40)

        # pentru prob la care se pierd pachetele
        self.label_p = self.create_label("Introduceti probabilitatea de forma a/b",
                         50, 150)
        self.p = Entry(self.i)
        self.p.place(x=450, y=150)

    def design_win(self):

        # setez titlul
        self.i.title("Receiver")
        # setez dimenisiunea
        self.i.geometry("900x900")
        # setez culoare bck
        self.i.configure(bg="lavenderblush")

    def design_button(self):
        #butonul de start
        # trebuie sa adaug o comanda pentru a incepe transmiterea
        self.start = Button(self.i, text='Start', fg='black', bg='plum', width=15, height=2,
                            command=self.partea_de_start)

        #butonul pentru inchiderea interfetei
        self.stop = Button(self.i, text='Stop', fg='black', bg='plum',
                           width=15, height=2, command=self.i.destroy)

        #setez coordonatele
        self.start.place(x=250, y=840)
        self.stop.place(x=500, y=840)

    def start_interface(self):
        #bucla pentru interfata
        self.i.mainloop()



    def text_box_create(self, x, y):
        #creez caseta text
        text_box=Text(self.i, width=50, height=30, bg='thistle')
        text_box.place(x=x, y=y)
        return text_box



    def create_label(self, text, x, y):
        #creez etichete
        l1=Label(self.i, text=text, bg='lavenderblush', font=('verdana', 15) )
        l1.place(x=x, y=y)
        return l1

    #functiile pentru update ale casetelor text
    def update_label_packet(self, text):
        self.text_box.insert(END, 'Am primit pachetul \t'+text+'\n\n')


    def update_label_ACK(self, nr):
        self.text_inf.insert(END, '\n\n Am trimis ACK pentru pachetul \t'+nr)


    def partea_de_start(self):
        # scot de pe interfata probabilitatea
        sir=self.p.get()
        # verfic ca acesta are forma pe care o vreau
        if not(sir[0]>='0 ' and sir[0]<='9' and sir[1]=='/' and sir[2]>='0' and sir[2]<='9'):
            messagebox.showinfo('Eroare', 'Probabilitatea trebuie sa aiba forma a/b.')
            self.p.delete(0, END)
            return
        # verific ca probabilitatea sa fie subunitara
        if not(sir[0]< sir[2]):
            messagebox.showinfo('Eroare', 'Probabilitatea trebuie sa fie subunitara!\n'
                                          'a < b')
            self.p.delete(0, END)
            return
        # daca am trecut de partea de validare, calculez probabilitatea
        InterfataGrafica.probabilitatea.insert(0, int(sir[0])/int(sir[2]))
        #InterfataGrafica.probabilitatea.insert()
        print('din interfata '+str(InterfataGrafica.probabilitatea[0]))
        # creez legatura cu socketul
        s_u.Socket_Utile.initializare()


