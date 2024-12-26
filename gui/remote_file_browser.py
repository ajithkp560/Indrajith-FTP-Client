from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt6.QtGui import QFileSystemModel

class RemoteFileBrowser(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.layout = QVBoxLayout(self)
    self.tree_view = QTreeView()
    self.layout.addWidget(self.tree_view)
    self.setLayout(self.layout)

  def get_tree_view(self):
    return self.tree_view