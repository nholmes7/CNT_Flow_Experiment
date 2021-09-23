from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import serial, pyqtgraph

# ser = serial.Serial(port='/dev/ttyUSB0',baudrate=115200,timeout=3)

class Sensor:
    '''
    A class for the info relating to each sensor connected to the system.
    Corresponds to an individual channel on the AD7746.

    ...

    Attributes
    ----------
    ID: int
        an index number ranging from 1 to 8 identifying the sensor
    status: int
        status 0 indicates sensor is disabled
        status 1 indicates sensor is polling
        status 2 indicates sensor is polling and recording
    values: list of ints
        a list of the values read from the sensor - used like a circular buffer
    timestamps: list of ints
        a list of the timestamps corresponding to the values read from the
        sensor - used like a circular buffer

    Public Methods
    --------------
    QueryFlow()
    '''

    def __init__(self,ID) -> None:
        self.ID = ID
        self.status = 0
        self.chip = int(ID/2) + 1
        self.channel = ID%2 + 1
        self.values = []
        self.timestamps = []

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

        # Colour palette for the graphs
        plot_colours = [
            ['#1f005c'],
            ['#1f005c','#ffb56b'],
            ['#1f005c', '#e30084', '#ffb56b'],
            ['#1f005c', '#b600ab', '#ff1146', '#ffb56b'],
            ['#1f005c', '#8c00a0', '#e30084', '#ff2830', '#ffb56b'],
            ['#1f005c', '#700092', '#c800a0', '#fe005d', '#ff4335', '#ffb56b'],
            ['#1f005c', '#600089', '#b600ab', '#e30084', '#ff1146', '#ff593e', '#ffb56b'],
            ['#1f005c', '#540083', '#a200a9', '#d00099', '#f60069', '#ff1e38', '#ff6844', '#ffb56b']
            ]

        # Initialize plot stuff
        self.lines = {}
        self.pens = [[pyqtgraph.mkPen(color=j,width=2) for j in i] for i in plot_colours]

        # set up variables
        self.statii = {
            'disabled':'',
            'polling':'background-color: rgb(114, 159, 207);',
            'recording':'background-color: rgb(138, 226, 52);'
        }
        
        # initialize sensor objects
        self.sensors = {}
        for i in range(8):
            self.sensors[i] = Sensor(i)
        
        self.ui.s1c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s1c1_button,0))
        self.ui.s1c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s1c2_button,1))
        self.ui.s2c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s2c1_button,2))
        self.ui.s2c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s2c2_button,3))
        self.ui.s3c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s3c1_button,4))
        self.ui.s3c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s3c2_button,5))
        self.ui.s4c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s4c1_button,6))
        self.ui.s4c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s4c2_button,7))

        # # Main loop timer used for sensor polling
        # self.loop_timer = QtCore.QTimer()
        # self.loop_timer.setInterval(250)
        # self.loop_timer.timeout.connect(self.PollSensors)
        # self.loop_timer.start()

    def PollSensors(self):
        command = bytes('#RC;','ascii')
        ser.write(command)
        reply = ser.read_until(expected=bytes(';','ascii'))
        # check to see if reply is simply "#;" which is the case if no sensors
        # are enabled
        if len(reply) == 2:
            return
        # if we do in fact have data, we can proceed with parsing
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
            ID = (sensor-1)*2 + (channel-1)
            self.sensors[ID].values.append(value)
            self.sensors[ID].timestamps.append(timestamp)
            if len(self.sensors[ID].values) > 100:
                self.sensors[ID].timestamps = self.sensors[ID].timestamps[-100:]
                self.sensors[ID].values = self.sensors[ID].values[-100:]
    
    def UpdatePlots(self):
        pass


    def ToggleStatus(self,button,ID):
        if self.sensors[ID].status == 0:
            self.sensors[ID].status = 1
            button.setStyleSheet(self.statii['polling'])
        elif self.sensors[ID].status == 1:
            self.sensors[ID].status = 2
            button.setStyleSheet(self.statii['recording'])
        elif self.sensors[ID].status == 2:
            self.sensors[ID].status = 0
            button.setStyleSheet(self.statii['disabled'])
        self.ResetPlot()

    def ResetPlot(self):
        # Clear the graph and re-plot
        self.ui.plotWidget.clear()
        # determine how many sensors are polling and/or recording
        count = 0
        for sensor in self.sensors:
            if self.sensors[sensor].status > 0:
                count += 1
        # draw a line for each sensor which is active
        i = 0
        j = 0
        for sensor in self.sensors:
            if self.sensors[sensor].status > 0:
                self.lines[i] = self.ui.plotWidget.plot(name=i,pen=self.pens[count-1][j])
                j += 1
            i += 1

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = flowControl()
    window.show()
    app.exec_()