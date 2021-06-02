from typing import Sized
import PySimpleGUIQt as sg
from PIL import Image
import os.path
import io
from numpy.core.fromnumeric import resize
import tensorflow
from tensorflow.keras.models import Model
import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
import numpy as np

model = tensorflow.keras.models.load_model('modelaug.hdf5')


# def open_cam():
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Can't receive frame")
#         break
#     rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#     cv2.imshow('frame',rgb)
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyALWindows()

def classify_image(imgpath):
    img = cv2.imread(imgpath)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    x = image.img_to_array(rgb_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    prediction = np.argmax(preds)
    return prediction


layout = [
    [sg.Text('', pad=(0,0),key='-EXPAND2-'), sg.Image('icon.png'),sg.Text('', pad=(0,0),key='-EXPAND-')],
    [sg.Text("Student Name: "), sg.Input(key='-STUDENTNAME-')],
    [sg.Text("Student Number"), sg.Input(key='-STUDENTNUMBER-')],
    [sg.Button('Submit')]]

# menulayout = [
#     [sg.Image('icon.png')],
#     [sg.Text(text='Placeholder', key='-MSG-')],
#     [sg.Button('Classification'), sg.Button('Detection')]
# ]

# file_list_column = [
#     [
#         sg.Text("Image Folder"),
#         sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
#         sg.FolderBrowse(),
#     ],
#     [
#         sg.Listbox(
#             values=[], enable_events=True, size=(40, 20),
#             key='-FILE_LIST-'
#         )
#     ],
#     [
#         sg.Button('Process'),
#
#     ],
#     [
#         sg.Text('Classification: ')
#     ]
# ]
# image_viewer_column = [
#     [sg.Text('Choose an image from the selected directory on the left')],
#     [sg.Text(size=(40, 1), key='-TOUT-')],
#     [sg.Image(key='-IMAGE-')],
# ]
# classlayout = [
#     [
#         sg.Column(file_list_column),
#         sg.VSeperator(),
#         sg.Column(image_viewer_column),
#     ]
# ]
# detlayout = [
#     [
#         sg.Image(filename='', key='image')
#     ],
#     [
#         sg.Button('Start Camera')
#     ]
# ]

window = sg.Window("Mask Master", layout).Finalize()
window.maximize()
win1_active = False
win2_active = False
win3_active = False
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == 'Submit' and win1_active == False:
        win1_active = True
        ilayout = [
            [sg.Text('', pad=(0,0),key='-EXPAND2-'), sg.Image('icon.png'),sg.Text('', pad=(0,0),key='-EXPAND-')],
            [sg.Text(text='Placeholder', key='-MSG-')],
            [sg.Button('Classification'), sg.Button('Detection')]
        ]
        message = "Welcome: " + values["-STUDENTNAME-"] + ", " + values["-STUDENTNUMBER-"]
        window.Hide()
        window1 = sg.Window("Mask Master", ilayout).Finalize()
        window1["-MSG-"].update(message)
        window1.maximize()
        while True:
            ev2, vals2 = window1.Read()
            if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
                window1.Close()
                win1_active = False
                window.UnHide()
                break
            if ev2 == 'Classification' and win2_active == False:
                window1.Hide()
                win2_active = True
                file_list_column = [
                    [
                        sg.Text("Image Folder"),
                        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
                        sg.FolderBrowse(),
                    ],
                    [
                        sg.Listbox(
                            values=[], enable_events=True, size=(40, 10),
                            key='-FILE_LIST-'
                        )
                    ],
                    [
                        sg.Button('Process'),

                    ],
                    [
                        sg.Text('Classification: '), sg.Text('', key='-CLASSRESULT')
                    ]
                ]
                image_viewer_column = [
                    [sg.Text('Choose an image from the selected directory on the left')],
                    [sg.Text(size=(40, 1), key='-TOUT-')],
                    [sg.Image(key='-IMAGE-')],
                ]
                classlayout = [
                    [
                        sg.Column(file_list_column),
                        sg.VSeperator(),
                        sg.Column(image_viewer_column),
                    ]
                ]
                window2 = sg.Window("Mask Master", classlayout).Finalize()
                window2.maximize()
                while True:
                    ev3, vals3 = window2.Read()
                    if ev3 == sg.WIN_CLOSED or ev3 == 'Exit':
                        window2.Close()
                        win2_active = False
                        window1.UnHide()
                        break
                    if ev3 == 'Process':
                        result = classify_image(filename)
                        window2['-CLASSRESULT-'].update(result)
                        print(result)

                    if ev3 == "-FOLDER-":
                        folder = vals3["-FOLDER-"]
                        try:
                            file_list = os.listdir(folder)
                        except:
                            file_list = []
                        fnames = [
                            f
                            for f in file_list
                            if
                            os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(
                                (".png", ".jpg", ".jpeg", ".tiff", ".bmp"))

                        ]
                        window2["-FILE_LIST-"].update(fnames)
                    elif ev3 == "-FILE_LIST-":
                        try:
                            filename = os.path.join(
                                vals3["-FOLDER-"], vals3["-FILE_LIST-"][0]
                            )
                            window2["-TOUT-"].update(filename)
                            window2["-IMAGE-"].update(filename=filename)
                        except:
                            pass
            elif ev2 == 'Detection' and win3_active == False:
                window1.Hide()
                window3 = sg.Window("Demo", location=(800, 400))
                detlayout = [
                    [
                        sg.Image(filename='', key='image')
                    ],
                    [
                        sg.Button('Start Camera')
                    ]
                ]
                window3.Layout(detlayout).Finalize()
                window3.Maximize()

                # window2 = sg.Window("Mask Master", detlayout)
                # window2.Finalize()

                cap = cv2.VideoCapture(0)

                while True:
                    event, values = window3.Read()
                    if event is 'Exit' or values is None:
                        break
                    ret, frame = cap.read()
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(rgb)
                    bio = io.BytesIO()

                    imgbytes = bio.getvalue()
                    window3.FindElement('image').Update(data=imgbytes)

        # window['-MSG-'].update(message)
    # if event == 'Classification':
    #     window1.Hide()
    #     window2 = sg.Window("Mask Master", classlayout, resizable=False, location=(800, 400)).Finalize()


    # if event == 'Process':
    #     result = classify_image(filename)
    #     print(result)
    #
    # if event == "-FOLDER-":
    #     folder = values["-FOLDER-"]
    #     try:
    #         file_list = os.listdir(folder)
    #     except:
    #         file_list = []
    #     fnames = [
    #         f
    #         for f in file_list
    #         if
    #         os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp"))
    #
    #     ]
    #     window2["-FILE_LIST-"].update(fnames)
    # elif event == "-FILE_LIST-":
    #     try:
    #         filename = os.path.join(
    #             values["-FOLDER-"], values["-FILE_LIST-"][0]
    #         )
    #         window2["-TOUT-"].update(filename)
    #         window2["-IMAGE-"].update(filename=filename)
    #     except:
    #         pass

window.close()