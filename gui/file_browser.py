from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt6.QtGui import QFileSystemModel

class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath("")  # Set to the root directory

        # File tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(""))  # Start at the root directory

        # Allow expanding directories and file selection
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.setHeaderHidden(True)

        layout.addWidget(self.tree_view)
