from mysql.connector import MySQLConnection, Error

vezaSaBazom = MySQLConnection(host='localhost', port="3333",
                               database='emd',
                               user='root', password='1234')

#Incijalizacija cursor objekta
cursor = vezaSaBazom.cursor()

def upisiUBazu(imeTablice, imenaAtributa, atributi):
    returnValue = True
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
    except (Error, IndexError) as error:
        print(error)
        returnValue = False

    return returnValue