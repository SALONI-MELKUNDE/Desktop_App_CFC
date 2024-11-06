
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTabWidget, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QTableWidget, QTableWidgetItem, QRadioButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io
import os


class CarbonFootprintCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carbon Footprint Calculator")
        self.setGeometry(100, 100, 600, 600)
        self.setFixedWidth(800)
        self.initUI()
        self.carbonCalculator = {}
        self.carbonCalculator.setdefault("Details", {})
        self.carbonCalculator.setdefault("Energy", {})
        self.carbonCalculator.setdefault("Waste", {})
        self.carbonCalculator.setdefault("Travel", {})
        self.carbonCalculator.setdefault("Results", {})

    def initUI(self):
        validator = QtGui.QDoubleValidator()
        validator.setRange(0, 9999.0, 1)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.my_font = QtGui.QFont()
        self.my_font.setBold(True)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tabs.addTab(self.tab1, "Welcome")
        self.tabs.addTab(self.tab2, "Energy")
        self.tabs.addTab(self.tab3, "Waste")
        self.tabs.addTab(self.tab4, "Travel/Transport")
        self.tabs.addTab(self.tab5, "Results")
        self.tabs.addTab(self.tab6, "Visualization")

        # First Tab - Welcome
        self.tab1_layout = QGridLayout(self.tab1)
        self.individual_rbtn = QRadioButton("Individual")
        self.individual_rbtn.setFont(QFont("Arial", 11, QFont.Bold))
        self.individual_rbtn.setChecked(True)
        self.sbusiness_rbtn = QRadioButton("Small Business Firm")
        self.sbusiness_rbtn.setFont(QFont("Arial", 11, QFont.Bold))
        self.bbusiness_rbtn = QRadioButton("Big Business Firm")
        self.bbusiness_rbtn.setFont(QFont("Arial", 11, QFont.Bold))
        self.tab1_name_label = QLabel("Name:")
        self.tab1_name_input = QLineEdit()
        self.tab1_name_input.setPlaceholderText("Enter your name")
        self.tab1_year_label = QLabel("Year:")
        self.tab1_year_input = QComboBox()
        self.tab1_year_input.addItems(["2021", "2022", "2023", "2024", "2025"])
        self.tab1_year_input.setCurrentIndex(3)
        self.tab1_next_button = QPushButton("Next")
        self.tab1_next_button.clicked.connect(lambda: self.switchTab(1))

        self.tab1_layout.addWidget(self.individual_rbtn, 1, 0, 1, 2)
        self.tab1_layout.addWidget(self.sbusiness_rbtn, 1, 3, 1, 2)
        self.tab1_layout.addWidget(self.bbusiness_rbtn, 1, 6, 1, 2)
        self.tab1_layout.addWidget(self.tab1_name_label, 2, 0, 1, 1)
        self.tab1_layout.addWidget(self.tab1_name_input, 2, 1, 1, 7)
        self.tab1_layout.addWidget(self.tab1_year_label, 3, 0, 1, 1)
        self.tab1_layout.addWidget(self.tab1_year_input, 3, 1, 1, 7)
        self.tab1_layout.addWidget(self.tab1_next_button, 4, 7, 1, 1)
        self.tab1_name_input.editingFinished.connect(lambda: self.carbonCalculator_func("Details"))
        self.tab1_year_input.currentIndexChanged.connect(lambda: self.carbonCalculator_func("Details"))

        # Second Tab - Energy
        self.tab2_layout = QGridLayout(self.tab2)
        self.tab2_layout.setAlignment(Qt.AlignCenter)

        self.tab2_input_layout = QGridLayout()
        self.tab2_input_layout.addWidget(QLabel("What is your average monthly electricity bill in euros?"), 0, 0)
        self.tab2_input_layout.addWidget(QLabel("What is your average monthly natural gas bill in euros?"), 1, 0)
        self.tab2_input_layout.addWidget(QLabel("What is your average monthly fuel bill for transportation in euros?"), 2, 0)
        self.tab2_electricity_input = QLineEdit()
        self.tab2_gas_input = QLineEdit()
        self.tab2_fuel_input = QLineEdit()
        self.tab2_electricity_input.setValidator(validator)
        self.tab2_gas_input.setValidator(validator)
        self.tab2_fuel_input.setValidator(validator)
        self.tab2_input_layout.addWidget(self.tab2_electricity_input, 0, 1)
        self.tab2_input_layout.addWidget(self.tab2_gas_input, 1, 1)
        self.tab2_input_layout.addWidget(self.tab2_fuel_input, 2, 1)
        self.tab2_layout.addLayout(self.tab2_input_layout, 0, 0, 1, 4)
        self.tab2_electricity_input.editingFinished.connect(lambda: self.carbonCalculator_func("Energy"))
        self.tab2_gas_input.editingFinished.connect(lambda: self.carbonCalculator_func("Energy"))
        self.tab2_fuel_input.editingFinished.connect(lambda: self.carbonCalculator_func("Energy"))

        self.tab2_previous_button = QPushButton("Previous")
        self.tab2_previous_button.clicked.connect(lambda: self.switchTab(0))
        self.tab2_next_button = QPushButton("Next")
        self.tab2_next_button.clicked.connect(lambda: self.switchTab(2))
        self.tab2_layout.addWidget(self.tab2_previous_button, 5, 0)
        self.tab2_layout.addWidget(self.tab2_next_button, 5, 3)

        # Third Tab - Waste
        self.tab3_layout = QGridLayout(self.tab3)
        self.tab3_layout.setAlignment(Qt.AlignCenter)

        self.tab3_input_layout = QGridLayout()
        self.tab3_input_layout.addWidget(QLabel("How much waste do you generate per month in kilograms?"), 0, 0)
        self.tab3_input_layout.addWidget(QLabel("How much of that waste is recycled or composted(in %)?"), 1, 0)
        self.tab3_waste_generated = QLineEdit()
        self.tab3_waste_recycle = QLineEdit()
        self.tab3_waste_generated.setValidator(validator)
        self.tab3_waste_recycle.setValidator(validator)
        self.tab3_input_layout.addWidget(self.tab3_waste_generated, 0, 1)
        self.tab3_input_layout.addWidget(self.tab3_waste_recycle, 1, 1)
        self.tab3_layout.addLayout(self.tab3_input_layout, 0, 0, 1, 4)
        self.tab3_waste_generated.editingFinished.connect(lambda: self.carbonCalculator_func("Waste"))
        self.tab3_waste_recycle.editingFinished.connect(lambda: self.carbonCalculator_func("Waste"))

        self.tab3_previous_button = QPushButton("Previous")
        self.tab3_previous_button.clicked.connect(lambda: self.switchTab(1))
        self.tab3_next_button = QPushButton("Next")
        self.tab3_next_button.clicked.connect(lambda: self.switchTab(3))
        self.tab3_layout.addWidget(self.tab3_previous_button, 4, 0)
        self.tab3_layout.addWidget(self.tab3_next_button, 4, 3)

        # Fourth Tab - Travel/Transport
        self.tab4_layout = QGridLayout(self.tab4)
        self.tab4_layout.setAlignment(Qt.AlignCenter)

        self.tab4_input_layout = QGridLayout()
        self.tab4_input_layout.addWidget(QLabel("How many kilometers do your employees travel per year for business purposes?"), 0, 0)
        self.tab4_input_layout.addWidget(QLabel("What is the average fuel efficiency of the vehicles used for business travel in litres/100kms?"), 1, 0)
        self.tab4_distance = QLineEdit()
        self.tab4_fuel_efficiency = QLineEdit()
        self.tab4_distance.setValidator(validator)
        self.tab4_fuel_efficiency.setValidator(validator)
        self.tab4_input_layout.addWidget(self.tab4_distance, 0, 1)
        self.tab4_input_layout.addWidget(self.tab4_fuel_efficiency, 1, 1)
        self.tab4_layout.addLayout(self.tab4_input_layout, 0, 0, 1, 4)
        self.tab4_distance.editingFinished.connect(lambda: self.carbonCalculator_func("Travel"))
        self.tab4_fuel_efficiency.editingFinished.connect(lambda: self.carbonCalculator_func("Travel"))

        self.tab4_previous_button = QPushButton("Previous")
        self.tab4_previous_button.clicked.connect(lambda: self.switchTab(2))
        self.tab4_next_button = QPushButton("Next")
        self.tab4_next_button.clicked.connect(lambda: self.switchTab(4))
        self.tab4_layout.addWidget(self.tab4_previous_button, 4, 0)
        self.tab4_layout.addWidget(self.tab4_next_button, 4, 3)

        # Fifth Tab - Results
        self.tab5gb = QGroupBox()
        self.tab5layout = QGridLayout()
        self.tab5gb.setLayout(self.tab5layout)

        self.tab5_layout = QGridLayout(self.tab5)

        self.table = QTableWidget(4, 2)  # Set up a table with 2 columns and an extra row for the total
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(["Operators", "Carbon Footprint"])
        self.table.horizontalHeader().setFont(self.my_font)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.table.setItem(0, 0, QTableWidgetItem("Energy"))
        self.table.setItem(1, 0, QTableWidgetItem("Waste"))
        self.table.setItem(2, 0, QTableWidgetItem("Business Travel"))
        self.table.setItem(3, 0, QTableWidgetItem("Total"))

        for col in range(3):  # Leave the last row editable for the total calculation
            self.table.item(col, 0).setFlags(Qt.ItemIsEnabled)
            self.table.setItem(col, 1, QtWidgets.QTableWidgetItem())
            self.table.item(col, 1).setFlags(Qt.ItemIsEnabled)

        self.table.item(3, 0).setFlags(Qt.ItemIsEnabled)  # Lock the "Total" label
        self.table.setItem(3, 1, QTableWidgetItem())
        self.table.item(3, 1).setFlags(Qt.ItemIsEnabled)

        self.tab5layout.addWidget(self.table, 0, 0)

        self.tab5_previous_button = QPushButton("Previous")
        self.tab5_previous_button.clicked.connect(lambda: self.switchTab(3))
        self.tab5_next_button = QPushButton("Next")
        self.tab5_next_button.clicked.connect(lambda: self.switchTab(5))
        self.tab5_calculate_button = QPushButton("Calculate")
        self.tab5_calculate_button.setFixedHeight(50)
        self.tab5_calculate_button.setFont(self.my_font)
        self.tab5_calculate_button.setStyleSheet('QPushButton {background-color: rgba(42, 161, 131); color: rgba(232, 237, 235); font-size: 16px}')
        self.tab5_layout.addWidget(self.tab5gb, 0, 0, 1, 3)
        self.tab5_layout.addWidget(self.tab5_previous_button, 1, 0)
        self.tab5_layout.addWidget(self.tab5_calculate_button, 1, 1)
        self.tab5_layout.addWidget(self.tab5_next_button, 1, 2)
        self.tab5_calculate_button.clicked.connect(self.calculate)

        # Sixth Tab - Visualization
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.tab6_layout = QVBoxLayout()
        self.tab6_layout.addWidget(self.canvas)
        self.tab6.setLayout(self.tab6_layout)

        self.download_pdf_button = QPushButton("Download PDF")
        self.download_pdf_button.clicked.connect(self.download_pdf)
        self.tab6_layout.addWidget(self.download_pdf_button)

        self.tab6_previous_button = QPushButton("Previous")
        self.tab6_previous_button.clicked.connect(lambda: self.switchTab(4))
        self.tab6_layout.addWidget(self.tab6_previous_button)

        self.layout.addWidget(self.tabs)

    def carbonCalculator_func(self, module: str):
        if module == "Details":
            mod = str
            if self.individual_rbtn.isChecked():
                mod = "Individual"
            elif self.sbusiness_rbtn.isChecked():
                mod = "Small Business Firm"
            elif self.bbusiness_rbtn.isChecked():
                mod = "Big Business Firm"
            self.carbonCalculator["Details"].update(
                {"Module": mod, "Name": self.tab1_name_input.text(), "Year": self.tab1_year_input.currentText()})
        elif module == "Energy":
            self.carbonCalculator["Energy"].update(
                {"Electricity": self.tab2_electricity_input.text(), "NaturalGas": self.tab2_gas_input.text(),
                 "Fuel": self.tab2_fuel_input.text()})
        elif module == "Waste":
            self.carbonCalculator["Waste"].update(
                {"Waste_generated": self.tab3_waste_generated.text(), "Waste_recycle": self.tab3_waste_recycle.text()})
        elif module == "Travel":
            self.carbonCalculator["Travel"].update(
                {"Distance": self.tab4_distance.text(), "Fuel_Efficiency": self.tab4_fuel_efficiency.text()})

    def calculate(self):
        energy_result = (float(self.carbonCalculator["Energy"]["Electricity"]) * 12 * 0.0005) + (
                float(self.carbonCalculator["Energy"]["NaturalGas"]) * 12 * 0.0053) + (
                                float(self.carbonCalculator["Energy"]["Fuel"]) * 12 * 2.32)
        waste_result = float(self.carbonCalculator["Waste"]["Waste_generated"]) * 12 * (
                0.57 - (float(self.carbonCalculator["Waste"]["Waste_recycle"]) / 100))
        travel_result = float(self.carbonCalculator["Travel"]["Distance"]) * (
                1 / float(self.carbonCalculator["Travel"]["Fuel_Efficiency"]) * 2.31)

        total_result = energy_result + waste_result + travel_result  # Calculate total carbon footprint

        self.table.setItem(0, 1, QTableWidgetItem("%.2f" % energy_result))
        self.table.setItem(1, 1, QTableWidgetItem("%.2f" % waste_result))
        self.table.setItem(2, 1, QTableWidgetItem("%.2f" % travel_result))
        self.table.setItem(3, 1, QTableWidgetItem("%.2f" % total_result))  # Display total

        # Update visualization with bar chart
        self.ax.clear()
        operators = ['Energy', 'Waste', 'Business Travel']
        results = [energy_result, waste_result, travel_result]
        self.ax.bar(operators, results, color=['blue', 'green', 'red'])
        self.ax.set_title("Carbon Footprint by Category")
        self.ax.set_ylabel("Carbon Footprint (kg CO2)")
        self.canvas.draw()

    def download_pdf(self):
        filename = "Carbon_Footprint_Report.pdf"
        pdf = canvas.Canvas(filename, pagesize=letter)
        pdf.setTitle("Carbon Footprint Report")

        # Page setup
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(30, 750, "Carbon Footprint Report")
        pdf.setFont("Helvetica", 12)

        # Add user details
        y_position = 720
        for key, value in self.carbonCalculator["Details"].items():
            pdf.drawString(30, y_position, f"{key}: {value}")
            y_position -= 20

        # Add results
        y_position -= 20
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(30, y_position, "Results")
        pdf.setFont("Helvetica", 12)
        y_position -= 20

        for i in range(4):  # Iterate over the table rows
            parameter = self.table.item(i, 0).text()
            value = self.table.item(i, 1).text()
            pdf.drawString(30, y_position, f"{parameter}: {value} kg CO2")
            y_position -= 20

        # Leave space between the results and the chart
        y_position -= 40

        # Save the plot as a temporary image
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)
        img = ImageReader(buf)

        # Add the image to the PDF with proper spacing
        pdf.drawImage(img, 50, y_position - 250, width=500, height=300)  # Adjusted position

        # Save the PDF
        pdf.save()
        buf.close()
        os.startfile(filename)  # Open the PDF after saving (Windows-specific)

    def switchTab(self, index):
        self.tabs.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarbonFootprintCalculator()
    window.show()
    sys.exit(app.exec_())
