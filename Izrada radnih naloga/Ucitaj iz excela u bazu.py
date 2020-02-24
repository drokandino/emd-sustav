import pandas as pd
from mysql.connector import MySQLConnection, Error

#print(sys.argv[1])

#Otvori vezu sa bazom
vezaSaBazom = MySQLConnection(host='localhost',
                               database='emd_novi',
                               user='root', password='1')

#Incijalizacija cursor objekta
cursor = vezaSaBazom.cursor()

def unesiAlatPoziciju(nacrt, alat, mjesto):
    upit = 'INSERT INTO alatPozicija(nacrt, alat, mjestoNavoja)\n VALUES(%s, %s, %s)'
    
    if pd.isna(alat):
        alat = 'nema'
   
    podaci = (nacrt, alat, mjesto)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()      
    except Error as error:
        print(error)

#Funkcija za uons podataka u relaciju pozicija
def unesiPoziciju(naziv, nacrt, materijal, poz, dimenzija, duljina):
    upit ='INSERT INTO pozicija(naziv, nacrt, idMaterijal, redniBr, dimenzija, duljina)\nVALUES(%s, %s, %s, %s, %s, %s)'
    
    if pd.isna(nacrt):
        nacrt = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    if pd.isna(materijal):
        materijal = "nema"
    if pd.isna(poz) or poz =='novo':
        poz = 0
    
    #Keriraj tuple sa podacima
    podaci = (naziv, nacrt, materijal, poz, dimenzija , duljina)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()      
    except Error as error:
        print(error)

#Ako narudzbenica ne postoji onda se koristi ovaj ID
narudzbenica_id = 0

def unesiNarudzbu(narudzbenica, rok): 
    upit ='INSERT INTO narudzba(narudzbenica, rok)\nVALUES(%s, %s)'
    
    #if pd.isna(narudzbenica):
    #   narudzbenica = narudzbenica_id #narudzbenica je PK!
    #   narudzbenica_id += 1
     
    #Rok(datum)
    #Oblikovanje datma u sql format
    dan = rok[:2]
    mjesec = rok[3:5]
    rok = "2019-"+ mjesec + "-" + dan
    
    podaci = (narudzbenica, rok)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)
        
def unesiPozicijaNarudzbu(narudzbenica, nacrt, komada):
    upit ='INSERT INTO pozicijaNarudzba(nacrt, narudzbenica, komada)\nVALUES(%s, %s, %s)'
    
    podaci = (nacrt, narudzbenica, komada)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)
    
def unesiNalog(nalog):
    upit ='INSERT INTO radniNalog(brojNaloga)\nVALUES(%s)'
    
    podaci = (nalog,)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)
    
    
def unesiNalogPoziciju(nacrt, nalog):
    upit ='INSERT INTO nalogPozicija(nacrt, nalog)\nVALUES(%s, %s)'
    
    if pd.isna(nacrt):
        nacrt = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    
    podaci = (nacrt, nalog)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
             
    except Error as error:
        print(error)
    
    
def unesiNalogNarudzbu(nalog, narudzba):
    upit ='INSERT INTO nalogNarudzba(nalog, narudzba)\nVALUES(%s, %s)'
    
    podaci = (nalog, narudzba)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)

def unesiMaterijal(materijal):
    upit ='INSERT INTO materijal(idMaterijal)\nVALUES(%s)'
    
    if pd.isna(materijal):
        materijal = "nema" #materijal je PK, nemoze vise redaka imati vrijednost "nema"    
    podaci = (materijal,)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)

def unesiAlat(alat):    
    #Rjesavanje slucaja gdje je alat zapisan kao npr. M6 + M8
    #Gdje je M6 vanjski navoj, a M8 unutranji navoj ?
    #Ako je takav slucaj onda se zove, dva puta, ista funkcija sa vanjskim, a poslje sa unutranjim navojem
    nastaviSaUpitom = True
    if pd.isna(alat) == False and '+' in alat:
        nastaviSaUpitom = False
        unesiAlat(alat[0:2])
        unesiAlat(alat[5:7])
    
    if pd.isna(alat):
        alat = 'nema'
    
    if nastaviSaUpitom == True:    
        upit ='INSERT INTO alat(ime)\nVALUES(%s)'
        podaci = (alat,)
        try:
            cursor.execute(upit, podaci)
            vezaSaBazom.commit()
            
        except Error as error:
            print(error)
        
def unesiTehnologiju(tehnologija):
    upit ='INSERT INTO tehnologija(cnc)\nVALUES(%s)'
    
    if pd.isna(tehnologija):
        tehnologija = "nema"
        
    podaci = (tehnologija,)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)
        
def unesiTehnologijuPoziciju(cnc, nacrt):
    upit ='INSERT INTO tehnologijaPozicija(cnc, nacrt)\nVALUES(%s, %s)'
    
    if pd.isna(nacrt):
        nacrt = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    if pd.isna(cnc):
        cnc = "nema"
    podaci = (cnc, nacrt)
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)

#glavna funkcija programa
#path je put do excel datoteke
def ucitajUBazu(path):
    global narudzbenica_id
    
    #Ucitavanja podataka iz excel tablice u dataframe objekt(2d array)
    #Header oznacava pocetak redaka tablice
    tablicaNaloga = pd.read_excel(path, sheet_name="List1", header=1)
    
    #Iteracija kroz cijelu tablicu(dataframe)
    #iterrows() vraca tuple(index, series)
    #series je tip podataka slican arrayu
    for i in tablicaNaloga.iterrows():
        #Spremi series u redak
        redak = i[1]
       
        #Za svaki redak kojemu stupac RN. nije nan, unesi ga u bazu
        if pd.isna(redak[0]) == False:
            #U slucaju da nepostoji broj narudzbe
            if pd.isna(redak['NARUDŽ.']):
                redak['NARUDŽ.'] = narudzbenica_id
                narudzbenica_id += 1
            
            #Kada su za alat spojene dvije celije
            if pd.isna(redak['VANJSKI']) == False and '+' in redak['VANJSKI']:
                redak['UNUT.'] = redak['VANJSKI'][5:7]
                redak['VANJSKI'] = redak['VANJSKI'][0:2]
            
            unesiAlat(redak['VANJSKI'])
            unesiAlat(redak['UNUT.'])
            unesiMaterijal(redak['MATERIJAL'])
            unesiPoziciju(redak['NAZIV ARTIKLA'], redak['NACRT'], redak['MATERIJAL'], redak['POZ'], redak['DIMENZIJA'], redak['DULJINA'])
            unesiAlatPoziciju(redak['NACRT'], redak['UNUT.'], 'unutarnji')
            unesiAlatPoziciju(redak['NACRT'], redak['VANJSKI'], 'vanjski')
            unesiTehnologiju(redak['CNC 2'])
            unesiTehnologiju(redak['CNC 1'])
            unesiTehnologijuPoziciju(redak['CNC 1'], redak['NACRT'])
            unesiTehnologijuPoziciju(redak['CNC 2'], redak['NACRT'])
            unesiNalog(redak['RN.'])
            unesiNalogPoziciju(redak['NACRT'], redak['RN.'])
            unesiNarudzbu(redak['NARUDŽ.'], redak['ROK'])
            unesiNalogNarudzbu(redak['RN.'], redak['NARUDŽ.'])
            unesiPozicijaNarudzbu(redak['NARUDŽ.'], redak['NACRT'], redak['KOM'])
        
        


#Kod za GUI
#Prvobitna zamisao je bila pokretati ovu datoteku, kao poziv putem komande linije, iz druge datoteke(JednostavanGui.py)
import PySimpleGUI as sg
import os

#pocetni layout prozora
layout = [ 
           [sg.Text('Tablica:')], 
           [sg.Button('Ucitaj tablicu'), sg.Button('Zatvori')]
         ]

#Funkcija vraca layout ovisno o tome koji layout koristimo
#tablcia je ime datoteke koju smo prethodno odabrali
#layout(string) je argument funkcije, oznacava koji koji layout zelimo da funkcija vrati
def createLayout(tablica, layout):
    #isti je kao i  prvi layout samo sto se dodatno ispisuje ime datoteke
    layoutNakonOdabiraDatoteke = [ 
               [sg.Text('Tablica: ' + tablica)], 
               [sg.Button('Ucitaj tablicu'), sg.Button("Ucitaj naloge u bazu"), sg.Button("Izradi naloge"), sg.Button('Zatvori')]]
    
    layoutNakonIzradeNaloga= [ 
               [sg.Text('Tablica: ' + tablica)], 
               [sg.Button('Ucitaj tablicu'), sg.Button('Prikazi naloge'), sg.Button('Zatvori')]]
    
    if layout == 'Nakon odabira datoteke':
        return layoutNakonOdabiraDatoteke
    elif layout == 'Nakon izrade naloga':
        return layoutNakonIzradeNaloga

#Napravi prozor sa izabranim layoutom
window = sg.Window("Izradi naloge").Layout(layout)

#Glavna petlja GUI-a
while True:
    #Event handling
    event, values= window.Read()
    #'Zatvori' referencira button imena 'Zatvori'
    #Analogno za ostale eventove
    if event in (None, 'Zatvori'):
        break
    
    if event in (None, 'Ucitaj tablicu'):
        #U varijabli tablica ce biti sadrzano ime izabrane datoteke
        tablica = sg.PopupGetFile('Odaberite datoteku')
        
        #Iz nekog razloga se ne moze napraviti novi prozor sa istim layoutom
        window.close()
        window = sg.Window("Izradi naloge").Layout(createLayout(tablica, 'Nakon odabira datoteke'))
    
    if event in (None, 'Ucitaj naloge u bazu'):
        #Poziv "main" funkcije ovog programa
        ucitajUBazu(tablica)
        cursor.close()
        vezaSaBazom.close()
    
    if event in (None, 'Izradi naloge'):    
        #Poziv programa Izradi radni nalog.py putem komandne linije
        os.system("python3.7  Izradi\ radni\ nalog.py")
        window.close()
        window = sg.Window("Izradi naloge").Layout(createLayout(tablica, 'Nakon izrade naloga'))
        print("Izvrseno")
    
    if event in (None, 'Prikazi naloge'):
        #Otvara file manager. 
        os.system("pcmanfm-qt")
    
window.close()
del window



