import sys
import src.image_processor_widget


if __name__ == '__main__':
    app = src.image_processor_widget.QApplication(sys.argv)
    ex = src.image_processor_widget.ImageProcessorWidget()
    ex.show()
    sys.exit(app.exec_())