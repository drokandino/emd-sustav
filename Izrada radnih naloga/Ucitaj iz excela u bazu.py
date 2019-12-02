import pandas as pd
from mysql.connector import MySQLConnection, Error
import datetime as dt


#vezaSaBazom je MySQLConnection objekt
vezaSaBazom = MySQLConnection(host='localhost',
                               database='emd',
                               user='root', password='1')
#Instanciranje cursor objekta
cursor = vezaSaBazom.cursor()
        
#Funkcija modificira bazu. Dodaje novi red u tablicu Narudzba
def unesiNarudzbu(brojNarudzbe, rok, nacrt):
    upit = 'INSERT INTO narudzba(brojNarudzbe, rok, nacrt)' + '\nVALUES(%s,%s,%s)'
    podaci = (brojNarudzbe, rok, nacrt)
    
    try:
        #Generiranje upita i slanje upita bazi
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    #Hvatanje errora
    except Error as error:
        print(error)
    
        
#Funkcija je analogna funkciji unesiNarudzbu
def unesiProizvod(nacrt, nazivArtikla, materijal, dimenzija, duljina, cnc1, cnc2):
    upit = 'INSERT INTO proizvod(nacrt, nazivArtikla, materijal, dimenzija, duljina, cnc1, cnc2)' + '\nVALUES(%s,%s,%s,%s,%s,%s,%s)'
    
    
    ##Ciscenje podataka
    #Dimenzija mora sadrzavati samo brojke, rezanje stringa nakon pojavljivanja slova 
    if dimenzija[0] == 'Ø':
        dimenzija = dimenzija[1:]
    if dimenzija[0] == 'S':
       dimenzija = dimenzija[2:]
    
    podaci = (nacrt, nazivArtikla, materijal, dimenzija, duljina, cnc1, cnc2)
    
    #Stvaranje liste iz tuple-a kako bi se mogli modificirati podaci
    #Iteracija kroz podatke u potrazi za nan vrijednostima
    #Nan vrijednost se mijenja sa praznim stringom
    lista = list(podaci)
    for (i, item) in enumerate(lista):
        if pd.isna(item):
            lista[i] = ""
            
    podaci = tuple(lista)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)
        print("\n")

#Funkcija je analogna funkciji unesiNarudzbu    
def unesiRadniNalog(brojNaloga, brojNarudzbe, nacrt):
    upit ='INSERT INTO radniNalog(brojNaloga, brojNarudzbe, nacrt)\nVALUES(%s, %s, %s)'
    podaci = (brojNaloga, brojNarudzbe, nacrt)

    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)

#Funkcija je analogna funkciji unesiNarudzbu    
def unesiKolicinuProizvoda(brojNarudzbe, nacrt, kom):
    upit ='INSERT INTO kolicinaProizvoda(brojNarudzbe, nacrt, kom)\nVALUES(%s, %s, %s)'
    podaci = (brojNarudzbe, nacrt, kom)

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
        unesiProizvod(redak['NACRT'], redak['NAZIV ARTIKLA'], redak['MATERIJAL'], redak['DIMENZIJA'], 
                      redak['DULJINA'], redak['CNC 1'], redak['CNC 2'])
    
    

#Brisanje cursor objekta    
cursor.close()
        
#Brisanje objekta
vezaSaBazom.close()