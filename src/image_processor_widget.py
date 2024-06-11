from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import threading


def predict_image(image):
    # todo: ml prediction
    return image


class ImageProcessorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 400, 300)

        self.mutex = threading.Lock()

        self.image_label = QLabel(self)
        self.image_label.setText("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)  # Fixed alignment setting

        self.process_button = QPushButton('Process Image', self)
        self.process_button.clicked.connect(self.processImage)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def process_image(self):
        self.mutex.acquire()

        options = QFileDialog.Options()
        file_name: str
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        if not file_name or not file_name.isascii():
            self.image_label.setText('No filepath provided or non-ascii symbol in filepath found')
            self.mutex.release()
            return

        image = cv2.imread(file_name)

        predicted_image = predict_image(image)

        self.display_image(predicted_image)

        self.mutex.release()

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)

        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
