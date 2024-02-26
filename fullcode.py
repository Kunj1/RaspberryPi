import RPi.GPIO as GPIO
import subprocess
from deepface import DeepFace
import cv2
import os
from datetime import datetime
from time import sleep
import numpy as np
import requests
from twilio.rest import Client
import random
from RPLCD.i2c import CharLCD

otp=''
lcd = CharLCD('PCF8574', 0x27)

C1 = 32
C2 = 36
C3 = 38
C4 = 40

L1 = 31
L2 = 33
L3 = 35
L4 = 37

def countdown(a):
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string("Capturing Image")
    lcd.cursor_pos = (1,5)
    lcd.write_string(f"in {a}..")

def sms():
    global otp
    url = r'https://freeimage.host/api/1/upload'
    api_key = '6d207e02198a847aa98d0a2a901485a5'
    image_path = r'/home/Facedetection/image.jpg'
    with open(image_path, 'rb') as file:
        image_data = file.read()
    params = {'key': api_key, 'action': 'upload', 'format': 'json'}

    response = requests.post(url, params=params, files={'source': image_data})

    if response.status_code == 200:
        data = response.json()
        image_url = data['image']['url']
        print("Image uploaded successfully. URL:", image_url)
    else:
        print("Error:", response.status_code)


    characters = '0123456789'
    otp = ''.join(random.choice(characters) for _ in range(5))


    account_sid = 'AC2d1627b6a27cd83700fdeae086600378'
    auth_token = 'd4015b5e7f029bf147a9d495135fdf51'
    client = Client(account_sid, auth_token)
    from_number = '+17606421558'
    to_number = '+916290679821'
    message_body = '\nHello from Raspberry pi Door Lock.\nALERT: Unknown person detected at home!! Please check the attached image.\nURL: '
    body2='\nUse this OTP to communicate with the unidentified person and grant access:'
    message = client.messages.create(body=message_body+image_url+body2+otp, from_=from_number, to=to_number)
    print("Message sent successfully. SID:", message.sid)


def solenoid():
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string("Access granted!")
    lcd.cursor_pos = (1,2)
    lcd.write_string("Door opened")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)
    GPIO.output(8, GPIO.HIGH)
    sleep(5)
    GPIO.output(8, GPIO.LOW)
    GPIO.cleanup()
    return
    



GPIO.setwarnings(False)

while True:
    lcd.clear()
    lcd.cursor_pos = (0,4)
    lcd.write_string("WELCOME!")
    lcd.cursor_pos = (1,1)
    lcd.write_string("Press the Bell!")

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)                              #LED
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)     #Button
    while True:
        state=GPIO.input(23)
        if state==False:
            break

    if True:
        GPIO.output(18, GPIO.HIGH)
        sleep(1.5)
        GPIO.output(18, GPIO.LOW)
        GPIO.cleanup()


        for i in range(3,0,-1):
            countdown(str(i))
            sleep(1)


        command="libcamera-jpeg -t 3000 -o /home/Facedetection/image.jpg"
        result=subprocess.run(command, shell= True, capture_output=True, text= True)


        lcd.clear()
        lcd.cursor_pos = (0,2)
        lcd.write_string("Please wait")
        lcd.cursor_pos = (1,1)
        lcd.write_string("for detection")


        image = cv2.imread(r'/home/Facedetection/image.jpg')
        os.remove(r'/home/Facedetection/image.jpg')
        brightness_factor = 2
        brightened_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
        diameter = 9
        sigma_color = 75 
        sigma_space = 75
        clarity_image = cv2.bilateralFilter(brightened_image, d=diameter, sigmaColor=sigma_color, sigmaSpace=sigma_space)
        sharpening_kernel = np.array([[-1, -1, -1],[-1, 9, -1],[-1, -1, -1]])  
        sharpened_image = cv2.filter2D(clarity_image, -1, sharpening_kernel)
        cv2.imwrite(r'/home/Facedetection/image.jpg', sharpened_image)

        
        flag=0
        os.chdir(r'/home/Facedetection/images')
        file_names=os.listdir()
        for file in file_names:
            if (file.endswith(".jpg")):
                print(file)
                result=DeepFace.verify(img1_path=file,img2_path=r'/home/Facedetection/image.jpg',model_name='Facenet', detector_backend='mtcnn',enforce_detection=False)
                print(result['distance'])
                if (result['distance']<0.15):
                    flag=1

                    solenoid()

                    break;
        if(flag==0):

            lcd.clear()
            lcd.cursor_pos = (0,1)
            lcd.write_string("Error! Contact")
            lcd.cursor_pos = (1,1)
            lcd.write_string("owner for OTP")
            
            sms()

            GPIO.setmode(GPIO.BOARD)

            GPIO.setup(L1, GPIO.OUT)
            GPIO.setup(L2, GPIO.OUT)
            GPIO.setup(L3, GPIO.OUT)
            GPIO.setup(L4, GPIO.OUT)

            GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            def readLine(line, characters):
                ch = ''
                GPIO.output(line, GPIO.HIGH)
                if(GPIO.input(C1) == 1):
                    ch = characters[0]
                if(GPIO.input(C2) == 1):
                    ch = characters[1]
                if(GPIO.input(C3) == 1):
                    ch = characters[2]
                if(GPIO.input(C4) == 1):
                    ch = characters[3]
                GPIO.output(line, GPIO.LOW)
                return ch

            try:
                s = ""
                while True:
                    t = ""
                    t += readLine(L1, ["1","2","3","A"])
                    t += readLine(L2, ["4","5","6","B"])
                    t += readLine(L3, ["7","8","9","C"])
                    t += readLine(L4, ["*","0","#","D"])
                    if(len(t) > 0):
                        lcd.clear()
                        lcd.cursor_pos = (0, 0)
                        if(t == 'A'):
                            print(s)
                            lcd.cursor_pos = (1, 0)
                            lcd.write_string(s)
                            break
                        elif(t == 'B'):
                            if(len(s) > 0):
                                lcd.cursor_pos = (0, 0)
                                s = s[0: len(s) - 1]
                                lcd.write_string(s)
                        elif(t == 'C'):
                            print(s, end = "\nString reset")
                            s = ""
                        else:
                            s += t
                            print(s)
                            lcd.write_string(s)
                    sleep(0.2)
            except KeyboardInterrupt:
                print("\nApplication stopped!")
            
            
            if(otp==s):
                print("Door Open")
                solenoid()

            else:
                lcd.clear()
                lcd.cursor_pos = (0,3)
                lcd.write_string("Wrong OTP")
                lcd.cursor_pos = (1,3)
                lcd.write_string("Try Again")
                sleep(5)

            
    GPIO.cleanup()