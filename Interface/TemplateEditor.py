from enum import Enum
from tkinter import Event, Tk, Button, Label, Entry, Toplevel, Misc
from tkinter.ttk import Combobox
from tkinter.constants import END, INSERT, SEL, WORD
from models import Template
from tkhtmlview import HTMLLabel, HTMLText
from DataSources.dataSources import GapFillSource


class TemplateEditor(Toplevel):
    def __init__(self, parent: Toplevel | Tk, master: Misc, obj: Template | None = None):
        super().__init__(master)
        self.parent = parent
        self.current_combo: Combobox = None
        self.currentTemplate = obj

        self.prepareInterface()

    def prepareInterface(self):
        self.title("Stwórz szablon")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

        name_label = Label(self, text="Nazwa szablonu:", bg="lightblue")
        name_entry = Entry(self, bg="white", fg="black")

        self.template_text = HTMLText(self, bg="lightblue", fg="black", wrap=WORD)
        self.template_text.bind("<KeyRelease>", self.__on_html_key_clicked)
        self.template_text.bind("<<TextModified>>", self.__on_text_changed)

        self.template_preview = HTMLLabel(self, bg="lightblue", fg="black", wrap=WORD)
        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black",
                          command=lambda: self.__save_template_clicked(name_entry.get(), self.template_text.get(1.0, END)))
        btn_insert_placeholder = Button(self, text="Wstaw lukę", bg="lightblue", fg="black",
                                        command=self.__template_window_insert_placeholder)

        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.template_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.template_preview.grid(row=1, column=3, columnspan=5, padx=5, pady=5, sticky="nsew")
        btn_save.grid(row=2, column=2, padx=(50, 5), pady=5, sticky="e")
        btn_insert_placeholder.grid(row=2, column=3, padx=(5, 50), pady=5, sticky="w")

        if self.currentTemplate:  
            name_entry.insert(INSERT, self.currentTemplate.name if self.currentTemplate.name is not None else "")
            self.template_text.insert(INSERT, self.currentTemplate.content if self.currentTemplate.content is not None else "")
            self.template_text.event_generate("<<TextModified>>")  

    def __on_html_key_clicked(self, event: Event):
        if event.keycode not in NonAlteringKeyCodes:
            self.template_text.event_generate("<<TextModified>>")

    def __on_text_changed(self, event):
        html_text = self.template_text.get("1.0", END)
        mb_tag = "MailBuddyGap>"
        replacement_text = '<span style="color:red;">'

        html_text = html_text.replace("<" + mb_tag, replacement_text)
        html_text = html_text.replace("</" + mb_tag, "</span>")

        self.template_preview.set_html(html_text)

    def __save_template_clicked(self, template_name: str, template_content: str) -> None:
        if template_name != "" and template_content != "":
            self.currentTemplate = Template(_name=template_name, _content=template_content)
            self.parent.add_template(self.currentTemplate)
        self.destroy()

    def hide_combobox(self):
        if self.current_combo:
            self.current_combo.destroy()

    def __template_window_insert_placeholder(self, placeholders: list[GapFillSource] = GapFillSource.all_instances) -> None:
        placeholder_text = "<MailBuddyGap> </MailBuddyGap>"
        combo_values = [key for placeholder in placeholders for key in placeholder.possible_values]

        def on_placeholder_selection(event):
            selected_placeholder = self.current_combo.get()
            if selected_placeholder:
                selected_text = self.template_text.tag_ranges(SEL)
                if selected_text:
                    self.template_text.delete(selected_text[0], selected_text[1])
                self.template_text.insert(INSERT, placeholder_text.replace(" ", selected_placeholder))
                self.template_text.event_generate("<<TextModified>>")

        def show_placeholder_menu(event):
            self.hide_combobox()
            self.current_combo = Combobox(self.template_text, values=combo_values)
            self.current_combo.bind("<<ComboboxSelected>>", on_placeholder_selection)
            self.current_combo.place(x=event.x_root, y=event.y_root)
            self.current_combo.focus_set()

            close_button = Button(self.current_combo, text="X", command=self.hide_combobox, bg="white")
            close_button.place(relx=0.90, rely=0, anchor="ne")

        self.template_text.insert(INSERT, placeholder_text)
        self.template_text.tag_configure("placeholder", background="lightgreen")

        self.template_text.bind("<Button-3>", show_placeholder_menu)

        start_index = "1.0"
        while True:
            start_index = self.template_text.search(placeholder_text, start_index, stopindex=END)
            if not start_index:
                break
            end_index = self.template_text.index(f"{start_index}+{len(placeholder_text)}c")
            self.template_text.tag_add("placeholder", start_index, end_index)
            start_index = end_index


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
