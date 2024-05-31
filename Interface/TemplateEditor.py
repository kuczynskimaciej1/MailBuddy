import re
from enum import Enum
from tkinter import Event, Tk, Button, Label, Entry, Toplevel, Misc
from tkinter.ttk import Combobox, Frame
from tkinter.constants import END, INSERT, SEL, WORD
from models import Template
from tkhtmlview import HTMLLabel, HTMLText
from DataSources.dataSources import GapFillSource
from .ExternalSourceImportWindow import ExternalSourceImportWindow


class TemplateEditor(Toplevel):
    placeholder_text = "<MailBuddyGap> </MailBuddyGap>"

    def __init__(self, parent: Toplevel | Tk, master: Misc, obj: Template | None = None):
        super().__init__(master)
        self.parent = parent
        self.combo_frame: Frame = None
        self.currentTemplate = obj if obj is not None else Template() #fix
        if self.currentTemplate and self.currentTemplate.dataimport:
            GapFillSource(self.currentTemplate.dataimport)

        self.update_combo_values()
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
        self.template_text.bind("<Button-3>", self.__show_placeholder_menu)  # RMB

        self.template_preview = HTMLLabel(self, bg="lightblue", fg="black", wrap=WORD)
        btn_save = Button(self, text="Zapisz", bg="lightblue", fg="black",
                          command=lambda: self.__save_template_clicked(name_entry.get(), self.template_text.get(1.0, END)))
        btn_insert_placeholder = Button(self, text="Wstaw lukę", bg="lightblue", fg="black",
                                        command=self.__template_window_insert_placeholder)
        btn_add_external_source = Button(self, text="Dodaj zewnętrzne źródło", bg="lightblue", fg="black",
                                         command=self.__add_external_source_clicked)

        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.template_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.template_preview.grid(row=1, column=3, columnspan=5, padx=5, pady=5, sticky="nsew")
        
        btn_add_external_source.grid(row=2, column=1, padx=(5, 50), pady=5, sticky="w")
        btn_insert_placeholder.grid(row=2, column=2, padx=(5, 50), pady=5, sticky="w")
        btn_save.grid(row=2, column=3, padx=(50, 5), pady=5, sticky="e")

        if self.currentTemplate:  
            name_entry.insert(INSERT, self.currentTemplate.name if self.currentTemplate.name is not None else "")
            self.template_text.insert(INSERT, self.currentTemplate.content if self.currentTemplate.content is not None else "")
            self.template_text.event_generate("<<TextModified>>")  


    def update_combo_values(self, placeholders: list[GapFillSource] = GapFillSource.all_instances):
         self.combo_values = [key for placeholder in placeholders for key in placeholder.possible_values]


    def __add_external_source_clicked(self):
        ExternalSourceImportWindow(self, self.parent.root, self.currentTemplate)
        
    def update(self):
        GapFillSource(self.currentTemplate.dataimport)
        self.update_combo_values()
        

    def __on_html_key_clicked(self, event: Event):
        if event.keycode not in [c.value for c in NonAlteringKeyCodes]: #python 3.11 fix
            self.template_text.event_generate("<<TextModified>>")


    def __on_text_changed(self, event):
        def update_preview():
            html_text = self.template_text.get("1.0", END)

            color_span_text = '<span style="color:red;">'
            pattern = r"<MailBuddyGap>\s*([^<>\s][^<>]*)\s*</MailBuddyGap>"
            matches = re.findall(pattern, html_text)
            
            preview_text = "" #TODO
            for m in matches:
                preview_text = GapFillSource.getPreviewText(m)
                html_text = html_text.replace(f"<MailBuddyGap>{m}</MailBuddyGap>", color_span_text + preview_text + "</span>")
                

            html_text = html_text.replace("<MailBuddyGap>", color_span_text)
            html_text = html_text.replace("</MailBuddyGap>", "</span>")
            self.template_preview.set_html(html_text)
            
        update_preview()
        

    def __save_template_clicked(self, template_name: str, template_content: str) -> None:
        if template_name != "" and template_content != "":
            self.currentTemplate = Template(_name=template_name, _content=template_content)
            self.parent.add_template(self.currentTemplate)
        self.destroy()


    def hide_combobox(self):
        if self.combo_frame:
            self.combo_frame.destroy()


    def __template_window_insert_placeholder(self) -> None:
        self.template_text.insert(INSERT, TemplateEditor.placeholder_text)
        self.template_text.tag_configure("placeholder", background="lightgreen")

        start_index = "1.0"
        while True:
            start_index = self.template_text.search(TemplateEditor.placeholder_text, start_index, stopindex=END)
            if not start_index:
                break
            end_index = self.template_text.index(f"{start_index}+{len(TemplateEditor.placeholder_text)}c")
            self.template_text.tag_add("placeholder", start_index, end_index)
            start_index = end_index


    def __show_placeholder_menu(self, event):
        self.hide_combobox()
        self.combo_frame = Frame(self.template_text)
        self.combo_frame.place(x=event.x+10, y=event.y+10)
        current_combo = Combobox(self.combo_frame, values=self.combo_values)
        current_combo.grid(row=0, column=0, sticky="nw")
        current_combo.bind("<<ComboboxSelected>>", self.__on_placeholder_selection)
        
        current_combo.focus_set()

        close_button = Button(self.combo_frame, text="X", command=self.hide_combobox, bg="white")
        close_button.grid(row=0, column=1, sticky="ne")
        


    def __on_placeholder_selection(self, event):
        cb: Combobox = self.combo_frame.children['!combobox'] # type: ignore
        selected_placeholder = cb.get()
        if selected_placeholder:
            selected_text = self.template_text.tag_ranges(SEL)
            if selected_text:
                self.template_text.delete(selected_text[0], selected_text[1])
            self.template_text.insert(INSERT, TemplateEditor.placeholder_text.replace(" ", selected_placeholder))
            self.template_text.event_generate("<<TextModified>>")


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
