import PySimpleGUI as sg

layout = [ [sg.Listbox(values=sg.list_of_look_and_feel_values(),
                      size=(20, 12), key='-LIST-', enable_events=True)],
           [sg.Text('Upisite broj:')], [sg.Text(size=(5, 1)), sg.InputText('broj')],
           [sg.Submit(), sg.Button('Zatvori')]
         ]

window = sg.Window("Ja sam prozor").Layout(layout)

while True:
    event, values= window.Read()
    if event in (None, 'Zatvori'):
        break
    print(values[0])
    sg.change_look_and_feel(values['-LIST-'][0])
    
window.close()
del window