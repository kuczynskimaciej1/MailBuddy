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
        
        entry_frame = tk.Frame(self.root, bg="lightblue", relief=tk.RIDGE, borderwidth=2)
        
        entry_scrollbar = tk.Scrollbar(entry_frame)
        
        entry_text = tk.Text(entry_frame, bg="lightblue", fg="black", wrap=tk.WORD, yscrollcommand=entry_scrollbar.set)
        
        entry_scrollbar.config(command=entry_text.yview)

        # Miejsce na przyciski nawigacyjne
        navigation_frame = tk.Frame(self.root, bg="lightblue")
        navigation_frame.pack(side=tk.TOP, fill=tk.X)

        btn_importuj = tk.Button(navigation_frame, text="Importuj", bg="lightblue", fg="black")
        btn_importuj.pack(side=tk.LEFT, padx=5, pady=5)

        btn_eksportuj = tk.Button(navigation_frame, text="Eksportuj", bg="lightblue", fg="black")
        btn_eksportuj.pack(side=tk.LEFT, padx=5, pady=5)

        btn_zaladuj = tk.Button(navigation_frame, text="Załaduj", bg="lightblue", fg="black")
        btn_zaladuj.pack(side=tk.LEFT, padx=5, pady=5)

        btn_wyslij = tk.Button(navigation_frame, text="Wyślij", bg="lightblue", fg="black", command=lambda: self.wyslij_mail(self.entry_adres.get(), entry_text.get(1.0, tk.END)))
        btn_wyslij.pack(side=tk.LEFT, padx=5, pady=5)

        btn_usun = tk.Button(navigation_frame, text="Usuń", bg="lightblue", fg="black", command=lambda: self.usun_tekst(entry_text))
        btn_usun.pack(side=tk.LEFT, padx=5, pady=5)

        btn_zapisz = tk.Button(navigation_frame, text="Zapisz", bg="lightblue", fg="black", command=lambda: self.zapisz_grupy(), state=tk.DISABLED)
        btn_zapisz.pack(side=tk.LEFT, padx=5, pady=5)

        btn_grupy = tk.Button(navigation_frame, text="Grupy", bg="lightblue", fg="black", command=lambda: self.utworz_grupe())
        btn_grupy.pack(side=tk.LEFT, padx=5, pady=5)

        btn_szablony = tk.Button(navigation_frame, text="Templates", bg="lightblue", fg="black", command=lambda: self.show_template_window())
        btn_szablony.pack(side=tk.LEFT, padx=5, pady=5)

        # miejsce na powiadomienia
        notifications_frame = tk.Frame(self.root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
        notifications_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
        notifications_label = tk.Label(notifications_frame, text="Miejsce na powiadomienia", bg="lightblue")
        notifications_label.pack(fill=tk.BOTH, expand=True)

        # miejsce na grupy mailowe
        groups_frame = tk.Frame(self.root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
        groups_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)

        grupy_label = tk.Label(groups_frame, text="Grupy mailowe", bg="lightblue")
        grupy_label.pack()

        self.grupy_listbox = tk.Listbox(groups_frame, bg="lightblue", fg="black")
        self.grupy_listbox.pack(fill=tk.BOTH, expand=True)
        self.grupy_listbox.bind('<Double-Button-1>', lambda event: self.edytuj_grupe())

        # Miejsce na templaty szablony maili jak kto woli
        self.templates_frame = tk.Frame(self.root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
        self.templates_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)

        szablony_label = tk.Label(self.templates_frame, text="Szablony wiadomości", bg="lightblue")
        szablony_label.pack()

        self.szablony_listbox = tk.Listbox(self.templates_frame, bg="lightblue", fg="black")
        self.szablony_listbox.pack(fill=tk.BOTH, expand=True)

        # Pole do wprowadzania tekstu maila
        entry_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
        entry_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        entry_text.pack(fill=tk.BOTH, expand=True)

        entry_adres_label = tk.Label(entry_frame, text="Wyślij do:", bg="lightblue")
        entry_adres_label.pack(side=tk.TOP, padx=5, pady=5)

        entry_adres = tk.Entry(entry_frame, bg="white", fg="black")
        entry_adres.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.entry_adres = entry_adres  # Zapisujemy referencję do pola adresu, aby móc go użyć później

    def run(self):
        self.prepareInterface()
        self.root.mainloop()

    def show_template_window(self):
        template_window = tk.Toplevel(self.root)
        template_window.title("Stwórz szablon")
        
        name_label = tk.Label(template_window, text="Nazwa szablonu:", bg="lightblue")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        
        name_entry = tk.Entry(template_window, bg="white", fg="black")
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        template_text = tk.Text(template_window, bg="lightblue", fg="black", wrap=tk.WORD)
        template_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        btn_save = tk.Button(template_window, text="Zapisz", bg="lightblue", fg="black", command=lambda: self.save_template(name_entry.get(), template_text.get(1.0, tk.END)))
        btn_save.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        btn_insert_placeholder = tk.Button(template_window, text="Wstaw luke", bg="lightblue", fg="black", command=lambda: self.insert_placeholder(template_text))
        btn_insert_placeholder.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def save_template(self, template_name, template_content):
        # Tutaj możesz zapisać nazwę i zawartość szablonu, na przykład do pliku lub bazy danych
        print("Nazwa szablonu:", template_name)
        print("Zawartość szablonu:", template_content)

    def insert_placeholder(self, template_text):
        placeholder_text = "_____"
        
        template_text.insert(tk.INSERT, placeholder_text)
        
        template_text.tag_configure("placeholder", background="lightgreen")
        
        start_index = "1.0"
        while True:
            start_index = template_text.search(placeholder_text, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = template_text.index(f"{start_index}+{len(placeholder_text)}c")
            
            template_text.tag_add("placeholder", start_index, end_index)
            
            start_index = end_index

    def usun_tekst(self, entry_text):
        entry_text.delete(1.0, tk.END)

    def wyslij_mail(self, recipient, message):
        print("Sending email to:", recipient)
        print("Message content:", message)

    def utworz_grupe(self):
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

    def update_grupy(self):
        self.btn_zapisz.config(state=tk.NORMAL)
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

    def dodaj_szablon(self):
        tresc_szablonu = simpledialog.askstring("Nowy szablon", "Wpisz treść szablonu:")
        if tresc_szablonu:
            self.szablony.append(tresc_szablonu)

if __name__ == "__main__":
    app = AppUI()
    app.run()