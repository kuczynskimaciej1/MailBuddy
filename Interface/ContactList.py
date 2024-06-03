from sqlalchemy.exc import IntegrityError
from tkinter import Button, Frame, Label, Entry, Scrollbar, Toplevel, Canvas, Checkbutton, BooleanVar, VERTICAL
from tkinter.constants import BOTH, LEFT, RIGHT, X, Y
from group_controller import GroupController
from models import Contact, Group
from .AddContactWindow import AddContactWindow

class ContactList(Toplevel):
    def __init__(self, parent: Toplevel, group: Group | None = None) -> None:
        super().__init__(parent)
        self.group = group
        self.parent = parent

    def prepareInterface(self):
        self.title("Dodaj kontakt z listy")
        
        group_editor_geometry = self.parent.winfo_geometry()
        self.geometry(group_editor_geometry)

        contact_frame = Frame(self)
        search_frame = Frame(contact_frame, bg="lightblue")
        search_label = Label(search_frame, text="Wyszukaj:", bg="lightblue")
        self.search_entry = Entry(search_frame, bg="white", fg="black")
        search_button = Button(search_frame, text="Szukaj", bg="lightblue", fg="black", command=self.search_contact)
        add_contact_button = Button(search_frame, text="Dodaj nowy kontakt", bg="lightblue", fg="black", command=self.add_manual_contact_window)
        scrollbar = Scrollbar(contact_frame, orient=VERTICAL)
        self.contact_canvas = Canvas(contact_frame, yscrollcommand=scrollbar.set)
        self.contact_inner_frame = Frame(self.contact_canvas)
        
        scrollbar.config(command=self.contact_canvas.yview)

        contact_frame.pack(fill=BOTH, expand=True)
        search_frame.pack(fill=X, padx=5, pady=5)
        search_label.pack(side=LEFT, padx=5, pady=5)
        self.search_entry.pack(side=LEFT, padx=5, pady=5, expand=True, fill=X)
        search_button.pack(side=LEFT, padx=5, pady=5)
        add_contact_button.pack(side=LEFT, padx=5, pady=5)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.contact_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.contact_canvas.create_window((0, 0), window=self.contact_inner_frame, anchor='nw')
        
        self.contact_canvas.configure(scrollregion=self.contact_canvas.bbox("all"))
        self.update()
        
    def clearEntries(self):
        for widget in self.contact_inner_frame.winfo_children():
            widget.destroy()
    
    def update(self):
        self.clearEntries()
        self.populateWindow()
        
    def populateWindow(self):
        shouldAddButton = self.parent != None
        if self.group:
            group_contacts = GroupController.get_contacts(self.group)
            group_emails = {contact.email for contact in group_contacts}
            
        for idx, c in enumerate(Contact.all_instances):
            shouldToggle = c.email in group_emails
            self.create_contact_widget(c, idx, added_to_group=shouldToggle, addBtn=shouldAddButton)
                    
           
    def create_contact_widget(self, c: Contact, idx: int, added_to_group: bool = False, addBtn: bool = True):
        def toggle_checkbox():
            if checkbox_var.get():
                self.add_contact_to_group(c)
            else:
                self.remove_contact_from_group(c)

        checkbox_var = BooleanVar(value=added_to_group)
        checkbox = Checkbutton(self.contact_inner_frame, variable=checkbox_var, command=toggle_checkbox) #bg="lightblue")
        checkbox.grid(row=idx, column=2, padx=4, pady=4)

        Label(self.contact_inner_frame, text=f"Mail {idx+1}:").grid(row=idx, column=0, padx=5, pady=5)
        Label(self.contact_inner_frame, text=f"{c.email} - {c.first_name} {c.last_name}").grid(row=idx, column=1, padx=5, pady=5)

    def add_contact_to_group(self, c: Contact):
        if self.group == None:
            return
        
        try:    
            GroupController.add_contact(self.group, c)
            self.parent.update()
        except IntegrityError:
            pass
                
    def remove_contact_from_group(self, c: Contact):
        GroupController.delete_connection(self.group, c)
        self.parent.update()
                
    def search_contact(self):
        search_criteria = self.search_entry.get().strip()
        self.clearEntries()
        
        for idx, c in enumerate(Contact.all_instances):
            if search_criteria in c.first_name or search_criteria in c.last_name or search_criteria in c.email:
                self.create_contact_widget(c, idx)
 
    def add_manual_contact_window(self):
       acw = AddContactWindow(self)
       acw.prepareInterface()
