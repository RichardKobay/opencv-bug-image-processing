from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from typing import Optional
from src.image_processing import process

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_path: Optional[str] = None
        self.raw_image: QImage = None
        self.processed_image: QImage = None
        self.init_ui()
        self.showMaximized()
    
    def init_ui(self):
        self.setWindowTitle("Bug detection")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        """Initialize the buttons layout"""
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        open_image_button = QPushButton("Open Image")
        open_image_button.clicked.connect(self.open_image)
        button_layout.addWidget(open_image_button)

        process_image_button = QPushButton("Process Image")
        process_image_button.clicked.connect(self.process_image)
        button_layout.addWidget(process_image_button)

        restore_changes_button = QPushButton("Restore Changes")
        restore_changes_button.clicked.connect(self.restore_image)
        button_layout.addWidget(restore_changes_button)

        """Initialize the image label"""
        self.image_label = QLabel("There's not a selected image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

    def open_image(self):
        """
        Open a file dialog to select an image and display it in the image label
        """
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if self.image_path:
            self.raw_image = QImage(self.image_path)
            self.update_image_label(self.raw_image)

    def process_image(self):
        """
        Process the image and display the processed image in the image label
        """
        if self.image_path:
            processed_cv_image = process(self.image_path)
            height, width, _ = processed_cv_image.shape
            bytes_per_line = 3 * width
            self.processed_image = QImage(processed_cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.update_image_label(self.processed_image)

    def restore_image(self):
        """
        Restore the original image in the image label
        """
        if self.raw_image:
            self.update_image_label(self.raw_image)

    def resizeEvent(self, event):
        """
        Resize the image label when the main window is resized
        """
        if self.raw_image:
            self.update_image_label(self.raw_image)
        elif self.processed_image:
            self.update_image_label(self.processed_image)
        super().resizeEvent(event)

    def update_image_label(self, image: QImage):
        """
        Update the image label with the given image
        """
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)