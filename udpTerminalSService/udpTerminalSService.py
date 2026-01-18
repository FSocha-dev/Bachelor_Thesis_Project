import socket as udps
import time
import datetime
import os
import sys
import json
import threading

class socketThread(threading.Thread):
    def __init__(self, threadID, name, UDP_HOST, UDP_PORT, textFilePath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.UDP_HOST = UDP_HOST
        self.UDP_PORT = UDP_PORT
        self.textFilePath = textFilePath
        # Open server socket
        try:
            self.serverSocket = udps.socket(udps.AF_INET, udps.SOCK_DGRAM)
            self.serverSocket.bind((self.UDP_HOST, self.UDP_PORT))
        except Exception as e:
            print("Problem with setting up socket.")
            print(e)

    def run(self):
        try:
            while True:
                serviceComms, serviceAddr = self.serverSocket.recvfrom(1024)
                serviceCommsStr = str(serviceComms, 'utf-8')
                with open(self.textFilePath, "w") as textFile:
                    tsepoch = time.time()
                    timeStampNow = datetime.datetime.fromtimestamp(tsepoch).strftime('%Y.%m.%d %H:%M:%S:%f')
                    serviceCommsStrTS = str(timeStampNow) #+ '\t' + serviceCommsStr + '\t' + str(serviceAddr[0])
                    textFile.write(serviceCommsStrTS)
                print(serviceCommsStrTS)
        except Exception as e:
            print("Problem with main loop - reading data from socket, printing them in the terminal or saving to file.")
            print(e)

# Read json
try:
    with open(os.path.join(sys.path[0], "config.json"), "r") as configFile:
        configData = json.load(configFile)
except Exception as e:
    print("Problem with json file.")
    print(e)

# Timestamp
tsepoch = time.time()
timeStampNow = datetime.datetime.fromtimestamp(tsepoch).strftime('%Y%m%d_%H%M%S')

# Address list
try:
    UDP_HOST = configData["UDP_HOST"]
except Exception as e:
    print("Problem with reading UDP_HOST.")
    print(e)

# Port
try:
    UDP_PORT_LISTEN_DATA = configData["UDP_PORT_LISTEN_SERVICE"]
except Exception as e:
    print("Problem with reading UDP_PORT_LISTEN_SERVICE.")
    print(e)

# TXT File with service data
try:
    #textFileServiceComm = configData["textFilePath"] + configData["textFileServiceComm"] + "serviceComm" + timeStampNow + ".txt"
    textFileServiceComm = configData["textFilePath"] + "data" + ".txt"
except Exception as e:
    print("Problem with reading one of the paths.")
    print(e)

# Start server
serverThread = socketThread(1, "SocketThread", UDP_HOST, UDP_PORT_LISTEN_DATA, textFileServiceComm)
serverThread.daemon = True
serverThread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()