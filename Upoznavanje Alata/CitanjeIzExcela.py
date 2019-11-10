import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('Osobe.xlsx', sheetname='Sheet1') #df --> Data frame objekt

print("Imena stupaca")
print(df.columns)

lista_imena = df['Ime']#Lista vrijednosti iz stupca Ime za svaki redak
print(lista_imena) 
print("")

for i in df.index:
    if lista_imena[i] == 'Marica':
        print(df['Broj mobitela'][i], "\n")
        
print(df.loc[2]) #Ispisuje redak iz tablice

##Dodavanje retka u data frame
df = df.append({'Ime' : 'Ivica', 'Prezime' : 'Kostelic'},  ignore_index = True)
