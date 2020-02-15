# The Bird Guys

> Senior Capstone Project
>
> codenameBirdBox@gmail.com

This is the repository for codenameBirdBox. More details to come shortly.

## Technologies
Codename BirdBox is built on Python3.7 and Flask. Additional technologies include:
* SQL Lite and SQL Alchemy for database and database connections
* WTForms for data entry 
* Werkzeug for password hashing and additional security
* Raspberry Pi as a server and mechanical components 
* The picamera python library for video stream
* The GPIO python library for interacting with the servo motor
 

Special thanks to the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
which was invaluable in getting our boilerplate code and basic authentication created. 

***

## Team Members

1. Trevor Buza

2. Robert Kazirut

3. Connor McNamara

4. Jake Marginet

5. Paul Albrecht

6. Harris Siddiqui

***

   ## BirdBox Links

[Github](https://github.com/ASatiricalDalek/codenameBirdBox)   

[Kanban](https://trello.com/b/9zt1aQkv/birdguykanban)

***

# Set Up Environment

1. Download and install PyCharm. You can get PyCharm for free as a student at the following link: [Jetbrains PyCharm](https://www.jetbrains.com/student/)

2. Make sure you have Git installed

3. Make sure you have Python 3.7 installed

4. Open PyCharm and select “Get from Version Control” on the first splash screen

5. Paste the following link from the repo in the URL box https://github.com/ASatiricalDalek/codenameBirdBox.git

6. Click on File>Settings>Project>Project Interpreter; in the dropdown box, select Python3.7. If Python3.7 does not appear, manually point PyCharm to the Python3.7 install directory

7. Once the interpreter is configured, a yellow bar will appear above your edit window telling you that you are missing requirements. Click the “install requirements” link to install all the packages.

***

# Database Migration
Codename BirdBox uses the Flask DB Migrate library as well as SQL Alchemy to make database 
operations easier. The structure of the database can be defined in Python, and then the Flask
DB Migration tool will convert the Python classes to SQL tables. 

The opposite is also true. So queries from the database can be returned and manipulated as Python
objects. To make changes to the database:

1. Modify the appropriate class in models.py. Each class represents a table
2. Run flask db migrate -m "commit message here" to build the migration file
3. Run flask db upgrade to modify the database based on the migration file just created

Optionally, you can run flask db downgrade to revert the DB to where it was before 
***
# Hardware Requirements
 Codename BirdBox is an IoT concept and as such there are hardware requirements in order to build the project.
 1. Raspberry Pi 3 Model B+ [link](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
 2. Parallax Continuous Rotation Servo [link](https://www.parallax.com/product/900-00008)
 3. Camera Module V2 [link](https://www.raspberrypi.org/products/camera-module-v2/)
***
# codenameBirdBox
##### Requirements Determination
***


>Current Version: Version 1.0  
>Date Last Updated: 01/14/2020  
>Last Updated By: Robert Kazirut  
>Approved By: Connor McNamara  
>Approved Date: 01/15/2020

***
#1. Introduction
### User Problem/Background to the Project

Most people love their pets more than almost anything. 
Sadly, sometimes we are separated from our favorite pets for longer than we'd like and we begin to miss them 
and wonder how they are doing. Not least of all, bird lovers, who want to check in on their winged companions and have
the peace of mind that they are ok and well taken care of, even in their absence.

Given the capabilities of projects created with 'Internet of Things' in mind, the request is that an bird monitoring
and feeding device be developed and an associated website could be deployed as a web service for consumers
of the product.
### Goals of the Project

Develop an bird monitoring and feeding device from raspberry pi and various other integrated devices as well as a
companion website which will allow users to watch a video stream of their bird as well as scheduling feedings,
or feed them now.
### Scope

Develop a bird monitoring device with the following functionality:

- Video transmission to an associated website
- Scheduled treat dispensing
- Triggered treat dispensing

Develop an associated website with the following functionality:

- Follow standards for websites in general functionality (For example, Account Creation, Secure Login, etc.)
- Access and view video transmission from bird monitoring device upon log in
- Schedule treat dispensing to monitoring device
- Trigger treat dispensing
***

## 2. Assumptions

- The video transmission is only taking place upon the user logging into their account
- The video transmission is inaccessible to users whom are not logged in
- The scheduled treat dispensing is dependent upon the device maintaining connectivity
- The potential functionality may need to wait until a 2nd phase post launch
  - Take a static photo
  - View static photo album webpage
  - Water monitoring
  - Notification when feeding occurs
  - Remember Me login functionality

***

## 3. Initial State

Currently there is no device or website. This project will be developed from scratch without a reference point.

***
   

