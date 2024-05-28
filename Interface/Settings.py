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
from MessagingService.accountInfo import discover_email_settings


class Settings:
    def __init__(self, root):
        self.root = root
        self.root.title("Ustawienia")
        self.root.configure(bg="lightblue")
        self.root.geometry("400x400")

    def prepareInterface(self):
        # TODO: tutaj powinniśmy ładować wartości z User
        example_emails = ["kuczynskimaciej1@poczta.onet.pl", "example1@example.com", "example2@example.com", "example3@example.com"]
        
        label = Label(
            self.root,
            text="MailBuddy",
            bg="lightblue",
            font=("Helvetica", 24))

        self.email_combobox = Combobox(self.root, values=example_emails)

        self.password_entry = Entry(self.root, show="*")
        
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
        self.password_entry.pack(pady=5)
        connect_button.pack(pady=5)
        change_email_button.pack(pady=5)
        close_button.pack(pady=5)

    def connect(self):
        email = self.email_combobox.get()
        password = self.password_entry.get()

        # TODO: połączenie z pocztą
        email_settings = discover_email_settings(email,password)
        messagebox.showinfo("Połączenie", f"Połączono z {email}")

    def change_email(self):
        new_email = simpledialog.askstring(
            "Zmień adres e-mail", "Dodaj nowy adres e-mail")
        if new_email:
            self.email_combobox.set(new_email)

    def close(self):
        self.root.destroy()