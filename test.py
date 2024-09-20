import sys
import os
import cv2
import numpy as np
import tensorflow as tf
from cvzone.HandTrackingModule import HandDetector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt

# Chargement du modèle TensorFlow
def custom_load_model(model_path):
    custom_objects = {
        'DepthwiseConv2D': lambda **kwargs: tf.keras.layers.DepthwiseConv2D(
            **{k: v for k, v in kwargs.items() if k != 'groups'}
        )
    }
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)

class CustomClassifier:
    def __init__(self, model, labels_path):
        self.model = model
        self.input_size = (224, 224)  # Taille d'entrée attendue par le modèle
        with open(labels_path, 'r') as file:
            self.labels = [line.strip() for line in file]

    def get_prediction(self, img):
        img_resized = cv2.resize(img, self.input_size)  # Redimensionner l'image
        img_array = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = tf.expand_dims(img_array, 0)
        
        predictions = self.model.predict(img_array)
        index = np.argmax(predictions[0])
        return predictions[0], index

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Détection de Signes")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialisation du détecteur de mains et du modèle
        self.detector = HandDetector(maxHands=1)
        model_path = r"C:\Users\gadle\OneDrive\Bureau\Projet_final\Model\keras_model.h5"
        labels_path = r"C:\Users\gadle\OneDrive\Bureau\Projet_final\Model\labels.txt"
        self.model = custom_load_model(model_path)
        self.classifier = CustomClassifier(self.model, labels_path)
        
        # Initialisation de la caméra
        self.vid = cv2.VideoCapture(0)
        
        # Configuration de l'interface utilisateur
        self.initUI()
        
        # Timer pour la mise à jour de la vidéo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Configuration des widgets pour l'image et le texte
        self.image_widget = QWidget()
        self.result_widget = QWidget()
        
        self.image_layout = QVBoxLayout()
        self.result_layout = QVBoxLayout()
        
        self.image_label = QLabel()
        self.image_label.setFont(QFont('Arial', 16))
        self.image_layout.addWidget(self.image_label)
        self.image_widget.setLayout(self.image_layout)
        
        self.result_label = QLabel("Aucune main détectée")
        self.result_label.setFont(QFont('Arial', 24))
        self.result_layout.addWidget(self.result_label)
        self.result_widget.setLayout(self.result_layout)
        
        # Bouton pour la collecte de données
        self.data_collection_button = QPushButton("Collecte de données")
        self.data_collection_button.setFont(QFont('Arial', 16))
        self.data_collection_button.setStyleSheet("""QPushButton {
            background-color: #f39c12; 
            color: white; 
            border-radius: 10px;  
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #e67e22; 
        }""")
        self.data_collection_button.clicked.connect(self.run_data_collection)
        self.result_layout.addWidget(self.data_collection_button)

        # Bouton pour quitter l'application
        self.quit_button = QPushButton("Quitter")
        self.quit_button.setFont(QFont('Arial', 16))
        self.quit_button.setStyleSheet("""QPushButton {
            background-color: #e74c3c; 
            color: white; 
            border-radius: 10px;  
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #c0392b; 
        }""")
        self.quit_button.clicked.connect(self.close)
        self.result_layout.addWidget(self.quit_button)
        
        self.layout.addWidget(self.image_widget)
        self.layout.addWidget(self.result_widget)
        
        self.image_widget.setMinimumWidth(400)
        self.result_widget.setMinimumWidth(400)

    def update_frame(self):
        ret, frame = self.vid.read()
        if not ret:
            return
        
        imgOutput = frame.copy()
        hands, frame = self.detector.findHands(frame)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgSize = 300
            offset = 20

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

            try:
                y1, y2 = max(0, y - offset), min(frame.shape[0], y + h + offset)
                x1, x2 = max(0, x - offset), min(frame.shape[1], x + w + offset)
                imgCrop = frame[y1:y2, x1:x2]

                aspectRatio = h / w
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = int(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = (imgSize - wCal) // 2
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = int(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = (imgSize - hCal) // 2
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                imgWhite_resized = cv2.resize(imgWhite, (224, 224))
                prediction, index = self.classifier.get_prediction(imgWhite_resized)

                cv2.rectangle(imgOutput, (x-offset, y-offset-70), (x-offset+400, y-offset+60-50), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgOutput, self.classifier.labels[index], (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                cv2.rectangle(imgOutput, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

                self.result_label.setText(self.classifier.labels[index])

            except Exception as e:
                print(f"Erreur lors du traitement de la main : {e}")

        # Convertir l'image pour PyQt
        frame_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Ajuster la taille de l'image pour s'adapter au QLabel tout en conservant le rapport d'aspect
        scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)

    def run_data_collection(self):
        # Fermer la fenêtre principale
        self.close()

        # Exécuter le script datacollection.py
        script_path = os.path.join(os.getcwd(), "datacollection.py")
        os.system(f'python "{script_path}"')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
