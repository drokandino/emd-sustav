import pandas as pd
from mysql.connector import MySQLConnection, Error

#Otvori vezu sa bazom
vezaSaBazom = MySQLConnection(host='localhost',
                               database='emd_novi',
                               user='root', password='1')

#Incijalizacija cursor objekta
cursor = vezaSaBazom.cursor()

#Funkcija za uons podataka u relaciju pozicija
def unesiPoziciju(naziv, nacrt, materijal, poz, dimenzija, duljina, vanjskiAlat, unutranjiAlat):
    upit ='INSERT INTO pozicija(naziv, nacrt, idMaterijal, redniBr, dimenzija, duljina, alatVanjski, alatUnutarnji)\nVALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
    
    if pd.isna(nacrt):
        nacrt = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    if pd.isna(materijal):
        materijal = "nema"
    if pd.isna(poz) or poz =='novo':
        poz = 0
        
    if pd.isna(vanjskiAlat) == False and '+' in vanjskiAlat:
        unutranjiAlat = vanjskiAlat[5:7]
        vanjskiAlat = vanjskiAlat[0:2]
    if pd.isna(vanjskiAlat):
        vanjskiAlat = 'nema'
    if pd.isna(unutranjiAlat):
        unutranjiAlat = 'nema'
    
    #Keriraj tuple sa podacima
    podaci = (naziv, nacrt, materijal, poz, dimenzija , duljina, vanjskiAlat, unutranjiAlat)
    
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()      
    except Error as error:
        print(error)

#Ako narudzbenica ne postoji onda se koristi ovaj ID
narudzbenica_id = 0

def unesiNarudzbu(narudzbenica, rok):
    #Koristienje globalne varijable u funkciji
    #global narudzbenica_id
    
    upit ='INSERT INTO narudzba(narudzbenica, rok)\nVALUES(%s, %s)'
    
    #if pd.isna(narudzbenica):
    #   narudzbenica = narudzbenica_id #narudzbenica je PK!
    #   narudzbenica_id += 1
     
    #Rok(datum)
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
#Ucitavanja podataka iz excel tablice u dataframe objekt(2d array)
#Header oznacava pocetak redaka tablice
tablicaNaloga = pd.read_excel('pregled radnih naloga 2019-10.xls', sheetname='List1', header=1)

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
        
        unesiAlat(redak['VANJSKI'])
        unesiAlat(redak['UNUT.'])
        unesiMaterijal(redak['MATERIJAL'])
        unesiPoziciju(redak['NAZIV ARTIKLA'], redak['NACRT'], redak['MATERIJAL'], redak['POZ'], redak['DIMENZIJA'], redak['DULJINA'], redak['VANJSKI'], redak['UNUT.'])
        unesiTehnologiju(redak['CNC 2'])
        unesiTehnologiju(redak['CNC 1'])
        unesiTehnologijuPoziciju(redak['CNC 1'], redak['NACRT'])
        unesiTehnologijuPoziciju(redak['CNC 2'], redak['NACRT'])
        unesiNalog(redak['RN.'])
        unesiNalogPoziciju(redak['NACRT'], redak['RN.'])
        unesiNarudzbu(redak['NARUDŽ.'], redak['ROK'])
        unesiNalogNarudzbu(redak['RN.'], redak['NARUDŽ.'])
        unesiPozicijaNarudzbu(redak['NARUDŽ.'], redak['NACRT'], redak['KOM'])
        
        
#Brisanje objekata iz memorije
cursor.close()
vezaSaBazom.close()