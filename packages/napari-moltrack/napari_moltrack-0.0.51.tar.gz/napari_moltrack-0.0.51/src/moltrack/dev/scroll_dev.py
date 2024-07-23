import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QCheckBox, QScrollArea

class ScrollWidget(QMainWindow):
    def __init__(self, n):
        super().__init__()

        self.setWindowTitle("Scroll Widget with Checkboxes")
        self.setGeometry(100, 100, 400, 300)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.setCentralWidget(scroll_area)

        # Container Widget
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Add checkboxes to the container
        for i in range(n):
            checkbox = QCheckBox(f"Checkbox {i+1}")
            container_layout.addWidget(checkbox)

        container.setLayout(container_layout)
        scroll_area.setWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    n = 50  # Change this number to however many checkboxes you need
    window = ScrollWidget(n)
    window.show()
    sys.exit(app.exec_())