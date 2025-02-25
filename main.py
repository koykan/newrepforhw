import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.load_data)
        self.load_data()

    def load_data(self):
        try:
            connection = sqlite3.connect('coffee.sqlite')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM coffee")
            data = cursor.fetchall()
            connection.close()

            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(
                ["ID", "Name", "Roast Level", "Ground", "Taste Description", "Price", "Volume"]
            )

            for row_index, row_data in enumerate(data):
                for col_index, col_data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        except sqlite3.Error as e:
            print(f"Database error: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeInfoApp()
    window.show()
    sys.exit(app.exec())
