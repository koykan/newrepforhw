import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee_id = coffee_id
        self.saveButton.clicked.connect(self.save_data)

        if self.coffee_id:
            self.load_data()

    def load_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        data = cursor.fetchone()
        connection.close()

        if data:
            self.nameInput.setText(data[1])
            self.roastLevelInput.setText(data[2])
            self.groundInput.setText(data[3])
            self.tasteDescriptionInput.setText(data[4])
            self.priceInput.setText(str(data[5]))
            self.volumeInput.setText(str(data[6]))

    def save_data(self):
        name = self.nameInput.text()
        roast_level = self.roastLevelInput.text()
        ground = self.groundInput.text()
        taste_description = self.tasteDescriptionInput.text()
        price = self.priceInput.text()
        volume = self.volumeInput.text()

        if not all([name, roast_level, ground, taste_description, price, volume]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        if self.coffee_id:
            cursor.execute('''
                UPDATE coffee
                SET name = ?, roast_level = ?, ground = ?, taste_description = ?, price = ?, volume = ?
                WHERE id = ?
            ''', (name, roast_level, ground, taste_description, price, volume, self.coffee_id))
        else:
            cursor.execute('''
                INSERT INTO coffee (name, roast_level, ground, taste_description, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, roast_level, ground, taste_description, price, volume))

        connection.commit()
        connection.close()
        self.accept()


class CoffeeInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.load_data)
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.load_data()

    def load_data(self):
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

    def add_coffee(self):
        dialog = AddEditCoffeeForm()
        if dialog.exec():
            self.load_data()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a row to edit!")
            return

        coffee_id = self.tableWidget.item(selected_row, 0).text()
        dialog = AddEditCoffeeForm(coffee_id)
        if dialog.exec():
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeInfoApp()
    window.show()
    sys.exit(app.exec())
