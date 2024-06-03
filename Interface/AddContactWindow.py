from tkinter import Button, Label, Entry, Toplevel, messagebox
from models import Contact


class AddContactWindow(Toplevel):
    def __init__(self, parent: Toplevel) -> None:
        super().__init__(parent)
        self.parent = parent
    
    def prepareInterface(self):
        self.title("Dodaj Kontakt")

        email_label = Label(self, text="Adres email:", bg="lightblue")
        self.email_entry = Entry(self, bg="white", fg="black")
        name_label = Label(self, text="Imię:", bg="lightblue")
        self.name_entry = Entry(self, bg="white", fg="black")
        surname_label = Label(self, text="Nazwisko:", bg="lightblue")
        self.surname_entry = Entry(self, bg="white", fg="black")
        btn_add_contact = Button(self, text="Dodaj kontakt", bg="lightblue", fg="black", command=self.add_manual_contact)

        email_label.grid(row=0, column=0, padx=5, pady=5)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        name_label.grid(row=1, column=0, padx=5, pady=5)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        surname_label.grid(row=2, column=0, padx=5, pady=5)
        self.surname_entry.grid(row=2, column=1, padx=5, pady=5)
        btn_add_contact.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def add_manual_contact(self):
        email = self.email_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        if email:
            newContact = Contact(_email=email, _first_name=name, _last_name=surname)
            self.parent.update()
            self.destroy()
            # TODO: Jakiś sygnał do parenta żeby się zaktualizował?
        else:
            messagebox.showerror("Błąd", "Podaj adres e-mail")

