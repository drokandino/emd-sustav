from PyQt5.QtWidgets import QWidget, QTabWidget, QMessageBox, QGridLayout, QLineEdit, QBoxLayout, QComboBox, QFormLayout, QVBoxLayout, QCheckBox
from PyQt5 import QtWidgets, QtGui, QtCore
from mysql.connector import Error, MySQLConnection
import BazaInterface
import Izradi_radni_nalog as rn
vezaSaBazom = MySQLConnection(host='localhost', port="3333",
                               database='emd',
                               user='root', password='1234')
vezaSaBazom.autocommit = True

#Incijalizacija cursor objekta
cursor = vezaSaBazom.cursor()

def openDbConnection():
    global vezaSaBazom, cursor
    vezaSaBazom = MySQLConnection(host='localhost', port="3333",
                               database='emd',
                               user='root', password='1234')
    cursor = vezaSaBazom.cursor()
    vezaSaBazom.autocommit = True

def closeDbConnection():
    global vezaSaBazom
    vezaSaBazom.close()    


class PrikazPodatakaProzor(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 200, 100, 300)
        self.setWindowIcon(QtGui.QIcon('..\LogoEMD.png'))
        self.setWindowTitle("Podaci")
        self.initPozicijaWidgets()
        self.initUnosPozicijeWidgets()
        self.initNaloziWidgets()
        self.initUnosMaterijalWidgets()
        self.initUnosNarudzbeWidgets()
        self.initUnosNalogaWidgets()
        self.initPrikazNarudzbeWidgets()
        self.initUi()
        

    def getNaziviPozicija(self):
        
        try:
            cursor.execute("SELECT naziv FROM pozicija")
        except Error as error:
            print(error)
        
        nazivi = cursor.fetchall()

        naziviLista = []
        for naziv in nazivi:
            naziviLista.append(str(naziv[0]))  
        return naziviLista

    def updatePozicijaLabels(self):
        if self.pozicijaPodaci:
            self.nacrtPozicije.setText("Nacrt: " + self.pozicijaPodaci[0][1])
            self.materijalPozicije.setText("Materijal: " + self.pozicijaPodaci[0][2])
            self.dimenzijaPozicije.setText("Dimenzija: " + self.pozicijaPodaci[0][4])
            self.duljinaPozicije.setText("Duljina: " + str(self.pozicijaPodaci[0][5]))
            self.daniIzradePozicije.setText("Dani izrade: " + str(self.pozicijaPodaci[0][6]))

            self.editDimenzija.setText(str(self.pozicijaPodaci[0][4]))
            self.editDuljina.setText(str(self.pozicijaPodaci[0][5]))
            self.editDani.setText(str(self.pozicijaPodaci[0][6]))
    
    def promjenaImenaPozicije(self):
        
        print(self.imenaPozicija.currentText())
        try:
            cursor.execute('SELECT * FROM pozicija WHERE naziv = "' + str(self.imenaPozicija.currentText()) + '"; ')
        except Error as error:
            print(error)
        self.pozicijaPodaci = cursor.fetchall()
        print(self.pozicijaPodaci)
        self.updatePozicijaLabels()
  

    def getMaterijali(self):
        try:
            cursor.execute("SELECT idMaterijal FROM materijal")
        except Error as error:
            print(error)

        materijali = cursor.fetchall()

        listaMaterijala = []
        for materijal in materijali:
            listaMaterijala.append(str(materijal[0]))
        return listaMaterijala

    def promjenaNaloga(self):
        pozicije = self.getNalogPozicija()
        if pozicije: 
            self.brojPozicijaLabel.setText("Pozicije na nalogu: " + str(pozicije))
        else:
            self.brojPozicijaLabel.setText("Pozicije na nalogu: nema")

        self.narudzba = self.getNarudzba()
        if self.narudzba:
            self.narudzbaLabel.setText("Narudzba: " + str(self.narudzba[0][0]) + "  Rok: " + str(self.narudzba[0][1]))
        else:
            self.narudzbaLabel.setText("Narudzba: nema  Rok: nema")
            
        self.updateNalogStatus()
    
    def pormjenaStatusaNaloga(self):
        self.naloziLabel.setText(str(self.getBrojeviNaloga(True)))        
        
    def getBrojeviNaloga(self, status):
        if status:
            try:
                cursor.execute('SELECT brojNaloga FROM radniNalog WHERE status = "' + str(self.statusNaloga.currentText()) + '";')
            except Error as error:
                print(error)
        else:
            try:
                cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
                cursor.execute("SELECT brojNaloga FROM radniNalog")
                vezaSaBazom.commit()
            except Error as error:
                print(error)

        nalozi = cursor.fetchall()

        listaNaloga = []
        for nalog in nalozi:
            listaNaloga.append(str(nalog[0]))  
        print(listaNaloga)
        return listaNaloga

    def getNalogPozicija(self):
        try:
            cursor.execute('SELECT naziv FROM nalogPozicija JOIN pozicija USING(nacrt) WHERE nalog = "' + str(self.brojNaloga.currentText()) + '"; ')
        except Error as error:
            print(error)
        
        nazivi = cursor.fetchall()

        naziviLista = []
        for naziv in nazivi:
            naziviLista.append(str(naziv[0]))  
        return naziviLista

    def getNarudzba(self):
        
        try:
            cursor.execute('SELECT narudzbenica, rok FROM narudzba JOIN nalognarudzba ON nalognarudzba.narudzba = narudzba.narudzbenica WHERE nalog = "' + str(self.brojNaloga.currentText()) + '";')
        except Error as error:
            print(error)

        narudzba = cursor.fetchall()
        print(narudzba)
        return narudzba

    def getNalogStatus(self):
        try:
            cursor.execute('SELECT status FROM radniNalog WHERE brojNaloga = "' + str(self.brojNaloga.currentText()) + '";')
        except Error as error:
            print(error)

        status = cursor.fetchall()

        if status:
            return status[0][0]

    def updateNalogStatus(self):
        status = self.getNalogStatus()
        if status == "Napravljen":
            self.statusNapravljen.setCheckState(2)
        else:
            self.statusNapravljen.setCheckState(0)
        if status == "U izradi":
            self.statusUIzradi.setCheckState(2)
        else:
            self.statusUIzradi.setCheckState(0)
        if status == "Ceka na izradu":
            self.statusCekaNaIzradu.setCheckState(2)
        else:
            self.statusCekaNaIzradu.setCheckState(0)

    
    def statusNapravljenChange(self):
        if self.statusNapravljen.checkState() == 2:
            try:
                cursor.execute('UPDATE radninalog SET status ="Napravljen" WHERE brojNaloga = "' + str(self.brojNaloga.currentText()) + '";')
                vezaSaBazom.commit()
            except Error as error:
                print(error)

            self.statusUIzradi.setCheckState(0)
            self.statusCekaNaIzradu.setCheckState(0)

    def statusUIzradiChange(self):
        if self.statusUIzradi.checkState() == 2:
            try:
                cursor.execute('UPDATE radninalog SET status ="U izradi" WHERE brojNaloga = "' + str(self.brojNaloga.currentText()) + '";')
                vezaSaBazom.commit()
            except Error as error:
                print(error)

            self.statusNapravljen.setCheckState(0)
            self.statusCekaNaIzradu.setCheckState(0)

    def statusCekaNaIzraduChange(self):
        if self.statusCekaNaIzradu.checkState() == 2:
            try:
                cursor.execute('UPDATE radninalog SET status ="Ceka na izradu" WHERE brojNaloga = "' + str(self.brojNaloga.currentText()) + '";')
                vezaSaBazom.commit()
            except Error as error:
                print(error)
            
            self.statusNapravljen.setCheckState(0)
            self.statusUIzradi.setCheckState(0)

    def getNacrtPozicije(self, imePozicije):
        try:
            cursor.execute('SELECT nacrt FROM pozicija WHERE naziv ="' + imePozicije + '";')
        except Error as error:
            print(error)

        nacrt = cursor.fetchall()
        return nacrt[0][0] 
    
    def getPozicije(self, narudzba):
        try:
            cursor.execute('SELECT naziv, komada FROM pozicijanarudzba JOIN pozicija USING(nacrt) WHERE narudzbenica LIKE(' + str(narudzba) + ');')
        except Error as error:
            print(error)

        pozicije = cursor.fetchall()
        print(pozicije)
        return pozicije

    def getNarudzbe(self):
        try:
            cursor.execute("SELECT narudzbenica FROM narudzba;")
        except Error as error:
            print(error)

        narudzbe = cursor.fetchall()
        listaNarudzbi = []
        for narudzba in narudzbe:
            narudzba = str(narudzba[0])
            if narudzba[-1] == "0":
                narudzba = narudzba[0:-2]
            listaNarudzbi.append(narudzba)
        
        return listaNarudzbi

    def initPozicijaWidgets(self):
        self.nacrtPozicije = QtWidgets.QLabel()
        self.materijalPozicije = QtWidgets.QLabel()
        self.dimenzijaPozicije = QtWidgets.QLabel()
        self.duljinaPozicije = QtWidgets.QLabel()
        self.daniIzradePozicije = QtWidgets.QLabel()
        self.urediPoziciju = QtWidgets.QPushButton("Uredi poziciju")
        self.urediPoziciju.clicked.connect(self.uredivanjePozicije)
        self.zavrsiUredivanjeButton = QtWidgets.QPushButton("Zavrsi uredivanje")
        self.zavrsiUredivanjeButton.clicked.connect(self.zavrsiUredivanje)
        
        self.imenaPozicija = QComboBox()
        self.imenaPozicija.addItems(self.getNaziviPozicija())
        self.imenaPozicija.currentIndexChanged.connect(self.promjenaImenaPozicije)

        self.editDimenzija = QLineEdit()
        self.editDuljina = QLineEdit()
        self.editDani = QLineEdit()
        self.editDimenzijaLabel = QtWidgets.QLabel("Dimenzija:")
        self.editDuljinaLabel = QtWidgets.QLabel("Duljina:")
        self.editDaniLabel = QtWidgets.QLabel("Dani:")
    
        self.promjenaImenaPozicije()

    def initUnosPozicijeWidgets(self):
        self.nazivUnos = QLineEdit()
        self.nacrtUnos = QLineEdit()
        self.dimenzijaUnos = QLineEdit()
        self.duljinaUnos = QLineEdit()
        self.danaUnos = QLineEdit()
        self.unesiButton = QtWidgets.QPushButton()
        self.unesiButton.setText("Unesi")
        self.unesiButton.clicked.connect(self.unesiPozicije)
        self.unosMaterijala = QLineEdit()

    def initNaloziWidgets(self):
        self.statusNalogaLabel = QtWidgets.QLabel()
        self.statusNalogaLabel.setText("Statusi naloga:")
        self.statusNaloga = QComboBox()
        self.statusNaloga.addItems(list(["Ceka na izradu", "U izradi", "Napravljen"]))
        self.statusNaloga.currentIndexChanged.connect(self.pormjenaStatusaNaloga)
        self.naloziLabel = QtWidgets.QLabel()
        self.naloziLabel.setText(str(self.getBrojeviNaloga(True)))
        
        self.brojNalogaLabel = QtWidgets.QLabel()
        self.brojNalogaLabel.setText("Broj Naloga:")
        self.brojNaloga = QComboBox()
        self.brojNaloga.duplicatesEnabled = False
        self.brojNaloga.addItems(self.getBrojeviNaloga(False))
        self.brojNaloga.currentIndexChanged.connect(self.promjenaNaloga)

        self.brojPozicijaLabel = QtWidgets.QLabel()
        self.brojPozicijaLabel.setText("Pozicije na nalogu: " + str(self.getNalogPozicija()))

        self.narudzbaLabel = QtWidgets.QLabel()
        self.narudzba = self.getNarudzba()
        if self.narudzba:
            self.narudzbaLabel.setText("Narudzba: " + str(self.narudzba[0][0]) + " Rok: " + str(self.narudzba[0][1]))

        self.statusNapravljen = QCheckBox()
        self.statusNapravljen.setText("Napravljen")
        self.statusNapravljen.stateChanged.connect(self.statusNapravljenChange)

        self.statusUIzradi = QCheckBox()
        self.statusUIzradi.setText("U izradi")
        self.statusUIzradi.stateChanged.connect(self.statusUIzradiChange)

        self.statusCekaNaIzradu = QCheckBox()
        self.statusCekaNaIzradu.setText("Ceka na izradu")
        self.statusCekaNaIzradu.stateChanged.connect(self.statusCekaNaIzraduChange)

        self.updateNalogStatus()

        self.generitajButton = QtWidgets.QPushButton()
        self.generitajButton.setText("Napravi excel")
        self.generitajButton.clicked.connect(lambda: self.generirajExcel(list([self.brojNaloga.currentText()])))


    def initUnosMaterijalWidgets(self):
        self.materijalLabel = QtWidgets.QLabel()
        self.materijalLabel.setText("Materijal:")

        self.materijalInput = QtWidgets.QLineEdit()

        self.unesiMaterijalButton = QtWidgets.QPushButton()
        self.unesiMaterijalButton.setText("Unesi")
        self.unesiMaterijalButton.clicked.connect(self.unesiMaterijal)

    def initUnosNarudzbeWidgets(self):
        self.brojNarudzbeUnos = QLineEdit()
        self.rokNarudzbeUnos = QLineEdit()
        self.brojPozicijaNaNarudzbi = QLineEdit()
        self.brojPozicijaNaNarudzbi.textEdited.connect(self.showPozicijaForms)
        self.pozicijeNaNarudzbi = []
        self.komadaPozicijeLista = []
        self.unesiNarudzbuButton = QtWidgets.QPushButton("Unesi narudzbu") 
        self.unesiNarudzbuButton.clicked.connect(self.unesiNarudzbu)
        
    def initUnosNalogaWidgets(self):
        self.brojNalogUnos = QLineEdit()
        self.brojPozicijaNaNalogu = QLineEdit()
        self.brojPozicijaNaNalogu.textEdited.connect(self.showPozicjeNaNaloguForms)
        self.pozicijeNaNalogu = []
        self.unesiNalogButton = QtWidgets.QPushButton("Unesi nalog")
        self.unesiNalogButton.clicked.connect(self.unesiNalog)
        self.izradiNalogButton = QtWidgets.QPushButton("Izradi excel")
        self.izradiNalogButton.clicked.connect(lambda: self.generirajExcel(list([self.brojNalogUnos.text()])))

    def initPrikazNarudzbeWidgets(self):
        self.narudzbenica = QtWidgets.QComboBox()
        self.narudzbenica.addItems(self.getNarudzbe())
        self.narudzbenica.currentIndexChanged.connect(self.promjenaNarudzbe)
        self.rokLabel = QtWidgets.QLabel()
        self.pozicijaKomada = [QtWidgets.QLabel()]
        
    def promjenaNarudzbe(self):
        pozicije = self.getPozicije(self.narudzbenica.currentText())
        
        for pozicijaKomada in self.pozicijaKomada:
            self.narudzbaTab.layout.removeWidget(pozicijaKomada)
        self.pozicijaKomada.clear()

        for i in range(len(pozicije)):
            pozicijaKomadaLabel = QtWidgets.QLabel()
            pozicijaKomadaLabel.setText("Pozicija: " + str(pozicije[i][0]) + "  Komada: " + str(pozicije[i][1]))
            self.narudzbaTab.layout.addWidget(pozicijaKomadaLabel)
            self.pozicijaKomada.append(pozicijaKomadaLabel)

    def showPozicjeNaNaloguForms(self):
        #Ako postoji text u inputu
        if self.brojPozicijaNaNalogu.text():

            #Ako postoje forme pozicja
            if len(self.pozicijeNaNalogu) > 0:
                #Obrisi stare retke
                for pozicija in self.pozicijeNaNalogu:
                    pozicija.hide()
                    self.unosNalogaTab.layout.removeRow(pozicija)
                    
                #ocisti polje formi pozicja
                self.pozicijeNaNalogu.clear()
                
            for i in range(int(self.brojPozicijaNaNalogu.text())):
                pozicija = QComboBox()
                
                pozicija.addItems(self.getNaziviPozicija())
                
                self.pozicijeNaNalogu.append(pozicija)
                
                self.unosNalogaTab.layout.addRow("Pozicija:", pozicija)
                
            self.unosNalogaTab.layout.removeRow(self.unesiNalogButton)
            self.unesiNalogButton = QtWidgets.QPushButton("Unesi nalog")
            self.unesiNalogButton.clicked.connect(self.unesiNalog)
            self.unosNalogaTab.layout.addWidget(self.unesiNalogButton)

            self.unosNalogaTab.layout.removeRow(self.izradiNalogButton)
            self.izradiNalogButton = QtWidgets.QPushButton("Izradi excel")
            self.izradiNalogButton.clicked.connect(lambda: self.generirajExcel(list([self.brojNalogUnos.text()])))
            self.unosNalogaTab.layout.addWidget(self.izradiNalogButton)
            

    def showPozicijaForms(self):
        #Ako postoji text u inputu
        if self.brojPozicijaNaNarudzbi.text():

            #Ako postoje forme pozicja
            if len(self.pozicijeNaNarudzbi) > 0:
                #Obrisi stare retke
                for pozicija in self.pozicijeNaNarudzbi:
                    pozicija.hide()
                    self.unosNarudzbeTab.layout.removeRow(pozicija)
                    
                for komada in self.komadaPozicijeLista:
                    self.unosNarudzbeTab.layout.removeRow(komada)

                #ocisti polje formi pozicja
                self.pozicijeNaNarudzbi.clear()
                self.komadaPozicijeLista.clear()

            for i in range(int(self.brojPozicijaNaNarudzbi.text())):
                pozicija = QComboBox()
                komada = QLineEdit()

                pozicija.addItems(self.getNaziviPozicija())
                
                self.pozicijeNaNarudzbi.append(pozicija)
                self.komadaPozicijeLista.append(komada)

                self.unosNarudzbeTab.layout.addRow("Pozicija:", pozicija)
                self.unosNarudzbeTab.layout.addRow("Komada:", komada)
                pozicija.hide()
            
            self.unosNarudzbeTab.layout.removeRow(self.unesiNarudzbuButton)
            self.unesiNarudzbuButton = QtWidgets.QPushButton("Unesi narudzbu") 
            self.unesiNarudzbuButton.clicked.connect(self.unesiNarudzbu)
            self.unosNarudzbeTab.layout.addWidget(self.unesiNarudzbuButton)
            
            for pozicija in self.pozicijeNaNarudzbi:
                pozicija.show()
            

    def initUi(self):
        self.tabs = QTabWidget()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.pozicijeTab = QWidget()
        self.naloziTab = QWidget()
        self.unosPozicijeTab = QWidget()
        self.unosMaterijalaTab = QWidget()
        self.unosNarudzbeTab = QWidget()
        self.unosNalogaTab = QWidget()
        self.narudzbaTab = QWidget()

        self.tabs.addTab(self.naloziTab, "Nalozi")
        self.tabs.addTab(self.pozicijeTab, "Pozicije")
        self.tabs.addTab(self.narudzbaTab, "Narudzbe")
        self.tabs.addTab(self.unosPozicijeTab, "Unos pozicije")
        self.tabs.addTab(self.unosMaterijalaTab, "Unos materijala")
        self.tabs.addTab(self.unosNarudzbeTab, "Unos narudzbe")
        self.tabs.addTab(self.unosNalogaTab, "Unos naloga")

        self.pozicijeTab.layout = QVBoxLayout(self)
        self.naloziTab.layout = QVBoxLayout(self)         
        self.unosPozicijeTab.layout = QFormLayout(self)
        self.unosMaterijalaTab.layout = QVBoxLayout(self)
        self.unosNarudzbeTab.layout = QFormLayout(self)
        self.unosNalogaTab.layout = QFormLayout(self)
        self.narudzbaTab.layout = QVBoxLayout(self)

        self.pozicijeTab.layout.addWidget(self.imenaPozicija)
        self.pozicijeTab.layout.addWidget(self.nacrtPozicije)
        self.pozicijeTab.layout.addWidget(self.materijalPozicije)
        self.pozicijeTab.layout.addWidget(self.dimenzijaPozicije)
        self.pozicijeTab.layout.addWidget(self.duljinaPozicije)
        self.pozicijeTab.layout.addWidget(self.daniIzradePozicije)
        self.pozicijeTab.layout.addWidget(self.urediPoziciju)
        
        self.pozicijeTab.layout.addWidget(self.editDimenzijaLabel)
        self.pozicijeTab.layout.addWidget(self.editDimenzija)
        self.pozicijeTab.layout.addWidget(self.editDuljinaLabel)
        self.pozicijeTab.layout.addWidget(self.editDuljina)
        self.pozicijeTab.layout.addWidget(self.editDaniLabel)
        self.pozicijeTab.layout.addWidget(self.editDani)
        self.pozicijeTab.layout.addWidget(self.zavrsiUredivanjeButton)
        
        self.editDani.hide()
        self.editDimenzija.hide()
        self.editDuljina.hide()
        self.editDimenzijaLabel.hide()
        self.editDuljinaLabel.hide()
        self.editDaniLabel.hide()
        self.zavrsiUredivanjeButton.hide()

        self.pozicijeTab.setLayout(self.pozicijeTab.layout)

        self.unosPozicijeTab.layout.addRow("Naziv:", self.nazivUnos)
        self.unosPozicijeTab.layout.addRow("Nacrt:", self.nacrtUnos)
        self.unosPozicijeTab.layout.addRow("Dimenzija:", self.dimenzijaUnos)
        self.unosPozicijeTab.layout.addRow("Duljina:", self.duljinaUnos)
        self.unosPozicijeTab.layout.addRow("Dana:", self.danaUnos)
        self.unosPozicijeTab.layout.addRow("Materijal:", self.unosMaterijala)
        self.unosPozicijeTab.layout.addWidget(self.unesiButton)

        self.unosPozicijeTab.setLayout(self.unosPozicijeTab.layout)

        self.unosNarudzbeTab.layout.addRow("Narudzbenica:", self.brojNarudzbeUnos)
        self.unosNarudzbeTab.layout.addRow("Rok:", self.rokNarudzbeUnos)
        self.unosNarudzbeTab.layout.addRow("Broj pozicija:", self.brojPozicijaNaNarudzbi)
        self.unosNarudzbeTab.layout.addWidget(self.unesiNarudzbuButton)

        self.unosNarudzbeTab.setLayout(self.unosNarudzbeTab.layout)
        self.naloziTab.layout.addWidget(self.statusNalogaLabel)
        self.naloziTab.layout.addWidget(self.statusNaloga)
        self.naloziTab.layout.addWidget(self.naloziLabel)
        self.naloziTab.layout.addWidget(self.brojNalogaLabel)
        self.naloziTab.layout.addWidget(self.brojNaloga)
        self.naloziTab.layout.addWidget(self.brojPozicijaLabel)
        self.naloziTab.layout.addWidget(self.narudzbaLabel)
        self.naloziTab.layout.addWidget(self.statusCekaNaIzradu)
        self.naloziTab.layout.addWidget(self.statusUIzradi)
        self.naloziTab.layout.addWidget(self.statusNapravljen)
        self.naloziTab.layout.addWidget(self.generitajButton)
        self.naloziTab.setLayout(self.naloziTab.layout)

        self.unosMaterijalaTab.layout.addWidget(self.materijalLabel)
        self.unosMaterijalaTab.layout.addWidget(self.materijalInput)
        self.unosMaterijalaTab.layout.addWidget(self.unesiMaterijalButton)
        self.unosMaterijalaTab.setLayout(self.unosMaterijalaTab.layout)

        self.unosNalogaTab.layout.addRow("Broj naloga:", self.brojNalogUnos)
        self.unosNalogaTab.layout.addRow("Broj pozicija:", self.brojPozicijaNaNalogu)
        self.unosNalogaTab.layout.addWidget(self.unesiNalogButton)
        self.unosNalogaTab.layout.addWidget(self.izradiNalogButton)
        self.unosNalogaTab.setLayout(self.unosNalogaTab.layout)

        self.narudzbaTab.layout.addWidget(self.narudzbenica)
        self.narudzbaTab.layout.addWidget(self.rokLabel)

        self.narudzbaTab.setLayout(self.narudzbaTab.layout)

        self.layout.addWidget(self.tabs, 0, 0)

        self.popUpWindow = QMessageBox()
        self.popUpWindow.setWindowTitle("Obavjest!")


    def showPopUpWindow(self, text, operationOutcome):
        if operationOutcome:
            self.popUpWindow.setText(text)
            self.popUpWindow.exec_()
        else:
           self.popUpWindow.setText("GREŠKA!")
           self.popUpWindow.exec_()


    def updateUiViews(self):
        self.imenaPozicija.clear()
        self.imenaPozicija.addItems(self.getNaziviPozicija())

        self.brojNaloga.clear()
        self.brojNaloga.addItems(self.getBrojeviNaloga(False))
        
        self.narudzbenica.addItems(self.getNarudzbe())


    def generirajExcel(self, listaNaloga):
        closeDbConnection()
        self.showPopUpWindow("Nalog je generiran!",  rn.main(listaNaloga))
        openDbConnection()
    

    #Materijal u poziciji mora prethodno postojati u bazi 
    def unesiPozicije(self):
        #Dohvaca sve materijale iz baze
        materijali = self.getMaterijali()
        
        #ako je materijal iz pozicje ne postoji u bazi, unesi ga u bazu
        if self.unosMaterijala.text() not in materijali:
            self.unesiMaterijal(self.unosMaterijala.text())

        #Zatim unesi poziciju
        atributi = list([self.nazivUnos.text(), self.nacrtUnos.text(), self.dimenzijaUnos.text(), self.duljinaUnos.text(), self.danaUnos.text(), self.unosMaterijala.text()])
        imenaAtributa = list(["naziv", "nacrt", "dimenzija", "duljina", "dana", "idMaterijal"])
        returnValue = BazaInterface.upisiUBazu("pozicija", imenaAtributa, atributi)
        self.showPopUpWindow("Poziija je unešena!", returnValue)
        self.updateUiViews()
    
    def unesiMaterijal(self, materijal):
        #ako je funkcija pozvana sa atributom ili se atribut dohvaca iz inputa
        if materijal:
            atributi = list([materijal])
        else:
            atributi = list([self.materijalInput.text()])
        
        imenaAtributa = list(["idMaterijal"])
        returnValue = BazaInterface.upisiUBazu("materijal", imenaAtributa, atributi)
        self.showPopUpWindow("Materijal je unešen", returnValue)
        self.updateUiViews()

    def uredivanjePozicije(self):
        self.dimenzijaPozicije.hide()
        self.duljinaPozicije.hide()
        self.daniIzradePozicije.hide()
        self.urediPoziciju.hide()

        self.editDaniLabel.show()
        self.editDani.show()

        self.editDimenzijaLabel.show()
        self.editDimenzija.show()
        
        self.editDuljinaLabel.show()
        self.editDuljina.show()

        self.zavrsiUredivanjeButton.show()


    def zavrsiUredivanje(self):
        operationSucces = True
        print(str(self.nacrtPozicije.text))
        try:
            cursor.execute('UPDATE pozicija SET dimenzija="' + str(self.editDimenzija.text()) + '",duljina="' + str(self.editDuljina.text()) + '",dana="' + str(self.editDani.text()) + '"WHERE nacrt = "' + str(self.pozicijaPodaci[0][1]) + '";')
            vezaSaBazom.commit()
        except Error as error:
            operationSucces = False
            print(error)
        
        self.editDani.hide()
        self.editDimenzija.hide()
        self.editDuljina.hide()
        self.zavrsiUredivanjeButton.hide()
        self.editDimenzijaLabel.hide()
        self.editDuljinaLabel.hide()
        self.editDaniLabel.hide()

        self.promjenaImenaPozicije()

        self.dimenzijaPozicije.show()
        self.duljinaPozicije.show()
        self.daniIzradePozicije.show()
        self.urediPoziciju.show()

        self.showPopUpWindow("Pozicija je uređena!", operationSucces)
        self.updateUiViews()

    def unesiNarudzbu(self):
        ###Unos u tablicu narudzba
        atributi = list([self.brojNarudzbeUnos.text(), self.rokNarudzbeUnos.text()])
        imenaAtributa = list(["narudzbenica", "rok"])
        returnValue1 = BazaInterface.upisiUBazu("narudzba", imenaAtributa, atributi)

        ###Unos u tablicu pozicija narudzba
        imenaAtributa = list(["nacrt", "narudzbenica", "komada"])
        for i in range(len(self.pozicijeNaNarudzbi)):
             nacrtPozicije = self.getNacrtPozicije(str(self.pozicijeNaNarudzbi[i].currentText()))
             atributi = list([nacrtPozicije, self.brojNarudzbeUnos.text(), str(self.komadaPozicijeLista[i].text())])
             returnValue2 = BazaInterface.upisiUBazu("pozicijanarudzba", imenaAtributa, atributi)
        self.showPopUpWindow("Narudzba je unesena!", (returnValue1 and returnValue2))
        self.updateUiViews()
    
    def unesiNalog(self):
        imenaAtributa = list(["brojNaloga", "generiran", "status"])
        atributi = list([self.brojNalogUnos.text(), "0", "Ceka na izradu"])
        returnValue1 = BazaInterface.upisiUBazu("radninalog", imenaAtributa, atributi)
        
        imenaAtributa = list(["nacrt", "nalog"])
        
        for pozicija in self.pozicijeNaNalogu:
            nacrtPozicije = self.getNacrtPozicije(str(pozicija.currentText()))
            atributi = list([nacrtPozicije, self.brojNalogUnos.text()])

            returnValue2 = BazaInterface.upisiUBazu("nalogpozicija", imenaAtributa, atributi)

        self.showPopUpWindow("Nalog je unesen", (returnValue2 and returnValue1))
        self.updateUiViews()