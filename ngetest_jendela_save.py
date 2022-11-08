import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QVBoxLayout, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self, parent=None):#--------------
        super(MainWindow, self).__init__(parent)#  |
        self.setWindowTitle("open file dialog")#   |
#												   |
        btn = QPushButton("Save File")#            |---- Just initialization
        layout = QVBoxLayout()#					   |
        layout.addWidget(btn)#                     |
        widget = QWidget()#                        |
        widget.setLayout(layout)#                  |
        self.setCentralWidget(widget)#-------------

        btn.clicked.connect(self.file_save) # connect clicked to self.open()
        self.show()

    def open(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files (*.*)')
        if path != ('', ''):
            print("File path : "+ path[0])
    
    def file_save(self):
        pd_df = pd.DataFrame({'a':[1,2,3,4],'b':[5,6,7,8]})
        name = QFileDialog.getSaveFileName(self, 'Save File', "./", "Excel File (*.xlsx)")
        if(name[0]!=''):
            pd_df.to_excel(name[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())