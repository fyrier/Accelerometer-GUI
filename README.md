Continuous authentication using Accelerometer data
===================

This repository contains the Graphical User Interface for a program using accelerometer data to authenticate users and identify the activity that they are performing. It is based on my Bachelor's Thesis, where all the premises and testing done to back the concept are presented (it can be found [here](https://e-archivo.uc3m.es/handle/10016/25731)). This GUI provides a way to test user authentication based on accelerometer data.

----------
Details
-------------
This project uses Texas Instrumets eZ430-Chronos smartwatch. To manage the connections between the computer and the clock, [chronoslib](https://github.com/rlabs/ez430-chronos-python) from [rlabs](https://github.com/rlabs)  is used. 
To recognize users and activities, the system uses [MEKA](http://meka.sourceforge.net/) to create a multi-target classifier, using Bcc and J48.
There are several error messages missing that will be added over the next days, please follow the instructions presented on this document to avoid crashing the program.

Prerequisites
-------------
Before using the GUI, there are a few conditions that need to be met:

 - The system gets the accelerometer data from [Texas Instruments eZ430-Chronos](http://www.ti.com/tool/ez430-chronos). Although this model is not longer in stock, it still receives support from Texas Instruments.
 - Data is sent from the smartwatch to an USB Access Point that comes with it. Its drivers need to be installed in the system. **If you are using Windows** they need to be installed through troubleshoot mode, as they are not signed. Windows drivers can be found [here](http://www.ti.com/lit/zip/slac341) and Linux drivers can be found [here](http://www.ti.com/lit/zip/slac388). Once the drivers are installed, test that data is sent correctly from the smartwatch to the computer using the provided software by Texas Instruments (Control Center).
 - This program is developed using Python 2.7 and it has been tested on Windows, **it hasn't been tested yet on Linux**. To use it on Linux, the port needs to be changed on chronoslib from `COM3` to `/dev/ttyACM0`, present on the variable `PORT`.
 - To be able to use chronoslib, serial library from Python must be installed on the computer.
 - To be able to access to MEKA algorithms, the /lib/ directory included on its code must be added to the project.

User manual
-------------
As mentioned, this GUI presents a way to test user and activity recognition based on accelerometer data. To train the system, it gets user information using the smartwatch and stores it. MEKA will later use that file (data.arff) to generate the model. 
Once one or more users are registered on the system they can be recognized by it performing any of the stated activities: resting, walking, running or jumping. More activities can be added by modifying the `main` method of the program, using Activity data type, assigning a new ID, name and training time to it. 
Over the next sections, each screen and its options will be discussed.

### 1. Main screen

Once you execute the program and if all the prerequisites are met correctly, the first screen that appears is the main screen. It presents the user with a text indicating where the user is ("User recognition") and a small text explaining the possible actions the user can perform. From the main screen there are two functions that can be accessed:

- **Add user**: to incorporate a new user to the system and for it to be able to recognize both the user and the activity, data needs to be recorded to learn how the user performs the specified activities.
- **Recognize user**: once a user is registered on the system, the program will receive data from the smartwatch for 30 seconds and will determine both the user and the activity.

<img align="center" src="https://github.com/fyrier/Accelerometer-GUI/blob/master/User%20Manual%20images/Pantalla%201.PNG">

### 2. Add user

The selection of the option **Add user** on the main screen will take the user to this screen. Its function is simple: inform the user of the actions that need to be performed and for how long in order to register them into the system.
On the screen the following message is shown: 
>"Training period for activity *x* (*name of the activity*) started. Please, perform this action for *time* seconds.

*x* corresponds with the activity ID, *name of the activity* to the name corresponding to that ID and *time* for the time in seconds that the user needs to be performing that activity. On the default version, the one provided, the activities are rest, walk, run and jump and they all need to be performed for 10 seconds.
Once the training period for an activity is finished, the message will indicate the user that they need to change the activity, and so on until data for all activities is collected.
There is a **Cancel** button on this screen that will take the user back to the main screen if selected, terminating the training process. **The selection of this option interrupts the model update to include the new user in the system, so the system will not be able to recognize this user if they choose to try the Recognize user option**. For the user to be incorporated into the system, the training process needs to be completed for **all** activities.
After data is recorded for every activity and the model is updated to register the new user, a message will indicate so and a Return button appears to take the user back to the main screen.
<img align="center" src="https://github.com/fyrier/Accelerometer-GUI/blob/master/User%20Manual%20images/Pantalla%202.PNG">

<img align="center" src="https://github.com/fyrier/Accelerometer-GUI/blob/master/User%20Manual%20images/pantalla%202.1.PNG">

**Please make sure** that you activate the ACC transmission on the smartwatch once the training process starts.

### 3. Recognize user

Once a user is registered on the system, they can be recognized if the select the option **Recognize user** on the main screen.        
When this option is selected, the message *Collecting user data. Please, stand by...*  appears on screen as well as a **Cancel** button to take the user back to the main screen. As soon as this option is selected, data will be recorded from the smartwatch to check with the generated model which user wears the smartwatch and the activity they are perfoming.
Once the model is consulted, its result is showed in the screen with the following message:
>Data belongs to user *x* with a probability of *x probability* while *activity* with a probability of *activity probability*.

*x* corresponds with the user ID, *x probability* with the probability that the data belongs to user x, *activity* is the activity that has been inferred by the system and *activity probability* with the probability that user x is performing that activity.
With this message, a **Return** button appears on the screen to take the user back to the main screen.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
<img align="center" src="https://github.com/fyrier/Accelerometer-GUI/blob/master/User%20Manual%20images/Patnalla%203.PNG">

<img align="center" src="https://github.com/fyrier/Accelerometer-GUI/blob/master/User%20Manual%20images/pantalla%203.1.PNG">

**Please make sure** that you activate the ACC transmission on the smartwatch once the recognition process starts.     
