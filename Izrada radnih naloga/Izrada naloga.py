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
    
        

def unesiProizvod(nacrt, nazivArtikla, materijal, dimenzija, duljina, cnc1, cnc2):
    upit = 'INSERT INTO proizvod(nacrt, nazivArtikla, materijal, dimenzija, duljina, cnc1, cnc2)' + '\nVALUES(%s,%s,%s,%s,%s,%s,%s)'
    podaci = (nacrt, nazivArtikla, materijal, dimenzija, duljina, cnc1, cnc2)
    
    try:
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    except Error as error:
        print(error)
    
     
#Ucitavanja podataka iz excel tablice u dataframe objekt(2d array)
#Header oznacava pocetak redaka tablice
tablicaNaloga = pd.read_excel('pregled radnih naloga 2019-10.xls', sheetname='List1', header=1)


#Brisanje cursor objekta    
cursor.close()
        
#Brisanje objekta
vezaSaBazom.close()