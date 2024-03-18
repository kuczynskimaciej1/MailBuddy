import tkinter as tk

def usun_tekst():
    entry_text.delete(1.0, tk.END)

def wyslij_mail():
    recipient = entry_adres.get()
    message = entry_text.get(1.0, tk.END)  
    print("Sending email to:", recipient)
    print("Message content:", message)

def utworz_grupe():
    pass

root = tk.Tk()
root.title("MailBuddy")
root.configure(bg="black")

# Miejsce na przyciski nawigacyjne
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

btn_zapisz = tk.Button(navigation_frame, text="Zapisz", bg="lightblue", fg="black")
btn_zapisz.pack(side=tk.LEFT, padx=5, pady=5)

btn_grupy = tk.Button(navigation_frame, text="Grupy", bg="lightblue", fg="black", command=utworz_grupe)
btn_grupy.pack(side=tk.LEFT, padx=5, pady=5)

# ma wyświtlić liste z template maili 
btn_zaladuj = tk.Button(navigation_frame, text="Tamplate", bg="lightblue", fg="black")
btn_zaladuj.pack(side=tk.LEFT, padx=5, pady=5)

# Miejsce na powiadomienia
notifications_frame = tk.Frame(root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
notifications_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
notifications_label = tk.Label(notifications_frame, text="Miejsce na powiadomienia", bg="lightblue")
notifications_label.pack(fill=tk.BOTH, expand=True)

# Miejsce na grupy mailowe
groups_frame = tk.Frame(root, bg="lightblue", width=200, height=100, relief=tk.RIDGE, borderwidth=2)
groups_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True, ipadx=5, ipady=5)
groups_label = tk.Label(groups_frame, text="Miejsce na grupy mailowe", bg="lightblue")
groups_label.pack(fill=tk.BOTH, expand=True)

# Pole do wprowadzania tekstu
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