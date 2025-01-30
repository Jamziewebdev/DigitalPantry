from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QCheckBox,QPushButton, QLabel, QHBoxLayout, QMessageBox
from database import add_item, update_item, get_item_by_id

class AddItemWindow(QWidget):
    def __init__(self, parent, edit_mode=False, item_id=None):
        super().__init__()
        self.parent = parent
        self.edit_mode = edit_mode
        self.item_id = item_id
        self.setWindowTitle("Edit Item" if edit_mode else "Add New Item")
        self.init_ui()

        if edit_mode:
            self.load_item_data()

    def init_ui(self):
        # Initializing the UI
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
            category_checkbox = QCheckBox(cat, self)
            self.category_checkboxes.append(category_checkbox)
            category_layout.addWidget(category_checkbox)
        layout.addLayout(category_layout)

        # Save button to submit item
        self.add_button = QPushButton("Save Item", self)
        self.add_button.clicked.connect(self.save_item)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def load_item_data(self):
        item = get_item_by_id(self.item_id)
        if item is not None:
            self.name_input.setText(item.name)
            self.quantity_input.setText(str(item.quantity))
            self.unit_dropdown.setCurrentText(item.unit)
            for checkbox in self.category_checkboxes:
                if checkbox.text() in [cat.name for cat in item.categories]:
                    checkbox.setChecked(True)
        else:
            QMessageBox.warning(self, "Error", "Could not load item!")

    def save_item(self):
        try:
            # Getting input values
            name = self.name_input.text().strip()
            quantity = float(self.quantity_input.text())
            unit = self.unit_dropdown.currentText()
            selected_categories = [cb.text() for cb in self.category_checkboxes if cb.isChecked()]

            # Validate input
            if not name:
                raise ValueError("Name must not be empty.")
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            # Add or update item in DB
            if self.edit_mode:
                update_item(self.item_id, name, quantity, unit, selected_categories)
                QMessageBox.information(self, "Success", "Item updated successfully!")
            else:
                add_item(name, quantity, unit, selected_categories)
                QMessageBox.information(self, "Success", "Item added successfully!")
            self.parent.view_items()
            self.close()
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
