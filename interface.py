import tkinter as tk
from tkinter import simpledialog

def usun_tekst():
    entry_text.delete(1.0, tk.END)

def wyslij_mail():
    recipient = entry_adres.get()
    message = entry_text.get(1.0, tk.END)  
    print("Sending email to:", recipient)
    print("Message content:", message)

def utworz_grupe():
    nazwa_grupy = simpledialog.askstring("Nazwa grupy", "Wpisz nazwę grupy:")
    if nazwa_grupy:
        adresy_email = simpledialog.askstring("Adresy email", "Wpisz adresy email oddzielone przecinkami:")
        if adresy_email:
            grupy[nazwa_grupy] = adresy_email.split(',')
            update_grupy()

def zapisz_grupy():
    with open("grupy.txt", "w") as f:
        for grupa, adresy in grupy.items():
            f.write(grupa + ':' + ','.join(adresy) + '\n')

def update_grupy():
    btn_zapisz.config(state=tk.NORMAL)
    grupy_listbox.delete(0, tk.END)
    for grupa in grupy.keys():
        grupy_listbox.insert(tk.END, grupa)

def edytuj_grupe():
    if grupy_listbox.curselection():
        indeks = grupy_listbox.curselection()[0]
        nazwa_grupy = grupy_listbox.get(indeks)
        adresy = ','.join(grupy[nazwa_grupy])
        nowe_adresy = simpledialog.askstring("Edytuj grupę", "Wpisz nowe adresy email oddzielone przecinkami:", initialvalue=adresy)
        if nowe_adresy:
            grupy[nazwa_grupy] = nowe_adresy.split(',')
            update_grupy()

def dodaj_szablon():
    tresc_szablonu = simpledialog.askstring("Nowy szablon", "Wpisz treść szablonu:")
    if tresc_szablonu:
        szablony.append(tresc_szablonu)
        ()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MailBuddy")
    root.configure(bg="black")

    # Inicjalizacja słowników i list
    grupy = {}
    szablony = []

    "Miejsce na przyciski nawigacyjne"
    navigation_frame = tk.Frame(root, bg="lightblue")
    navigation_frame.pack(side=tk.TOP, fill=tk.X)

    btn_importuj = tk.Button(navigation_frame, text="Importuj", bg="lightblue", fg="black")
    btn_importuj.pack(side=tk.LEFT, padx=5, pady=5)

    btn_eksportuj = tk.Button(navigation_frame, text="Eksportuj", bg="lightblue", fg="black")
    btn_eksportuj.pack(side=tk.LEFT, padx=5, pady=5)

    btn_zaladuj = tk.Button(navigation_frame, text="Załaduj", bg="lightblue", fg="black")
    btn_zaladuj.pack(side=tk.LEFT, padx=5, pady=5)

    btn_wyslij = tk.Button(navigation_frame, text="Wyślij", bg="lightblue", fg="black", command=wyslij_mail)
    btn_wyslij.pack(side=tk.LEFT, padx=5, pady=5)

    btn_usun = tk.Button(navigation_frame, text="Usuń", bg="lightblue", fg="black", command=usun_tekst)
    btn_usun.pack(side=tk.LEFT, padx=5, pady=5)

    btn_zapisz = tk.Button(navigation_frame, text="Zapisz", bg="lightblue", fg="black", command=zapisz_grupy, state=tk.DISABLED)
    btn_zapisz.pack(side=tk.LEFT, padx=5, pady=5)

    btn_grupy = tk.Button(navigation_frame, text="Grupy", bg="lightblue", fg="black", command=utworz_grupe)
    btn_grupy.pack(side=tk.LEFT, padx=5, pady=5)

    btn_szablony = tk.Button(navigation_frame, text="Templates", bg="lightblue", fg="black", command=dodaj_szablon)
    btn_szablony.pack(side=tk.LEFT, padx=5, pady=5)

    "miejsce na powiadomienia"
    notifications_frame = tk.Frame(root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
    notifications_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
    notifications_label = tk.Label(notifications_frame, text="Miejsce na powiadomienia", bg="lightblue")
    notifications_label.pack(fill=tk.BOTH, expand=True)

    "miejsce na grupy mailowe"
    groups_frame = tk.Frame(root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
    groups_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)

    grupy_label = tk.Label(groups_frame, text="Grupy mailowe", bg="lightblue")
    grupy_label.pack()

    grupy_listbox = tk.Listbox(groups_frame, bg="lightblue", fg="black")
    grupy_listbox.pack(fill=tk.BOTH, expand=True)
    grupy_listbox.bind('<Double-Button-1>', lambda event: edytuj_grupe())

    "Miejsce na templaty szablony maili jak kto woli "
    templates_frame = tk.Frame(root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
    templates_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)

    szablony_label = tk.Label(templates_frame, text="Szablony wiadomości", bg="lightblue")
    szablony_label.pack()

    szablony_listbox = tk.Listbox(templates_frame, bg="lightblue", fg="black")
    szablony_listbox.pack(fill=tk.BOTH, expand=True)

    "Pole do wprowadzania tekstu maila"
    entry_frame = tk.Frame(root, bg="lightblue", relief=tk.RIDGE, borderwidth=2)
    entry_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)

    entry_scrollbar = tk.Scrollbar(entry_frame)
    entry_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    entry_adres_label = tk.Label(entry_frame, text="Wyślij do:", bg="lightblue")
    entry_adres_label.pack(side=tk.TOP, padx=5, pady=5)

    entry_adres = tk.Entry(entry_frame, bg="white", fg="black")
    entry_adres.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    entry_text = tk.Text(entry_frame, bg="lightblue", fg="black", wrap=tk.WORD, yscrollcommand=entry_scrollbar.set)
    entry_text.pack(fill=tk.BOTH, expand=True)

    entry_scrollbar.config(command=entry_text.yview)

    root.mainloop()