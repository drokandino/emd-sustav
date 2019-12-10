from mysql.connector import MySQLConnection, Error

#Trenutna verzija pise u txt datoteku
#file postaje objekt pomocu kojeg se manipulira datoteka, "w" - write
file = open("Radni Nalog.txt", "w")


try:
    #Povezivanje sa bazom
    vezaSabazom = MySQLConnection(host='localhost',
                                   database='emd',
                                   user='root', password='1')
    
    #Cursor objekti za sljanje upita bazi
    cursor = vezaSabazom.cursor(buffered=True)
    pomocniCursor = vezaSabazom.cursor(buffered=True)
    
    #Izvrsavanje upita
    cursor.execute('SELECT * FROM radniNalog;')
    
    #Uzima redak iz izalza prethodng upita. Taj redak pretvara u array
    redak = cursor.fetchone()
    
    #Zapisivanje u datoteku
    file.write("Broj radnog naloga: " + str(redak[0]) + "\n" +
               "Broj narudzbe: " + str(redak[1]) + "\n" +
               "Nacrt: " + str(redak[2]) + "\n")
    
    #Dohvacanje podataka za isti radni nalog iz druge tablice
    pomocniCursor.execute('SELECT * FROM proizvod WHERE nacrt = "' + str(redak[2]) + '";')
    redak2 = pomocniCursor.fetchone()
    print(redak2)
    


except Error as error:
    print(error)



cursor.close()
vezaSabazom.close()