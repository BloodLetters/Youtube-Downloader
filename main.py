import PySimpleGUI as sg
import pytube
import JsonReader

from SizeCalculation import Calculation

logs = 0
layout = [[sg.Text("")],
          [sg.Text("Youtube URL  "), sg.Input(key='-INPUT-'), sg.Button('View')],
          [sg.Text("Download Path"), sg.InputText(key='-FOLDER-'), sg.FolderBrowse(key="-BROWSE-")],
          [sg.Text("Resolution       "), sg.Combo(['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'], default_value='360p', key='Kualitas')],
          [sg.Text("")],
          [sg.Text("Title: ", size=(60, 1), key='-TITLE-')],
          [sg.Text("View: ", size=(40, 1), key='-VIEW-')],
          [sg.Text("Rating: ", size=(40, 1), key='-RATE-')],
          [sg.Text("Size: ", size=(40, 1), key='-SIZE-')],
          [sg.Text(size=(40, 1), key='-PNJG-')],
          [sg.Multiline(size=(65, 10), disabled=True, key="-LOG-")],
          [sg.Text("")],
          [sg.Button('Download'), sg.Button("Load Download Path", key="Load"), sg.Button('Save Download Path', key="save"), sg.Button('Quit')]]

window = sg.Window('Youtube video downloader!', layout)

while True:
    event, values = window.read()

    if event == "Load":
        if JsonReader.getPath() == "":
            logs = logs + 1
            window['-LOG-'].write(str(logs) + ". Save Url Is None!\n")
        else:
            if JsonReader.getPath() != "":
                window['-FOLDER-'].update(JsonReader.getPath())

    if event == "save":
        if window['-FOLDER-'].get == "":
            logs = logs + 1
            window['-LOG-'].write(str(logs) + ". You cannot save empty folder Path!\n")
        else:
            JsonReader.setFolder(window['-FOLDER-'].get())

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event == 'View':
        if window['-INPUT-'].get() == "":
            logs = logs + 1
            window['-LOG-'].write(str(logs) + ". Youtube Url Cant Empty!\n")
        elif "http" in window['-INPUT-'].get() or "https" in window['-INPUT-'].get():
            if "youtube" in window['-INPUT-'].get().lower():
                yt = pytube.YouTube(window['-INPUT-'].get())
                window['-TITLE-'].update("Title: " + yt.title)
                window['-VIEW-'].update("View: " + str(yt.views))
                window['-RATE-'].update("Rating: " + str(yt.rating))
                try:
                    window['-SIZE-'].update("Size: " + Calculation(yt.streams.filter(res=window['Kualitas'].get()).first().filesize))
                except AttributeError:
                    logs = logs + 1
                    window['-SIZE-'].update("Size: None")
                    window['-LOG-'].write(str(logs) + ". Video Does not have " + window['Kualitas'].get() + " Resolution\n")
            else:
                logs = logs + 1
                window['-LOG-'].write(str(logs) + ". Put youtube correct url!\n")
        else:
            logs = logs + 1
            window['-LOG-'].write(str(logs) + ". Put youtube correct url!\n")

    if event == "Download":
        if window['-INPUT-'].get() == "":
            logs = logs + 1
            window['-LOG-'].write(str(logs) + ". Youtube Url is None!\n")
        else:
            yt = pytube.YouTube(window['-INPUT-'].get())
            yt.streams.filter(res=window['Kualitas'].get()).first().download(JsonReader.getPath())

window.close()
