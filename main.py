from MessagingService.senders import *
from models import *
from interface import AppUI
from DataSources.dataSources import DatabaseHandler

if __name__ == "__main__":
    ui = AppUI()
    ui.prepareInterface()
    ui.run()

