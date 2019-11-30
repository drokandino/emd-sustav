import pandas as pd
from mysql.connector import MySQLConnection, Error
import datetime as dt


#vezaSaBazom je MySQLConnection objekt
vezaSaBazom = MySQLConnection(host='localhost',
                               database='emd',
                               user='root', password='1')
       

#Funkcija modificira bazu. Dodaje novi red u tablicu Narudzba
def unesi_narudzbu(brojNarudzbe, rok, nacrt):
    upit = 'INSERT INTO narudzba(brojNarudzbe, rok, nacrt)' + '\nVALUES(%s,%s,%s)'
    podaci = (brojNarudzbe, rok, nacrt)
    
    try:
        #Instanciranje cursor objekta, generiranje upita i slanje upita bazi
        cursor = vezaSaBazom.cursor()
        cursor.execute(upit, podaci)
        vezaSaBazom.commit()
        
    #Hvatanje errora
    except Error as error:
        print(error)
    
    #Brisanje cursor objekta
    finally:
        cursor.close()
        
          
           

#Ucitavanja podataka iz excel tablice u dataframe objekt(2d array)
#Header oznacava pocetak redaka tablice
tablicaNaloga = pd.read_excel('pregled radnih naloga 2019-10.xls', sheetname='List1', header=1)



#Brisanje objekta
vezaSaBazom.close()