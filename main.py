import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from a_propos import AProposDialog  # Importer la classe AProposDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Bienvenue à l'App de Reconnaissance")
        self.setGeometry(200, 200, 600, 400)
        self.setWindowIcon(QIcon('logo.png'))  # Assurez-vous que 'logo.png' est disponible dans le répertoire

        # Initialisation de l'interface utilisateur
        self.initUI()

    def initUI(self):
        # Création d'un widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Création du layout
        layout = QVBoxLayout()

        # Ajout du logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("C:/Users/gadle/OneDrive/Bureau/MC-BABA/logo.png")  # Chemin vers le logo
        logo_pixmap = logo_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Redimensionner le logo
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Titre principal
        title_label = QLabel("MC BABA AYEEE!!!")
        title_label.setFont(QFont('Arial', 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")

        # Sous-titre
        subtitle_label = QLabel("Détection des gestes avec intelligence artificielle")
        subtitle_label.setFont(QFont('Verdana', 16))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d;")

        # Bouton pour démarrer la reconnaissance
        start_button = QPushButton("Commencer la reconnaissance")
        start_button.setFont(QFont('Arial', 18, QFont.Bold))
        start_button.setStyleSheet(""" 
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        start_button.clicked.connect(self.run_recognition)

        # Bouton pour la collecte de données
        data_collection_button = QPushButton("Collecte de données")
        data_collection_button.setFont(QFont('Arial', 18, QFont.Bold))
        data_collection_button.setStyleSheet(""" 
            QPushButton {
                background-color: #e67e22;
                color: white;
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        data_collection_button.clicked.connect(self.run_data_collection)

        # Bouton "À propos"
        about_button = QPushButton("À propos")
        about_button.setFont(QFont('Arial', 14))
        about_button.setStyleSheet(""" 
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        about_button.clicked.connect(self.show_about)

        # Bouton pour fermer l'application
        close_button = QPushButton("Fermer")
        close_button.setFont(QFont('Arial', 14))
        close_button.setStyleSheet(""" 
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_button.clicked.connect(self.close)

        # Ajout des widgets au layout
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(30)
        layout.addWidget(start_button)
        layout.addWidget(data_collection_button)
        layout.addWidget(about_button)  # Bouton "À propos"
        layout.addWidget(close_button)  # Ajout du bouton pour fermer

        # Définition du layout pour le widget central
        layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(layout)

    def run_recognition(self):
        # Exécution du fichier test.py
        script_path = os.path.join(os.getcwd(), "test.py")
        
        # Fermer la fenêtre principale
        self.close()

        # Exécuter le script test.py
        os.system(f'python "{script_path}"')

    def run_data_collection(self):
        # Fermer la fenêtre principale
        self.close()

        # Exécuter le script datacollection.py qui se trouve à la racine du projet
        script_path = os.path.join(os.getcwd(), "datacollection.py")
        os.system(f'python "{script_path}"')

    def show_about(self):
        # Créer une instance de la boîte de dialogue "À propos"
        about_dialog = AProposDialog(self)
        about_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()  # Plein écran au démarrage
    sys.exit(app.exec_())
