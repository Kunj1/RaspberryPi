import os
from deepface import DeepFace

os.chdir(r'D:/Kunj/raspberry pi/images/0')
file_names=os.listdir()
for file in file_names:
    if (file.endswith(".jpg")):
        print(file)
        result=DeepFace.verify(img1_path=file,img2_path=r"D:/Kunj/raspberry pi/images/1/2.jpg",model_name='Facenet', detector_backend='mtcnn', enforce_detection=False)
        if (result['distance']<0.15):
            print("Door Open")
        else:
            print("F off")
