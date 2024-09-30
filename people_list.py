import sys
import os
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from PyQt6 import QtSql as qts
from dotenv import load_dotenv

class DateDelegate(qtw.QStyledItemDelegate):

    def createEditor(self, parent, option, proxyModelIndex):
        date_inp = qtw.QDateEdit(parent, calendarPopup=True)
        return date_inp


class PersonForm(qtw.QWidget):

    def __init__(self, people_model):
        super().__init__()
        self.setLayout(qtw.QFormLayout())
        self.nome = qtw.QLineEdit()
        self.layout().addRow('Name: ', self.nome)
        self.cognome = qtw.QLineEdit()
        self.layout().addRow('Cognome: ', self.cognome)
        self.datanascita = qtw.QDateEdit(calendarPopup=True)
        self.layout().addRow('Data Nascita: ', self.datanascita)
        self.comunenascita = qtw.QLineEdit()
        self.layout().addRow('Comune Nascita: ', self.comunenascita)
        self.provnascita = qtw.QLineEdit()
        self.layout().addRow('Prov. Nascita: ', self.provnascita)
        self.codicefiscale = qtw.QLineEdit()
        self.layout().addRow('C.F.: ', self.codicefiscale)

        self.contatti = qtw.QHBoxLayout()
        self.contatti.addWidget(qtw.QLabel('Email: '))
        self.email = qtw.QLineEdit()
        self.contatti.addWidget(self.email)
        self.contatti.addWidget(qtw.QLabel('Tel.: '))
        self.tel = qtw.QLineEdit()
        self.contatti.addWidget(self.tel)
        self.contatti.addWidget(qtw.QLabel('Cell.: '))
        self.cell = qtw.QLineEdit()
        self.contatti.addWidget(self.cell)

        self.layout().addRow(self.contatti)

        self.init_mapper(people_model)


    def init_mapper(self, people_model):
        self.mapper = qtw.QDataWidgetMapper(self)
        self.mapper.setModel(people_model)
        self.mapper.setItemDelegate(
            qts.QSqlRelationalDelegate(self)
        )
        self.mapper.addMapping(
            self.nome,
            people_model.fieldIndex('nome')
        )
        self.mapper.addMapping(
            self.cognome,
            people_model.fieldIndex('cognome')
        )
        self.mapper.addMapping(
            self.datanascita,
            people_model.fieldIndex('datanascita')
        )
        self.mapper.addMapping(
            self.comunenascita,
            people_model.fieldIndex('comunenascita')
        )
        self.mapper.addMapping(
            self.provnascita,
            people_model.fieldIndex('provnascita')
        )
        self.mapper.addMapping(
            self.codicefiscale,
            people_model.fieldIndex('codicefiscale')
        )
        self.mapper.addMapping(
            self.tel,
            people_model.fieldIndex('tel')
        )
        self.mapper.addMapping(
            self.email,
            people_model.fieldIndex('email')
        )
        self.mapper.addMapping(
            self.cell,
            people_model.fieldIndex('cell')
        )
        self.mapper.model().select()


    def show_person(self, person_index):
        self.mapper.setCurrentIndex(person_index.row())


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
        self.person_form = PersonForm(self.people_model)
        self.stack.addWidget(self.person_form)


    def show_person(self, person_id):
        query = qts.QSqlQuery(self.db)
        query.prepare('SELECT * FROM people WHERE id=:id')
        query.bindValue(':id', person_id)
        query.exec()
        query.next()
        person = {
            'id': query.value(0),
            'nome': query.value(1),
            'cognome': query.value(2),
            'sesso': query.value(3),
            'datanascita': query.value(4),
        }
        self.person_form.show_person(person)
        self.stack.setCurrentWidget(self.person_form)


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

    
    def get_id_for_row(self, index):
        index = index.siblingAtColumn(0)
        person_id = self.people_list.model().data(index)
        return person_id


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(960, 720)
    sys.exit(app.exec())
