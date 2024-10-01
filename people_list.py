import sys
import os

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtSql as qts

from dotenv import load_dotenv

import forms

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow Constructor"""
        super().__init__()
        # main ui code goes here

        self.stack = qtw.QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_dotenv()

        self.init_db()

        self.init_models()

        self.init_form()

        self.statusBar().showMessage("Welcome!")

        self.setup_menu()
        self.setup_toolbar()
        self.setup_list()

        # end main ui code
        self.show()


    def init_dotenv(self):
        dotenvfile_exists = os.path.exists('./.env')
        if dotenvfile_exists == False:
            qtw.QMessageBox.critical(
                None, '.env file error',
                'The file .env doesn\'t exists.'
            )
            sys.exit(1)
        load_dotenv()


    def init_db(self):
        self.db = qts.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('pyasd.db')

        if not self.db.open():
            error = self.db.lastError().text()
            qtw.QMessageBox.critical(
                None, 'DB Conn error',
                'Could not open db file: '
                f'{error}'
            )
            sys.exit(1)

        required_tables = {os.getenv('TBL_PEOPLE')}
        tables = self.db.tables()
        missing_tables = required_tables - set(tables)
        if missing_tables:
            qtw.QMessageBox.critical(
                None, 'DB Integrity error',
                'Missing tables, please repair DB: '
                f'{missing_tables}'
            )
            sys.exit(1)

        query = self.db.exec('SELECT count(*) FROM people')
        query.next()
        count = query.value(0)
        print(f'There are {count} people in the db.')


    def init_models(self):
        # Persone
        self.people_model = qts.QSqlRelationalTableModel()
        self.people_model.setTable('people')
        self.people_model.setQuery(
            "SELECT * "
            "FROM people"
        )
        self.people_model.setHeaderData(1, qtc.Qt.Orientation.Horizontal, 'Nome')
        self.people_model.setHeaderData(2, qtc.Qt.Orientation.Horizontal, 'Cognome')
        self.people_model.setHeaderData(3, qtc.Qt.Orientation.Horizontal, 'Sesso')
        self.people_model.setHeaderData(4, qtc.Qt.Orientation.Horizontal, 'Data Nascita')


    def init_form(self):
        self.person_form = forms.PersonForm(self.people_model)
        self.stack.addWidget(self.person_form)


    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        help_menu = menubar.addMenu('Help')

        self.open_action = file_menu.addAction('Open')
        save_action = file_menu.addAction('Save')
        quit_action = file_menu.addAction('Quit', self.close)
        
        """
        redo_action = qtg.QAction('Redo', self)
        redo_action.triggered.connect(self.textedit.redo)
        edit_menu.addAction(redo_action)
        """


    def setup_toolbar(self):
        toolbar = self.addToolBar('Controls')
        toolbar.addAction('Elimina', self.delete_person)
        toolbar.addAction('Nuovo', self.add_person)
        toolbar.addAction('Back to list',
            self.show_list)

        toolbar.setMovable(False)
        toolbar.setFloatable(False)

    
    def show_list(self):
        self.person_form.mapper.submit()
        self.people_list.resizeColumnsToContents()
        self.people_list.resizeRowsToContents()
        self.stack.setCurrentWidget(self.people_list)        


    def delete_person(self):
        selected = self.people_list.selectedIndexes()
        for index in selected or []:
            self.people_model.removeRow(index.row())

    
    def add_person(self):
        self.stack.setCurrentWidget(self.people_list)
        self.people_model.insertRows(
            self.people_model.rowCount(), 1
        )


    def setup_list(self):
        # A single Replace Widget
        self.people_list = qtw.QTableView()
        self.people_list.setModel(self.people_model)
        self.stack.addWidget(self.people_list)
        self.stack.setCurrentWidget(self.people_list)
        self.people_list.doubleClicked.connect(self.person_form.show_person)
        self.people_list.doubleClicked.connect(lambda: self.stack.setCurrentWidget(self.person_form))
        self.people_list.resizeColumnsToContents()
        self.people_list.resizeRowsToContents()

    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(960, 720)
    sys.exit(app.exec())
