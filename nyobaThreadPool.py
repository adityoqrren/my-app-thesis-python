from PyQt5 import QtCore
import logging
import sys

from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, QCoreApplication, QRunnable, QThreadPool
)
from PyQt5.QtWidgets import (

    QApplication,

    QLabel,

    QMainWindow,

    QPushButton,

    QVBoxLayout,

    QWidget,

)

logging.basicConfig(format="%(message)s", level=logging.INFO)

class Signals(QObject):
    now = pyqtSignal(int)
    finished = pyqtSignal()


class HelloWorldTask(QRunnable):
    def __init__(self, myInt):
        super().__init__()
        self.myInt = myInt
        self.signal = Signals()

    def run(self):
        import time

        time.sleep(3)
        logging.info(f"Running thread {self.myInt}")
        time.sleep(3)
        self.signal.now.emit(self.myInt)
        self.signal.finished.emit()



class Window(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi()


    def setupUi(self):

        self.setWindowTitle("QThreadPool + QRunnable")

        self.resize(250, 150)

        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        # Create and connect widgets

        self.label = QLabel("Hello, World!")

        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        countBtn = QPushButton("Click me!")

        countBtn.clicked.connect(self.runTasks)

        # Set the layout

        layout = QVBoxLayout()

        layout.addWidget(self.label)

        layout.addWidget(countBtn)

        self.centralWidget.setLayout(layout)

    
    def check(self):
        logging.info(f"Thread Done")

    def printNow(self, myInt):
        logging.info(f"now in: {myInt}")


    def runTasks(self):

        threadCount = QThreadPool.globalInstance().maxThreadCount()

        self.label.setText(f"Running {threadCount} Threads")

        pool = QThreadPool.globalInstance()

        hello = HelloWorldTask(1)
        hello2 = HelloWorldTask(2)
        hello3 = HelloWorldTask(3)
        hello4 = HelloWorldTask(4)
        hello5 = HelloWorldTask(5)
        hello6 = HelloWorldTask(6)
        hello7 = HelloWorldTask(7)
        hello8 = HelloWorldTask(8)
        hello9 = HelloWorldTask(9)
        hello10 = HelloWorldTask(10)

        hello.signal.now.connect(self.printNow)
        hello2.signal.now.connect(self.printNow)
        hello3.signal.now.connect(self.printNow)
        hello4.signal.now.connect(self.printNow)
        hello5.signal.now.connect(self.printNow)
        hello6.signal.now.connect(self.printNow)
        hello7.signal.now.connect(self.printNow)
        hello8.signal.now.connect(self.printNow)
        hello9.signal.now.connect(self.printNow)
        hello10.signal.now.connect(self.printNow)

        hello.signal.finished.connect(self.check)
        hello2.signal.finished.connect(self.check)
        hello3.signal.finished.connect(self.check)
        hello4.signal.finished.connect(self.check)
        hello5.signal.finished.connect(self.check)
        hello6.signal.finished.connect(self.check)
        hello7.signal.finished.connect(self.check)
        hello8.signal.finished.connect(self.check)
        hello9.signal.finished.connect(self.check)
        hello10.signal.finished.connect(self.check)

        pool.start(hello)
        pool.start(hello2)
        pool.start(hello3)
        pool.start(hello4)
        pool.start(hello5)
        pool.start(hello6)
        pool.start(hello7)
        pool.start(hello8)
        pool.start(hello9)
        pool.start(hello10)


app = QApplication(sys.argv)

window = Window()

window.show()

sys.exit(app.exec())


# if __name__ == "__main__":
#     import sys


    # pool = QThreadPool.globalInstance()
    # print("Multithreading with maximum %d threads" % pool.maxThreadCount())

    # pool.start(hello)
    # pool.start(hello2)
    # pool.start(hello3)
    # pool.start(hello4)
    # pool.start(hello5)
    # pool.start(hello6)
    # pool.start(hello7)
    # pool.start(hello8)
    # pool.start(hello9)
    # pool.start(hello10)

    # sys.exit(app.exec_())