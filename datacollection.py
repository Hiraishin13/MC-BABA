import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Paramètres de la fenêtre principale
        self.setWindowTitle("Application de capture d'images")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2E3440; color: #ECEFF4;")  # Couleurs modernes

        self.cap = None  # Initialisation retardée de la caméra
        self.detector = None  # Initialisation retardée du détecteur
        self.offset = 20
        self.imgSize = 300
        self.counter = 0
        self.folder = self.create_local_folder()
        self.imgWhite = None

        # Layout principal
        main_layout = QHBoxLayout()

        # Layout pour la vidéo
        video_layout = QVBoxLayout()

        # Label pour afficher le flux vidéo
        self.video_label = QLabel(self)
        self.video_label.setGeometry(150, 20, 640, 480)
        self.video_label.setStyleSheet("border: 3px solid #88C0D0; border-radius: 10px;")  # Style moderne
        video_layout.addWidget(self.video_label)

        # Bouton pour capturer l'image
        self.capture_button = QPushButton("Capturer l'image", self)
        self.capture_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 16px; border-radius: 15px; padding: 15px;")
        self.capture_button.clicked.connect(self.capture_image)
        video_layout.addWidget(self.capture_button)

        # Bouton pour quitter l'application
        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setStyleSheet(
            "background-color: #f44336; color: white; font-size: 16px; border-radius: 15px; padding: 15px;")
        self.quit_button.clicked.connect(self.close)
        video_layout.addWidget(self.quit_button)

        # Ajouter le layout vidéo au layout principal
        main_layout.addLayout(video_layout)

        # Label pour afficher les messages
        self.message_label = QLabel(self)
        self.message_label.setStyleSheet("font-size: 16px; padding: 15px;")
        main_layout.addWidget(self.message_label)

        # Widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer pour mettre à jour l'affichage vidéo
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_frame)
        self.timer.start(10)

        # Message initial
        self.message_label.setText("Appuyez sur 'Capturer l'image' pour prendre une photo.")

    def create_local_folder(self):
        # Définir un dossier par défaut pour stocker les images capturées
        folder = r"C:\Users\gadle\OneDrive\Bureau\Projet_final\Data"
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def start_camera(self):
        # Initialiser la caméra et le détecteur de main
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)

    def show_frame(self):
        if self.cap is None or self.detector is None:
            self.start_camera()  # Lancer la caméra si elle n'est pas encore démarrée

        success, img = self.cap.read()
        if not success:
            return  # Si la capture échoue, on sort de la fonction
        
        hands, img = self.detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            # Créer une image blanche
            self.imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255

            # Découper l'image autour de la main
            imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]

            # Vérifier que l'image découpée a des dimensions valides
            if imgCrop.size != 0:
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = self.imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))  # Redimensionner l'image découpée
                    wGap = math.ceil((self.imgSize - wCal) / 2)
                    self.imgWhite[:, wGap:wCal + wGap] = imgResize

                else:
                    k = self.imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))  # Redimensionner l'image découpée
                    hGap = math.ceil((self.imgSize - hCal) / 2)
                    self.imgWhite[hGap:hCal + hGap, :] = imgResize

            else:
                print("Erreur : imgCrop est vide ou invalide.")

        # Convertir l'image en format compatible avec PyQt5
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.video_label.setPixmap(pixmap)

    def capture_image(self):
        if self.imgWhite is not None:
            self.counter += 1
            image_path = os.path.join(self.folder, f"Image_{time.time()}.jpg")
            cv2.imwrite(image_path, self.imgWhite)
            self.message_label.setText(f"Image {self.counter} capturée et sauvegardée à {image_path}.")
        else:
            self.message_label.setText("Aucune image à capturer.")

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

# Exécuter l'application
app = QApplication(sys.argv)
window = MainWindow()
window.showFullScreen()
sys.exit(app.exec_())
