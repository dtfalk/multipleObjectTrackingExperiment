# **Multiple Object Tracking Task**


Hello! My name is David Tobias Falk, employee at the APEX Lab at the University of Chicago. This is a short walkthrough of the features of this multiple object tracking experiment. This will include explanations of where to find things, and how some of the more complicated aspects of the code work. 

There are three versions of the task in this repository: a behavorial version, a lab streaming layer version, and a net station version. Hopefully these will cover your use cases, or at least give you some over-commented code you can use to design a version that fits your use cases. 

## **Contact Info**
Email: dtfalk@uchicago.edu, davidtobiasfalk@gmail.com
Cell: 1-413-884-2553
Feel free to reach out if you have questions, comments or concerns. If you use my phone, then please text me first as I will assume that you are spam if you call me out of the blue. 

## **Things that apply to all of the versions**
I have built this code to allow the user a lot of freedom for modifying the task. Most of the things that will be changeable are found in each version's **constants.py** and **gameOptions.py** files. The constants file largely handles things such as background colors, durations of various parts of the game (resting state, amount of time for real trials, how long we show the level screen for, etc...). The game options file is filled with boolean variables. When a given variable is **True**, then that part of the game's functionality will be activated, and when it is **False** it will be deactivated. For example, setting **levelSelectEnabled** to **True** provides the user with the ability to choose which level they start on. I would reccomend poking around these files as they are well commented and contain the bulk of the easy ways that you have to modify the task. Also, the code to start each version's experiment is in the "main.py" file found in each of the folders. Just run "python main.py" after navigating to the version's directory and your experiment will run!

## **How the game changes as you progress through the levels**
Explaining this part has baffled me for a long while. I am still unsure how to clearly explain it. On level 1, you begin with **startingTargets** (defined in the constants file) number of targets, with ball speed equal to 1 and a **startingDistractors** number of distractors. If you succeed, then a distractor is added. As you keep succeeding, distractors keep getting added until you hit the **distractorOverflow** (defined in constants) limit at which point we rest the distractors to their lowest level and increase the ball speed. YOu go through the same process, increasing the distractors until you hit the distractor overflow limit and then increasing the ball speed, until you hit the **speedOverflow** limit, at which point we increase the number of targets by one, reset the ball speed, and set the number of distractors to the number of targets. In previous versions, the number of distractors would start as the number of targets minus one, but we realized that subjects would just track the distractors because there were fewer distractors than targets. The out of the box version that is on this page has the number of distractors range from the number of targets, to the number of targets plus two. The range of distractors and the range of ball speeds can be increased/decreased by incrementing/decrementing their associated overflow variables in the constants file. Here is a table descibing how the current level relates to the number of targets, distractors, and ball speed

| Level      | Number of Targets      | Ball Speed      | Number of Distractors     |
| ---------- | ---------------------- | --------------- | ------------------------- |
| 1          | 2                      | 1               | 2                         |
| 2          | 2                      | 1               | 3                         |
| 3          | 2                      | 1               | 4                         |
| 4          | 2                      | 2               | 2                         |
| 5          | 2                      | 2               | 3                         |
| 6          | 2                      | 2               | 4                         |
| 7          | 2                      | 3               | 2                         |
| 8          | 2                      | 3               | 3                         |
| 9          | 2                      | 3               | 4                         |
| 10         | 3                      | 1               | 3                         |
| 11         | 3                      | 1               | 4                         |
| 12         | 3                      | 1               | 5                         |
| 13         | 3                      | 2               | 3                         |
| 14         | 3                      | 2               | 4                         |
| 15         | 3                      | 2               | 5                         |
| 16         | 3                      | 3               | 3                         |
| 17         | 3                      | 3               | 4                         |
| 18         | 3                      | 3               | 5                         |
| 19         | 4                      | 1               | 4                         |
| 20         | 4                      | 1               | 5                         |
| 21         | 4                      | 1               | 6                         |

## **Things specific to the lab streaming layer version**
If you want to do real time EEG analysis/feedback for your study, then this version is the version for you. It assumes that your EEG data is able to be transmitted over Lab Streaming Layer. This version can be used for realtime feedback and for offline data collection. So there are three important components in this version: the experiment, the offline collection code, and the realtime analysis code. If you have any worries about if your computer can handle all three of these tasks simultaneously, then I would reccomend spreading the task out over multiple computers. The offline data collection is located in the **realtimeFunctions** folder in a file called **offlineCollection.py**. It is geared toward our lab's current setup which has light sensor data as the 129th channel, with the first 128 channels being our EEG data. This file will collect data from the EEG/light sensor stream and the events stream from the experiment, and combine this data into a nice **subjectNumber_raw.fif** file so that you can easily use this data in MNE and scikit-learn for analyszing the data and developing classifiers. These files will be saved to the **results** folder along with the behavorial/summary data and the temporary data which includes minute by minute EEG data, light sensor data and the events data. The **realtimeAnalysis.py** file found in the **realtimeFunctions.py** folder is the code for doing real time analysis on a subject and providing predictions one can use to modify the game while the user is playing it. Note that this is a crude version, and should mostly serve as a template for how *you* want to do *your* realtime analysis/feedback. If you space this out over three computers, then you will need to run each of these files separately. Otherwise, I have created a master file called **masterAnalysisFile.py** that you can run and it will run all three of these files concurrently. I don't really reccomend this due to the computational load it will place on your computer, but it might work. I don't have access to the EEG machine at the moment so i cannot test if this will work. The **EEGTestOutlet.py** and **testFIF.py** files are files I made for testing my code, so you likely won't need those. Importantly, the **dictionaries.py** file contains the translations between event ID numbers and their descriptions. MNE requires that events (annotations) be stored as integer values. SO in a subject's raw.fif file you might see something like "9234" which translates to "two out of three targets identified with four distractors". The dictionaries you find in **dictionaries.py** are how to translate between these numbers and the events they describe.

## **Netstation version of the code**
This version is very similar to the lab streaming layer version of the code, except with the translation dictionaries changed and there is no real time component. Net station limits us to sending four letter strings as events, so if oyu want to see what event corresponds to what tag and vice versa, then look in this version's **constants.py** file.