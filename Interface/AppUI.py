from collections.abc import Callable, Iterable
from types import TracebackType
from traceback import print_tb
from typing import NoReturn
from tkinter import Menu, simpledialog, Listbox, Tk, Frame, Label, Entry, Scrollbar
from tkinter.constants import BOTH, RIDGE, END, LEFT, RIGHT, TOP, X, Y, INSERT
from models import IModel, Template, Group
from tkhtmlview import HTMLLabel
from .GroupEditor import GroupEditor
from .Settings import Settings
from .TemplateEditor import TemplateEditor


def errorHandler(xd, exctype: type, excvalue: Exception, tb: TracebackType):
    msg = f"{exctype}: {excvalue}, {print_tb(tb)}"
    print(msg)
    simpledialog.messagebox.showerror("Error", msg)

Tk.report_callback_exception = errorHandler

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
        self.__create_mailing_group_pane()
        self.__create_template_pane()
        self.__create_mail_input_pane()
        self.populateInterface()


    def populateInterface(self) -> None:
        modelType_func_mapper = {
            Template: self.add_template,
            Group: self.add_group
            }
        
        for (modelType, ui_func) in modelType_func_mapper.items():
            ui_func(modelType.all_instances)


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

    def clearData(self):
        self.grupy = []
        self.szablony = []

    def update(self):
        self.clearData()
        self.populateInterface()

    def __add_group_clicked(self):
        self.show_group_window()
        
    def show_group_window(self, g: Group | None = None):
        group_editor = GroupEditor(self, g)
        group_editor.prepareInterface()

    def __send_clicked(event) -> None:
        print("send mail")
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

        edit_menu = Menu(menubar, tearoff=0)
        add_menu = Menu(edit_menu, tearoff=0)
        add_menu.add_command(
            label="Template",
            command=self.__add_template_clicked)
        add_menu.add_command(label="Group", command=self.__add_group_clicked)
        edit_menu.add_cascade(label="Add...", menu=add_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_command(label="Open Settings", command=self.__openSettings_clicked)
        menubar.add_command(label="Send", command=lambda: self.__send_clicked())


        self.root.config(menu=menubar)
    
    

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

    def __openSettings_clicked(self):
        root = Tk()  # Otwórz ponownie okno logowania
        settings = Settings(root)
        settings.prepareInterface()
        root.mainloop()




