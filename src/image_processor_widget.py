import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import threading
import os

class ImageProcessorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 800, 600)  # Увеличение размера окна

        self.mutex = threading.Lock()

        self.image_label = QLabel(self)
        self.image_label.setText("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.process_button = QPushButton('Process Image', self)
        self.process_button.clicked.connect(self.process_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.process_button)

        self.setLayout(layout)

    def process_image(self):
        self.mutex.acquire()

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        if not file_name or not file_name.isascii():
            self.image_label.setText('No filepath provided or non-ascii symbol in filepath found')
            self.mutex.release()
            return

        try:
            # Формирование команды для запуска скрипта detect.py
            command = [
                'python', os.path.expanduser('src/yolov9-2/detect.py'),
                '--img', '1280', '--conf', '0.1',
                '--weights', os.path.expanduser('src/yolov9-2/runs/train/exp7/weights/best.pt'),
                '--source', file_name,
                '--project', os.path.expanduser('src/res'),
                '--name', 'results', '--exist-ok'
            ]

            # Запуск команды
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            # Проверка вывода на ошибки
            if result.returncode != 0:
                self.image_label.setText(f'Error executing detect.py: {result.stderr}')
            else:
                print(result.stdout)

        except subprocess.CalledProcessError as e:
            self.image_label.setText(f'Error executing detect.py: {e.stderr}')
            print(f"Error executing detect.py: {e.stderr}")

        new_path = file_name.replace('/test/images/', '/res/results/')

        self.display_image(new_path)

        self.mutex.release()

    def display_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Конвертация BGR в RGB

        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
