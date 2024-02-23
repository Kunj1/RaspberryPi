import os
from deepface import DeepFace

os.chdir(r'D:/Kunj/raspberry pi/images/0')
file_names=os.listdir()
for file in file_names:
    start=time.now()
    if (file.endswith(".jpg")):
        print(file)
        result=DeepFace.verify(img1_path=file,img2_path=r"D:/Kunj/raspberry pi/images/1/edited_img.jpg",enforce_detection=False)
        if (result['verified']):
            print("Door Open")
        else:
            print("F off")