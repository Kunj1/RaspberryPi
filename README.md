# Raspberry Pi Face Detection Door Lock

Welcome to the Raspberry Pi Face Detection Door Lock project! This project combines face detection technology with Raspberry Pi to create a secure door lock system.

## Overview

The Raspberry Pi Face Detection Door Lock project utilizes various components such as a Raspberry Pi board, a camera module, a solenoid lock, an LCD display, and more. When a person presses the doorbell button, the system captures an image, processes it using deep learning-based face detection, and grants access if the detected face matches a pre-defined database of authorized users.

*This project has been run on the Miniforge3 anaconda environment on the Raspberry Pi 4 Model B 4GB RAM*

## Features

- Face detection and recognition using the DeepFace library
- The 'Facenet' model has been used with 'mtcnn' as the backend for a balanced efficient and accurate face detection.
- Integration with a solenoid lock mechanism for door access control
- Real-time communication with the owner via SMS alerts
- One-time password (OTP) verification for unrecognized faces
- User-friendly interaction through an LCD display

## Components Used

- Raspberry Pi board
- Camera module (e.g., Raspberry Pi Camera)
- Solenoid lock
- LCD display (2x16)
- Button switch for doorbell
- LED and buzzer for visual and audible notifications
- Keypad module for OTP entry

## Software Dependencies

- Twilio API has been used for SMS alert system : [https://console.twilio.com/]
- Freeimage API has been used for upload and access of images on cloud : [https://freeimage.host/]
- Miniforge3 anaconda environment : [https://github.com/conda-forge/miniforge]

## Methodology

1. Press the doorbell button to trigger the image capture process.
2. Brighten, add clarity and sharpnen the image for better detection(Adjust the values according to the lighting and camera quality).
3. Process the captured image using deep learning-based face detection.
4. If the detected face matches an authorized user, grant access by opening the solenoid lock.
5. If the face is unrecognized, send an SMS alert to the owner with an image and an OTP.
6. The owner can share the OTP with the visitor for manual entry via the keypad module.

## Future Scope

In the future, this project can be expanded with additional features such as:

- Integration with cloud-based face recognition services for enhanced accuracy
- Mobile app integration for remote access and control
- Voice recognition for hands-free operation
- Retina and movement scanning with the detection model to enhance accuracy

## Implementation

The project implementation involves hardware setup, software installation, and code deployment. 

## Commercialization & Development Strategy

To commercialize and further develop this project, consider the following strategies:

- Collaborate with security system companies for product integration.
- Conduct market research to identify potential users and their requirements.
- Establish partnerships with hardware manufacturers for mass production.
- Continuously improve the software with updates and new features based on user feedback.
