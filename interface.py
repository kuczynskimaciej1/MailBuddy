from collections.abc import Callable, Iterable
from enum import Enum
from sqlalchemy.exc import IntegrityError
from types import TracebackType
from traceback import print_tb
from typing import Literal, Any, NoReturn
from tkinter import Event, Menu, simpledialog, ttk, Listbox, Tk, Text, Button, Frame, Label, Entry, Scrollbar, Toplevel, Misc, messagebox, Menubutton, Canvas,Checkbutton,BooleanVar, VERTICAL, RAISED
from tkinter.ttk import Combobox
from tkinter.constants import NORMAL, DISABLED, BOTH, RIDGE, END, LEFT, RIGHT, TOP, X, Y, INSERT, SEL, WORD
from group_controller import GroupController
from models import Contact, IModel, Template, Group
from tkhtmlview import HTMLLabel, HTMLText
from DataSources.dataSources import GapFillSource

def errorHandler(xd, exctype: type, excvalue: Exception, tb: TracebackType):
    msg = f"{exctype}: {excvalue}, {print_tb(tb)}"
    print(msg)
    simpledialog.messagebox.showerror("Error", msg)


Tk.report_callback_exception = errorHandler


class Settings:
    def __init__(self, root):
        self.root = root
        self.root.title("Ustawienia")
        self.root.configure(bg="lightblue")
        self.root.geometry("400x400")

    def prepareInterface(self):
        # TODO: tutaj powinniśmy ładować wartości z User
        example_emails = ["example1@example.com", "example2@example.com", "example3@example.com"]
        
        label = Label(
            self.root,
            text="MailBuddy",
            bg="lightblue",
            font=("Helvetica", 24))

        self.email_combobox = Combobox(self.root, values=example_emails)
        
        connect_button = Button(
            self.root,
            text="Połącz",
            bg="lightblue",
            fg="black",
            command=self.connect)
        
        change_email_button = Button(
            self.root,
            text="Dodaj nowy adres mailowy",
            bg="lightblue",
            fg="black",
            command=self.change_email)
        
        close_button = Button(
            self.root,
            text="Wyłącz ustawienia",
            bg="lightblue",
            fg="black",
            command=self.close)
        
        label.pack(pady=20)
        self.email_combobox.pack(pady=5)
        connect_button.pack(pady=5)
        change_email_button.pack(pady=5)
        close_button.pack(pady=5)

    def connect(self):
        email = self.email_combobox.get()
        # TODO: połączenie z pocztą
        messagebox.showinfo("Połączenie", f"Połączono z {email}")

    def change_email(self):
        new_email = simpledialog.askstring(
            "Zmień adres e-mail", "Dodaj nowy adres e-mail")
        if new_email:
            self.email_combobox.set(new_email)

    def close(self):
        self.root.destroy()

class AppUI():
    def __init__(self) -> None:
        self.root = Tk()
        self.grupy: list[Group] = []  
        self.szablony: list[Template] = []
        self.template_window: TemplateEditor = None

    def prepareInterface(self) -> None:
        self.root.title("MailBuddy")
        self.root.configure(bg="black")
        self.root.minsize(width=800, height=470)
        self.root.protocol("WM_DELETE_WINDOW", self.__exit_clicked)

        self.__create_menu()
        self.__create_navigation()
  
        self.__create_mailing_group_pane()
        self.__create_template_pane()
        self.__create_mail_input_pane()

    def add_periodic_task(self, period: int, func: Callable):
        # TODO można poprawić żeby się odpalało tylko przy dodaniu obiektu,
        # przemyśleć
        def wrapper():
            func()
            self.root.after(period, wrapper)
        wrapper()

    def run(self):
        self.root.mainloop()

    def __exit_clicked(self) -> NoReturn | None:
        # Wait for saving objects to DB
        print("Exiting")
        exit()

    def add_template(self, content: Template | Iterable[Template]):
        if isinstance(content, Template):
            if content not in self.szablony:
                self.szablony.append(content)
        else:
            [self.szablony.append(i)
             for i in content if i not in self.szablony]
        self.__update_listbox(self.template_listbox, self.szablony)

    def add_group(self, g: Group | Iterable[Group]):
        if isinstance(g, Group):
            if g not in self.grupy:
                self.grupy.append(g)
        else:
            [self.grupy.append(i) for i in g if i not in self.grupy]
        self.__update_listbox(self.grupy_listbox, self.grupy)

    def __add_group_clicked(self):
        self.show_group_window()
        
    def show_group_window(self, g: Group | None = None):
        group_editor = GroupEditor(self, g)
        group_editor.prepareInterface()

    def __send_clicked(event) -> None:
        print("send mail")
        pass

    def __importuj_clicked(self):
        pass

    def __eksportuj_clicked(self):
        pass

    def __template_selection_changed(self, _event):
        selected = self.template_listbox.curselection()
        if len(selected) > 0:
            self.showTemplate(self.szablony[selected[0]])

    def __group_doubleclicked(self, _event):
        selected = self.grupy_listbox.curselection()
        if len(selected) > 0:
            elem = int(self.grupy_listbox.get(selected[0]).split(':')[0])
            self.show_group_window(self.grupy[elem])

    def __group_selection_changed(self, _event):
        selected: int = self.grupy_listbox.curselection()
        if len(selected) > 0:
            g: Group = self.grupy[selected[0]]
            mails = [", ".join(x.email) for x in g.contacts]
            self.entry_adres.delete(0, END) 
            self.entry_adres.insert(INSERT, mails)

    def __template_doubleclicked(self, _event):
        ui_selection = self.template_listbox.curselection()
        if len(ui_selection) > 0:
            selected = self.szablony[ui_selection[0]]
            self.show_template_window(selected)

    def showTemplate(self, selected: Template):
        self.entry_text.delete('1.0', END)
        self.entry_text.insert(END, selected.content)

    @staticmethod
    def __update_listbox(lb: Listbox, content: Iterable[IModel] | dict[IModel]):
        if isinstance(content, Iterable):
            lb.delete(0, END)
            [lb.insert(END, i) for i in content]
        elif isinstance(content, dict):
            lb.delete(0, END)
            [lb.insert(END, k) for k in content.keys()]
        else:
            raise AttributeError(
                f"Wrong type of 'content', expected dict or Iterable, got {
                    type(content)}")

    def __add_template_clicked(self):
        self.show_template_window()

    def __create_menu(self):
        menubar = Menu(self.root)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import", command=self.__importuj_clicked)
        file_menu.add_command(label="Export", command=self.__eksportuj_clicked)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        add_menu = Menu(edit_menu, tearoff=0)
        add_menu.add_command(
            label="Template",
            command=self.__add_template_clicked)
        add_menu.add_command(label="Group", command=self.__add_group_clicked)
        edit_menu.add_cascade(label="Add...", menu=add_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_command(label="Open Settings", command=self.logout)

        self.root.config(menu=menubar)
    

    def __create_navigation(self):
        navigation_frame = Frame(self.root, bg="lightblue")

        btn_plik = Menubutton(
            navigation_frame, text="Plik", bg="lightblue", fg="black", relief=RAISED, bd=2)
        plik_menu = Menu(btn_plik, tearoff=0)
        plik_menu.add_command(
            label="Importuj",
            command=self.__importuj_clicked)
        plik_menu.add_command(
            label="Eksportuj",
            command=self.__eksportuj_clicked)
        btn_plik.configure(menu=plik_menu)

        btn_plik = Menubutton(
            navigation_frame, text="Plik", bg="lightblue", fg="black", relief=RAISED, bd=2)
        plik_menu = Menu(btn_plik, tearoff=0)
        plik_menu.add_command(
            label="Importuj",
            command=self.__importuj_clicked)
        plik_menu.add_command(
            label="Eksportuj",
            command=self.__eksportuj_clicked)
        btn_plik.configure(menu=plik_menu)

        btn_wyslij = Button(navigation_frame, text="Wyślij", bg="lightblue", fg="black",
                            command=lambda: self.__send_clicked()
                            )
        btn_usun = Button(navigation_frame, text="Usuń", bg="lightblue", fg="black",
                          # command=lambda: self.usun_tekst(entry_text)
                          )
        btn_grupy = Button(navigation_frame, text="Grupy", bg="lightblue", fg="black",
                           command=lambda: self.__add_group_clicked())
        btn_szablony = Button(navigation_frame, text="Templates", bg="lightblue", fg="black",
                              command=lambda: self.__add_template_clicked())
        btn_settings = Button(navigation_frame, text="Ustawienia", bg="lightblue", fg="black",
                              command=self.logout)

        navigation_frame.pack(side=TOP, fill=X)
        btn_wyslij.pack(side=LEFT, padx=5, pady=5)
        btn_usun.pack(side=LEFT, padx=5, pady=5)
        btn_grupy.pack(side=LEFT, padx=5, pady=5)
        btn_szablony.pack(side=LEFT, padx=5, pady=5)
        btn_settings.pack(side=RIGHT, padx=5, pady=5)

    

    def __create_mailing_group_pane(self):
        groups_frame = Frame(
            self.root, bg="lightblue", width=200, height=100, relief=RIDGE, borderwidth=2)
        grupy_label = Label(
            groups_frame, text="Grupy mailowe", bg="lightblue")
        self.grupy_listbox = Listbox(groups_frame, bg="lightblue", fg="black")
        self.grupy_listbox.bind(
            '<<ListboxSelect>>',
            self.__group_selection_changed)
        self.grupy_listbox.bind('<Double-1>', self.__group_doubleclicked)

        groups_frame.pack(side=LEFT, padx=10, pady=10,
                          fill=BOTH, expand=True, ipadx=5, ipady=5)
        grupy_label.pack()
        self.grupy_listbox.pack(fill=BOTH, expand=True)

    def __create_template_pane(self):
        templates_frame = Frame(
            self.root, bg="lightblue", width=200, height=100, relief=RIDGE, borderwidth=2)
        szablony_label = Label(
            templates_frame, text="Szablony wiadomości", bg="lightblue")
        self.template_listbox = Listbox(
            templates_frame, bg="lightblue", fg="black")
        self.template_listbox.bind(
            '<<ListboxSelect>>',
            self.__template_selection_changed)
        self.template_listbox.bind('<Double-1>', self.__template_doubleclicked)

        templates_frame.pack(side=LEFT, padx=10, pady=10,
                             fill=BOTH, expand=True, ipadx=5, ipady=5)
        szablony_label.pack()
        self.template_listbox.pack(fill=BOTH, expand=True)

    def __create_mail_input_pane(self):
        entry_frame = Frame(self.root, bg="lightblue",
                            relief=RIDGE, borderwidth=2)
        entry_scrollbar = Scrollbar(entry_frame)
        self.entry_html_label = HTMLLabel(
            entry_frame, html="", bg="lightblue")
        entry_adres_label = Label(
            entry_frame, text="Wyślij do:", bg="lightblue", anchor="s")
        self.entry_adres = Entry(entry_frame, bg="white", fg="black")

        entry_frame.pack(side=TOP, padx=10, pady=10,
                         fill=BOTH, expand=True, ipadx=5, ipady=5)
        entry_scrollbar.pack(side=RIGHT, fill=Y)
        self.entry_html_label.pack(fill=BOTH, expand=True)
        entry_adres_label.pack(side=TOP, padx=5, pady=5)
        self.entry_adres.pack(side=TOP, padx=5, pady=5, fill=X)

    def showTemplate(self, selected: Template):
        self.entry_html_label.set_html(selected.content)

    def show_template_window(self, obj: Template | None = None):
        self.template_window = TemplateEditor(self, self.root, obj)
        self.template_window.prepareInterface()

    def logout(self):
       
        root = Tk()  # Otwórz ponownie okno logowania
        settings = Settings(root)
        settings.prepareInterface()
        root.mainloop()

class TemplateEditor(Toplevel):
    def __init__(self, parent: AppUI, master: Misc,
                 obj: Template | None = None):
        super().__init__(master)
        self.parent = parent
        self.current_combo: Combobox = None
        self.currentTemplate = obj

    def prepareInterface(self):
        self.title("Stwórz szablon")

        name_label = Label(self, text="Nazwa szablonu:", bg="lightblue")
        name_entry = Entry(self, bg="white", fg="black")
        
        self.template_text = HTMLText(self, bg="lightblue", fg="black", wrap=WORD)
        self.template_text.bind("<KeyRelease>", self.__on_html_key_clicked)
        self.template_text.bind("<<TextModified>>", self.__on_text_changed)
        
        self.template_preview = HTMLLabel(self, bg="lightblue", fg="black", wrap=WORD)
        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black", command=lambda: self.__save_template_clicked(
            name_entry.get(), self.template_text.get(1.0, END)))
        btn_insert_placeholder = Button(self, text="Wstaw luke", bg="lightblue", fg="black",
                                        command=self.__template_window_insert_placeholder)
        
        
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.template_text.grid(row=1, column=0, columnspan=2,
                           padx=5, pady=5, sticky="nsew")
        self.template_preview.grid(row=1, column=3, columnspan=5, padx=5, pady=5, sticky="nsew")
        btn_save.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        btn_insert_placeholder.grid(
            row=2, column=1, padx=5, pady=5, sticky="w")
        
        if self.currentTemplate: # if anything is present in template
            name_entry.insert(
                INSERT,
                self.currentTemplate.name if self.currentTemplate.name is not None else "")
            
            self.template_text.insert(
                INSERT,
                self.currentTemplate.content if self.currentTemplate.content is not None else "")
            self.template_text.event_generate("<<TextModified>>") # Initial render
    
    def __on_html_key_clicked(self, event: Event):
        if event.keycode not in NonAlteringKeyCodes:
            self.template_text.event_generate("<<TextModified>>")

    def __on_text_changed(self, event):
        html_text = self.template_text.get("1.0", END)
        mb_tag = "MailBuddyGap>"
        replacement_text = '<span style="color:red;">'
        
        # Only preview change, original text remains intact - contains mb_tag
        html_text = html_text.replace("<" + mb_tag, replacement_text)
        html_text = html_text.replace("</" + mb_tag, "</span>")
        
        self.template_preview.set_html(html_text)

    def __save_template_clicked(
            self, template_name: str, template_content: str) -> None:
        if template_name != "" and template_content != "":
            self.currentTemplate = Template(
                _name=template_name, _content=template_content)
            self.parent.add_template(self.currentTemplate)
        self.destroy()

    def hide_combobox(self):
        if self.current_combo:
            self.current_combo.destroy()

    def __template_window_insert_placeholder(
            self, placeholders: list[GapFillSource] = GapFillSource.all_instances) -> None:
        placeholder_text = "<MailBuddyGap> </MailBuddyGap>"
        combo_values = [key for placeholder in placeholders for key in placeholder.possible_values]
        
        def on_placeholder_selection(event):
            # TODO: Debug - usuwa tylko zaznaczony tekst, może niechcąco usunąć inny fragment
            selected_placeholder = self.current_combo.get()
            if selected_placeholder:
                selected_text = self.template_text.tag_ranges(SEL)
                if selected_text:
                    self.template_text.delete(selected_text[0], selected_text[1])
                self.template_text.insert(INSERT, placeholder_text.replace(" ", selected_placeholder))
                self.template_text.event_generate("<<TextModified>>")

        def show_placeholder_menu(event):
            self.hide_combobox()
            self.current_combo = Combobox(
                self.template_text, values=combo_values)
            #TODO: Debug populating combobox
            self.current_combo.bind(
                "<<ComboboxSelected>>", on_placeholder_selection)
            self.current_combo.place(x=event.x_root, y=event.y_root)
            self.current_combo.focus_set()
            
            close_button = Button(
                self.current_combo, text="X", command=self.hide_combobox, bg="white")
            close_button.place(relx=0.90, rely=0, anchor="ne")

        self.template_text.insert(INSERT, placeholder_text)
        self.template_text.tag_configure("placeholder", background="lightgreen")

        self.template_text.bind("<Button-3>", show_placeholder_menu)

        start_index = "1.0"
        while True:
            start_index = self.template_text.search(
                placeholder_text, start_index, stopindex=END)
            if not start_index:
                break
            end_index = self.template_text.index(
                f"{start_index}+{len(placeholder_text)}c")
            self.template_text.tag_add("placeholder", start_index, end_index)
            start_index = end_index

class GroupEditor(Toplevel):
    def __init__(self, parent: AppUI, edited: Group | None = None):
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

class ContactList(Toplevel):
    def __init__(self, parent: Toplevel | GroupEditor, group: Group | None = None) -> None:
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
        shouldAddButton = self.parent != None and isinstance(self.parent, GroupEditor)
        for idx, c in enumerate(Contact.all_instances):
            self.create_contact_widget(c, idx, addBtn=shouldAddButton)
        
        if self.group:
            group_contacts = GroupController.get_contacts(self.group)
            group_emails = {contact.email for contact in group_contacts}
            for idx, c in enumerate(Contact.all_instances):
                added_to_group = c.email in group_emails
                self.create_contact_widget(c, idx, added_to_group, addBtn=shouldAddButton)
           
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
            if isinstance(self.parent, GroupEditor):
                self.parent.update()
        except IntegrityError:
            pass
                
    def remove_contact_from_group(self, c: Contact):
        GroupController.delete_connection(self.group, c)
        if isinstance(self.parent, GroupEditor):
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

class AddContactWindow(Toplevel):
    def __init__(self, parent: Toplevel | ContactList) -> None:
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

class NonAlteringKeyCodes(Enum):
    # List is non-exhaustive, should be tested
    # via https://asawicki.info/nosense/doc/devices/keyboard/key_codes.html
    
    # Backspace = 8
    # Tab = 9
    Num_Key_5 = 12
    # Enter = 13
    Shift = 16
    Ctrl = 17
    Alt = 18
    Pause_Break = 19
    Caps_Lock = 20
    Esc = 27
    # Space = 32
    Page_Up = 33
    Page_Down = 34
    End = 35
    Home = 36
    Left_Arrow = 37
    Up_Arrow = 38
    Right_Arrow = 39
    Down_Arrow = 40
    Print_Screen = 44
    Insert = 45
    # Delete = 46

