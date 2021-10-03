from serial.serialutil import SerialException
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import serial, pyqtgraph,time

# set up the serial ports - set flags to indicate which devices are connected
try:
    ser = serial.Serial(port='/dev/ttyACM0',baudrate=115200,timeout=3)
    flowmeter_connected_flag = True
except SerialException:
    flowmeter_connected_flag = False
try:
    serP0 = serial.Serial(port='/dev/ttyUSB0',baudrate=115200,timeout=3)
    P0_connected_flag = True
except SerialException:
    P0_connected_flag = False
try:
    serP1 = serial.Serial(port='/dev/ttyUSB1',baudrate=115200,timeout=3)
    P1_connected_flag = True
except SerialException:
    P1_connected_flag = False

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
    chip: int
        the index for the sensor/AD7746 device the individual sensor is
        connected to - corresponds with the GUI numbering
    channel: int
        which AD7746 channel the sensor is connnected to
    values: list of ints
        a list of the values read from the sensor - used like a circular buffer
    timestamps: list of ints
        a list of the timestamps corresponding to the values read from the
        sensor - used like a circular buffer
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
        
        self.recording_flag = False
        self.record_colour = 0

        # initialize sensor objects
        self.sensors = {}
        for i in range(8):
            self.sensors[i] = Sensor(i)

        self.pressure_1 = {'value':0,'timestamp':0}
        self.pressure_2 = {'value':0,'timestamp':0}
        
        self.ui.s1c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s1c1_button,0))
        self.ui.s1c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s1c2_button,1))
        self.ui.s2c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s2c1_button,2))
        self.ui.s2c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s2c2_button,3))
        self.ui.s3c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s3c1_button,4))
        self.ui.s3c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s3c2_button,5))
        self.ui.s4c1_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s4c1_button,6))
        self.ui.s4c2_button.clicked.connect(lambda: self.ToggleStatus(self.ui.s4c2_button,7))

        self.ui.recordButton.clicked.connect(self.ToggleRecordStatus)

        # check the connection and status of each sensor
        if flowmeter_connected_flag:
            self.StartupConnectivityCheck()
            self.StartupConnectivityCheck()
        
        # Main loop timer used for sensor polling
        self.loop_timer = QtCore.QTimer()
        self.loop_timer.setInterval(100)
        self.loop_timer.timeout.connect(self.PollSensors)
        self.loop_timer.start()

        # Timer used to flash record button whilst recording
        self.record_flash_timer = QtCore.QTimer()
        self.record_flash_timer.setInterval(400)
        self.record_flash_timer.timeout.connect(self.ToggleRecordColour)
        self.record_flash_timer.start()

    def ToggleRecordColour(self):
        if self.recording_flag:
            if self.record_colour == 0:
                self.record_colour = 1
                self.ui.recordButton.setStyleSheet('background-color: rgb(255, 0, 0);')
            else:
                self.record_colour = 0
                self.ui.recordButton.setStyleSheet('')
    
    def ToggleRecordStatus(self):
        if self.recording_flag == False:
            self.recording_flag = True
        else:
            self.recording_flag = False
            self.ui.recordButton.setStyleSheet('')

    def StartupConnectivityCheck(self):
        for ID in self.sensors:
            command = '#RS' + str(self.sensors[ID].chip) + str(self.sensors[ID].channel)+ ';'
            command = bytes(command,'ascii')
            print('Sending status check: ' + command.decode('ascii'))
            ser.write(command)
            reply = ser.read_until(expected=bytes(';','ascii'))
            reply = reply.decode('ascii',errors = 'ignore')
            print('Received: ' + reply)
            

    def PollSensors(self):
        if P0_connected_flag:
            self.PollPressure(1,serP0)
        if P1_connected_flag:
            self.PollPressure(2,serP1)
        if flowmeter_connected_flag:
            self.PollFlow()
        self.UpdatePlots()

    def PollFlow(self):
        command = bytes('#RC;','ascii')
        print('Sending poll command: ' + command.decode('ascii'))
        ser.write(command)
        reply = ser.read_until(expected=bytes(';','ascii'))
        reply = reply.decode('ascii',errors = 'ignore')
        print('Received: ' + reply)
        # check to see if reply is simply "#;" which is the case if no sensors
        # are enabled
        if len(reply) == 2:
            return
        # if we do in fact have data, we can proceed with parsing
        self.ParseFlowValues(reply)

    def PollPressure(self,ID,serP):
        command = bytes('P\r','ascii')
        print('Pressure poll command: ' + command.decode('ascii'))
        serP.write(command)
        reply = serP.read_until(expected=bytes('>','ascii'))
        reply = reply.decode('ascii',errors = 'ignore')
        print('Received: ' + reply)
        self.ParsePressure(reply,ID)

    def ParsePressure(self,reply,ID):
        pressure = reply.split(' ')
        pressure = float(pressure[0])
        timestamp = time.time()
        pressure_sensor = {
            1:self.pressure_1,
            2:self.pressure_2
        }
        pressure_sensor[ID]['value'] = pressure*6894.76         # convert to Pa
        pressure_sensor[ID]['timestamp'] = timestamp
        if self.recording_flag:
            self.UpdatePressureLog(ID,pressure,timestamp)

    def UpdatePressureLog(self,ID,pressure,timestamp):
        with open('data_log','a') as file:
            line = '9,' + str(ID) + ',' + str(timestamp) + ',' + str(pressure*6894.76) + '\n'
            file.writelines(line)
    
    def UpdateLogFile(self,sensor,channel,timestamp,value):
        with open('data_log','a') as file:
            line = str(sensor) + ',' + str(channel) + ',' + str(timestamp) + ',' + str(value) + '\n'
            file.writelines(line)

    def ParseFlowValues(self,reply):
        reply = reply[1:-1]
        for i in range(int(len(reply)/16)):
            reading = reply[i*16:(i+1)*16]
            # print('Parsed reading: ' + reading)
            sensor = int(reading[0])
            channel = int(reading[1])
            value = int(reading[2:8],base=16)
            timestamp = int(reading[8:],base=16)
            ID = (sensor-1)*2 + (channel-1)
            self.sensors[ID].values.append(value)
            self.sensors[ID].timestamps.append(timestamp)
            # chop off excess data so that list behaves like a circular buffer
            # and doesn't grow huge in a hurry
            if len(self.sensors[ID].values) > 100:
                self.sensors[ID].timestamps = self.sensors[ID].timestamps[-100:]
                self.sensors[ID].values = self.sensors[ID].values[-100:]
            
            if self.recording_flag:
                self.UpdateLogFile(sensor,channel,timestamp,value)
    
    def UpdatePlots(self):
        for ID in self.lines:
            self.lines[ID].setData(self.sensors[ID].timestamps,self.sensors[ID].values)
        self.ui.progressBar.setProperty('value',self.pressure_1['value'])


    def ToggleStatus(self,button,ID):
        # deal with colour coding of GUI elements first
        if self.sensors[ID].status == 0:
            self.sensors[ID].status = 1
            button.setStyleSheet(self.statii['polling'])
        # elif self.sensors[ID].status == 1:
        #     self.sensors[ID].status = 2
        #     button.setStyleSheet(self.statii['recording'])
        elif self.sensors[ID].status == 1:
            self.sensors[ID].status = 0
            button.setStyleSheet(self.statii['disabled'])
        # reset plot elements
        self.ResetPlot()
        # notify Teensy which sensor to activate or deactivate
        if flowmeter_connected_flag:
            if self.sensors[ID].status == 0:
                self.ActivateSensor(ID,0)
            elif self.sensors[ID].status == 1:
                self.ActivateSensor(ID,1)

    def ActivateSensor(self,ID,direction):
        if direction == 0:
            command = '#DS' + str(self.sensors[ID].chip) + str(self.sensors[ID].channel) + ';'
        elif direction == 1:
            command = '#AS' + str(self.sensors[ID].chip) + str(self.sensors[ID].channel) + ';'
        command = bytes(command,'ascii')
        print('Sending activate command: ' + command.decode('ascii'))
        ser.write(command)
        reply = ser.read_until(expected=bytes(';','ascii'))
        reply = reply.decode('ascii',errors = 'ignore')
        print('Received: ' + reply)
        # compare record of active sensors returned by the teensy with record
        # of active sensors stored in the python program to check for errors
        self.VerifyActiveSensors(reply)

    def VerifyActiveSensors(self,reply):
        reply = reply[1:-1]
        teensy_active = int(reply[2:],base=2)
        gui_active = 0
        for ID in self.sensors:
            if self.sensors[ID].status > 0:
                gui_active += pow(2,ID)
        if teensy_active != gui_active:
            raise Warning("Active sensor error!  Microcontroller and GUI not \
                in agreement.")
        return

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