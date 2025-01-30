from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QComboBox, QCheckBox,
    QPushButton, QLabel, QHBoxLayout, QMessageBox
)
from database import add_item


class AddItemWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Add New Item")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter item name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        # Quantity input
        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText("Enter quantity")
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.quantity_input)

        # Unit dropdown
        self.unit_dropdown = QComboBox(self)
        self.unit_dropdown.addItems(["Liter", "Deciliter", "Centiliter", "Kilogram", "Gram", "Piece"])
        layout.addWidget(QLabel("Unit:"))
        layout.addWidget(self.unit_dropdown)

        # Category checkboxes
        self.categories = ["Spices", "Condiments", "Grains", "Baking", "Drinks", "Dairy", "Proteins", "Vegetables"]

        category_layout = QHBoxLayout()
        self.category_checkboxes = []
        for cat in self.categories:
            checkbox = QCheckBox(cat, self)
            self.category_checkboxes.append(checkbox)
            category_layout.addWidget(checkbox)
        layout.addLayout(category_layout)

        # Add button to submit item
        self.add_button = QPushButton("Add Item", self)
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_item(self):
        try:
            name = self.name_input.text().strip()
            quantity = float(self.quantity_input.text())
            unit = self.unit_dropdown.currentText()
            selected_categories = [cb.text() for cb in self.category_checkboxes if cb.isChecked()]

            if not name or quantity <= 0:
                raise ValueError("Name cannot be empty and quantity must be greater than zero.")

            # Add to DB
            add_item(name, quantity, unit, selected_categories)

            # Refresh parent table and close window
            self.parent.view_items()
            QMessageBox.information(self, "Success", "Item added successfully!")
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
