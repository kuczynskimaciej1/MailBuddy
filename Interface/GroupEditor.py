from tkinter import Text, Button, Label, Entry, Tk, Toplevel
from tkinter.constants import END, INSERT, WORD
from group_controller import GroupController
from models import Contact, Group
from .ContactList import ContactList


class GroupEditor(Toplevel):
    def __init__(self, parent: Toplevel | Tk, edited: Group | None = None):
        super().__init__(parent.root)
        self.parent = parent
        self.currentGroup = edited

    def prepareInterface(self):
        name_label = Label(self, text="Nazwa grupy:", bg="lightblue")
        self.name_entry = Entry(self, bg="white", fg="black")
        email_label = Label(self, text="Adresy email:", bg="lightblue")
        self.email_text = Text(self, bg="lightblue", fg="black", wrap=WORD)
        btn_add_list_contact = Button(self, text="Dodaj z listy", bg="lightblue", fg="black", command=self.add_contact_from_list_window)
        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black", command=self.__save_group_clicked)
        
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        email_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.email_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        btn_add_list_contact.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        btn_save.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.update()

        
    def update(self):
        if self.currentGroup:
            self.title(f"Edytuj grupę {self.currentGroup.name}")
            self.name_entry.delete(0, END)
            self.name_entry.insert(0, self.currentGroup.name)
            self.currentGroup.contacts = GroupController.get_contacts(self.currentGroup)
            self.email_text.delete('1.0', END)  # Clear current content
            [self.add_contact(c) for c in self.currentGroup.contacts]
        else:
            self.title("Dodaj grupę")

    def add_contact(self, c: Contact):
        self.email_text.insert(INSERT, str(c.email) + "\n")

    def add_contact_from_list_window(self):
        contact_list_window = ContactList(self, self.currentGroup)
        contact_list_window.prepareInterface()
        # TODO: Odebrać info o dodawanych kontaktach, wywoływać add_contact

    def __save_group_clicked(self) -> None:
        if not self.currentGroup:
            self.currentGroup = Group(_name = self.name_entry.get())
        else:
            self.currentGroup.name = self.name_entry.get()
        txt = self.email_text.get(1.0, END).strip()
        email_addresses = [address for address in txt.replace("\n", "").split(",") if address.strip()]
        # TODO: Przy zmianie kontrolek w grupie będzie trzeba zmienić wywoływanie konstruktora - te kontakty powinny być zapisane wcześniej, bez możliwości dodawania ich od tak z palca
        for mail in email_addresses:
            try:
                self.currentGroup._add_contact(Contact(_email=mail))
            except AttributeError as e:
                raise e
        self.parent.add_group(self.currentGroup)
        self.destroy()
