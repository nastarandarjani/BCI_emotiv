import os
import sys
print(str(sys.path))
sys.path.insert(0, '..//py3//cyUSB//')
sys.path.insert(0, '')

import cyPyWinUSB as hid
import queue
from cyCrypto.Cipher import AES
import asyncio

import websockets
import numpy as np 
from scipy import signal
 
def butter_bandpass(lowcut, highcut, fs, order=5): 
    return signal.butter(order, [lowcut, highcut], fs=fs, btype='band') 
 
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5): 
    b, a = butter_bandpass(lowcut, highcut, fs, order=order) 
    y = signal.lfilter(b, a, data)
    return y 
 
def update(data, packet_data): 
    data = np.roll(data, -1, axis = 1) 
    data[:, 255] = packet_data
            
    theta,alpha, beta = get_frequency(data) 
    radius = extract_power(theta, alpha, beta)
    return data, radius

def extract_power(theta, alpha, beta):
    fs = 128
    _, s_alpha = signal.welch(alpha, fs, nperseg=len(alpha))
    _, s_theta = signal.welch(theta, fs, nperseg=len(theta))
    ind = np.array([1, 1, 1, 0, 0,0, 0,0,0,0,0, 1, 1,1])
    radius = (np.mean(np.mean(s_alpha[ind, :], axis = 1)) - 350) *2
    return radius

def get_frequency(data): 
    #Sampling frequency 
    Fs = 128 
 
    theta = butter_bandpass_filter(data, 4, 8, Fs, order=5) 
    alpha = butter_bandpass_filter(data, 8, 13, Fs, order=5) 
    beta = butter_bandpass_filter(data, 13, 30, Fs, order=5) 
 
    return theta, alpha, beta 

tasks = queue.Queue()

class EEG(object):
    
    def __init__(self):
        self.hid = None
        self.delimiter = ", "
        
        devicesUsed = 0
    
        for device in hid.find_all_hid_devices():
                print(device.product_name )
                if device.product_name == 'EEG Signals':
                    devicesUsed += 1
                    self.hid = device
                    self.hid.open()
                    self.serial_number = device.serial_number
                    device.set_raw_data_handler(self.dataHandler)
        if devicesUsed == 0:
            print('No Devices!')
            os._exit(0)
        sn = self.serial_number
        
        # EPOC+ in 16-bit Mode.
        k = ['\0'] * 16
        k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]
        
        # EPOC+ in 14-bit Mode.
        #k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]
        
        self.key = str(''.join(k))
        self.cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)

    def dataHandler(self, data):
        join_data = ''.join(map(chr, data[1:]))
        data = self.cipher.decrypt(bytes(join_data,'latin-1')[0:32])
        if str(data[1]) == "32": # No Gyro Data.
            return
        tasks.put(data)

    def convertEPOC_PLUS(self, value_1, value_2):
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        return edk_value

    def get_data(self):
       
        data = tasks.get()
        #print(str(data[0])) COUNTER

        try:
            packet_data = ""
            for i in range(2,16,2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            for i in range(18,len(data),2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            packet_data = packet_data[:-len(self.delimiter)]
            return str(packet_data)

        except Exception as exception2:
            print(str(exception2))

cyHeadset = EEG()


async def handler(websocket, path):
    print('slms')
    #  0, 001, 002, 03, 04, 05, 06, 07, 08, 09, 10, 011, 012, 13 
    # F3, FC5, AF3, F7, T7, P7, O1, O2, P8, T8, F8, AF4, FC6, F4 
    data = np.zeros((14, 256))
    while True:
        while tasks.empty():
            pass
        x = cyHeadset.get_data()
        x = np.array(x.split(', '), dtype = float)
        data, radius = update(data, x)
        print(radius)
        await websocket.send(str(radius))
        # await websocket.send('slm')



start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
