from PyQt6 import QtWidgets as qtw
from PyQt6 import QtSql as qts


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