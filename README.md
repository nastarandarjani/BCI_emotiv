# BCI_EMOTIV
This project consists of a Python server that reads EEG signals from an EMOTIV gadget via device and a React Native client that displays a circle whose size changes based on the focus metric which received from EEG signals.

## Description
The server code reads EEG signals from an [EMOTIV Epoc+](https://www.emotiv.com/epoc/) device via a dongle and stores the online signals in a matrix with dimensions of 14 channels by 256 samples per channel. As new data is received, the server rolls the matrix and fills in the last column.
The server then applies a butter filter to the signal to obtain alpha frequency band signals, and extracts the mean power of those signals using the Welsh method.
The radius value is assigned to a variable named "radius" and is sent through a WebSocket to localhost on port 8000.
On the client side, which is an Android app, the user can input the URL address of ngrok in a text box.
After a successful connection, the client receives the radius value from the server and updates the size of a circle displayed in the app accordingly.
The radius value is also displayed in the upper part of the circle.

The goal of the app is to provide biofeedback to the user by visualizing the changes in the size of the circle.
As the user relaxes, the circle becomes bigger and vice versa.


## Installation

### server side
1. Clone the repository.
2. Install Python (version 3.7.16 or prior).
3. Install required Python packages by running `pip install -r requirements.txt`.
4. Download and install the [ngrok application](https://ngrok.com/), to forward the data from server to client.

### Client Side

1. Clone the repository.
2. Install Chocolatey, which is a popular package manager for Windows.
3. Install Node.js (by running `choco install -y nodejs-lts microsoft-openjdk11`).
4. Install Android Studio and Android SDK.
5. Install all the packages needed for the client repository by NPM package manager by running `npm install` in the windows command prompt.
   In case an of error, use `npm install --legacy-peer-deps` command.
6. Build the Android app by running `npm run android`. The build might take a long time for the first time. So be patient.

***Note 1:*** Building a React Native app with native code, requires the Android 13 (Tiramisu) SDK in particular.

***Note 2:*** Don't forget to add Android SDK and python to the environment variables.

***Note 3:*** In order to execute the client app, it needed to be installed on a simulator or an external cell phone device.
For external cell phones, enable developer options and check the USB debugging option.
The `npm run android` command will start the simulator if there’s no external device connected.

## Running program

1. Turn on the Emotive device and insert the USB Dongle.
2. Open a cmd window in the BCI-Server-main folder and run `python3 main.py` command.
3. Open ngrok.exe file and run `ngrok http 8000`.
4. In the android application on your mobile, insert the ngrok url in the textbox and press connect button.

## Code explanation
### Server
Most of the server code stems from the examples in the Cykit repository, but some will be explained here. 
Decryption and utility functions are out of the scope of this documentation.
*	`__init__` function will find the device and its serial number to work with later.
* `Handler` function will wait for the data to be put in the queue and sent to the WebSocket. 
* `start_server` variable is defined as a WebSocket serving the client's data.
* `asyncio.get_event_loop()` run twice. 
First time for starting the WebSocket server and second time in order to run the app forever.
* `butter_bandpass` and `butter_bandpass_filter` functions return the filtered signals with relative frequency ranges.
* `update` function update a 14*256 dimension matrix and return the radius value.
* `get_frequency` and `extract_power` functions filters the signals and return the mean power spectral density (PSD) value of the alpha frequency bands.

### Client (App) 
The client app is made of Android and IOS configuration folders, required JavaScript files for react-native, main functionality, and package.json, which contain JavaScript packages. 
The main functionality of the client is in the App.js file.
This file contains the app function, which presents the main component rendered on the cell phone. 
*	Values that the screen re-renders if changed are known as States, and their default values are defined using the function `useState`, as below:
```
const [data, setData] = useState();
```
* The `useEffect` function runs after the component’s initial render and whenever a designated state changes.
*	A circle is shown using a tag called View (equal to div in HTML) and the curve (border-radius) value.
Attributes of this tag are width, height, distance to the top of the screen, and border-radius value.
If the data is valid, a `finalData` value and a constant are added to these values.

### Usage

1. Ensure that the server is running and is sending data to `localhost:8000`.
2. Open the android app on an Android device or emulator.
3. The app will display a circle whose size changes based on the alpha power of brain waves received from the server.
4. The radius value is also displayed in the upper side of the circle.

### Acknowledgments
The extracting Emotiv device data and decoding process is derived from [CyKit](https://github.com/CymatiCorp/CyKit) repository.
All the related documentation are available in the mentioned repository.
