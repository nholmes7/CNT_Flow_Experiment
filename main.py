from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import serial, pyqtgraph

# ser = serial.Serial(port='/dev/ttyUSB0',baudrate=115200,timeout=3)

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

        # Configure the plots and their settings
        background_colour = self.palette().color(QtGui.QPalette.Window)
        styles = {"color": 'k', "font-size": "14px"}
        self.ui.plotWidget.setBackground(background_colour)
        self.ui.plotWidget.setTitle('Flow Sensor Signals',color='k',size = '16pt')
        self.ui.plotWidget.setLabel("bottom", "Time (s)", **styles)
        self.ui.plotWidget.addLegend(offset = (1,-125))

        # Pen objects used for plotting style.
        plot_colours = ['#1f005c','#540083','#a200a9','#d00099','#f60069','#ff1e38','#ff6844','#ffb56b']
        # self.pens = {}
        # i = 0
        # for gas in self.MFCs:
        #     self.pens[gas] = pyqtgraph.mkPen(color=plot_colours[i],width=2)
        #     i = i+1

        # Initialize plot
        self.lines = {}
        self.pens = {}
        for i in range(8):
            self.pens[i] = pyqtgraph.mkPen(color=plot_colours[i],width=2)
            self.lines[i] = self.ui.plotWidget.plot(pen=self.pens[i])

        # set up variables
        self.statii = {
            'disabled':'',
            'polling':'background-color: rgb(114, 159, 207);',
            'recording':'background-color: rgb(138, 226, 52);'
        }
        self.status = [0,0,0,0,0,0,0,0]
        self.sensor_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]        

        self.ui.s1c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s1c1_button,1))
        self.ui.s1c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s1c2_button,2))
        self.ui.s2c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s2c1_button,3))
        self.ui.s2c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s2c2_button,4))
        self.ui.s3c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s3c1_button,5))
        self.ui.s3c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s3c2_button,6))
        self.ui.s4c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s4c1_button,7))
        self.ui.s4c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s4c2_button,8))

        # # Main loop timer used for sensor polling
        # self.loop_timer = QtCore.QTimer()
        # self.loop_timer.setInterval(250)
        # self.loop_timer.timeout.connect(self.PollSensors)
        # self.loop_timer.start()

    def PollSensors(self):
        command = bytes('#RC;','ascii')
        ser.write(command)
        reply = ser.read_until(expected=bytes(';','ascii'))
        reply = reply.decode('ascii',errors = 'ignore')
        self.ParseReply(reply)
        self.UpdatePlots()

    def ParseReply(self,reply):
        reply = reply[1:-1]
        for i in range(len(reply)/16):
            reading = reply[(i-1)*8,i*8]
            sensor = int(reading[0])
            channel = int(reading[1])
            value = int(reading[2:8])
            timestamp = int(reading[8:])
            time_index = (sensor-1)*4 + channel-1
            val_index = (sensor-1)*4 + channel
            self.sensor_data[time_index].append(timestamp)
            self.sensor_data[val_index].append(value)
            if len(self.sensor_data[time_index]) > 100:
                self.sensor_data[time_index] = self.sensor_data[time_index][-100:]
                self.sensor_data[val_index] = self.sensor_data[val_index][-100:]
    
    def UpdatePlots(self):
        pass


    def ToggleStatus(self,button,sensor):
        if self.status[sensor-1] == 0:
            self.status[sensor-1] = 1
            button.setStyleSheet(self.statii['polling'])
        elif self.status[sensor-1] == 1:
            self.status[sensor-1] = 2
            button.setStyleSheet(self.statii['recording'])
        elif self.status[sensor-1] == 2:
            self.status[sensor-1] = 0
            button.setStyleSheet(self.statii['disabled'])
        self.ResetPlot()

    def ResetPlot(self):
        # Clear the graph and re-plot
        self.ui.plotWidget.clear()
        i = 0
        for status in self.status:
            if status > 0:
                self.lines[i] = self.ui.plotWidget.plot(name=i,pen=self.pens[i])
            i += 1

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = flowControl()
    window.show()
    app.exec_()