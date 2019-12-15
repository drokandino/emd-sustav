import pandas as pd
from mysql.connector import MySQLConnection, Error

#Otvori vezu sa bazom
vezaSaBazom = MySQLConnection(host='localhost',
                               database='emd_novi',
                               user='root', password='1')

#Incijalizacija cursor objekta
cursor = vezaSaBazom.cursor()

#Funkcija za uons podataka u relaciju pozicija
def unesiPoziciju(naziv, nacrt):
    upit ='INSERT INTO pozicija(naziv, nacrt)\nVALUES(%s, %s)'
    
    if pd.isna(nacrt):
        nacrt = 'nema' #nacrt je PK, vise proizvoda moze neimati nacrt
    
    #Keriraj tuple sa podacima
    podaci = (naziv, nacrt)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)

#Ako narudzbenica ne postoji onda se koristi ovaj ID
narudzbenica_id = 0

def unesiNarudzbu(narudzbenica):
    #Koristienje globalne varijable u funkciji
    global narudzbenica_id
    
    upit ='INSERT INTO narudzba(narudzbenica)\nVALUES(%s)'
    
    #if pd.isna(narudzbenica):
    #   narudzbenica = narudzbenica_id #narudzbenica je PK!
    #   narudzbenica_id += 1
        
    podaci = (narudzbenica,)
    
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
    
        #unesiPoziciju(redak['NAZIV ARTIKLA'], redak['NACRT'])
        #unesiNarudzbu(redak['NARUDŽ.'])
        #unesiNalog(redak['RN.'])
        #unesiNalogPoziciju(redak['NACRT'], redak['RN.'])
        unesiNalogNarudzbu(redak['RN.'], redak['NARUDŽ.'])
#Brisanje objekata iz memorije
cursor.close()
vezaSaBazom.close()