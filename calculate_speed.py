import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculate Speed")
        grid = QGridLayout()

        distance_label = QLabel("Distance: ")
        self.distance_line_edit = QLineEdit()

        time_label = QLabel("Time(in hrs): ")
        self.time_line_edit = QLineEdit()

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Metric (km)","Imperial (miles)"])

        calculate_button = QPushButton("Calculate Speed")
        calculate_button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("")

        # Add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.unit_combo,0,2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)



        self.setLayout(grid)

    def calculate_speed(self):
        speed = float(self.distance_line_edit.text()) / float(self.time_line_edit.text())
        if self.unit_combo.currentText() == "Metric (km)":
            self.output_label.setText(f"Speed is {speed}km/hr.")
        else:
            self.output_label.setText(f"Speed is {speed}mph.")

app = QApplication(sys.argv)

speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())
