from collections.abc import Callable, Iterable
from typing import Literal, Any, NoReturn
from tkinter import Menu, simpledialog, ttk, Listbox, Tk, Text, Button, Frame, Label, Entry, Scrollbar, Toplevel, Misc, messagebox, Menubutton, Canvas, VERTICAL, RAISED
from tkinter.ttk import Combobox
from tkinter.constants import NORMAL, DISABLED, BOTH, RIDGE, END, LEFT, RIGHT, TOP, X, Y, INSERT, SEL, WORD
from models import Contact, IModel, Template
from tkhtmlview import HTMLLabel


def errorHandler(xd, exctype: type, excvalue: Exception, tb):
    msg = f"{exctype}: {excvalue}, {tb}"
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
        label = Label(
            self.root,
            text="MailBuddy",
            bg="lightblue",
            font=(
                "Helvetica",
                24))
        label.pack(pady=20)

        self.email_entry = Entry(self.root, bg="white", fg="black")
        self.email_entry.pack(pady=5)

        connect_button = Button(
            self.root,
            text="Połącz",
            bg="lightblue",
            fg="black",
            command=self.connect)
        connect_button.pack(pady=5)

        change_email_button = Button(
            self.root,
            text="Zmień adres mailowy",
            bg="lightblue",
            fg="black",
            command=self.change_email)
        change_email_button.pack(pady=5)

        close_button = Button(
            self.root,
            text="Wyłącz aplikację",
            bg="lightblue",
            fg="black",
            command=self.close)
        close_button.pack(pady=5)

    def connect(self):
        email = self.email_entry.get()
        # TODO: implementacja połączenie z mailem
        messagebox.showinfo("Połączenie", f"Połączono z  {email}")

    def change_email(self):
        new_email = simpledialog.askstring(
            "Zmień adres e mail ", "Dodaj nowy adres e mail ")
        if new_email:
            self.email_entry.delete(0, END)
            self.email_entry.insert(0, new_email)

    def close(self):
        self.root.destroy()


class AppUI():
    def __init__(self) -> None:
        self.root = Tk()
        self.grupy = {}
        self.szablony: list[Template] = []
        self.template_window: TemplateEditor = None

    def prepareInterface(self) -> None:
        self.root.title("MailBuddy")
        self.root.configure(bg="black")
        self.root.minsize(width=800, height=470)
        self.root.protocol("WM_DELETE_WINDOW", self.__exit_clicked)

        self.__create_menu()
        self.__create_navigation()
        self.__create_notification_pane()
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

    def add_group(self, name: str, emails: Iterable[Contact]):
        self.grupy[name] = emails
        self.__update_listbox(self.grupy_listbox, self.grupy)

    def __add_group_clicked(self):
        self.show_group_window()

    def show_group_window(self, group_name: str | None = None,
                          contacts: Iterable[Contact] | None = None):
        group_editor = GroupEditor(self, group_name, contacts)
        group_editor.prepareInterface()

    def __send_clicked() -> None:
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
            elem = self.grupy_listbox.get(selected[0])
            self.show_group_window(elem, self.grupy[elem])

    def __group_selection_changed(self, _event):
        selected: int = self.template_listbox.curselection()
        if len(selected) > 0:
            self.showTemplate(self.szablony[selected[0]])

    def __template_doubleclicked(self, _event):
        selected = self.szablony[self.template_listbox.curselection()[0]]
        self.show_template_window(selected)

    def showTemplate(self, selected: Template):
        self.entry_text.delete('1.0', END)
        self.entry_text.insert(END, selected.content)

    @staticmethod
    def __update_listbox(lb: Listbox, content: Iterable[str] | dict[IModel]):
        if isinstance(content, list):
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

    def __create_notification_pane(self):
        notifications_frame = Frame(
            self.root, bg="lightblue", width=200, height=100, relief=RIDGE, borderwidth=2)
        notifications_label = Label(
            notifications_frame, text="Miejsce na powiadomienia", bg="lightblue")

        notifications_frame.pack(
            side=LEFT, padx=10, pady=10, fill=BOTH, expand=True, ipadx=5, ipady=5)
        notifications_label.pack(fill=BOTH, expand=True)

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
        entry_adres = Entry(entry_frame, bg="white", fg="black")

        entry_frame.pack(side=TOP, padx=10, pady=10,
                         fill=BOTH, expand=True, ipadx=5, ipady=5)
        entry_scrollbar.pack(side=RIGHT, fill=Y)
        self.entry_html_label.pack(fill=BOTH, expand=True)
        entry_adres_label.pack(side=TOP, padx=5, pady=5)
        entry_adres.pack(side=TOP, padx=5, pady=5, fill=X)

    def showTemplate(self, selected: Template):
        self.entry_html_label.set_html(selected.content)

    def show_template_window(self, obj: Template | None = None):
        self.template_window = TemplateEditor(self, self.root, obj)
        self.template_window.prepareInterface()

    def logout(self):
        # TODO to jest do zmiany, okno powinno zostać przemianowane na ustawienia, gdzie
        # logujemy się do providerów poczty, sam program nie ma blokady
        # względem użytkownika

        self.root.destroy()  # Zamknij główne okno aplikacji
        root = Tk()  # Otwórz ponownie okno logowania
        settings = Settings(root)
        settings.prepareInterface()
        root.mainloop()


class TemplateEditor(Toplevel):
    def __init__(self, parent: AppUI, master: Misc,
                 obj: Template | None = None):
        super().__init__(master)
        self.parent = parent
        self.current_combo = None
        self.currentTemplate = obj

    def prepareInterface(self):
        self.title("Stwórz szablon")

        name_label = Label(self, text="Nazwa szablonu:", bg="lightblue")
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = Entry(self, bg="white", fg="black")
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        if self.currentTemplate:
            name_entry.insert(
                INSERT,
                self.currentTemplate.name if self.currentTemplate.name is not None else "")

        template_text = Text(self, bg="lightblue", fg="black", wrap=WORD)
        template_text.grid(row=1, column=0, columnspan=2,
                           padx=5, pady=5, sticky="nsew")
        if self.currentTemplate:
            template_text.insert(
                INSERT,
                self.currentTemplate.content if self.currentTemplate.content is not None else "")

        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black", command=lambda: self.__save_template_clicked(
            name_entry.get(), template_text.get(1.0, END)))
        btn_save.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        btn_insert_placeholder = Button(self, text="Wstaw luke", bg="lightblue", fg="black",
                                        command=lambda: self.__template_window_insert_placeholder(template_text))
        btn_insert_placeholder.grid(
            row=2, column=1, padx=5, pady=5, sticky="w")

    def __save_template_clicked(
            self, template_name: str, template_content: str) -> None:
        if template_name != "" and template_content != "":
            self.currentTemplate = Template(
                _name=template_name, _content=template_content)
            self.parent.add_template(self.currentTemplate)
        self.destroy()

    def __template_window_insert_placeholder(
            self, template_text: str, placeholders: list[str] = []) -> None:
        placeholder_text = "_____"

        def on_placeholder_selection(event):
            selected_placeholder = self.current_combo.get()
            if selected_placeholder:
                selected_text = template_text.tag_ranges(SEL)
                if selected_text:
                    template_text.delete(selected_text[0], selected_text[1])
                template_text.insert(INSERT, selected_placeholder)

        def hide_combobox():
            if self.current_combo:
                self.current_combo.place_forget()

        def show_placeholder_menu(event):
            hide_combobox()
            self.current_combo = Combobox(
                template_text, values=placeholders)
            self.current_combo.bind(
                "<<ComboboxSelected>>", on_placeholder_selection)
            self.current_combo.place(x=event.x_root, y=event.y_root)
            self.current_combo.focus_set()
            # Dodanie przycisku "x" do zamknięcia comboboxa
            close_button = Button(
                self.current_combo, text="X", command=hide_combobox, bg="white")
            close_button.place(relx=0, rely=0, anchor="nw")

        template_text.insert(INSERT, placeholder_text)
        template_text.tag_configure("placeholder", background="lightgreen")

        if not hasattr(self, 'current_combo'):
            self.current_combo = None

        template_text.bind("<Button-3>", show_placeholder_menu)

        start_index = "1.0"
        while True:
            start_index = template_text.search(
                placeholder_text, start_index, stopindex=END)
            if not start_index:
                break
            end_index = template_text.index(
                f"{start_index}+{len(placeholder_text)}c")
            template_text.tag_add("placeholder", start_index, end_index)
            start_index = end_index


class GroupEditor(Toplevel):
    def __init__(self, parent: 'AppUI', groupName: str | None = None,
                 edited: Iterable['Contact'] | None = None):
        super().__init__(parent.root)
        self.parent = parent
        self.groupName = groupName
        self.currentGroup = edited

    def prepareInterface(self):
        self.title("Dodaj grupę")

        name_label = Label(self, text="Nazwa grupy:", bg="lightblue")
        name_label.grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = Entry(self, bg="white", fg="black")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        if self.groupName:
            self.name_entry.insert(INSERT, self.groupName)

        email_label = Label(self, text="Adresy email:", bg="lightblue")
        email_label.grid(row=1, column=0, padx=5, pady=5)

        self.email_text = Text(self, bg="lightblue", fg="black", wrap=WORD)
        self.email_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        if self.currentGroup:
            [self.add_contact(c) for c in self.currentGroup]

        btn_add_list_contact = Button(
            self,
            text="Dodaj z listy",
            bg="lightblue",
            fg="black",
            command=self.add_contact_from_list_window)
        btn_add_list_contact.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        btn_add_manual_contact = Button(
            self,
            text="Dodaj ręcznie",
            bg="lightblue",
            fg="black",
            command=self.add_manual_contact_window)
        btn_add_manual_contact.grid(
            row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_save = Button(
            self,
            text="Zapisz",
            bg="lightblue",
            fg="black",
            command=self.__save_group_clicked)
        btn_save.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="ew")

    def add_contact(self, c: 'Contact'):
        self.email_text.insert(INSERT, str(c.email) + "\n")

    def add_contact_from_list_window(self):
        def search_contact():
            search_criteria = search_entry.get().strip().lower()
            for widget in contact_inner_frame.winfo_children():
                widget.destroy()
            for idx, (email, name, surname) in enumerate(fake_data):
                if search_criteria in name.lower() or search_criteria in surname.lower(
                ) or search_criteria in email.lower():
                    Label(
                        contact_inner_frame,
                        text=f"Mail {
                            idx +
                            1}:").grid(
                        row=idx,
                        column=0,
                        padx=5,
                        pady=5)
                    Label(contact_inner_frame, text=f"{
                          email} - {name} {surname}").grid(row=idx, column=1, padx=5, pady=5)
                    Button(
                        contact_inner_frame,
                        text="Dodaj kontakt",
                        bg="lightblue",
                        fg="black",
                        command=lambda email=email: add_contact_from_list(email)).grid(
                        row=idx,
                        column=2,
                        padx=5,
                        pady=5)

        contact_window = Toplevel(self)
        contact_window.title("Dodaj Kontakt")

        group_editor_geometry = self.winfo_geometry()

        contact_window.geometry(group_editor_geometry)

        contact_frame = Frame(contact_window)
        contact_frame.pack(fill=BOTH, expand=True)

        search_frame = Frame(contact_frame, bg="lightblue")
        search_frame.pack(fill=X, padx=5, pady=5)

        search_label = Label(search_frame, text="Wyszukaj:", bg="lightblue")
        search_label.pack(side=LEFT, padx=5, pady=5)

        search_entry = Entry(search_frame, bg="white", fg="black")
        search_entry.pack(side=LEFT, padx=5, pady=5, expand=True, fill=X)

        search_button = Button(
            search_frame,
            text="Szukaj",
            bg="lightblue",
            fg="black",
            command=search_contact)
        search_button.pack(side=LEFT, padx=5, pady=5)

        scrollbar = Scrollbar(contact_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        contact_canvas = Canvas(contact_frame, yscrollcommand=scrollbar.set)
        contact_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=contact_canvas.yview)

        contact_inner_frame = Frame(contact_canvas)
        contact_canvas.create_window(
            (0, 0), window=contact_inner_frame, anchor='nw')

        fake_data = [("mail1@example.com", "John", "Doe"),
                     ("mail2@example.com", "Jane", "Smith"),
                     ("mail3@example.com", "Michael", "Johnson"),
                     ("mail4@example.com", "Emily", "Brown"),
                     ("mail5@example.com", "William", "Jones"),
                     ("mail6@example.com", "Olivia", "Taylor"),
                     ("mail7@example.com", "David", "Anderson"),
                     ("mail8@example.com", "Sophia", "Thomas"),
                     ("mail9@example.com", "James", "Jackson"),
                     ("mail10@example.com", "Emma", "White"),
                     ("mail11@example.com", "Benjamin", "Harris"),
                     ("mail12@example.com", "Isabella", "Martin"),
                     ("mail13@example.com", "Daniel", "Thompson"),
                     ("mail14@example.com", "Ava", "Garcia"),
                     ("mail15@example.com", "Alexander", "Martinez"),
                     ("mail16@example.com", "TEST", "16"),
                     ("mail17@example.com", "TEST", "17")]

        def add_contact_from_list(email):
            self.email_text.insert(END, email + "\n")

        for idx, (email, name, surname) in enumerate(fake_data):
            Label(
                contact_inner_frame,
                text=f"Mail {
                    idx +
                    1}:").grid(
                row=idx,
                column=0,
                padx=5,
                pady=5)
            Label(contact_inner_frame,
                  text=f"{email} - {name} {surname}").grid(row=idx,
                                                           column=1,
                                                           padx=5,
                                                           pady=5)
            Button(
                contact_inner_frame,
                text="Dodaj kontakt",
                bg="lightblue",
                fg="black",
                command=lambda email=email: add_contact_from_list(email)).grid(
                row=idx,
                column=2,
                padx=5,
                pady=5)

        def on_frame_configure(event):
            contact_canvas.configure(scrollregion=contact_canvas.bbox("all"))

        contact_inner_frame.bind("<Configure>", on_frame_configure)

    def add_manual_contact_window(self):
        contact_window = Toplevel(self)
        contact_window.title("Dodaj Kontakt")

        email_label = Label(
            contact_window,
            text="Adres email:",
            bg="lightblue")
        email_label.grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = Entry(contact_window, bg="white", fg="black")
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        name_label = Label(contact_window, text="Imię:", bg="lightblue")
        name_label.grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = Entry(contact_window, bg="white", fg="black")
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        surname_label = Label(contact_window, text="Nazwisko:", bg="lightblue")
        surname_label.grid(row=2, column=0, padx=5, pady=5)
        self.surname_entry = Entry(contact_window, bg="white", fg="black")
        self.surname_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_add_contact = Button(
            contact_window,
            text="Dodaj kontakt",
            bg="lightblue",
            fg="black",
            command=self.add_manual_contact)
        btn_add_contact.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="ew")

    def add_manual_contact(self):
        email = self.email_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        if email:
            self.email_text.insert(END, f"{email}\n")
        else:
            messagebox.showerror("Błąd", "Podaj adres e-mail")

    def __save_group_clicked(self) -> None:
        result = []
        group_name, email_addresses = self.name_entry.get(), self.email_text.get(1.0, END)
        for line in email_addresses.split("\n"):
            if line.strip():
                email, *name_surname = line.strip().split(" - ")
                if name_surname:
                    name, surname = " ".join(
                        name_surname[:-1]), name_surname[-1]
                else:
                    name, surname = "", ""
                result.append(Contact(name, surname, email))
        self.parent.add_group(group_name, result)
        self.destroy()
