from collections.abc import Iterable
import tkinter as tk
from tkinter import simpledialog

class AppUI():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.grupy = {}
        self.szablony = []

    def prepareInterface(self) -> None:
        self.root.title("MailBuddy")
        self.root.configure(bg="black")
        self.root.minsize(width=800, height=470)
        
        self.__create_navigation()
        self.__create_notification_pane()
        self.__create_mailing_group_pane()
        self.__create_template_pane()
        self.__create_mail_input_pane()

    def run(self):
        self.root.mainloop()

    def add_template(self, content: str | Iterable[str]):
        if isinstance(content, str):
            self.szablony.append(content)
        else:
            [self.szablony.append(i) for i in content]
        self.__update_listbox(self.template_listbox, self.szablony)
        
    
    # def usun_tekst(entry_text: tk.Text):
    #     entry_text.delete(1.0, tk.END)

    def __send_clicked() -> None:
        print("send mail")
        pass

    def __add_group_clicked(self):
        nazwa_grupy = simpledialog.askstring("Nazwa grupy", "Wpisz nazwę grupy:")
        if nazwa_grupy:
            adresy_email = simpledialog.askstring("Adresy email", "Wpisz adresy email oddzielone przecinkami:")
            if adresy_email:
                self.grupy[nazwa_grupy] = adresy_email.split(',')
                self.update_grupy()

    def zapisz_grupy(self):
        with open("grupy.txt", "w") as f:
            for grupa, adresy in self.grupy.items():
                f.write(grupa + ':' + ','.join(adresy) + '\n')

    def update_grupy(self, btn_zapisz):
        btn_zapisz.config(state=tk.NORMAL)
        self.grupy_listbox.delete(0, tk.END)
        for grupa in self.grupy.keys():
            self.grupy_listbox.insert(tk.END, grupa)

    def edytuj_grupe(self):
        if self.grupy_listbox.curselection():
            indeks = self.grupy_listbox.curselection()[0]
            nazwa_grupy = self.grupy_listbox.get(indeks)
            adresy = ','.join(self.grupy[nazwa_grupy])
            nowe_adresy = simpledialog.askstring("Edytuj grupę", "Wpisz nowe adresy email oddzielone przecinkami:", initialvalue=adresy)
            if nowe_adresy:
                self.grupy[nazwa_grupy] = nowe_adresy.split(',')
                self.update_grupy()
              
    @staticmethod
    def __update_listbox(lb: tk.Listbox, content: Iterable[str]):
        lb.delete(0, tk.END)
        [lb.insert(tk.END, i) for i in content]

    def __add_template_clicked(self):
        tresc_szablonu = simpledialog.askstring("Nowy szablon", "Wpisz treść szablonu:")
        if tresc_szablonu:
            self.add_template(tresc_szablonu)
    
        
    def __create_navigation(self):
        navigation_frame = tk.Frame(self.root, bg="lightblue")
        btn_importuj = tk.Button(navigation_frame, text="Importuj", bg="lightblue", fg="black")        
        btn_eksportuj = tk.Button(navigation_frame, text="Eksportuj", bg="lightblue", fg="black")
        btn_zaladuj = tk.Button(navigation_frame, text="Załaduj", bg="lightblue", fg="black")
        btn_wyslij = tk.Button(navigation_frame, text="Wyślij", bg="lightblue", fg="black", 
                               command=lambda: self.__send_clicked()
                               )
        btn_usun = tk.Button(navigation_frame, text="Usuń", bg="lightblue", fg="black", 
                             #command=lambda: self.usun_tekst(entry_text)
                             )
        btn_zapisz = tk.Button(navigation_frame, text="Zapisz", bg="lightblue", fg="black", 
                               command=lambda: self.zapisz_grupy(btn_zapisz), state=tk.DISABLED)
        btn_grupy = tk.Button(navigation_frame, text="Grupy", bg="lightblue", fg="black", 
                              command=lambda: self.__add_group_clicked())
        btn_szablony = tk.Button(navigation_frame, text="Templates", bg="lightblue", fg="black", 
                                 command=lambda: self.__add_template_clicked())
        
        navigation_frame.pack(side=tk.TOP, fill=tk.X)
        btn_importuj.pack(side=tk.LEFT, padx=5, pady=5)
        btn_eksportuj.pack(side=tk.LEFT, padx=5, pady=5)
        btn_zaladuj.pack(side=tk.LEFT, padx=5, pady=5)
        btn_wyslij.pack(side=tk.LEFT, padx=5, pady=5)
        btn_usun.pack(side=tk.LEFT, padx=5, pady=5)
        btn_zapisz.pack(side=tk.LEFT, padx=5, pady=5)
        btn_grupy.pack(side=tk.LEFT, padx=5, pady=5)
        btn_szablony.pack(side=tk.LEFT, padx=5, pady=5)
    
    def __create_notification_pane(self):
        notifications_frame = tk.Frame(self.root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
        notifications_label = tk.Label(notifications_frame, text="Miejsce na powiadomienia", bg="lightblue")
        
        notifications_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
        notifications_label.pack(fill=tk.BOTH, expand=True)

    def __create_mailing_group_pane(self):
        groups_frame = tk.Frame(self.root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
        grupy_label = tk.Label(groups_frame, text="Grupy mailowe", bg="lightblue")
        grupy_listbox = tk.Listbox(groups_frame, bg="lightblue", fg="black")
        
        groups_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
        grupy_label.pack()
        grupy_listbox.pack(fill=tk.BOTH, expand=True)
        grupy_listbox.bind('<Double-Button-1>', lambda event: self.edytuj_grupe())

    def __create_template_pane(self):
        templates_frame = tk.Frame(self.root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
        szablony_label = tk.Label(templates_frame, text="Szablony wiadomości", bg="lightblue")
        self.template_listbox = tk.Listbox(templates_frame, bg="lightblue", fg="black")
        
        templates_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
        szablony_label.pack()
        self.template_listbox.pack(fill=tk.BOTH, expand=True)

    def __create_mail_input_pane(self):
        entry_frame = tk.Frame(self.root, bg="lightblue", relief=tk.RIDGE, borderwidth=2)
        entry_scrollbar = tk.Scrollbar(entry_frame)
        self.entry_text = tk.Text(entry_frame, bg="lightblue", fg="black", wrap=tk.WORD, yscrollcommand=entry_scrollbar.set)
        entry_scrollbar.config(command=self.entry_text.yview)
        entry_adres_label = tk.Label(entry_frame, text="Wyślij do:", bg="lightblue", anchor="s")
        entry_adres = tk.Entry(entry_frame, bg="white", fg="black")
        
        entry_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
        entry_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_text.pack(fill=tk.BOTH, expand=True)
        entry_adres_label.pack(side=tk.TOP, padx=5, pady=5)
        entry_adres.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

