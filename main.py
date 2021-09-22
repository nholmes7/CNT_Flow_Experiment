from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui

class flowControl(QtWidgets.QMainWindow):
    # override the init method
    def __init__(self, *args, **kwargs):
        # whenever you override the init method in a Qt object you need to run 
        # super().__init__ and pass in any arguments that were passed in so it 
        # still behaves like a Qt widget
        super().__init__(*args, **kwargs)
        
        # setupUi builds the GUI onto the flow_control QMainWindow object
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set up variables
        self.statii = {
            'disabled':'',
            'polling':'background-color: rgb(114, 159, 207);',
            'recording':'background-color: rgb(138, 226, 52);'
        }
        self.status = 'disabled'

        # sensor_buttons = [
        #     self.ui.s1c1_button,
        #     self.ui.s1c2_button,
        #     self.ui.s2c1_button,
        #     self.ui.s2c2_button,
        #     self.ui.s3c1_button,
        #     self.ui.s3c2_button,
        #     self.ui.s4c1_button,
        #     self.ui.s4c2_button
        # ]

        # # make connections to UI elements
        # for button in sensor_buttons:
        #     button.clicked.connect(lambda: self.toggle_colour(button))
        self.ui.s1c1_button.clicked.connect(lambda: self.toggle_colour(self.ui.s1c1_button))
        self.ui.s1c2_button.clicked.connect(lambda: self.toggle_colour(self.ui.s1c2_button))
        self.ui.s2c1_button.clicked.connect(lambda: self.toggle_colour(self.ui.s2c1_button))
        self.ui.s2c2_button.clicked.connect(lambda: self.toggle_colour(self.ui.s2c2_button))
        self.ui.s3c1_button.clicked.connect(lambda: self.toggle_colour(self.ui.s3c1_button))
        self.ui.s3c2_button.clicked.connect(lambda: self.toggle_colour(self.ui.s3c2_button))
        self.ui.s4c1_button.clicked.connect(lambda: self.toggle_colour(self.ui.s4c1_button))
        self.ui.s4c2_button.clicked.connect(lambda: self.toggle_colour(self.ui.s4c2_button))

    def toggle_colour(self,button):
        if self.status == 'disabled':
            self.status = 'polling'
            button.setStyleSheet(self.statii['polling'])
        elif self.status == 'polling':
            self.status = 'recording'
            button.setStyleSheet(self.statii['recording'])
        elif self.status == 'recording':
            self.status = 'disabled'
            button.setStyleSheet(self.statii['disabled'])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = flowControl()
    window.show()
    app.exec_()