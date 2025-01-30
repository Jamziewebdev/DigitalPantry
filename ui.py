from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QComboBox
from database import get_items, delete_item_from_db, get_items_by_category, get_all_categories
from add_item_window import AddItemWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Digital Pantry')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Category dropdown for filtering
        self.category_dropdown = QComboBox(self)
        self.category_dropdown.addItem("All Categories")
        layout.addWidget(self.category_dropdown)

        # Refresh categories
        self.refresh_categories()

        # Connect category selection to filter
        self.category_dropdown.currentTextChanged.connect(self.filter_items)

        # Viewing table
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Name', 'Quantity', 'Unit', 'Categories', 'Edit', 'Delete'])
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
            self.add_item_to_table(item)

    def add_item_to_table(self, item):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(item.name))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(item.quantity)))
        self.table.setItem(row_position, 2, QTableWidgetItem(item.unit))
        self.table.setItem(row_position, 3, QTableWidgetItem(", ".join([cat.name for cat in item.categories])))

        # Edit button
        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(lambda: self.open_edit_item_window(item.id))
        self.table.setCellWidget(row_position, 4, edit_button)

        # Delete button
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda: self.delete_item(item.id))
        self.table.setCellWidget(row_position, 5, delete_button)

    def open_add_item_window(self):
        self.add_item_window = AddItemWindow(self)
        self.add_item_window.show()

    def open_edit_item_window(self, item_id):
        self.edit_item_window = AddItemWindow(self, edit_mode=True, item_id=item_id)
        self.edit_item_window.show()

    def delete_item(self, item_id):
        try:
            delete_item_from_db(item_id)
            self.view_items()  # Refresh table
        except Exception as e:
            print("Error deleting item:", e)

    def filter_items(self):
        selected_category = self.category_dropdown.currentText()
        self.table.setRowCount(0)
        if selected_category == "All Categories":
            items = get_items()
        else:
            items = get_items_by_category(selected_category)
        for item in items:
            self.add_item_to_table(item)

    def refresh_categories(self):
        self.category_dropdown.clear()
        self.category_dropdown.addItem("All Categories")
        try:
            categories = get_all_categories()
            self.category_dropdown.addItems([cat.name for cat in categories])
        except Exception as e:
            print("Error refreshing categories:", e)
