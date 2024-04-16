from collections.abc import Callable, Iterable
from typing import Literal, Any, NoReturn
from tkinter import Menu, simpledialog, ttk, Listbox, Tk, Text, Button, Frame, Label, Entry, Scrollbar, Toplevel, Misc, messagebox, Menubutton, RAISED
from tkinter.ttk import Combobox
from tkinter.constants import NORMAL, DISABLED, BOTH, RIDGE, END, LEFT, RIGHT, TOP, X, Y, INSERT, SEL, WORD
from models import Template
from tkhtmlview import HTMLLabel


class LoginWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Logowanie")
        self.root.configure(bg="lightblue")
        self.root.geometry("300x200")

        label = Label(self.root, text="MailBuddy", bg="lightblue", font=("Helvetica", 24))
        label.pack(pady=20)

        self.username_entry = Entry(self.root, bg="white", fg="black")
        self.username_entry.pack(pady=5)

        self.password_entry = Entry(self.root, bg="white", fg="black", show="*")
        self.password_entry.pack(pady=5)

        login_button = Button(self.root, text="Zaloguj się", bg="lightblue", fg="black", command=self.login)
        login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        #  dane logowania czy są test
        if username == "test" and password == "test":
            self.root.destroy() 
            app = AppUI()  
            app.prepareInterface() 
            app.run()  
        else:
            messagebox.showerror("Błąd logowania", "Nieprawidłowa nazwa użytkownika lub hasło")

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

        self.__create_navigation()
        self.__create_notification_pane()
        self.__create_mailing_group_pane()
        self.__create_template_pane()
        self.__create_mail_input_pane()

    def add_periodic_task(self, period: int, func: Callable):
        # TODO można poprawić żeby się odpalało tylko przy dodaniu obiektu, przemyśleć
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
            [self.szablony.append(i) for i in content if i not in self.szablony]
        self.__update_listbox(self.template_listbox, self.szablony)

    def add_group_clicked(self):
        group_editor = GroupEditor(self)
        group_editor.prepareInterface()

    def __send_clicked() -> None:
        print("send mail")
        pass

    def __template_selection_changed(self, _event):
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
    def __update_listbox(lb: Listbox, content: Iterable[str]):
        lb.delete(0, END)
        [lb.insert(END, i) for i in content]

    def __add_template_clicked(self):
        self.show_template_window()

    def __create_navigation(self):
        navigation_frame = Frame(self.root, bg="lightblue")
        
        btn_plik = Menubutton(
            navigation_frame, text="Plik", bg="lightblue", fg="black", relief=RAISED, bd=2)
        plik_menu = Menu(btn_plik, tearoff=0)
        plik_menu.add_command(label="Importuj", command=self.__importuj_clicked)
        plik_menu.add_command(label="Eksportuj", command=self.__eksportuj_clicked)
        btn_plik.configure(menu=plik_menu)

        btn_wyslij = Button(navigation_frame, text="Wyślij", bg="lightblue", fg="black",
                               command=lambda: self.__send_clicked()
                               )
        btn_usun = Button(navigation_frame, text="Usuń", bg="lightblue", fg="black",
                             # command=lambda: self.usun_tekst(entry_text)
                             )
        btn_grupy = Button(navigation_frame, text="Grupy", bg="lightblue", fg="black",
                   command=lambda: self.add_group_clicked())
        btn_szablony = Button(navigation_frame, text="Templates", bg="lightblue", fg="black",
                                 command=lambda: self.__add_template_clicked())
        btn_wyloguj = Button(navigation_frame, text="Wyloguj", bg="lightblue", fg="black",
                             command=self.logout)

        navigation_frame.pack(side=TOP, fill=X)
        btn_plik.pack(side=LEFT, padx=5, pady=5)
        btn_wyslij.pack(side=LEFT, padx=5, pady=5)
        btn_usun.pack(side=LEFT, padx=5, pady=5)
        btn_grupy.pack(side=LEFT, padx=5, pady=5)
        btn_szablony.pack(side=LEFT, padx=5, pady=5)
        btn_wyloguj.pack(side=RIGHT, padx=5, pady=5)

    def __importuj_clicked(self):
        pass

    def __eksportuj_clicked(self):
        pass

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

        groups_frame.pack(side=LEFT, padx=10, pady=10,
                          fill=BOTH, expand=True, ipadx=5, ipady=5)
        grupy_label.pack()
        self.grupy_listbox.pack(fill=BOTH, expand=True)
        self.grupy_listbox.bind('<Double-Button-1>',
                           lambda event: self.edytuj_grupe())

    def __create_template_pane(self):
        templates_frame = Frame(
            self.root, bg="lightblue", width=200, height=100, relief=RIDGE, borderwidth=2)
        szablony_label = Label(
            templates_frame, text="Szablony wiadomości", bg="lightblue")
        self.template_listbox = Listbox(
            templates_frame, bg="lightblue", fg="black")
        self.template_listbox.bind('<<ListboxSelect>>', self.__template_selection_changed)
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
        self.root.destroy()  # Zamknij główne okno aplikacji
        root = Tk()  # Otwórz ponownie okno logowania
        login_window = LoginWindow(root)
        root.mainloop()

class TemplateEditor(Toplevel):
    def __init__(self, parent: AppUI, master: Misc, obj: Template | None = None):
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
            name_entry.insert(INSERT, self.currentTemplate.name if self.currentTemplate.name is not None else "")

        template_text = Text(self, bg="lightblue", fg="black", wrap=WORD)
        template_text.grid(row=1, column=0, columnspan=2,
                           padx=5, pady=5, sticky="nsew")
        if self.currentTemplate:
            template_text.insert(INSERT, self.currentTemplate.content if self.currentTemplate.content is not None else "")

        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black", command=lambda: self.__save_template_clicked(
            name_entry.get(), template_text.get(1.0, END)))
        btn_save.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        btn_insert_placeholder = Button(self, text="Wstaw luke", bg="lightblue", fg="black",
                                           command=lambda: self.__template_window_insert_placeholder(template_text))
        btn_insert_placeholder.grid(
            row=2, column=1, padx=5, pady=5, sticky="w")

    def __save_template_clicked(self, template_name: str, template_content: str) -> None:
        if template_name != "" and template_content != "":
            self.currentTemplate = Template(_name=template_name, _content=template_content)
            self.parent.add_template(self.currentTemplate)
        self.destroy()

    def __template_window_insert_placeholder(self, template_text: str, placeholders: list[str] = []) -> None:
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
    def __init__(self, parent: AppUI):
        super().__init__(parent.root)
        self.parent = parent

    def prepareInterface(self):
        self.title("Dodaj grupę")

        name_label = Label(self, text="Nazwa grupy:", bg="lightblue")
        name_label.grid(row=0, column=0, padx=5, pady=5)

        name_entry = Entry(self, bg="white", fg="black")
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        email_label = Label(self, text="Adresy email:", bg="lightblue")
        email_label.grid(row=1, column=0, padx=5, pady=5)

        email_text = Text(self, bg="lightblue", fg="black", wrap=WORD)
        email_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black", command=lambda: self.__save_group_clicked(
            name_entry.get(), email_text.get(1.0, END)))
        btn_save.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def __save_group_clicked(self, group_name: str, email_addresses: str) -> None:
        emails = email_addresses.split()
        self.parent.grupy[group_name] = emails
        self.parent.grupy_listbox.insert(END, group_name)
        self.destroy()

if __name__ == "__main__":
    root = Tk()  
    login_window = LoginWindow(root)
    root.mainloop()