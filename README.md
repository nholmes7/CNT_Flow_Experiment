# About this Project
This project was developed in the summer of 2021 as a means for testing experimental carbon-nanotube based flow sensors.  The project combines a graphical user interface (GUI) written in python, and microcontroller code written for a Teensy 4.0 using the Arduino ecosystem.  The microcontroller reads sensor values from a set of Analog Devices AD7746 ICs over an I<sup>2</sup>C connection, buffers the values, and relays them to the python prgram over a USB serial connection.  The python program also polls two pressure transducers over USB serial connection.
# Getting Started
To get a local copy of this project running, follow these steps.
1. Install [virtualenv](https://pypi.org/project/virtualenv/).

    The below command is recommended, however other options are outlined on the [project page](https://virtualenv.pypa.io/en/latest/installation.html).
    ```
    pipx install virtualenv
    ```
2. Install python dependencies.

    **Windows**
    ```
    virtualenv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
    **Linux**
    ```
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
## Prerequisites
## Linux
## Windows
# Use
To run the program, simply run:
```
python main.py
```
The GUI displays a representation of how the sensing elements are laid out relative to one another.  A live plot of the streamed sensor values and a bar indicating the measured differential pressure are included for live monitoring of the experiment.
> **_NOTE:_** As currently configured on 2021/10/17, the pressure differential bar is of little use as the scale does not adjust properly.

<img src="images/GUI Demo Oct 6.png" width="600">

The sensing elements may be clicked to enable the corresponding channel and begin streaming data.  With the desired data streaming, the record button may be pressed to begin writing the data to a file.  The output file can be specified using the browse button in the Save Path field.
> **_NOTE:_** As of 2021/10/17, the file browse button has not been connected to anything.  The program writes to a file called `data_log`.  The program will continually append to the `data_log` file each time the record button is pressed.  The `data_log` file contents must be deleted prior to pressing the record button if a new file is desired.
# Licence
Distributed under the BSD License. See `LICENSE` for more information.
