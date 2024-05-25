from sys import exit, argv
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QFileDialog, QVBoxLayout
from PyQt6.QtGui import QIcon
import downzip
import threading

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Downloader")
        self.setFixedSize(600, 200) 
        self.setWindowIcon(QIcon("icon.ico"))

        # Set dark mode stylesheet
        self.setStyleSheet("""
            background-color: #333;
            color: #FFF;
        """)
    
        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()

        self.folder_checkbox = QCheckBox("Enable Folder Selection")
        self.folder_checkbox.setStyleSheet("color: #888;")  # Set checkbox color to gray
        self.folder_checkbox.toggled.connect(self.toggle_browsing)
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setEnabled(False)  # Disable the folder path input initially
        self.folder_browse_button = QPushButton("Browse")
        self.folder_browse_button.setStyleSheet("background-color: #444; color: #FFF;")  # Set button color to darker gray
        self.folder_browse_button.setEnabled(False)  # Disable the browse button initially
        self.folder_browse_button.clicked.connect(self.browse_folder)

        self.unpack_checkbox = QCheckBox("Automatically overwrite files with the same name")
        self.unpack_checkbox.setStyleSheet("color: #888;")  # Set checkbox color to gray
        self.launch_checkbox = QCheckBox("Automatically launch inkscape.exe")
        self.launch_checkbox.setStyleSheet("color: #888;")  # Set checkbox color to gray
        self.launch_checkbox.setChecked(True)

        self.download_button = QPushButton("Download and Unpack")
        self.download_button.setStyleSheet("background-color: #444; color: #FFF;")  # Set button color to dark gray
        self.download_button.clicked.connect(self.download_and_unpack)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.folder_checkbox)
        layout.addWidget(self.folder_path_input)
        layout.addWidget(self.folder_browse_button)
        layout.addWidget(self.unpack_checkbox)
        layout.addWidget(self.launch_checkbox)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def toggle_browsing(self, checked):
        self.folder_path_input.setEnabled(checked)
        self.folder_browse_button.setEnabled(checked)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            self.folder_path_input.setText(folder_path)

    def download_and_unpack(self):
        url = self.url_input.text()
        output_path = self.folder_path_input.text() if self.folder_checkbox.isChecked() else None
        yes_flag = "-y" if self.unpack_checkbox.isChecked() else ""

        args = [url]
        if output_path:
            args.append(output_path)
        if self.unpack_checkbox.isChecked():
            args.append("-y")
        if self.launch_checkbox.isChecked():
            args.append("-launch")


        try:
            downzip_thread = threading.Thread(target=downzip.main, args=(args,))
            downzip_thread.start()
        except Exception as e:
            import traceback; traceback.print_exc()
            print(e)

def main():
    app = QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec())
    
if __name__ == '__main__':
    gui_thread = threading.Thread(target=main)
    gui_thread.start()
    gui_thread.join()

    
