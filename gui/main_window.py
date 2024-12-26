from functools import partial

from PyQt6.QtWidgets import QMainWindow, QWidget, QSplitter, QVBoxLayout, QDialog, QApplication
from PyQt6.QtGui import QAction, QIcon, QStandardItem
from PyQt6.QtCore import Qt, QThread

from ftp.ftp_functions import FTP_Functions
from gui.file_browser import FileBrowser
from gui.open_connection_dialog import OpenNewConnectionDialog
from gui.remote_file_browser import RemoteFileBrowser
from gui.remote_files_model import FTPModel


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.current_item = None
    self.current_path = None
    self.setWindowTitle("Indrajith FTP Client")
    self.setGeometry(100, 100, 800, 600)

    self.initUI()

  def initUI(self):
    self.createMenuBar()
    self.createMainContainer()

  def createMenuBar(self):
    menubar = self.menuBar()

    # File menu
    file_menu = menubar.addMenu("File")

    exit_action = QAction("Exit", self)
    exit_action.triggered.connect(self.close)
    file_menu.addAction(exit_action)

    new_conn_action = QAction("&FTP Connect", self)
    new_conn_action.triggered.connect(self.open_new_conn_dialog)
    file_menu.addAction(new_conn_action)

  def createMainContainer(self):
    # Central widget and layout
    central_widget = QWidget()
    self.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)

    # Create splitter for two halves
    splitter = QSplitter(Qt.Orientation.Horizontal)

    # Add two table widgets
    file_browser = FileBrowser()
    remote_file_browser = RemoteFileBrowser()

    splitter.addWidget(file_browser)
    splitter.addWidget(remote_file_browser)

    self.file_model = FTPModel()

    self.remote_tree_view = remote_file_browser.get_tree_view()
    self.remote_root = self.file_model.get_root()

    self.remote_tree_view.setModel(self.file_model)
    self.remote_tree_view.expanded.connect(self.on_directory_expanded)

    splitter.setSizes([400, 400])

    layout.addWidget(splitter)

  def showAboutDialog(self):
    print("About dialog shown")

  def open_new_conn_dialog(self):
    conn_dialog = OpenNewConnectionDialog()
    conn_dialog.center_on_screen()
    if conn_dialog.exec() == QDialog.DialogCode.Accepted:
      inputs = conn_dialog.get_inputs()

      hostname = inputs["hostname"]
      username = inputs["username"]
      password = inputs["password"]
      print("Hostname:", hostname)
      print("Username:", username)
      print("Password:", password)

      if self.current_path is None:
        self.current_path = "/"
      if self.current_item is None:
        self.current_item = self.remote_root

      self.thread = QThread()
      self.ftp = FTP_Functions(hostname, username, password)
      self.ftp.moveToThread(self.thread)
      self.thread.started.connect(lambda: self.ftp.list_files("/"))
      self.ftp.dataReady.connect(self.on_data_ready)
      self.ftp.finished.connect(self.thread.quit)
      self.ftp.finished.connect(self.ftp.deleteLater)
      self.thread.finished.connect(self.thread.deleteLater)
      self.thread.start()


  def center_on_screen(self):
    screen = QApplication.primaryScreen().geometry()
    dialog_geometry = self.geometry()
    x = (screen.width() - dialog_geometry.width()) // 2
    y = (screen.height() - dialog_geometry.height()) // 2
    self.move(x, y)

  def on_data_ready(self, files):
    self.load_from_path(files, self.current_item, self.current_path)

  def load_from_path(self, files, item, path):
    if item is not None:
      if item.hasChildren():
          item.removeRows(0, item.rowCount())
    for name, size, is_dir in files:
      try:
        child_item = QStandardItem(name)
        child_item.setData(f"{path}/{name}/", Qt.ItemDataRole.UserRole)

        if is_dir:
          child_item.appendRow(QStandardItem("Loading..."))  # Placeholder

        size_item = QStandardItem(str(size))
        file_type = QStandardItem("DIR" if is_dir else "FILE")

        item.appendRow([child_item, file_type, size_item])
      except Exception as e:
        print(f"Error processing file: {name}, {e}")

  def on_directory_expanded(self, index):
    item = self.file_model.itemFromIndex(index)
    path = item.data(Qt.ItemDataRole.UserRole)

    print("Expanding directory:", path)

    try:
      if not hasattr(self, 'ftp_thread') or not self.ftp_thread.isRunning():
        self.setup_ftp_thread()

      # Store the item for population when data is ready
      self.current_item = item
      self.current_path = path

      self.ftp.list_files(path)
    except Exception as e:
        print(f"Error expanding directory: {e}")

  def setup_ftp_thread(self):
    self.thread = QThread()
    self.ftp.moveToThread(self.thread)

    self.ftp.dataReady.connect(self.on_data_ready)
    self.ftp.finished.connect(self.thread.quit)
    self.ftp.finished.connect(self.ftp.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.start()