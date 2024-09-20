from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt

class AProposDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("À propos")
        self.setGeometry(0, 0, 800, 600)  # Dimensions de la fenêtre

        # Passer à plein écran
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        # Créer un widget central et une mise en page
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)  # Centrer les éléments

        title_label = QLabel("Application de Reconnaissance de Gestes")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #3498db; margin-bottom: 20px;")

        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 28px; color: #7f8c8d; margin-bottom: 10px;")

        description_label = QLabel("Cette application utilise l'intelligence artificielle pour reconnaître les gestes des mains.")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 22px; color: #2c3e50; margin-bottom: 20px;")

        project_info_label1 = QLabel("Ce projet a pour but de développer une application innovante de reconnaissance gestuelle.")
        project_info_label1.setAlignment(Qt.AlignCenter)
        project_info_label1.setWordWrap(True)
        project_info_label1.setStyleSheet("font-size: 20px; color: #2c3e50; margin-bottom: 15px;")

        project_info_label2 = QLabel("Les technologies utilisées incluent Python, OpenCV, et TensorFlow.")
        project_info_label2.setAlignment(Qt.AlignCenter)
        project_info_label2.setWordWrap(True)
        project_info_label2.setStyleSheet("font-size: 20px; color: #2c3e50; margin-bottom: 15px;")

        project_info_label3 = QLabel("L'application facilite la communication pour les personnes malentendantes.")
        project_info_label3.setAlignment(Qt.AlignCenter)
        project_info_label3.setWordWrap(True)
        project_info_label3.setStyleSheet("font-size: 20px; color: #2c3e50; margin-bottom: 30px;")

        dev_label = QLabel("Développé par Gad LELO.")
        dev_label.setAlignment(Qt.AlignCenter)
        dev_label.setStyleSheet("font-size: 24px; color: #7f8c8d; margin-bottom: 20px;")

        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;  /* Ajuster la taille du bouton */
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_button.clicked.connect(self.close)

        # Ajout des widgets à la mise en page
        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(description_label)
        layout.addWidget(project_info_label1)
        layout.addWidget(project_info_label2)
        layout.addWidget(project_info_label3)
        layout.addWidget(dev_label)
        layout.addWidget(close_button)

        # Ajouter le widget central à la boîte de dialogue
        self.setLayout(layout)
