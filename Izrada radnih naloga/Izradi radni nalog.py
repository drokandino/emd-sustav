from mysql.connector import MySQLConnection, Error
from openpyxl import load_workbook


try:
    #Povezivanje sa bazom
    vezaSabazom = MySQLConnection(host='localhost',
                                   database='emd_novi',
                                   user='root', password='1')
    
    #Cursor objekti za sljanje upita bazi
    cursor = vezaSabazom.cursor(buffered=True)
    cursor2 = vezaSabazom.cursor(buffered=True)
    
# =============================================================================
#     #Izvrsavanje upita
#     cursor.execute('SELECT * FROM radniNalog;')
#     
#     #Uzima redak iz izalza prethodng upita. Taj redak pretvara u array
#     redak = cursor.fetchone()
# =============================================================================
    
# =============================================================================
#     #Zapisivanje u datoteku
#     file.write("Broj radnog naloga: " + str(redak[0]) + "\n" +
#                "Broj narudzbe: " + str(redak[1]) + "\n" +
#                "Nacrt: " + str(redak[2]) + "\n")
#     
# =============================================================================
    
# =============================================================================
#     #Dohvacanje podataka za isti radni nalog iz druge tablice
#     pomocniCursor.execute('SELECT * FROM proizvod WHERE nacrt = "' + str(redak[2]) + '";')
#     redak2 = pomocniCursor.fetchone()
#     print(redak2)
# =============================================================================
    

except Error as error:
    print(error)


    

try:
    #While petlja prolazi kroz svaki nalog
    cursor.execute('SELECT brojNaloga FROM radniNalog')
    while True:
        nalog = cursor.fetchone()
        if nalog == None:
            break
        
        #Ucitavanje template objekta i ucitavanje sheet-a
        nalogTemplate = load_workbook('Primjeri naloga/radni nalog template.xlsx') #Work book
        sheet = nalogTemplate.get_sheet_by_name("List1")    
        
        #Zapisivanje broja naloga
        sheet['J1'] = nalog[0]
        
        #Dohvacanje svih nacrta(proizvoda) koji pripadaju trenutnom radnom nalogu
        cursor2.execute('SELECT nacrt FROM nalogPozicija WHERE nalog = "' + str(nalog[0])+'";')
        nacrti = cursor2.fetchall()
        
        #Za svaki prethodno dohvanceni nacrt, dohvati iz baze naziv proizvoda, materijal, cnc
        for i in range(len(nacrti)):
            cursor2.execute('SELECT naziv FROM pozicija WHERE nacrt= "' + str(nacrti[i][0])+'";')    
            naziv = cursor2.fetchall()
            
            #Zapisivanje u excel(template) nacrta i naziva
            sheet['C'+str(11+i)] = nacrti[i][0]
            sheet['B'+str(11+i)] = naziv[0][0]  
            
            #Dohvacanje matetrijala iz baze i pisanje u nalog
            cursor2.execute('SELECT idMaterijal FROM pozicija WHERE nacrt= "' + str(nacrti[i][0])+'";')
            materijal = cursor2.fetchall()
            sheet['D'+str(11+i)] = materijal[0][0]
            sheet['B5'] = materijal[0][0]
            
            cursor2.execute('SELECT dimenzija, duljina FROM pozicija WHERE nacrt = "' + str(nacrti[i][0])+'";')
            dimenzijaDuljina = cursor2.fetchall()
            sheet['E' + str(i + 11)] = dimenzijaDuljina[0][0]
            sheet['F' + str(i + 11)] = dimenzijaDuljina[0][1]
            
            #Dohvacanje cnc tehnologija i pisanje isith u nalog
            cursor2.execute('SELECT cnc FROM tehnologijaPozicija WHERE nacrt= "' + str(nacrti[i][0])+'";')
            cnc = cursor2.fetchall()
            cnc_lista = []
            
            cnc_lista.append(cnc[0][0]) 
            
            if cnc[0][0] == 'nema':
                cnc_lista[0] = ''
            if len(cnc) > 1 and cnc[1][0] == 'nema':
                cnc_lista[1]= ''
            
            
            if len(cnc) > 1:
                cnc_lista.append(cnc[1][0])
                sheet['J' + str(11+i)] = cnc_lista[0] +'+' + cnc_lista[1]
                sheet['B' + str(6+i)] = cnc_lista[0] +'+' + cnc_lista[1]
            else:
                sheet['J' + str(11+i)] = cnc_lista[0]
            
            #Zapisivanje rednog broja
            cursor2.execute('SELECT redniBr FROM pozicija WHERE nacrt= "' + str(nacrti[i][0])+'";')
            redniBr = cursor2.fetchone()
            sheet['A' + str(11+i)] = redniBr[0]
            
# =============================================================================
#             cursor2.execute('SELECT narudzba FROM nalogNarudzba WHERE nalog= "' + str(nalog[0])+'";')
#             narudzbe = cursor2.fetchall()
#             print(len(narudzbe), narudzbe[], len(nacrti))
#             
#             if len(narudzbe) == len(nacrti):
#                 cursor2.execute('SELECT rok FROM narudzba WHERE narudzbenica= "' + str(narudzbe[i][0])+'";')
#             elif len(narudzbe) < len(nacrti):
#                cursor2.execute('SELECT rok FROM narudzba WHERE narudzbenica= "' + str(narudzbe[0][0])+'";')
#                    
#             rok = cursor2.fetchone()
#             print(rok)
#             #sheet['K' + str(11+i)] = rok[0][0]
# =============================================================================
            
            #Zapisivanje roka u nalog
            #Nalog br. 176, 166 imaju zapisan krivi datum
            cursor2.execute('SELECT rok FROM narudzba JOIN pozicijaNarudzba USING(narudzbenica) WHERE nacrt = "' + str(nacrti[i][0])+'";')
            rok = cursor2.fetchone()
            
            #Zbog nekog razloga jedan redak iz prethodnog upita je None
            #To je za randi nalog 180. Taj radni nalog nema nacrt
            if rok != None:
                sheet['K' + str(11+i)] = rok[0]
                print(rok[0])
                
        #Spremi kao novi file
        nalogTemplate.save('Radni nalog ' + str(nalog[0]) + '.xlsx')

            
except Error as error:
    print(error)
    


cursor.close()
vezaSabazom.close()