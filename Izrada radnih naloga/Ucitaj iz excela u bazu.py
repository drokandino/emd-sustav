import pandas as pd
from mysql.connector import MySQLConnection, Error

#Otvori vezu sa bazom
vezaSaBazom = MySQLConnection(host='localhost',
                               database='emd_novi',
                               user='root', password='1')

#Incijalizacija cursor objekta
cursor = vezaSaBazom.cursor()

#Funkcija za uons podataka u relaciju pozicija
def unesiPoziciju(naziv, nacrt, materijal, poz):
    upit ='INSERT INTO pozicija(naziv, nacrt, idMaterijal, redniBr)\nVALUES(%s, %s, %s, %s)'
    
    if pd.isna(nacrt):
        nacrt = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    if pd.isna(materijal):
        materijal = "nema"
    if pd.isna(poz) or poz =='novo':
        poz = 0
    #Keriraj tuple sa podacima
    podaci = (naziv, nacrt, materijal, poz)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)

#Ako narudzbenica ne postoji onda se koristi ovaj ID
narudzbenica_id = 0

def unesiNarudzbu(narudzbenica, rok):
    #Koristienje globalne varijable u funkciji
    global narudzbenica_id
    
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
        
        unesiMaterijal(redak['MATERIJAL'])
        unesiPoziciju(redak['NAZIV ARTIKLA'], redak['NACRT'], redak['MATERIJAL'], redak['POZ'])
        unesiTehnologiju(redak['CNC 2'])
        unesiTehnologiju(redak['CNC 1'])
        unesiTehnologijuPoziciju(redak['CNC 1'], redak['NACRT'])
        unesiTehnologijuPoziciju(redak['CNC 2'], redak['NACRT'])
        unesiNalog(redak['RN.'])
        unesiNalogPoziciju(redak['NACRT'], redak['RN.'])
        unesiNarudzbu(redak['NARUDŽ.'], redak['ROK'])
        unesiNalogNarudzbu(redak['RN.'], redak['NARUDŽ.'])
        
#Brisanje objekata iz memorije
cursor.close()
vezaSaBazom.close()