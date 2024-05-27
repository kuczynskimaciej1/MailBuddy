from tkinter import END, Misc, Tk, Toplevel
import tkinter.messagebox as msg
import tkinter.filedialog as fd
from tkinter.ttk import Button, Label, Combobox, Treeview
from openpyxl import load_workbook

from DataSources.dataSources import GapFillSource


class ExternalSourceImportWindow(Toplevel):
    def __init__(self, parent: Toplevel | Tk, master: Misc) -> None:
        super().__init__(master)
        
        self.prepareInterface()

    
    def prepareInterface(self):
        self.title("Importuj dane")
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        self.label = Label(self, text="Select an Excel file:")
        self.select_button = Button(self, text="Browse", command=self.browse_file)
        self.combobox_label = Label(self, text="Worksheet names:")
        self.combobox = Combobox(self)
        self.combobox.bind("<<ComboboxSelected>>", self.update_preview)
        self.treeview = Treeview(self)

        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.select_button.grid(row=0, column=1, padx=10, pady=10)
        self.combobox_label.grid(row=1, column=0, padx=10, pady=10)
        self.combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.treeview.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")


    def browse_file(self):
        self.file_path = fd.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xlsm"), ("All files", "*.*")]
        )
        
        if self.file_path:
            self.load_worksheets()
            

    def update_preview(self, event=None):
        selected_sheet = self.combobox.get()
        if not selected_sheet or not self.file_path:
            return
        
        try:
            workbook = load_workbook(self.file_path)
            sheet = workbook[selected_sheet]
            preview_data = []
            
            for i, column in enumerate(sheet.iter_cols(values_only=True)):
                self.treeview.heading(i+1, text=column)
                for row in sheet.iter_rows(min_row=1, max_row=5, values_only=True):
                    preview_data.append(row)

            self.treeview.configure(state='normal')
            self.treeview.delete('1.0', END)
            
            for row in preview_data:
                self.treeview.insert(END, f"{row}\n")
            
            self.treeview.configure(state='disabled')
        except Exception as e:
            msg.showerror("Error", f"Failed to read the selected worksheet: {e}")


    def load_worksheets(self):
        try:
            workbook = load_workbook(self.file_path)
            sheet_names = workbook.sheetnames
            self.combobox['values'] = sheet_names
            if sheet_names:
                self.combobox.current(0)  # Set the first sheet as the default selection
        except Exception as e:
            msg.showerror("Error", f"Failed to read the Excel file: {e}")


    def save_data(self):
        selected_sheet = self.combobox.get()
        if not selected_sheet or not self.file_path:
            msg.showwarning("Warning", "No worksheet selected or file not loaded.")
            return
        
        try:
            # GapFillSource()
            # self.destroy()
            pass
        except Exception as e:
            msg.showerror("Error", f"Failed to create GapFillSource: {e}")

