import PySimpleGUI as sg
import os
#pocetni layout
layout = [ 
           [sg.Text('Tablica:')], 
           [sg.Button('Ucitaj tablicu'), sg.Button('Zatvori')]
         ]

def createLayout(tablica):
    #isti je kao i  prvi layout samo sto se dodatno ispisuje ime datoteke
    layoutNakonOdabiraDatoteke = [ 
               [sg.Text('Tablica: ' + tablica)], 
               [sg.Button('Ucitaj tablicu'), sg.Button("Izradi naloge"), sg.Button('Zatvori')]
                                 ]
    return layoutNakonOdabiraDatoteke


window = sg.Window("Izradi naloge").Layout(layout)


while True:
    event, values= window.Read()
    if event in (None, 'Zatvori'):
        break
    
    if event in (None, 'Ucitaj tablicu'):
        tablica = sg.PopupGetFile('Please enter a file name')
        window.close()
        
        #Iz nekog razloga se ne moze napraviti novi prozor sa istim layoutom
        window = sg.Window("Izradi naloge").Layout(createLayout(tablica))
        
    if event in (None, 'Izradi naloge'):    
        os.system("python3  Ucitaj\ iz\ excela\ u\ bazu.py")
        
    
window.close()
del window