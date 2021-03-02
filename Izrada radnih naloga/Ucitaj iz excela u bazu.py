import pandas as pd
import sys
import Izradi_radni_nalog as rn
import Izradi_raspored as IzradaRasporeda 
from mysql.connector import MySQLConnection, Error
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLineEdit, QFileDialog, QWidget, QTableView, QProgressBar, QTabWidget, QGridLayout, QVBoxLayout, QComboBox, QFormLayout
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtWidgets, QtGui, QtCore

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

#Opcenita funckija za insert u tablice
#Omogucuje insert u sve tablice iz baze
#Zahtjeva da su vrijednosti atributa vec u dogovorenom formatu 
def upisiUBazu(imeTablice, imenaAtributa, atributi):
    upit = 'INSERT INTO ' + imeTablice + '('
    
    #for appenda imena atributa tablice u string upit
    for i in range(len(imenaAtributa)):
        upit += imenaAtributa[i] 
        if i != len(imenaAtributa) - 1:
            upit += ', '
        
    upit += ')\n VALUES('
    
    #Appenda %s u string upita
    for i in range(len(atributi)):
        upit += '%s'
        if i != len(atributi) - 1:
            upit += ', '
    
    upit += ')'
    
    try:
        cursor.execute(upit, atributi)
        vezaSaBazom.commit()      
    except Error as error:
        print(error)
        print("Atributi:", atributi[0])
    
    #Ispisi progress bar
    print (''.join(progress))

narudzbenica_id = 0
#Funkcija formatira podatke u dogovoreni format prije unosa pojedinog redka u bazu
def urediPodatke(redak):
    #Rjesavanje slucaja gdje je alat zapisan kao npr. M6 + M8
    #Gdje je M6 vanjski navoj, a M8 unutranji navoj ?
    #M6 se zapise u vanjski, a m8 u unutarnji
    if pd.isna(redak['VANJSKI']) == False and '+' in redak['VANJSKI']:
        alat = redak['VANJSKI']
        redak['VANJSKI'] = alat[0:2]
        redak['UNUT.'] = alat[5:7]
    
    if pd.isna(redak['VANJSKI']):
        redak['VANJSKI'] = 'nema'
    
    if pd.isna(redak['UNUT.']):
        redak['UNUT.'] = 'nema'
    
    if pd.isna(redak['MATERIJAL']):
        redak['MATERIJAL'] = "nema" #materijal je PK, nemoze vise redaka imati vrijednost "nema"  
    
    if pd.isna(redak['NACRT']):
        redak['NACRT'] = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    if pd.isna(redak['MATERIJAL']):
        redak['MATERIJAL'] = "nema"
    if pd.isna(redak['POZ']) or redak['POZ'] =='novo':
        redak['POZ'] = 0
    
    if pd.isna(redak['CNC 1']):
        redak['CNC 1'] = "nema"
    if pd.isna(redak['CNC 2']):
        redak['CNC 2'] = "nema"
        
    #U slucaju da nepostoji broj narudzbe
    global narudzbenica_id
    if pd.isna(redak['NARUDŽ.']):
        redak['NARUDŽ.'] = narudzbenica_id
        narudzbenica_id += 1
    
    rok = redak['ROK']
    dan = rok[:2]
    mjesec = rok[3:5]
    redak['ROK'] = "2019-"+ mjesec + "-" + dan
     
    
    return redak

#Funkcja koja inicjalizira porgres bar varijablu, prima polje naloga kao argument
progress = list('[')
def progressBarInit(nalozi):
    global progress

    #Ocisti progess
    progress.clear()
    progress.append("[")

    for i in nalozi:
        progress += " "
    progress += "]"

#glavna funkcija programa
#path je put do excel datoteke
#Radni nalozi je array sa radnim nalozima koje treba ucitati
def ucitajUBazu(path, radniNalozi):
    
    #Ucitavanja podataka iz excel tablice u dataframe objekt(2d array)
    #Header oznacava pocetak redaka tablice
    tablicaNaloga = pd.read_excel(path, sheet_name="List1", header=1)
    
    global progressBarGui
    progressBarGui.show()
    progressBarInit(radniNalozi)
    brojacRedova = 0
    
    #Iteracija kroz cijelu tablicu(dataframe)
    #iterrows() vraca tuple(index, series)
    #series je tip podataka slican arrayu
    for i in tablicaNaloga.iterrows():  
        #Spremi series u redak
        redak = i[1]

        #Za svaki redak kojemu stupac RN. nije nan i ako se RN: nalazi u arrayu radniNalozi unesi ga u bazu
        if (pd.isna(redak[0]) == False)  and (redak[0] in radniNalozi):
            redak = urediPodatke(redak)
            
            brojacRedova += 1
            try:
                progress[brojacRedova] = "#"
            except IndexError as error:
                print(error)

            progressBarGui.setValue( int( (brojacRedova/(len(progress) - 2) ) * 100))
            
            upisiUBazu('alat', ('ime',), (redak['VANJSKI'],))
            upisiUBazu('alat', ('ime',), (redak['UNUT.'],))
            upisiUBazu('materijal', ('idMaterijal',), (redak['MATERIJAL'],))
            upisiUBazu('pozicija', ('naziv', 'nacrt', 'idMaterijal', 'redniBr', 'dimenzija', 'duljina', 'dana'), (redak['NAZIV ARTIKLA'], redak['NACRT'], redak['MATERIJAL'], redak['POZ'], redak['DIMENZIJA'], redak['DULJINA'], redak['DANA']))
            upisiUBazu('alatPozicija', ('nacrt', 'alat', 'mjestoNavoja'), (redak['NACRT'], redak['UNUT.'], 'unutarnji'))
            upisiUBazu('alatPozicija', ('nacrt', 'alat', 'mjestoNavoja'), (redak['NACRT'], redak['VANJSKI'], 'vanjski'))
            upisiUBazu('tehnologija', ('cnc',), (redak['CNC 1'],))
            upisiUBazu('tehnologija', ('cnc',), (redak['CNC 2'],))
            upisiUBazu('tehnologijaPozicija', ('cnc', 'nacrt'), (redak['CNC 1'], redak['NACRT']))
            upisiUBazu('tehnologijaPozicija', ('cnc', 'nacrt'), (redak['CNC 2'], redak['NACRT']))
            upisiUBazu('radniNalog', ('brojNaloga',), ( redak['RN.'],))
            upisiUBazu('nalogPozicija', ('nacrt', 'nalog'), (redak['NACRT'], redak['RN.']))
            upisiUBazu('narudzba', ('narudzbenica', 'rok'), (redak['NARUDŽ.'], redak['ROK']))
            upisiUBazu('nalogNarudzba', ('nalog', 'narudzba'), (redak['RN.'], redak['NARUDŽ.']))
            upisiUBazu('pozicijaNarudzba', ('narudzbenica', 'nacrt', 'komada'), (redak['NARUDŽ.'], redak['NACRT'], redak['KOM']))

    
    progressBarGui.setValue(0)
    return True

def ucitajPozicije(path, listaNacrta):
    tablica = pd.read_excel(path, sheet_name="List1", header=1)
    
    global progressBarGui
    progressBarGui.show()
    progressBarCounter = 0
    for i in tablica.iterrows():
        redak = i[1]

        if str(redak['NACRT']) in listaNacrta:
            progressBarCounter = progressBarCounter + 1
            progressBarGui.setValue((progressBarCounter / len(listaNacrta)) * 100)
            print(progressBarCounter, len(listaNacrta))

            redak = urediPodatke(redak)
            print(redak["NAZIV ARTIKLA"], redak["NACRT"])
            upisiUBazu("materijal", ('idMaterijal', ), (redak['MATERIJAL'], ))
            upisiUBazu('pozicija', ('naziv', 'nacrt', 'idMaterijal', 'redniBr', 'dimenzija', 'duljina', 'dana'), (redak['NAZIV ARTIKLA'], redak['NACRT'], redak['MATERIJAL'], redak['POZ'], redak['DIMENZIJA'], redak['DULJINA'], redak['DANA']))
            


#Klasa koja nasljeduje QAbstractTableModel
#Sluzi za kreaciju modela iz pandas dataframe objekta 
#Model se kasnije korsiti za prikaz tablice 
class PandasQtModel(QAbstractTableModel):

    #Konstruktor prima dataFrame objekt
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self.data = data
    
    def rowCount(self, parent=None):
        return self.data.shape[0]

    def columnCount(self, parnet=None):
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data.columns[col]
        return None

    def getData(self, index):
        return str(self.data.iloc[index.row(), index.column()])

class TableViewProzor(QTableView):

    imeTablice = ""

    def __init__(self):
        super(TableViewProzor, self).__init__()
        self.fileName = ""
    
    def setImeTablice(self, ime):
        imeTablice = ime

        self.setWindowTitle(imeTablice)

    def prikaziProzor(self):
        self.show()
        self.setGeometry(300, 200, 1300, 700)
    
    def loadTable(self, fileName):
        self.fileName = fileName
        self.tablicaNaloga = pd.read_excel(self.fileName, sheet_name="List1", header=1)
        self.tableModel = PandasQtModel(self.tablicaNaloga)
        self.setModel(self.tableModel)

import PrikazPodatakaProzor as PrikazPodataka
        
#Klasa za main window
class Prozor(QMainWindow):

    def getGeneriraniNalozi(self):
        
        try:
            cursor.execute("SELECT brojNaloga FROM radninalog WHERE generiran = '1'")
        except Error as error:
            print(error)
        nalozi = cursor.fetchall()
        
        naloziStr = ""
        for x in range(len(nalozi)):
            nalozi[x] = str(nalozi[x][0])
            naloziStr += nalozi[x] + ", "
        
        return naloziStr

    def getUcitaniNalozi(self, returnType):
        
        try:
            cursor.execute("SELECT brojNaloga FROM radninalog")
        except Error as error:
            print(error)
        
        nalozi = cursor.fetchall()

        if returnType == "string":
            naloziStr = ""
            for x in range(len(nalozi)):
                nalozi[x] = str(nalozi[x][0])
                naloziStr += nalozi[x] + ", "
            
            return naloziStr
        elif returnType == "list":
            listaNaloga = list()
            for nalog in nalozi:
                listaNaloga.append(int(nalog[0]))
            print(listaNaloga)
            return listaNaloga

    def __init__(self):
        super(Prozor, self).__init__()
        self.setGeometry(200, 200, 800, 250)
        self.setWindowTitle("EMD")
        self.setWindowIcon(QtGui.QIcon('..\LogoEMD.png')) 
        self.initUI()
        self.fileName = ""
        self.radniNalozi = []
        self.tableViewProzor = TableViewProzor()
        self.prikazPodataka = PrikazPodataka.PrikazPodatakaProzor()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Tablica:")
        self.label.move(10, 20)

        self.label2 = QtWidgets.QLabel(self)
        self.label2.move(60, 27)

        self.generiraniNaloziLabel = QtWidgets.QLabel(self)
        self.generiraniNaloziLabel.setText("Izradeni nalozi: " + self.getGeneriraniNalozi())
        self.generiraniNaloziLabel.move(10, 100)
        self.generiraniNaloziLabel.adjustSize()

        self.ucitaniNalozi = QtWidgets.QLabel(self)
        self.ucitaniNalozi.move(10, 130)
        self.ucitaniNalozi.setText("Ucitani nalozi: " + self.getUcitaniNalozi("string"))
        self.ucitaniNalozi.adjustSize()

        self.butt1 = QtWidgets.QPushButton(self)
        self.butt1.setText("Ucitaj tablicu")
        self.butt1.clicked.connect(self.otvoriTablicu)
        self.butt1.move(10, 60)

        self.ucitajSveButton = QtWidgets.QPushButton(self)
        self.ucitajSveButton.setText("Ucitaj sve naloge u bazu")
        self.ucitajSveButton.adjustSize()
        self.ucitajSveButton.move(120, 60)
        self.ucitajSveButton.hide()
        self.ucitajSveButton.clicked.connect(self.ucitajSveNaloge)

        self.closeButton = QtWidgets.QPushButton(self)
        self.closeButton.setText("Zatvori")
        self.closeButton.move(10, 100)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.hide()

        self.izradiNalogeButton = QtWidgets.QPushButton(self)
        self.izradiNalogeButton.setText("Izradi naloge")
        self.izradiNalogeButton.move(290, 60)
        self.izradiNalogeButton.clicked.connect(self.izradiNaloge)
    
        self.showTableButton = QtWidgets.QPushButton(self)
        self.showTableButton.setText("Prikazi tablicu")
        self.showTableButton.move(390, 60)
        self.showTableButton.hide()
        self.showTableButton.clicked.connect(self.prikaziTablicu)

        self.ucitajOznaceneButton = QtWidgets.QPushButton(self)
        self.ucitajOznaceneButton.setText("Ucitaj oznacene naloge")
        self.ucitajOznaceneButton.adjustSize()
        self.ucitajOznaceneButton.move(500, 60)
        self.ucitajOznaceneButton.hide()
        self.ucitajOznaceneButton.clicked.connect(self.ucitajNaloge)
        
        self.pregledBazeButton = QtWidgets.QPushButton(self)
        self.pregledBazeButton.setText("Pregled i unos podataka")
        self.pregledBazeButton.move(10, 165)
        self.pregledBazeButton.adjustSize()
        self.pregledBazeButton.clicked.connect(self.prikaziPodatke)

        self.izradaRasporedaButton = QtWidgets.QPushButton(self)
        self.izradaRasporedaButton.setText("Izrada rasporeda")
        self.izradaRasporedaButton.move(180, 165)
        self.izradaRasporedaButton.adjustSize()
        self.izradaRasporedaButton.clicked.connect(self.izradaRasporeda)

        self.ucitajPozicijeButton = QtWidgets.QPushButton(self)
        self.ucitajPozicijeButton.setText("Ucitaj sve pozicije")
        self.ucitajPozicijeButton.move(650, 60)
        self.ucitajPozicijeButton.clicked.connect(self.ucitajSvePozicije)
        self.ucitajPozicijeButton.hide()
        self.ucitajPozicijeButton.adjustSize()
        
        self.ucitajOznaceneNacrteButton = QtWidgets.QPushButton(self)
        self.ucitajOznaceneNacrteButton.setText("Ucitaj oznacene nacrte")
        self.ucitajOznaceneNacrteButton.adjustSize()
        self.ucitajOznaceneNacrteButton.move(650, 120)
        self.ucitajOznaceneNacrteButton.clicked.connect(self.ucitajOznaceneNacrte)
        self.ucitajOznaceneNacrteButton.hide()
        
        global progressBarGui
        progressBarGui = QProgressBar(self)
        progressBarGui.setGeometry(10, 200, 300, 20)
        progressBarGui.hide()

        self.popUpWindow = QMessageBox()
        self.popUpWindow.setWindowTitle("Obavjest!")
        self.popUpWindow.setGeometry(400, 300, 50, 50)

        IzradaRasporeda.main()

    def izradaRasporeda(self):
        IzradaRasporeda.reopen()


    def ucitajSvePozicije(self):
        #Loadaj tablicu u memoriju
        self.tableViewProzor.loadTable(self.fileName)
        nacrti = []

        for red in range(self.tableViewProzor.tableModel.rowCount()):
            index = self.tableViewProzor.tableModel.index(red, 3)
            data = str(self.tableViewProzor.tableModel.getData(index))
            if data != "nan":
                nacrti.append(data)
        

        ucitajPozicije(self.fileName, nacrti)
        self.prikazPodataka.updateUiViews()

    def prikaziPodatke(self): 
        self.prikazPodataka.show()

    def ucitajNaloge(self):
        redovi = self.tableViewProzor.selectionModel().selectedIndexes()
        
        for index in sorted(redovi):
            self.radniNalozi.append(float(self.tableViewProzor.tableModel.getData(index)))
        
        print("Ucitavaju se nalozi:", self.radniNalozi)
        ucitajUBazu(self.fileName, self.radniNalozi)
        self.radniNalozi.clear()
        self.ucitaniNalozi.setText("Ucitani nalozi: " + self.getUcitaniNalozi("string"))
        self.ucitaniNalozi.adjustSize()
        self.izradiNalogeButton.show()
        self.prikazPodataka.updateUiViews()
        
    def ucitajOznaceneNacrte(self):
        indexi = self.tableViewProzor.selectionModel().selectedIndexes()
        nacrti = []
        for index in indexi:
            nacrti.append(str(self.tableViewProzor.tableModel.getData(index)))

        ucitajPozicije(self.fileName, nacrti)
        self.prikazPodataka.updateUiViews()

    def prikaziTablicu(self):
        self.tableViewProzor.loadTable(self.fileName)
        self.tableViewProzor.prikaziProzor()        
        self.ucitajOznaceneButton.show()
        self.ucitajOznaceneNacrteButton.show()

    def izradiNaloge(self):
        lista = self.getUcitaniNalozi("list")
        closeDbConnection()
        if rn.main(lista):
            self.popUpWindow.setText("Nalozi su generirani!")
            self.popUpWindow.exec_()
        else:
           self.popUpWindow.setText("GREŠKA!")
           self.popUpWindow.exec_()
        openDbConnection()

    def close(self):
        cursor.close()
        vezaSaBazom.close()
        self.close()

    def update(self):
        self.label.adjustSize()

    def getSviNalozi(self):
        #Loda se tablica u memoriju
        self.tableViewProzor.loadTable(self.fileName)
        
        nalozi = []
        
        for red in range(self.tableViewProzor.tableModel.rowCount()):
            index = self.tableViewProzor.tableModel.index(red, 0)
            data = float(self.tableViewProzor.tableModel.getData(index))
            if str(data) != 'nan':
                nalozi.append(data)

        print(nalozi)
        return nalozi

    def ucitajSveNaloge(self):
        #Ako ucitajUBazu() vraca true, nema errora
        if ucitajUBazu(self.fileName, self.getSviNalozi()):
            self.izradiNalogeButton.show()
            self.ucitaniNalozi.setText("Ucitani nalozi: " + self.getUcitaniNalozi("string"))
            self.ucitaniNalozi.adjustSize()
            self.prikazPodataka.updateUiViews()
            
    
    def otvoriTablicu(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Odaberi tablicu", "","All Files (*);;Python Files (*.py)", options=options)
        if self.fileName:
            print(self.fileName)
            self.ucitajSveButton.show()
            self.showTableButton.show()
            self.label2.setText(self.fileName)
            self.label2.adjustSize()
            self.tableViewProzor.setImeTablice(self.fileName)
            self.ucitajPozicijeButton.show()



def main():
    #openDbConnection()
    app = QApplication(sys.argv)
    win = Prozor()
    view = QTableView()

    win.show()
    sys.exit(app.exec_())

main()


