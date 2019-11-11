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
df = df.append({'Ime' : 'Ivica', 'Prezime' : 'Kostelic', 'Broj mobitela' : '0981233244'},  ignore_index = True)
#df.fillna(0)
#df.isnull()


for i, j in df.iterrows(): #Iteracija kroz cijelu tablicu(df)
    print(i, j)
    print()
    
for i in df.columns:
    for j in range(4):
        print(df[i][j])
        