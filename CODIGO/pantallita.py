import pickle

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl

import speech_recognition as sr

import nltk
import moviepy.editor as mp
from pydub.utils import make_chunks

import os
from pydub import AudioSegment

import time

import PopUp as pu


video = ""

class Window(QWidget):
    def __init__(self, app):
        super().__init__()



        self.app = app
        self.setWindowTitle("Thinking Out Loud - Práctica 1 - Sistemas Inteligentes")
        self.setGeometry(650, 100, 1100, 900)
        self.setWindowIcon(QIcon('player.png'))


        p = self.palette()
        p.setColor(QPalette.Window, Qt.white)
        self.setPalette(p)

        self.init_ui()

        self.show()


    def init_ui(self):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        self.guardarCambios = QPushButton('GUARDAR CAMBIOS')
        self.guardarCambios.setDisabled(True)

        self.sugerirCodigos = QPushButton('SUGERIR CÓDIGOS')
        self.sugerirCodigos.setDisabled(True)

        self.guardarCambios.setStyleSheet('QPushButton {background-color: #F64F1A; color: black; font-weight: bold;}')
        self.sugerirCodigos.setStyleSheet('QPushButton {background-color: #F64F1A; color: black; font-weight: bold;}')
        self.guardarCambios.clicked.connect(self.guardarCambiosFunc)#TODO pasarle la funcion
        self.sugerirCodigos.clicked.connect(self.abrir_ventana)#TODO pasarle la funcion

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.textbox = QLabel("Selecciona un video para iniciar el proceso, gracias.\nMientras no haya video, los Botones Inferiores estarán deshabilitados", self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.textbox.setFixedWidth(1100)
        self.textbox.setFixedHeight(400)


        self.lista = []

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        secondHboxLayout = QVBoxLayout()
        secondHboxLayout.setContentsMargins(10, 10, 10, 10)

        thirdHboxLayout = QHBoxLayout()
        thirdHboxLayout.setContentsMargins(10, 10, 10, 10)


        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        secondHboxLayout.addWidget(self.textbox)
        thirdHboxLayout.addWidget(self.guardarCambios)
        thirdHboxLayout.addWidget(self.sugerirCodigos)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(secondHboxLayout)
        vboxLayout.addLayout(thirdHboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            audio = self.video_to_audio(filename)
            self.lista = self.transcription("gopro.wav")
            file1 = open("temporal.txt", "a+")
            file1.close()
            if len(self.lista) != 0:
                print(len(self.lista))
                print(self.lista)
                with open('temporal.txt', 'w') as file2:
                    for lista in self.lista:
                        file2.write('%s\n' % lista)
            file2.close()
            self.textbox.setText("")


    def guardarCambiosFunc(self):

        ficheroNuevo = open("temporal.txt", "r")
        contenido = ficheroNuevo.read()
        print(contenido)
        pathGuardarModelo = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        print(pathGuardarModelo)
        with open(pathGuardarModelo+'/Transcripcion.txt', 'wb') as f:
            pickle.dump(contenido, f)

        ficheroNuevo.close()


    def video_to_audio(self, path):
        miVideo = mp.VideoFileClip(path)
        hola = miVideo.audio.write_audiofile("gopro.wav")
        return hola


    def transcription(self, path):

        myaudio = AudioSegment.from_file(path, "wav")
        chunk_length_ms = 26000
        chunks = make_chunks(myaudio, chunk_length_ms)

        folder_name = "audio-chunks"

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        for i, chunk in enumerate(chunks):
            chunk_name = os.path.join(folder_name, f"chunk{i}.wav")
            chunk.export(chunk_name, format="wav")
        print("Chunks exportados correctamente...")
        r = sr.Recognizer()
        whole_text = ""
        lista_chunks = []
        file1 = open("chunks.txt", "a")
        for i, audio_chunk in enumerate(chunks, start=0):  # Antes era 1

            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                try:
                    text = r.recognize_google(audio_listened, language='es-ES')
                    print('chunk', i)
                    tokenizar = nltk.word_tokenize(text)  # lista
                    y = 0
                    while y < len(tokenizar):
                        if tokenizar[y] == 'giro' and tokenizar[y + 1] == 'derecha':
                            tokenizar.insert(y + 2, '<SW-TL-R>')
                        elif tokenizar[y] == 'giro' and tokenizar[y + 1] == 'izquierda':
                            tokenizar.insert(y + 2, '<SW-TL-L>')
                        elif tokenizar[y] == 'subo' and tokenizar[y + 1] == 'marcha':
                            tokenizar.insert(y + 2, '<GU>')
                        elif tokenizar[y] == 'bajo' and tokenizar[y + 1] == 'marcha':
                            tokenizar.insert(y + 2, '<GD>')
                        elif tokenizar[y] == 'bajo' and tokenizar[y + 1] == 'de' and tokenizar[y + 2] == 'marcha':
                            tokenizar.insert(y + 3, '<GD>')
                        elif tokenizar[y] == 'intermitente' and tokenizar[y + 1] == 'izquierda':
                            tokenizar.insert(y + 2, '<LB-ON>')
                        elif tokenizar[y] == 'intermitente' and tokenizar[y + 1] == 'derecha':
                            tokenizar.insert(y + 2, '<RB-ON>')
                        elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'embrague':
                            tokenizar.insert(y + 2, '<G-ON>')
                        elif tokenizar[y] == 'suelto' and tokenizar[y + 1] == 'embrague':
                            tokenizar.insert(y + 2, '<G-OFF>')
                        elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'acelerador':
                            tokenizar.insert(y + 2, '<T-ON>')
                        elif tokenizar[y] == 'suelto' and tokenizar[y + 1] == 'acelerador':
                            tokenizar.insert(y + 2, '<T-OFF>')
                        elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'freno':
                            tokenizar.insert(y + 2, '<B-ON>')
                        elif tokenizar[y] == 'piso' and tokenizar[y + 1] == 'frenos':
                            tokenizar.insert(y + 2, '<B-ON>')
                        elif tokenizar[y] == 'suelto' and tokenizar[y + 1] == 'freno':
                            tokenizar.insert(y + 2, '<B-OFF>')
                        ##CODIGOS DE ESTIMULOS
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'frente':
                            tokenizar.insert(y + 2, '<FV>')
                        elif tokenizar[y] == 'mira' and tokenizar[y + 1] == 'enfrente':
                            tokenizar.insert(y + 2, '<FV>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'retrovisor' and tokenizar[
                            y + 2] == 'central':
                            tokenizar.insert(y + 3, '<FV-MIRROR>')
                        elif tokenizar[y] == 'mira' and tokenizar[y + 1] == 'retrovisor' and tokenizar[
                            y + 2] == 'central':
                            tokenizar.insert(y + 3, '<FV-MIRROR>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'central':
                            tokenizar.insert(y + 2, '<FV-MIRROR>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'izquierda':
                            tokenizar.insert(y + 2, '<LV>')
                        elif tokenizar[y] == 'retrovisor' and tokenizar[y + 1] == 'izquierda':
                            tokenizar.insert(y + 2, '<LV-MIRROR>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'retrovisor' and tokenizar[
                            y + 2] == 'izquierda':
                            tokenizar.insert(y + 3, '<LV-MIRROR>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'frente' and tokenizar[
                            y + 2] == 'izquierda':
                            tokenizar.insert(y + 3, '<FLV>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'derecha':
                            tokenizar.insert(y + 2, '<RV>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'retrovisor' and tokenizar[
                            y + 2] == 'derecha':
                            tokenizar.insert(y + 3, '<RV-MIRROR>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'frente' and tokenizar[y + 2] == 'derecha':
                            tokenizar.insert(y + 3, '<FRV>')
                        elif tokenizar[y] == 'miro' and tokenizar[y + 1] == 'detras':
                            tokenizar.insert(y + 2, '<BV>')
                            #LIMPIEZA TEXTO
                        elif tokenizar[y] == '[':
                            tokenizar.insert('')
                        elif tokenizar[y] == ']':
                            tokenizar.insert('')
                        elif tokenizar[y] == ',':
                            tokenizar.insert(' ')
                        elif tokenizar[y] == '\'':
                            tokenizar.insert('')

                        y = y + 1

                    lista_chunks.insert(i, tokenizar)

                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text} "

                    whole_text += text
                    whole_text += '\n'
        x = 0
        while x < len(lista_chunks):
            print('Chunk' + str(x) + ': ' + str(lista_chunks[x]))
            print('\n\n')
            x = x + 1

        self.guardarCambios.setDisabled(False)
        self.sugerirCodigos.setDisabled(False)

        return lista_chunks

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()#TODO STOP
            print('STOPPED VIDEO')
        else:

            self.rellenarLabel()
            self.app.processEvents()
            self.mediaPlayer.play()
            print('VIDEO PLAYING')

    def rellenarLabel(self):
        f = open("temporal.txt", "r")
        content = f.read()
        self.textbox.setText(content)
        f.close()

    def abrir_ventana(self):

        self.window = QtWidgets.QMainWindow()
        self.ui = pu.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
            

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


app = QApplication(sys.argv)
window = Window(app)
sys.exit(app.exec_())

