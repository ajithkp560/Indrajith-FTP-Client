from PyQt6.QtGui import QStandardItemModel


class FTPModel(QStandardItemModel):
  def __init__(self):
    super().__init__()
    self.setHorizontalHeaderLabels(["Name", "Type", "Size"])
    self.root_item = self.invisibleRootItem()

  def get_root(self):
    return self.root_item
