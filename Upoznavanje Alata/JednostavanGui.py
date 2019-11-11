import PySimpleGUI as sg

layout = [ [sg.Text('Upisite broj:')], [sg.Text(size=(5, 1)), sg.InputText('broj')],
           [sg.Submit()]
         ]

window = sg.Window("Ja sam prozor").Layout(layout)
button, values = window.Read()

print(button, values[0])