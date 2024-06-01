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
from models import Contact, IModel, Template, Group, User
from tkhtmlview import HTMLLabel, HTMLText
from DataSources.dataSources import GapFillSource
#from main import ui
#import MessagingService.smtp_data


class Settings(Toplevel):
    def __init__(self, parent: Toplevel | Tk):
        super().__init__(parent.root)
        self.parent = parent
        self.title("Ustawienia")
        self.configure(bg="lightblue")
        self.geometry("400x400")

    def prepareInterface(self):
        label = Label(
            self,
            text="MailBuddy",
            bg="lightblue",
            font=("Helvetica", 24))

        self.email_combobox = Combobox(self)

        self.password_entry = Entry(self, show="*")

        connect_button = Button(
            self,
            text="Połącz",
            bg="lightblue",
            fg="black",
            command=self.connect)
        
        change_email_button = Button(
            self,
            text="Dodaj nowy adres mailowy",
            bg="lightblue",
            fg="black",
            command=self.change_email)
        
        close_button = Button(
            self,
            text="Wyłącz ustawienia",
            bg="lightblue",
            fg="black",
            command=self.close)
        
        label.pack(pady=20)
        self.email_combobox.pack(pady=5)
        self.password_entry.pack(pady=5)
        connect_button.pack(pady=5)
        change_email_button.pack(pady=5)
        close_button.pack(pady=5)
        self.updateCombobox()

    def updateCombobox(self):
        created_users = []
        for u in User.all_instances:
            created_users.append(u._email)
        
        self.email_combobox['values'] = created_users

    def getUser(self):
        email = self.email_combobox.get()
        password = self.password_entry.get()
        
        for u in User.all_instances:
            if u.email == email and u.password == password:
                u.selected = True
                u.password = password
                return u
        return User(_email=email, _password=password, _selected=True)

    def connect(self):
        user = self.getUser()
        
        email_settings = user.discover_email_settings()
        print(email_settings)
        user._smtp_host = email_settings['smtp']['hostname']
        print(user._smtp_host)
        user._smtp_port = email_settings['smtp']['port']
        print(user._smtp_port)
        user._smtp_socket_type = email_settings['smtp']['socket_type']
        print(user._smtp_socket_type)
        messagebox.showinfo("Połączenie", f"Połączono z {user._email}")

    def change_email(self):
        new_email = simpledialog.askstring(
            "Zmień adres e-mail", "Dodaj nowy adres e-mail")
        if not new_email:
            return
        
        User(_email=new_email)
        if new_email:
            self.email_combobox.set(new_email)

    def close(self):
        self.root.destroy()