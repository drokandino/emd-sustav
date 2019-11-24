import mysql.connector
from mysql.connector import Error

#Funkcija koja spaja mysql bazu
def connectDatabase():
    connection = None
    
    try:
        #connect() metoda se povezuje sa bazom i vraca MySQLConnection objekt
        #Prima argumente o nacinu spajanja sa bazom
        connection = mysql.connector.connect(host='localhost',
                                       database='python_mysql',
                                       user='root')
                                       
        #Ako je uspjesno uspostavjena veza sa bazom ispisat ce se potvrda poruka
        if connection.is_connected():
            print('Connected to MySQL database')
            
        #Instanciranje cursor objketa preko connection objekta
        #cursor objekt služi za izvršavanje SQL naredbi
        cursor = connection.cursor()
        #Izvršavanje SQL upita u bazi, izabire sve stupce iz relacije books
        cursor.execute("SELECT * FROM books")
        
        #fetchone() vraca sljedeci redak iz tablice, kao listu python objekata
        redak = cursor.fetchone()
        #Printa sve retke iz SQL upita
        while redak is not None:
            print(redak)
            redak = cursor.fetchone()
            
 
    #Hvata exception i printa ga
    except Error as e:
        print(e)
 
    #Ako je veza sa bazom uspjesna, zatvori konekciju
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
 
 
connectDatabase()