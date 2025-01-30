from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from database import get_items, delete_item_from_db
from add_item_window import AddItemWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Digital Pantry')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Viewing table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Quantity', 'Unit', 'Categories', 'Actions'])
        layout.addWidget(self.table)

        # 'Add Item' button
        self.add_button = QPushButton('Add Item')
        self.add_button.clicked.connect(self.open_add_item_window)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        self.view_items()

    def view_items(self):
        self.table.setRowCount(0)
        items = get_items()
        for item in items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(item.name))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(item.quantity)))
            self.table.setItem(row_position, 2, QTableWidgetItem(item.unit))
            self.table.setItem(row_position, 3, QTableWidgetItem(", ".join([cat.name for cat in item.categories])))

            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda state, row=row_position: self.delete_item(row))
            self.table.setCellWidget(row_position, 4, delete_button)

    def open_add_item_window(self):
        self.add_item_window = AddItemWindow(self)
        self.add_item_window.show()

    def delete_item(self, row):
        item_name = self.table.item(row, 0).text()
        item_id = self.get_item_id_by_name(item_name)
        delete_item_from_db(item_id)
        self.view_items()

    def get_item_id_by_name(self, name):
        for item in get_items():
            if item.name == name:
                return item.id
