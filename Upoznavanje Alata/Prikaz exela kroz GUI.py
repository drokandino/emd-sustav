import PySimpleGUI as sg

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

text_za_prikaz = 'Tekst'


def ucitajExcel():
    df = pd.read_excel('Osobe.xlsx', sheet_5name='Sheet1')
    text_za_prikaz = df.columns
    return df

layout = [ 
           [sg.Button('Ucitaj excel'), sg.Button('Zatvori')], 
           [sg.Text(text_za_prikaz, size=(40, 10), auto_size_text = True, key='_TEXT_')]
           
         ]

window = sg.Window("Ja sam prozor").Layout(layout)

sg.Text('Ucitaj excel').Update("bla")
while True:
    event, values= window.Read()
    #window.Finalize()
    window.Element('_TEXT_').Update(text_za_prikaz)
    print(text_za_prikaz)
    
    if event in (None, 'Zatvori'):
        break
    if event == 'Ucitaj excel':
       df = ucitajExcel()
       text_za_prikaz = str(df.loc[1])
    
window.close()
del window
