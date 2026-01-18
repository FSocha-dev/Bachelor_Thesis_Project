import socket as udps
import time
import os
import sys
import json
import threading
from datetime import datetime
from tkinter import *
from tkinter import messagebox as msb
from PIL import Image, ImageTk

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
                    sessionData, sessionAddr = self.serverSocket.recvfrom(1024)
                    sessionDataStr = str(sessionData, 'utf-8')
                    if sessionDataStr == "d5:a7:d7:32:a8:ca":
                        deviceTag = "Room 1"
                        date = datetime.now()
                        var = str(date)
                        entry1.delete(0,END)
                        entry1.insert(0, var)
                        tempVal = var + '\t' + deviceTag
                        img_r = Label(topFrame, image=img_red)
                        img_r.grid(row=1, column=2)
                        img_r.place()
                    elif sessionDataStr == "d5:a7:d7:32:a8:cb":
                        deviceTag = "Room 2"
                        date = datetime.now()
                        var = str(date)
                        entry2.delete(0,END)
                        entry2.insert(0, var)
                        tempVal = var + '\t' + deviceTag
                        img_r = Label(topFrame, image=img_red)
                        img_r.grid(row=2, column=2)
                        img_r.place()
                    elif sessionDataStr == "d5:a7:d7:32:a8:cc":
                        deviceTag = "Room 3"
                        date = datetime.now()
                        var = str(date)
                        entry3.delete(0,END)
                        entry3.insert(0, var)
                        tempVal = var + '\t' + deviceTag
                        img_r = Label(topFrame, image=img_red)
                        img_r.grid(row=3, column=2)
                        img_r.place()
                    if sessionDataStr == "d5:a7:d7:32:a8:ca" and "d5:a7:d7:32:a8:cb" and "d5:a7:d7:32:a8:cc":
                        textFile = open(self.textFilePath, "a")
                        sessionDataStrTS = var + '\t' + deviceTag + '\t' + str(sessionAddr[0])
                        textFile.write(sessionDataStrTS + "\n")
                    file = open("save_data.txt", "a")
                    file.write(tempVal + "\n")
                    file.close()   
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

# TimeStamp
date = datetime.now()
timeStampNow = date.strftime('%Y%m%d_%H%M%S')

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

# TXT File with session data
try:
    textFileSessionData = configData["textFilePath"] + configData["textFileSessionData"] + "Session_data_" + timeStampNow + ".txt"
except Exception as e:
    print("Problem with reading one of the paths.")
    print(e)

#funkcje przyciskow
def click_action_show_logs():
    new_window = Tk("okno Save log")
    new_window.title("Saved logs")
    new_window.geometry("380x480")
    T = Text(new_window, height = 24, width = 34)
    l = Label(new_window, text = "Saved logs")
    l.config(font =("Courier", 14))
    save_data = open("save_data.txt").read()
    b = Button(new_window, text = "Exit",
            command = new_window.destroy)
    l.pack()
    T.pack()
    b.pack()
    T.insert(END, save_data)
    
def click_reset():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    img_g = Label(topFrame, image=img_green)
    img_g.grid(row=1, column=2)
    img_g.place()
    img_g = Label(topFrame, image=img_green)
    img_g.grid(row=2, column=2)
    img_g.place()
    img_g = Label(topFrame, image=img_green)
    img_g.grid(row=3, column=2)
    img_g.place()
    
#utworzenie glownego okna
window = Tk("glowne okno aplikacji")
window.title("App")
window.geometry("650x500")

#utworzenie ramek
topFrame = Frame(window)
topFrame.pack(side=TOP)
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)

#wczytanie obrazow i ich przeskalowanie
image1 = Image.open("green_button.png")
image1 = image1.resize((70, 70))
image2 = Image.open("red_button.png")
image2 = image2.resize((70, 70))
img_green = ImageTk.PhotoImage(image1)
img_red = ImageTk.PhotoImage(image2)

#rozne czcionki
font_comic = ("Comic Sans MS", 10, "bold")
font_times20 = ("Times New Roman", 22, "bold")
font_times15 = ("Times New Roman", 15)

#wyswietlenie glownych napisow
lo = Label(topFrame, text="Lo.", font=font_times20, padx=50, pady=20)
lo.grid(row=0, column=0)
id = Label(topFrame, text="ID", font=font_times20, padx=40)
id.grid(row=0, column=1)
status = Label(topFrame, text="Status", font=font_times20, padx=40)
status.grid(row=0, column=2)
timestamp = Label(topFrame, text="Timestamp", font=font_times20, padx=40)
timestamp.grid(row=0, column=3)

#napisy poboczne
one = Label(topFrame, text="1.", font=font_times15, pady=30)
one.grid(row=1, column=0)
two = Label(topFrame, text="2.", font=font_times15, pady=30)
two.grid(row=2, column=0)
three = Label(topFrame, text="3.", font=font_times15, pady=30)
three.grid(row=3, column=0)
room1 = Label(topFrame, text="room 1", font=font_times15, pady=30)
room1.grid(row=1, column=1)
room2 = Label(topFrame, text="room 2", font=font_times15, pady=30)
room2.grid(row=2, column=1)
room3 = Label(topFrame, text="room 3", font=font_times15, pady=30)
room3.grid(row=3, column=1)

#utworzenie entry widgetow 
entry1 = Entry(topFrame, width = 26)
entry1.grid(row=1, column=3)
entry2 = Entry(topFrame, width = 26)
entry2.grid(row=2, column=3)
entry3 = Entry(topFrame, width = 26)
entry3.grid(row=3, column=3)

#wyswietlenie obrazow
img_g = Label(topFrame, image=img_green)
img_g.grid(row=1, column=2)
img_g.place()
img_g2 = Label(topFrame, image=img_green)
img_g2.grid(row=2, column=2)
img_g2.place()
img_g3 = Label(topFrame, image=img_green)
img_g3.grid(row=3, column=2)
img_g3.place()

#utworzenie przyciskow i wywolanie funkcji click_reset
show_logs = Button(bottomFrame, height=4, width=13, text="SHOW LOGS", relief=SOLID, font=font_times15, command = click_action_show_logs)
reset = Button(bottomFrame, height=4, width=13, text="RESET", relief=SOLID, font=font_times15, command=click_reset)
quit = Button(bottomFrame, height=4, width=13, text="QUIT", relief=SOLID, font=font_times15, command=window.destroy)

#wyswietlenie przyciskow
show_logs.pack(side=LEFT, expand=YES, fill=BOTH)
reset.pack(side=LEFT, expand=YES, fill=BOTH)
quit.pack(side=LEFT, expand=YES, fill=BOTH)

# Start server
serverThread = socketThread(1, "SocketThread", UDP_HOST, UDP_PORT_LISTEN_DATA, textFileSessionData)
serverThread.daemon = True
serverThread.start()
window.mainloop()