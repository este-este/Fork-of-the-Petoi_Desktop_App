#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Original Code:
    # Rongzhong Li
    # Petoi LLC
    # May.22nd, 2022

# Class Refactoring and Other Modifications
    # este este
    # https://github.com/este-este/Fork-of-the-Petoi_Desktop_App
    # 18-May-2025
    # v001.00.00
    # Minimum Python version: 3.10 if match-case code is used, otherwise 3.7.1 (checked by using vermin 1.6.0:  https://pypi.org/project/vermin/ )
'''
    The original file, SkillComposer.py has a class, SkillComposer, that relied on global and cross-module attributes and functions as well as transitive project imports.  The refactored revision, SkillComposer_C.py, has a self-contained class, SkillComposer, that avoids such dependencies.  Instead, it encapsulates newly created ArdSerial, Configure, CommonVar, Translate and Logger class objects.

    This file contains a "__main__" region so it can be run as a standalone program.
'''


# Import
#region     Import
    #region

# External Imports
import inspect
import sys
import time
import random
import tkinter.font as tkFont
import copy
import threading
import re
from enum import IntEnum
import platform
import platform
import tkinter as tk                # See https://docs.python.org/3/library/tkinter.html
import tkinter.messagebox           # Import the messagebox module specifically
from PIL import ImageTk, Image
import datetime
import os

# Project Imports
from logger_C import Logger
from translate_C import Translate

from commonVar_C import CommonVar
from config_C import Configure
from ardSerial_C import ArdSerial

    #endregion
#endregion  Import


# Class
#region     Class

class SkillComposer:
    # Called in SkillComposer __main__
    def __init__(self, callerName = None, model = None, lan = None):     # Note the parameters that are passed to the constructor.

        '''
        Purpose / Responsibility:
            Create an object to manage the SkillComposer application window and hold the lower level objects.

        Project Dependencies:
            Uses classes Logger, CommonVar, Configure and ArdSerial objects.
        '''

        sys.path.append("../pyUI")

        self.callerName = callerName
        self.selfName = self.__class__.__name__

        self.logger = Logger(self.selfName)                                          # Unlike other class objects a unique class Logger object must belong to each class

        # Initialize the log file that the logger objects will use.
        with open("./logfile.log", "w+", encoding="ISO-8859-1") as logfile:
            pass
        time.sleep(1)
        self.logger.log.info("ardSerial Date: Feb. 27, 2025")
        self.logger.log.info(f"Log Date: {time.strftime('%b. %d, %Y')}")

        self.translate = Translate(self.selfName)                                               # Create Translate object to use throughout
        self.commonVar = CommonVar(self.selfName)                                               # Create CommonVar object to use throughout
        self.configure = Configure(self.selfName, self.commonVar, self.translate, model, lan)   # Create Configure object to use throughout
        self.ardSerial = ArdSerial(self.selfName, self.configure, self.translate)               # Create ArdSerial object to use here


        if lan == None:
            pass
        else:
            self.translate.language = self.translate.languageList[lan]

        self.ardSerial.connectPort()
        pass

        # Test Code
        #region Test Code

        '''
            # Put test code here
        '''

        #endregion Test Code


# Lists & Dictionaries
#region     Lists & Dictionaries

    # Lists
    #region     Lists

        self.sixAxisNames = ['Yaw', 'Pitch', 'Roll', 'Spinal', 'Height', 'Sideway']
        self.dialTable_Dict_StrStr = {'Connect': 'Connected', 'Servo': 'p', 'Gyro': 'G', 'Random': 'z'}
        self.tipDial = ['tipConnect', 'tipServo', 'tipGyro', 'tipRandom']
        self.labelSkillEditorHeader = ['Repeat', 'Set', 'Step', 'Trig', 'Angle', 'Delay', 'Note', 'Del', 'Add']
        self.tipSkillEditor = ['tipRepeat', 'tipSet', 'tipStep',  'tipTrig', 'tipTrigAngle','tipDelay', 'tipNote', 'tipDel', 'tipAdd', ]

        # word_file = '/usr/share/dict/words'
        # WORDS = open(word_file).read().splitlines()
        self.animalNames = [  # used for memorizing individual frames
            'ant', 'bat', 'bear', 'bee', 'bird', 'buffalo', 'cat', 'chicken', 'cow', 'dog', 'dolphin', 'duck', 'elephant',
            'fish', 'fox', 'frog', 'goose', 'goat', 'horse', 'kangaroo', 'lion', 'monkey', 'owl', 'ox', 'penguin', 'person',
            'pig', 'rabbit', 'sheep', 'tiger', 'whale', 'wolf', 'zebra']
        self.WORDS = self.animalNames

        self.cLoop, self.cSet, self.cStep, self.cTrig, self.cAngle, self.cDelay, self.cNote, self.cDel, self.cAdd = range(len(self.labelSkillEditorHeader) )

    #endregion     Lists


    # Dictionaries (used in ardSerial_C.py AND/OR elsewhere)
    #region        Dictionaries

        self.axisDisable = {
            'Nybble': [0, 5],
            'Bittle': [0, 5],
            # 'BittleX': [0, 5],
            'BittleX+Arm': [0, 5],
            'DoF16' : []
        }

        self.jointConfig = {
            'Nybble': '><',
            'Bittle': '>>',
            'DoF16': '>>'
        }

        self.triggerAxis = {
            0: 'None',
            1: 'Pitch',
            -1: '-Pitch',
            2: 'Roll',
            -2: '-Roll',
        }

        # -ee- BittleRWinSet has some display issues (image is too big as are the widgets that surround the image, making the entire window too big)
            # The following are some initial attempts to address this.

        self.BittleRWinSet_test = {
            "sliderW": 300,          # The width of the slider rail corresponding to joint numbers 0 to 3          # Was "sliderW": 380
            "sixW": 7,               # The width of six IMU Axis Names lable
            "rowUnbindButton": 11,   # The row number where the unbind button is located
            "rowJoint1": 2,          # The row number of the label with joint number 2 and 3
            "sliderLen": 260,        # The length of the slider rail corresponding to joint numbers 4 to 15
            "rSpan": 3,              # The number of rows occupied by the slider rail corresponding to joint numbers 4 to 15
            "rowJoint2": 4,          # The row number of the label with joint number 4 or 15 is located
            "rowFrameImu": 13,       # The row number of the IMU button frame is located
            "imuSliderLen": 220,     # The length of the IMU slider rail
            "schedulerHeight": 580,  # The height of action frame scheduler                                         # Was "schedulerHeight": 580
            "rowFrameImage": 5,      # The row number of the image frame is located                                 # Was "rowFrameImage": 5
            "imgWidth": 200,         # The width of image                                                           # Was "imgWidth": 320
            "imgRowSpan": 6          # The number of lines occupied by the image frame                              # Was "imgRowSpan": 7
        }

        self.BittleRWinSet_original = {
            "sliderW": 380,          # The width of the slider rail corresponding to joint numbers 0 to 3
            "sixW": 10,              # The width of six IMU Axis Names lable
            "rowUnbindButton": 12,   # The row number where the unbind button is located
            "rowJoint1": 2,          # The row number of the label with joint number 2 and 3
            "sliderLen": 260,        # The length of the slider rail corresponding to joint numbers 4 to 15
            "rSpan": 4,              # The number of rows occupied by the slider rail corresponding to joint numbers 4 to 15
            "rowJoint2": 4,          # The row number of the label with joint number 4 or 15 is located
            "rowFrameImu": 13,       # The row number of the IMU button frame is located
            "imuSliderLen": 220,     # The length of the IMU slider rail
            "schedulerHeight": 580,  # The height of action frame scheduler
            "rowFrameImage": 5,      # The row number of the image frame is located
            "imgWidth": 320,         # The width of image
            "imgRowSpan": 7          # The number of lines occupied by the image frame
        }

        self.BittleRWinSet = {
            "sliderW": 380,          # The width of the slider rail corresponding to joint numbers 0 to 3
            "sixW": 10,              # The width of six IMU Axis Names lable
            "rowUnbindButton": 12,   # The row number where the unbind button is located
            "rowJoint1": 2,          # The row number of the label with joint number 2 and 3
            "sliderLen": 260,        # The length of the slider rail corresponding to joint numbers 4 to 15
            "rSpan": 4,              # The number of rows occupied by the slider rail corresponding to joint numbers 4 to 15
            "rowJoint2": 4,          # The row number of the label with joint number 4 or 15 is located
            "rowFrameImu": 13,       # The row number of the IMU button frame is located
            "imuSliderLen": 220,     # The length of the IMU slider rail
            "schedulerHeight": 580,  # The height of action frame scheduler
            "rowFrameImage": 5,      # The row number of the image frame is located
            "imgWidth": 320,         # The width of image
            "imgRowSpan": 7          # The number of lines occupied by the image frame
        }

        self.BittleRMacSet = {
            "sliderW": 300,          # The width of the slider rail corresponding to joint numbers 0 to 3
            "sixW": 10,              # The width of six IMU Axis Names lable
            "rowUnbindButton": 10,   # The row number where the unbind button is located
            "rowJoint1": 2,          # The row number of the label with joint number 2 and 3
            "sliderLen": 185,        # The length of the slider rail corresponding to joint numbers 4 to 15
            "rSpan": 5,              # The number of rows occupied by the slider rail corresponding to joint numbers 4 to 15
            "rowJoint2": 4,          # The row number of the label with joint number 4 or 15 is located
            "rowFrameImu": 12,       # The row number of the IMU button frame is located
            "imuSliderLen": 125,     # The length of the IMU slider rail
            "schedulerHeight": 360,  # The height of action frame scheduler
            "rowFrameImage": 5,      # The row number of the image frame is located
            "imgWidth": 200,         # The width of image
            "imgRowSpan": 5          # The number of lines occupied by the image frame
        }

        self.RegularWinSet = {
            "sliderW": 320,
            "sixW": 6,
            "rowUnbindButton": 5,
            "rowJoint1": 11,
            "sliderLen": 150,
            "rSpan": 3,
            "rowJoint2": 2,
            "rowFrameImu": 6,
            "imuSliderLen": 125,
            "schedulerHeight": 310,
            "rowFrameImage": 3,
            "imgWidth": 200,
            "imgRowSpan": 2
        }

        self.RegularMacSet = {
            "sliderW": 338,
            "sixW": 5,
            "rowUnbindButton": 5,
            "rowJoint1": 11,
            "sliderLen": 150,
            "rSpan": 3,
            "rowJoint2": 2,
            "rowFrameImu": 6,
            "imuSliderLen": 125,
            "schedulerHeight": 310,
            "rowFrameImage": 3,
            "imgWidth": 200,
            "imgRowSpan": 2
        }

        self.parameterWinSet = {
            "Nybble": self.RegularWinSet,
            "Bittle": self.RegularWinSet,
            # "BittleX": self.RegularWinSet,
            "BittleX+Arm": self.BittleRWinSet,
            "DoF16": self.RegularWinSet,
        }

        self.parameterMacSet = {
            "Nybble": self.RegularMacSet,
            "Bittle": self.RegularMacSet,
            # "BittleX": self.RegularMacSet,
            "BittleX+Arm": self.BittleRMacSet,
            "DoF16": self.RegularMacSet,
        }

    #endregion        Dictionaries

#endregion     Lists & Dictionaries


        # Use class Configure object to set "self.model" to one of the 3 base robot types:  Nybble, Bittle, BittleX+Arm
        self.configName = self.configure.model_
        self.configure.configName = self.configure.model_
        self.configure.model_ = self.configure.model_.replace(' ','')   # removes the space in e.g. "Bittle X" (model name received from robot) to give e.g. "BittleX"
        if 'BittleX+Arm' in self.configure.model_:
            self.model = 'BittleX+Arm'
        elif self.configure.model_== 'BittleX':
            self.model = 'Bittle'
        elif self.configure.model_== 'NybbleQ':
            self.model = 'Nybble'
        else:                                       # This acts as a pass-through for other "future" robot models
            self.model = self.configure.model_

        # Set ardSerial.postureTable to the dictionary of Posture Name (key) : Servo Angle list (value) pairs appropriate for the given model.
        self.ardSerial.setPostureTable(self.model)      

        self.scaleNames = self.commonVar.scaleNames[self.model]        # Model dependent list:  Scale Names (e.g. ['Head Pan', 'Head Tilt', ...]

        # Create GUI window and instantiate widget lists.
        self.windowSkillComposer_Tk = tk.Tk()       # Creates the main window of the GUI.
        self.sliders = list()                       # To hold all of the tkSlider widgets for the Joint Controller part of the GUI
        self.sliderValues = list()
        self.dialCheckbuttonValues_List_tkBooleanVar = list()
        self.controllerLabels = list()              # To hold all the tkLabel widgets for the Joint Controller part of the GUI

        self.binderValues_List_tkIntVar = list()              # Holds a list of states (-1, 0, +1) for the 16 servos (0-15) to indicate whether each servo is unbound (0), forward bound (+1) or reverse bound (-1)
        self.previousBinderValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     # Same idea but holds the previous bound (+1 or -1) or unbound (0) state of the servos
        self.binderButtons_List_tkRadioButtons = list()              # To hold all the Binder tkButton widgets for the Joint Controller part of the GUI

        self.keepChecking = True        # -ee- Was used when checking ports via multiple threads. Still used in updatePortMenu(), dial(), on_closing()
        self.ready = 0
        self.creatorInfoAcquired = False
        self.creator_tkStringVar = tk.StringVar()
        self.location_tkStringVar = tk.StringVar()
        self.creator_tkStringVar.set(self.translate.txt('Nature'))
        self.location_tkStringVar.set(self.translate.txt('Earth'))

        # Get computer OS name
        self.OSname = self.windowSkillComposer_Tk.call('tk', 'windowingsystem')
        print(self.OSname)
        self.windowSkillComposer_Tk.geometry('+100+10')
        self.windowSkillComposer_Tk.resizable(False, False)

        # Do OS dependent configuration of the GUI

        # For MacOS
        if self.OSname == 'aqua':
            self.backgroundColor = 'gray'
        else:
            self.backgroundColor = None

        # For Windows OS
        if self.OSname == 'win32':
            winVer = platform.release()
            self.ardSerial.printH('Windows version:', winVer)
            self.windowSkillComposer_Tk.iconbitmap(self.commonVar.resourcePath + 'Petoi.ico')

            # Set control parameters for this OS
            if winVer.isnumeric() and int(winVer) > 10:
                self.frameItemWidth = [2, 4, 3, 5, 4, 4, 6, 3, 3]  # for some Windows 11, 10 -> 6
            else:
                self.frameItemWidth = [2, 4, 3, 5, 4, 4, 10, 3, 3]
            self.headerOffset = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            self.parameterSet = self.parameterWinSet[self.model]

            # self.buttonW = 20
            self.buttonW = 10           # width of button
            self.calibButtonW = 8
            self.canvasW = 330
            self.mirrorW = 2
            self.MirrorW = 10
            self.connectW = 8
            self.dialW = 7
            self.portW = 5
            self.dialPad = 2
        else:
            if self.OSname == 'aqua':
                self.frameItemWidth = [2, 2, 3, 4, 3, 3, 4, 1, 1]
                self.headerOffset = [2, 2, 2, 2, 2, 2, 2, 2, 2]
            else:
                self.frameItemWidth = [2, 2, 3, 4, 4, 4, 5, 2, 2]
                self.headerOffset = [0, 0, 1, 1, 0, 0, 0, 0, 1]

            self.parameterSet = self.parameterMacSet[self.model]

            # self.buttonW = 18
            self.buttonW = 8
            self.calibButtonW = 6
            self.canvasW = 420
            self.mirrorW = 1
            self.MirrorW = 9
            self.connectW = 8
            self.dialW = 6
            self.portW = 12
            self.dialPad = 3

        # Do OS independent configuration of the GUI

        self.myFont = tkFont.Font(
            family='Times New Roman', size=20, weight='bold')
        self.windowSkillComposer_Tk.title(self.translate.txt('skillComposerTitle'))
        self.totalFrame = 0
        self.activeFrame = 0
        self.frameList = list()
        self.frameData = [0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          8, 0, 0, 0, ]
        self.originalAngle = [0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              8, 0, 0, 0, ]
        self.pause = False
        self.playStop = False
        self.mirror = False

        # Create the GUI                # -ee- An 'x' after the # below indicates that function has been reviewed and, typically, had some documentation and/or refactoring done.
        self.createMenu()           #x Creates the top menu, currently = "Model, Language, Utility, Help"
        self.createController()     #x Creates the left side of GUI with the slider controls / buttons.
        self.placeProductImage()    #x Places the robot image on the left side of the GUI
        self.createDial()           #x Creates upper-right side "State Dials", currently = "Connect, COM_List, Servo, Gyro, Random" and just below "Send" box and button.
        self.createPosture()        # Creates middle_1-right side "Preset Postures" buttons
        self.createSkillEditor()    # Creates middle_2-right side "Skill Editor" buttons, currently = "Play, Import, Restart, Export" and just below "Undo, Redo, >|<, Mirror All, Behavior"
        self.createRowScheduler()   # Creates bottom-right side "Row Scheduler" heading and row "0", currently = "NumLoops, Set, Step, Trigger,Angle, Delay, Note, Del, Add"

        self.windowSkillComposer_Tk.protocol('WM_DELETE_WINDOW', self.on_closing)        # Set up for closing the window
        self.windowSkillComposer_Tk.update()                                             # Display the window

        self.windowSkillComposer_Tk.focus_force()    # force the main interface to get focus
        self.ready = 1
        self.windowSkillComposer_Tk.mainloop()

    # Use enums instead of "magic numbers" for accessing lists.
        # Unfortunately, Python's implementation of enums is clumsy, compared to that of other languages.  However, IMO, they are better than using "magic numbers" in the code.

    class enumFrameDials_Child(IntEnum):                    # Use as a declared index to access self.frameDials.winfo_children()[]
        stateDialsLabel_tkLabel_Index       = 0
        Connect_tkCheckbutton_Index         = 1
        Servo_tkCheckbutton_Index           = 2
        Gyro_tkCheckbutton_Index            = 3
        Random_tkCheckbutton_Index          = 4
        goodPortsMenu_tkOptionMenu_Index    = 5


    class enumDialCheckbuttonValues_List_Item(IntEnum):     # Use as a declared index to access self.dialCheckbuttonValues_List_tkBooleanVar
        Connect_Index         = 0
        Servo_Index           = 1
        Gyro_Index            = 2
        Random_Index          = 3


    def rgbtohex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'


    # Called in __init__(), changeLan()
    def createMenu(self):       # Add the menu across the top of the GUI window
        self.menubar_tkMenu = tk.Menu(self.windowSkillComposer_Tk, background='#ff8000', foreground='black', activebackground='white',
                            activeforeground='black')
        file_tkMenu = tk.Menu(self.menubar_tkMenu, tearoff=0, background='#ffcc99', foreground='black')
        for model in self.commonVar.modelOptions:
            file_tkMenu.add_command(label=model, command=lambda model=model: self.changeModel(model))
        self.menubar_tkMenu.add_cascade(label=self.translate.txt('Model'), menu=file_tkMenu)

        lan_tkMenu = tk.Menu(self.menubar_tkMenu, tearoff=0)

        for language in self.translate.languageList:
            lan_tkMenu.add_command(label=self.translate.languageList[language]['lanOption'], command=lambda lanChoice=language: self.changeLan(lanChoice))

        self.menubar_tkMenu.add_cascade(label=self.translate.txt('lanMenu'), menu=lan_tkMenu)

        util_tkMenu = tk.Menu(self.menubar_tkMenu, tearoff=0)
        util_tkMenu.add_command(label=self.translate.txt('Eye color picker'), command=lambda: self.popEyeColor())
        util_tkMenu.add_command(label=self.translate.txt('Creator Information'), command=lambda: self.getCreatorInfo())
        self.menubar_tkMenu.add_cascade(label=self.translate.txt('Utility'), menu=util_tkMenu)
        
        helpMenu_tkMenu = tk.Menu(self.menubar_tkMenu, tearoff=0)
        helpMenu_tkMenu.add_command(label=self.translate.txt('About'), command=self.showAbout)
        self.menubar_tkMenu.add_cascade(label=self.translate.txt('Help'), menu=helpMenu_tkMenu)

        self.windowSkillComposer_Tk.config(menu=self.menubar_tkMenu)


    # NOT currently called anywhere
    def scheduler(self):
        print('Scheduler')


    # NOT currently called anywhere
    def uploadFirmware(self):
        print('Uploader')
        Uploader()


    # Called in __init__(), changeModel()
    def createController(self):
        self.frameController_tkFrame = tk.Frame(self.windowSkillComposer_Tk)
        self.frameController_tkFrame.grid(row=0, column=0, rowspan=9, padx=(5, 10), pady=5)

        jointController_tkLabel = tk.Label(self.frameController_tkFrame, text=self.translate.txt('Joint Controller'), font=self.myFont)
        jointController_tkLabel.grid(row=0, column=0, columnspan=8)

        unbindButton_tkButton = tk.Button(self.frameController_tkFrame, text=self.translate.txt('Unbind All'), fg='blue', command=self.unbindAll)
        rowUnbindButton = self.parameterSet['rowUnbindButton']    # The row number where the unbind button is located
        unbindButton_tkButton.grid(row=rowUnbindButton, column=3, columnspan=2)

        # Append the just created widgets to the lists
        self.controllerLabels.append(jointController_tkLabel)
        self.controllerLabels.append(unbindButton_tkButton)

        centerWidth = 2     # Column span (width) for center (where the robot image is)

        # Initialize the widgets for the 16 servos
        for servo in range(16):    # Servo 0-15
            cSPAN = 1                                       # Set widget column SPAN to 1 (default column width)

            # For the 16 servo tkScale widgets:
                # Set up row & row SPAN, column & column SPAN, 
                # orientation, width, length, "tick" direction, location (left / right, front / back)
            if servo < 4:                                   # Servo 0-3  (Top)
                tickDirection = 1                               # Positive tickDirection used for positive scale with widget tkScale
                cSPAN = 4                                       # Change widget column SPAN to 4 for servo 0-3 (Top Left / Right)

                # Set widget Row #
                if servo < 2:                               # Servo 0, 1 (on Left side)
                    ROW = 0                                     # Widget start in row 0 for servo 0, 1
                else:                                       # Servo 2, 3 (on Right side)
                    ROW = self.parameterSet['rowJoint1']        # Widget start in row [# in parameterSet] for servo 2, 3

                # Set widget Column #
                if 0 < servo < 3:                           # Servo 1, 2 (on Right side))
                    COL = 4                                     # Widget start in column 4 for servo 1, 2
                else:                                       # Servo 0, 3 (on Left side)
                    COL = 0                                     # Widget start in column 0 for servo 0, 3

                # Set widget Row height, orientation, and length
                rSPAN = 1                                   # Set widget row SPAN to 1 (row height)
                ORI = tk.HORIZONTAL                         # Set orientation constant to horizontal
                LEN = self.parameterSet['sliderW']          # Set slider width

            else:                                           # Servo 4-16 (Middle & Bottom)
                tickDirection = -1
                leftQ = (servo - 1) % 4 > 1                     # Is this servo on the left side of the Joint Controller GUI section?
                frontQ = servo % 4 < 2                          # Is this servo on the front (top) of the Joint Controller GUI section?
                # upperQ = i / 4 < 3

                LEN = self.parameterSet['sliderLen']                                # The length of the slider rail corresponding to servo numbers 4 to 15
                rSPAN = self.parameterSet['rSpan']                                  # The number of rows occupied by the slider rail corresponding to servo numbers 4 to 15
                ROW = self.parameterSet['rowJoint2'] + (1 - frontQ) * (rSPAN + 2)   # The row number of the label with servo number 4 or 15 is located

                if leftQ:
                    COL = 3 - servo // 4                        # Floor division (round down to nearest integer)
                else:
                    COL = centerWidth + 2 + servo // 4
                ORI = tk.VERTICAL                           # Set orientation constant to vertical

            widgetState = tk.NORMAL                                 # Default:  Normal = enabled

            # Set tkScale color and state to be "not available"/disabled or "available"/enabled
            if servo in self.commonVar.NaJoints[self.model]:
                clr = 'light yellow'
                widgetState = tk.DISABLED
            else:
                clr = 'yellow'
                widgetState = tk.NORMAL                             # Default:  Normal = enabled

            # Initialize servo side name
            if servo in range(8, 12):       # Servo 8-11
                sideLabel = self.translate.txt(self.commonVar.sideNames[servo % 8]) + '\n'    # Get side name - NOTE the new line char (e.g. 'Left Front', 'Right Front', ...)
            else:                           # All other servo number
                sideLabel = ''

            # Create servo slider label (e.g. Left Front (8) Arm )
            side_ServoIndex_ScaleName_tkLabel = tk.Label(self.frameController_tkFrame,
                          text=sideLabel + '(' + str(servo) + ')\n' + self.translate.txt(self.scaleNames[servo]))
            side_ServoIndex_ScaleName_tkLabel.grid(row=ROW + 1, column=COL, columnspan=cSPAN, pady=2, sticky='s')

            # Create servo slider "Value_tk...Var" and tkScale widget
            servoSliderValue_tkDoubleVar = tk.DoubleVar()      # -ee- why not tk.IntVar?
            servoSliderBar_tkScale = tk.Scale(self.frameController_tkFrame, state=widgetState, fg='blue', bg=clr, variable=servoSliderValue_tkDoubleVar, orient=ORI,
                              borderwidth=2, relief='flat', width=8, from_=-180 * tickDirection, to=180 * tickDirection,
                              length=LEN, tickinterval=90, resolution=1, repeatdelay=100, repeatinterval=100,
                              command=lambda value, servo=servo: self.setAngle(servo, value))
            servoSliderBar_tkScale.grid(row=ROW + 2, column=COL, rowspan=rSPAN, columnspan=cSPAN)
            servoSliderBar_tkScale.set(0)        # Initialize at value of 0

            # Append the just created widgets to the lists
            self.sliders.append(servoSliderBar_tkScale)
            self.sliderValues.append(servoSliderValue_tkDoubleVar)
            self.controllerLabels.append(side_ServoIndex_ScaleName_tkLabel)

            # Initialize servo binder button widget
            if servo in range(16):
                binderValue_tkIntVar = tk.IntVar()          # This object is used to group the pair of tkRadioButton objects associated with EACH servo joint (possible values = -1, 0, +1)
                binderValues_Dict_StrInt = {"+": 1,
                                            "-": -1, }

                 # Loop with binderValueSignIndex = 0 then binderValueSignIndex = 1 to access values "1" then "-1" in binderValues_Dict_StrInt
                    # This creates two tkRadioButton widgets for each servo joint.  One is for forward motion binding (+1) and the other is for reverse motion binding (-1)
                for binderValueSignIndex in range(2): 
                    binderButton_tkRadioButton = tk.Radiobutton(
                        self.frameController_tkFrame, 
                        text=list(binderValues_Dict_StrInt)[binderValueSignIndex],  # Set text of tkRadioButton to "+", "-" (from the dictionary)
                        fg='blue', 
                        variable=binderValue_tkIntVar,      # Must use the same binderValue_tkIntVar object to group the two tkRadioButton objects (+ button / - button) together
                                                            # Stores the shared value of the radio buttons (either 1, -1, or 0 for unbound).  
                                                                # Changes when either + or - button is pressed for a given servo joint.  
                                                                # In updateRadio(), two presses on the same button will unbind the servo joint (set their common variable binderValue_tkIntVar = 0)
                        value=list(binderValues_Dict_StrInt.values())[binderValueSignIndex],    # Value to increment or decrement (set to 1 for + and -1 for -) - does not later change!
                        indicator=0,                        # Make the radio button look like a regular button instead of a circular radio button
                        state=widgetState,                  # Set state to normal or disabled
                        background="light blue", width=1,
                        command=lambda servo=servo: self.updateRadio(servo))        # function to use when the tkRadioButton is pressed
                    if servo < 4:
                        binderButton_tkRadioButton.grid(row=ROW + 1, column=COL + (1 - binderValueSignIndex) * (cSPAN - 1), sticky='s')
                    else:
                        binderButton_tkRadioButton.grid(row=ROW + 2 + binderValueSignIndex * (rSPAN - 1), column=COL, sticky='ns'[binderValueSignIndex])

                    binderValue_tkIntVar.set(0)     # Initialize at value of 0 (unbound)

                    if binderValueSignIndex == 0:
                        self.commonVar.tip(binderButton_tkRadioButton, self.translate.txt('tipBinder'))       # Set Forward Binder Button Tip
                    else:
                        self.commonVar.tip(binderButton_tkRadioButton, self.translate.txt('tipRevBinder'))    # Set Reverse Binder Button Tip

                    # Append the just created widgets to the lists
                    self.binderButtons_List_tkRadioButtons.append(binderButton_tkRadioButton)

                self.binderValues_List_tkIntVar.append(binderValue_tkIntVar)    # store the "two tkRadioButton shared" binderValue_tkIntVar object for this servo joint


        # Initialize six axis IMU widgets

        self.frameImu_tkFrame = tk.Frame(self.frameController_tkFrame)
        rowFrameImu = self.parameterSet['rowFrameImu']    # The row number of the IMU button frame is located
        sliderLen = self.parameterSet['imuSliderLen']     # The length of the IMU slider rail
        self.frameImu_tkFrame.grid(row=rowFrameImu, column=3, rowspan=6, columnspan=2)

        # Set up for initializing the 6 axes of the IMU widgets
        for servo in range(6):
            frm = -40
            to2 = 40
            if servo in self.axisDisable[self.model]:
                widgetState = tk.DISABLED
                clr = 'light yellow'
            else:
                widgetState = tk.NORMAL
                clr = 'yellow'
            if servo == 2:
                frm = -30
                to2 = 30
            elif servo == 3:
                frm = -15
                to2 = 15
            elif servo == 4:
                frm = -50
                to2 = 40

            sixAxisImu_tkLabel = tk.Label(self.frameImu_tkFrame, text=self.translate.txt(self.sixAxisNames[servo]), width=self.parameterSet['sixW'], height=2, fg='blue',
                          bg='Light Blue')
            sixAxisImu_tkLabel.grid(row=servo, column=0)

            sixAxisImuSliderValue__tkDoubleVar = tk.DoubleVar()
            sixAxisImuSliderBar_tkScale = tk.Scale(self.frameImu_tkFrame, state=widgetState, fg='blue', bg=clr, variable=sixAxisImuSliderValue__tkDoubleVar, orient=tk.HORIZONTAL,
                              borderwidth=2, relief='flat', width=10, from_=frm, to=to2, length=sliderLen, resolution=1,
                              command=lambda ang, servo=servo: self.set6Axis(servo, ang))  # tickinterval=(to2-frm)//4,
            sixAxisImuSliderBar_tkScale.grid(row=servo, column=1, columnspan=centerWidth)

            sixAxisImuSliderBar_tkScale.set(0)

            # Append the just created widgets to the lists
            self.sliders.append(sixAxisImuSliderBar_tkScale)
            self.sliderValues.append(sixAxisImuSliderValue__tkDoubleVar)
            self.controllerLabels.append(sixAxisImu_tkLabel)


    # Called in deacGyrp(), dial()
    def buttonDialActive(self, idx, buttonActive = False):
        if buttonActive:
            self.dialCheckbuttonValues_List_tkBooleanVar[idx].set(True)
            self.frameDials.winfo_children()[idx+1].config(fg='green')
        else:
            self.dialCheckbuttonValues_List_tkBooleanVar[idx].set(False)
            self.frameDials.winfo_children()[idx+1].config(fg='red')


    # Called in createDial(), updatePortMenu(), dial()
    def deacGyrp(self):
        function_name = inspect.currentframe().f_code.co_name
        self.boardVer = self.configure.version_
        # printH("boardVer:", self.boardVer)
        if self.boardVer[0] == 'N':     # Check for a Nyboard
            res = self.ardSerial.send(['G', 0])
            if res != -1:
                if res[0][0] == 'G':
                    res = self.ardSerial.send(['G', 0])
                    if res != -1 and res[0][0] == 'g':
                        self.buttonDialActive(2, False)
                        # printH("gyro status:", res)
                        self.logger.log.debug(f'gyro is deactivated successfully.')
                    else:
                        self.buttonDialActive(2, True)
                elif res[0][0] == 'g':
                    self.buttonDialActive(2, False)
                    # printH("gyro status:", res)
                    self.logger.log.debug(f'gyro status:{res}')
                else:
                    self.buttonDialActive(2, True)
            else:
                self.buttonDialActive(2, True)
        else:
            res = self.ardSerial.send(['gb', 0])
            # printH("res:", res)
            if res != -1 and res[0][0] == 'g':
                self.buttonDialActive(2, False)
                # print("Gyro is deactivated successfully.")
                self.logger.log.debug(f'gyro is deactivated successfully.')
            else:
                self.buttonDialActive(2, True)

        # Use enum instead of index = 2 to access that item of dialCheckbuttonValues_List_tkBooleanVar which is the Gyro tkCheckbutton tkBooleanVar value
        self.logger.log.debug(f'gyro status:{self.dialCheckbuttonValues_List_tkBooleanVar[self.enumDialCheckbuttonValues_List_Item.Gyro_Index.value].get()}')


    # Called in __init__(), changeLan()
    # Create the State Dials at the Right Top of the SkillComposer window
    def createDial(self):
        # Here, the term "Dial" refers to a tk.Checkbutton that can be toggled on or off, not a dial in the traditional sense.
        # frameDials holds these buttons but also holds the Port tk.Optionmenu, the Send tk.Entry box and the Send tk.Button.

        self.frameDials = tk.Frame(self.windowSkillComposer_Tk)     # create a frame, on self.window, to hold the "State Dials", currently for:  Connect, Port, Servo, Gyro, Random
        self.frameDials.grid(row=0, column=1)    # position frameDial on the grid layout of self.window.

        stateDialsLabel_tkLabel = tk.Label(self.frameDials, text=self.translate.txt('State Dials'), font=self.myFont)
        stateDialsLabel_tkLabel.grid(row=0, column=0, columnspan=5, pady=5)
        stateDialsLabel_tkLabel.custom_name = 'labelDial_tkLabel'        # Attach a custom name to this widget

        stateDial_DefaultValues_List = [1, 1, 0, 0]
        stateDialTextColors_List = ['red','green']

        # Create State Dials (check buttons) section
        for dialTableIndex in range(len(self.dialTable_Dict_StrStr)):          # Loop through the, currently 4, dials:  Connect, Servo, Gyro, Random
            key = list(self.dialTable_Dict_StrStr)[dialTableIndex]             # make list from keys in self.dialTable dictionary and then access the key at dialIndex

            buttonText = key    # key is a string which is immutable so this assignment is by value, not by reference

            # Set Connect dial button state only
            if len(self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr) > 0 or dialTableIndex == 0:       # key = Connect
                dialState = tk.NORMAL       # Enable all Checkbuttons if we have good ports or only the Connect Checkbutton when there are NO good ports
            else:
                dialState = tk.DISABLED     # Otherwise disable

            # Set dial button width
            if dialTableIndex == 0:         # The Connect / Connected tkCheckbutton (toggle)
                wth = self.connectW         # wider width for connect tkCheckbutton
                if len(self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr) > 0:
                    stateDial_DefaultValues_List[0] = True
                    buttonText = 'Connected'
                else:
                    stateDial_DefaultValues_List[0] = False
                    buttonText = 'Connect'
            else:
                wth = self.dialW        # standard dial width

            # Create actual dial button
            buttonValue_tkBooleanVar = tk.BooleanVar()
            buttonValue_tkBooleanVar.set(stateDial_DefaultValues_List[dialTableIndex])

            button_tkCheckbutton = tk.Checkbutton(
                self.frameDials, 
                text=self.translate.txt(buttonText), 
                indicator=0, width=wth, 
                fg=stateDialTextColors_List[stateDial_DefaultValues_List[dialTableIndex]], 
                state=dialState, var=buttonValue_tkBooleanVar,
                command=lambda dialTableIndex=dialTableIndex: self.dialChange(dialTableIndex)
            )
            button_tkCheckbutton.grid(
                row=1, 
                column=dialTableIndex + (dialTableIndex > 0),     # dialIndex + (dialIndex > 0) gives the column progression 0,2,3,4 so as to skip column 1 (where the Port tk.Optionmenu is located)
                padx=self.dialPad
            )
            button_tkCheckbutton.custom_name = key + "_tkCheckbutton"   # Attach a custom name to this widget

            self.commonVar.tip(button_tkCheckbutton, self.translate.txt(self.tipDial[dialTableIndex]))

            self.dialCheckbuttonValues_List_tkBooleanVar.append(buttonValue_tkBooleanVar)

        # self.deacGyrp()       # This is not needed here since createPortMenu() calls updatePortMenu() which calls updatePortMenu() to then call deacGyrp() there.

        # Create Port OptionMenu (must be added to frameDials after the Checkbuttons)
        self.createPortMenu()

        # Create Send newCmd section
        self.newCmd_tkStringVar = tk.StringVar()
        newCmd_tkEntry = tk.Entry(self.frameDials, textvariable=self.newCmd_tkStringVar)
        newCmd_tkEntry.grid(row=2, column=0, columnspan=4, padx=3, sticky=tk.E + tk.W)

        # Originally, this button and the above Checkbutton were given the same name of "button"  This is allowed (different scope) but is still confusing.
        send_tkButton = tk.Button(self.frameDials,text=self.translate.txt('Send'),fg='blue',width=self.dialW-2,command=self.sendCmd)
        send_tkButton.grid(row=2, column=4, padx=3)

        newCmd_tkEntry.bind(sequence='<Return>', func=lambda event: self.sendCmd(event))


    # Called in createDial()
    def createPortMenu(self):
        self.port_tkStringVar = tk.StringVar()      # Initialize
        self.goodPorts_MenuOptions_List_Str = [self.translate.txt('None')]  # Initialize the Port Menu options list with "None"
        self.goodPortsMenu_tkOptionMenu = tk.OptionMenu(self.frameDials, self.port_tkStringVar, *self.goodPorts_MenuOptions_List_Str)        # OptionMenu is a drop down menu
        self.goodPortsMenu_tkOptionMenu.custom_name = 'goodPortsMenu_tkOptionMenu'        # Attach a custom name to this widget

        self.goodPortsMenu_tkOptionMenu.config(width=self.portW, fg='blue')
        self.port_tkStringVar.trace('w', lambda *args: self.changePort())
        self.goodPortsMenu_tkOptionMenu.grid(row=1, column=1, padx=2)

        self.updatePortMenu()

        self.commonVar.tip(self.goodPortsMenu_tkOptionMenu, self.translate.txt('tipPortMenu'))


    # Called in createPortMenu(),dial()
    # Originally was put on a thread with keepCheckingPort() in __init__() and dial() [under some conditions]
    # It is still needed but now is just called in createPortMenu() and dial() [ both called by createDial() ]
    def updatePortMenu(self):
        print('\n***@@@ update menu function started')#debug
        self.goodPorts_MenuOptions_List_Str = list(self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr.values())        # Initialize the Port Menu options list with the list of "good" ports

        # new way
        self.goodPortsMenu_tkOptionMenu["menu"].delete(0, "end")        # Clear the menu before adding new items

        # old way
        # menu = self.portMenu_tkOptionMenu['menu']
        # menu.delete(0, 'end')

        widgetState = tk.NORMAL     # Default state is enabled

        if len(self.goodPorts_MenuOptions_List_Str) == 0:
            self.goodPorts_MenuOptions_List_Str.insert(0, self.translate.txt('None'))
            widgetState = tk.DISABLED       # Will disable if there are no ports.
            if self.keepChecking:
                # Use enum instead of index = 0 to access that item of dialCheckbuttonValues_List_tkBooleanVar which is the Connect tkCheckbutton tkBooleanVar value
                self.dialCheckbuttonValues_List_tkBooleanVar[self.enumDialCheckbuttonValues_List_Item.Connect_Index.value].set(True)

                # Use enum instead of index = 1 to access the child of framedials which is the Connect tkCheckbutton
                self.frameDials.winfo_children()[self.enumFrameDials_Child.Connect_tkCheckbutton_Index.value].config(
                    text=self.translate.txt('Listening'), 
                    fg='orange'
                )
            else:
                self.frameDials.winfo_children()[self.enumFrameDials_Child.Connect_tkCheckbutton_Index.value].config(
                    text=self.translate.txt('Connect'), 
                    fg='red'
                )
        else:
            if len(self.goodPorts_MenuOptions_List_Str) > 1:
                self.goodPorts_MenuOptions_List_Str.insert(0, self.translate.txt('All'))
            if self.keepChecking:
                self.frameDials.winfo_children()[self.enumFrameDials_Child.Connect_tkCheckbutton_Index.value].config(
                    text=self.translate.txt('Connected'), 
                    fg='green'
                )
                self.deacGyrp()

        # Test code for examining self.frameDials.winfo_children()
        '''
        for child in self.frameDials.winfo_children():
            # Check if the widget has a 'text' property
            if isinstance(child, tk.Widget) and hasattr(child, 'cget'):
                # Get the 'text' value of the widget
                text_value = child.cget('text')
                print(f"Found widget: {child} with text = {text_value}")
        '''

        # Load the port menu with the list of good ports
        for goodPortString in self.goodPorts_MenuOptions_List_Str:
            self.goodPortsMenu_tkOptionMenu["menu"].add_command(label=goodPortString, command=lambda goodPortString=goodPortString: self.port_tkStringVar.set(goodPortString))
        self.port_tkStringVar.set(self.goodPorts_MenuOptions_List_Str[0])

        # Set tkCheckbutton state
        buttons = [self.frameDials.winfo_children()[i] for i in [2,3,4]]     # Retrieve buttons 2, 3, 4 (Servo, Gyro, Random)          use [2,4] to skip 3 (Gyro)
        for button in buttons:
            button.config(state=widgetState)

        # Set tkOptionMenu state
        self.goodPortsMenu_tkOptionMenu.config(state=widgetState)

        print('\n***@@@ update menu function ended')#debug


    # Called in createPortMenu()
    def changePort(self):
        buttons = [self.frameDials.winfo_children()[i] for i in [2,3,4]]     # Retrieve buttons 2, 3, 4 (Servo, Gyro, Random)          [2,4] by skipping 3 was used to disable the gyro
        for button in buttons:
            if len(self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr) == 0:
                button.config(state=tk.DISABLED)
            else:
                button.config(state=tk.NORMAL)

        # Refactored to only use a dictionary with SPO keys and PortNameStr values (i.e. a Dict_SPO_to_PortNameStr)


        # new way
            # self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr has the following states:
                # If there is are multiple good ports then self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr is an dictionary with those multiple entries.
                # If there are no good ports then self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr is an empty dictionary.
                # if there is only one good port then self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr is a dictionary with that single entry.

            # SkillComposer.ardSerial.send() is the only function that currently uses the global object "ports".
                # Currently, that function can accept a dictionary of type Dict_SPO_to_PortNameStr or a simple list of port names.
                # There is no need to support both types for global object "ports".
                # In fact, there is no need to use a global object "ports" at all, since SkillComposer.ardSerial.send() can directly access and use self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr

            # So, eliminate the global object "ports" plus related code (in "old way" below) and just use self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr directly in SkillComposer.ardSerial.send().


        # old way
            # Convert goodPorts dictionary to a list of (key, value) pairs; 
                # Do a dictionary comprehension to make an inverted dictionary where the value is the key and the key is the value
        # inv_dict = {v: k for k, v in self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr.items()}
        #     # old way
        # if self.port_tkStringVar.get() == self.translate.txt('All'):
        #     ports = self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr                # here, ports is a Dict_SPO_to_PortNameStr
        # elif self.port_tkStringVar.get() == self.translate.txt('None'):
        #     ports = []
        # else:
        #     singlePort = inv_dict[self.port_tkStringVar.get()]
        #     ports = [singlePort]                                                    # here, ports is a list of a single Serial Port Object


    # Called in __init__(), changeLan(), changeModel()
    # Creates the Posture frame and the buttons for each posture.
    def createPosture(self):
        self.framePosture_tkFrame = tk.Frame(self.windowSkillComposer_Tk)
        self.framePosture_tkFrame.grid(row=1, column=1)
        labelPosture_tkLabel = tk.Label(self.framePosture_tkFrame, text=self.translate.txt('Postures'), font=self.myFont)
        labelPosture_tkLabel.grid(row=0, column=0, columnspan=4)
        i = 0
        for pose in self.ardSerial.postureTable:    # pose is a string consisting of a skill name (e.g. "balance")
            button_tkButton = tk.Button(self.framePosture_tkFrame, text=self.translate.txt(pose), fg='blue', width=self.buttonW,
                            command=lambda pose=pose: self.setPose(pose))
            button_tkButton.grid(row=i // 3 + 1, column=i % 3, padx=3)
            i += 1


    # Called in __init__(), changeLan()
    # Creates the SkillEditor Frame plus the Frame label and frame buttons.
    def createSkillEditor(self):
        self.frameSkillEditor_tkFrame = tk.Frame(self.windowSkillComposer_Tk)
        self.frameSkillEditor_tkFrame.grid(row=2, column=1)

        labelSkillEditor_tkLabel = tk.Label(self.frameSkillEditor_tkFrame, text=self.translate.txt('Skill Editor'), font=self.myFont)
        labelSkillEditor_tkLabel.grid(row=0, column=0, columnspan=4)

        pd = 3  # padding for the buttons

        self.buttonPlay_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('Play'), width=self.buttonW, fg='green',
                                 command=self.playThread)
        self.buttonPlay_tkButton.grid(row=1, column=0, padx=pd)

        self.commonVar.tip(self.buttonPlay_tkButton, self.translate.txt('tipPlay'))

        buttonImp_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('Import'), width=self.buttonW, fg='blue',
                           command=self.popImport)
        buttonImp_tkButton.grid(row=1, column=1, padx=pd)

        self.commonVar.tip(buttonImp_tkButton, self.translate.txt('tipImport'))

        buttonRestart_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('Restart'), width=self.buttonW, fg='red',
                               command=self.restartSkillEditor)
        buttonRestart_tkButton.grid(row=1, column=2, padx=pd)

        self.commonVar.tip(buttonRestart_tkButton, self.translate.txt('tipRestart'))

        buttonExp_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('Export'), width=self.buttonW, fg='blue',
                           command=self.export)
        buttonExp_tkButton.grid(row=1, column=3, padx=pd)

        self.commonVar.tip(buttonExp_tkButton, self.translate.txt('tipExport'))

        buttonUndo_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('Undo'), width=self.buttonW, fg='blue', state=tk.DISABLED,
                            command=self.restartSkillEditor)
        buttonUndo_tkButton.grid(row=2, column=0, padx=pd)

        buttonRedo_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('Redo'), width=self.buttonW, fg='blue', state=tk.DISABLED,
                            command=self.restartSkillEditor)
        buttonRedo_tkButton.grid(row=2, column=1, padx=pd)

        cbMiroX_tkCheckbutton = tk.Checkbutton(self.frameSkillEditor_tkFrame, text=self.translate.txt('mirror'), indicator=0, width=self.MirrorW,
                              fg='blue', variable=self.mirror, onvalue=True, offvalue=False,
                              command=self.setMirror)
        cbMiroX_tkCheckbutton.grid(row=2, column=2, sticky='e', padx=pd)

        self.commonVar.tip(cbMiroX_tkCheckbutton, self.translate.txt('tipMirrorXport'))

        buttonMirror_tkButton = tk.Button(self.frameSkillEditor_tkFrame, text=self.translate.txt('>|<'), width=self.mirrorW, fg='blue',
                              command=self.generateMirrorFrame)
        buttonMirror_tkButton.grid(row=2, column=2, sticky='w', padx=pd)

        self.commonVar.tip(buttonMirror_tkButton, self.translate.txt('tipMirror'))

        self.gaitOrBehavior_tkStringVar = tk.StringVar()
        self.GorB_tkOptionMenu = tk.OptionMenu(self.frameSkillEditor_tkFrame, self.gaitOrBehavior_tkStringVar, self.translate.txt('Gait'), self.translate.txt('Behavior'))
        self.GorB_tkOptionMenu.config(width=6, fg='blue')
        self.gaitOrBehavior_tkStringVar.set(self.translate.txt('Behavior'))
        self.GorB_tkOptionMenu.grid(row=2, column=3, padx=pd)

        self.commonVar.tip(self.GorB_tkOptionMenu, self.translate.txt('tipGorB'))


    #   Called in createSkillEditor()
    def setMirror(self):
        self.mirror = not self.mirror


    # Called in __init__()
    def createRowScheduler(self):
        self.frameRowScheduler_tkFrame = tk.Frame(self.windowSkillComposer_Tk)  # https://blog.teclado.com/tkinter-scrollable-frames/
        self.frameRowScheduler_tkFrame.grid(row=3, column=1, sticky='we')

        self.vRepeat_tkIntVar = tk.IntVar()
        self.loopRepeat_tkEntry = tk.Entry(self.frameRowScheduler_tkFrame, width=self.frameItemWidth[self.cLoop], textvariable=self.vRepeat_tkIntVar)
        self.loopRepeat_tkEntry.grid(row=0, column=self.cLoop)

        self.commonVar.tip(self.loopRepeat_tkEntry, self.translate.txt('tipRepeat'))

        for i in range(1, len(self.labelSkillEditorHeader)):
            label_tkLabel = tk.Label(self.frameRowScheduler_tkFrame, text=self.translate.txt(self.labelSkillEditorHeader[i]),
                          width=self.frameItemWidth[i] + self.headerOffset[i])
            label_tkLabel.grid(row=0, column=i, sticky='w')
            if self.tipSkillEditor[i]:
                self.commonVar.tip(label_tkLabel, self.translate.txt(self.tipSkillEditor[i]))

        schedulerHeight = self.parameterSet['schedulerHeight']    # The height of action frame scheduler
        canvas_tkCanvas = tk.Canvas(self.frameRowScheduler_tkFrame, width=self.canvasW, height=schedulerHeight, bd=0)
        scrollbar_tkScrollbar = tk.Scrollbar(self.frameRowScheduler_tkFrame, orient='vertical', cursor='double_arrow', troughcolor='yellow',
                              width=15, command=canvas_tkCanvas.yview)
        self.scrollableFrame_tkFrame = tk.Frame(canvas_tkCanvas)

        self.scrollableFrame_tkFrame.bind(
            '<Configure>',
            lambda e: canvas_tkCanvas.config(
                scrollregion=canvas_tkCanvas.bbox('all')
            )
        )
        canvas_tkCanvas.create_window((0, 0), window=self.scrollableFrame_tkFrame, anchor='nw')
        canvas_tkCanvas.config(yscrollcommand=scrollbar_tkScrollbar.set)
        canvas_tkCanvas.grid(row=1, column=0, columnspan=len(self.labelSkillEditorHeader))

        scrollbar_tkScrollbar.grid(row=1, column=len(self.labelSkillEditorHeader), sticky='ens')
        self.restartSkillEditor()


    # Called in placeProductImage()
    def createImage(self, frame, imgFile, imgW):
        img = Image.open(imgFile)
        ratio = img.size[0] / imgW
        img = img.resize((imgW, round(img.size[1] / ratio)))
        image = ImageTk.PhotoImage(img)
        imageFrame = tk.Label(frame, image=image)    # borderwidth=2, relief='raised'
        imageFrame.image = image
        return imageFrame


    # Called in __init(), changeModel()
    def placeProductImage(self):
        rowFrameImage = self.parameterSet['rowFrameImage']    # The row number of the image frame is located
        imgWidth = self.parameterSet['imgWidth']              # The width of image
        rowSpan = self.parameterSet['imgRowSpan']             # The number of lines occupied by the image frame

        self.frameImage = self.createImage(self.frameController_tkFrame, self.commonVar.resourcePath + self.model + '.jpeg', imgWidth)

        self.frameImage.grid(row=rowFrameImage, column=3, rowspan=rowSpan, columnspan=2)


    # Called in createMenu()
    def changeLan(self, lanChoice):
        function_name = inspect.currentframe().f_code.co_name
        if self.ready and self.translate.txt('lan') != lanChoice:
            inv_triggerAxis = {self.translate.txt(v): k for k, v in self.triggerAxis.items()}

            self.translate.language = self.translate.languageList[lanChoice]

            self.configure.defaultLan = lanChoice
            self.logger.log.debug(f"{self.configure.defaultLan}")

            self.windowSkillComposer_Tk.title(self.translate.txt('skillComposerTitle'))
            self.menubar_tkMenu.destroy()
            self.createMenu()

            textControllerLabel = self.translate.txt('Joint Controller')
            self.controllerLabels[0].config(text=textControllerLabel)

            textControllerLabel = self.translate.txt('Unbind All')
            self.controllerLabels[1].config(text=textControllerLabel)

            for i in range(6):
                self.controllerLabels[2 + 16 + i].config(text=self.translate.txt(self.sixAxisNames[i]))
            for i in range(16):
                if i in range(8, 12):
                    sideLabel = self.translate.txt(self.commonVar.sideNames[i % 8]) + '\n'
                else:
                    sideLabel = '\n'
                self.controllerLabels[2 + i].config(text=sideLabel + '(' + str(i) + ')\n' + self.translate.txt(self.scaleNames[i]))

                for d in range(2):
                    if d == 0:
                        self.commonVar.tip(self.binderButtons_List_tkRadioButtons[i * 2], self.translate.txt('tipBinder'))
                    else:
                        self.commonVar.tip(self.binderButtons_List_tkRadioButtons[i * 2 + 1], self.translate.txt('tipRevBinder'))

            self.frameDials.destroy()
            self.framePosture_tkFrame.destroy()
            self.frameSkillEditor_tkFrame.destroy()
            self.createDial()       # Note:  deacGyrp() is called in createDial() which is called in createPortMenu() which is called in updatePortMenu()
            self.createPosture()
            self.createSkillEditor()
            for i in range(len(self.labelSkillEditorHeader)):
                if i > 0:
                    self.frameRowScheduler_tkFrame.winfo_children()[i].config(text=self.translate.txt(self.labelSkillEditorHeader[i]))
                if self.tipSkillEditor[i]:
                    self.commonVar.tip(self.frameRowScheduler_tkFrame.winfo_children()[i], self.translate.txt(self.tipSkillEditor[i]))
            for r in range(len(self.frameList)):
                self.commonVar.tip(self.getWidget(r, self.cLoop), self.translate.txt('tipLoop'))
                tt = '='  # +self.translate.txt('Set')
                ft = 'sans 12'
                if self.activeFrame == r:
                    ft = 'sans 14 bold'
                    if self.frameList[r][2] != self.frameData:
                        tt = '!'  # + self.translate.txt('Save')
                        self.getWidget(r, self.cSet).config(fg='red')
                self.getWidget(r, self.cSet).config(text=tt, font=ft)

                step = self.getWidget(r, self.cStep).get()
                self.getWidget(r, self.cStep).config(values=('1', '2', '4', '8', '12', '16', '32', '48', '64', self.translate.txt('max')))
                self.getWidget(r, self.cStep).delete(0, tk.END)
                if step.isnumeric():
                    self.getWidget(r, self.cStep).insert(0, step)
                else:
                    self.getWidget(r, self.cStep).insert(0, self.translate.txt('max'))

                vTrig = self.getWidget(r, self.cTrig).get()
                self.getWidget(r, self.cTrig).config(values=list(map(lambda x:self.translate.txt(x),self.triggerAxis.values())))
                self.getWidget(r, self.cTrig).delete(0, tk.END)
                self.getWidget(r, self.cTrig).insert(0, self.translate.txt(self.triggerAxis[inv_triggerAxis[vTrig]]))


    # Called in createMenu()
    def showAbout(self):
        tk.messagebox.showinfo('Petoi Controller UI',
                            u'Petoi Controller for OpenCat\nOpen Source on GitHub\nCopyright © Petoi LLC\nwww.petoi.com')
        self.windowSkillComposer_Tk.focus_force()


    # Called in createMenu()
    def changeModel(self, model):
        if self.ready and model != self.model:
            self.configName = model
            model = model.replace(' ', '')

            # new way:  Use match-case statement
            match model:
                case 'Bittle' | 'BittleX':
                    model = 'Bittle'
                case 'Nybble' | 'NybbleQ':
                    model = 'Nybble'

            # old way
            # if 'Bittle' in model and model != "BittleX+Arm": # Bittle or Bittle X will be Bittle
            #     model = 'Bittle'

            # Reinitialize these objects to make ready for then setting up the Joint Controller part of the GUI with a different model.
            self.model = copy.deepcopy(model)

            # new way
            self.ardSerial.setPostureTable(self.model)      # Sets self.ardSerial.postureTable.

            # old way (eliminated self.postureTable in SkillComposer)
            # self.postureTable = self.ardSerial.postureDict[self.model]


            self.framePosture_tkFrame.destroy()
            self.frameImage.destroy()
            self.frameController_tkFrame.destroy()
            self.sliders=list()
            self.sliderValues = list()
            self.controllerLabels = list()
            self.previousBinderValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.binderValues_List_tkIntVar = list()
            self.binderButtons_List_tkRadioButtons=list()
            if self.OSname == 'win32':
                self.parameterSet = self.parameterWinSet[self.model]
            else:
                self.parameterSet = self.parameterMacSet[self.model]

            if self.model == 'BittleX+Arm':
                self.scaleNames = self.commonVar.BittleRScaleNames
            else:
                self.scaleNames = self.commonVar.RegularScaleNames

            self.createController()

#            widgetState = NORMAL
#            for i in range(16):
#                 if i in NaJoints[self.model]:
#                     clr = 'light yellow'
#                 else:
#                     clr = 'yellow'
#                 self.sliders[i].config(state=widgetState, bg=clr)
#                 self.sliders[i].grid(row=i)
#                 self.binderButton[i * 2].config(state=widgetState)
#                 self.binderButton[i * 2 + 1].config(state=widgetState)

            self.createPosture()
            self.placeProductImage()
            self.restartSkillEditor()


    # Called in updateButtonCommand(), loadSkillDataText(), loadSkill(), restartSkillEditor() plus called by buttons that are set up via addFrame() itself
    # Adds a skill frame row with the buttons to specify the values for each field in the skill frame
    def addFrame(self, currentRow):
        singleFrame_tkFrame = tk.Frame(self.scrollableFrame_tkFrame, borderwidth=1, relief=tk.RAISED)

        vChecked_tkBooleanVar = tk.BooleanVar()

            # 1st widget (button) in a skill frame row
        loopCheck_tkCheckbutton = tk.Checkbutton(singleFrame_tkFrame, variable=vChecked_tkBooleanVar, text=str(currentRow), onvalue=True, offvalue=False,
                                indicator=0, width=self.frameItemWidth[self.cLoop],
                                command=lambda currentRow=currentRow: self.setCheckBox(currentRow))
        loopCheck_tkCheckbutton.grid(row=0, column=self.cLoop)
        self.commonVar.tip(loopCheck_tkCheckbutton, self.translate.txt('tipLoop'))
        #        rowLabel = Label(singleFrame, text = str(currentRow), width = self.frameItemWidth[cLabel])
        #        rowLabel.grid(row=0, column=cLabel)

            # 2nd widget (button) in a skill frame row
        setButton_tkButton = tk.Button(singleFrame_tkFrame, text='=',  # +self.translate.txt('Set')
                           font='sans 14 bold', fg='blue',  # width=self.frameItemWidth[self.cSet],
                           command=lambda currentRow=currentRow: self.setFrame(currentRow))

        vStep_tkStringVar = tk.StringVar()
            # 3rd widget (spinbox)
        tk.Spinbox(singleFrame_tkFrame, width=self.frameItemWidth[self.cStep],
                values=('1', '2', '4', '8', '12', '16', '32', '48', '64', self.translate.txt('max')), textvariable=vStep_tkStringVar, wrap=True).grid(
            row=0, column=self.cStep)


        vTrig_tkStringVar = tk.StringVar()
            # 4th widget (spinbox)
        spTrig_tkSpinbox = tk.Spinbox(singleFrame_tkFrame, width=self.frameItemWidth[self.cTrig], values=list(map(lambda x:self.translate.txt(x),self.triggerAxis.values())),
                         textvariable=vTrig_tkStringVar, wrap=True)
        spTrig_tkSpinbox.grid(row=0, column=self.cTrig)

        vAngle_tkIntVar = tk.IntVar()
            # 5th widget (spinbox)
        tk.Spinbox(singleFrame_tkFrame, width=self.frameItemWidth[self.cAngle], from_=-128, to=127, textvariable=vAngle_tkIntVar,
                wrap=True).grid(
            row=0, column=self.cAngle)
            
        vDelay_tkIntVar = tk.IntVar()

        delayOption = list(range(0, 100, 50)) + list(range(100, 1000, 100)) + list(range(1000, 6001, 1000))
            # 6th widget
        tk.Spinbox(singleFrame_tkFrame, width=self.frameItemWidth[self.cDelay], values=delayOption, textvariable=vDelay_tkIntVar,
                wrap=True).grid(
            row=0, column=self.cDelay)

        vNote_tkStringVar = tk.StringVar()
        while True:
            note = random.choice(self.WORDS)
            if len(note) <= 5:
                break
        vNote_tkStringVar.set(note + str(currentRow))  # 'note')
        color = self.rgbtohex(random.choice(range(64, 192)), random.choice(range(64, 192)), random.choice(range(64, 192)))
            # 7th widget
        tk.Entry(singleFrame_tkFrame, width=self.frameItemWidth[self.cNote], fg=color, textvariable=vNote_tkStringVar, bd=1).grid(row=0,
                                                                                                      column=self.cNote)

            # 8th widget
        delButton_tkButton = tk.Button(singleFrame_tkFrame, text='<', fg='red', width=self.frameItemWidth[self.cDel],
                           command=lambda currentRow=currentRow: self.delFrame(currentRow))

            # 9th widget
        addButton_tkButton = tk.Button(singleFrame_tkFrame, text='v', fg='green', width=self.frameItemWidth[self.cAdd],
                           command=lambda currentRow=currentRow: self.addFrame(currentRow + 1))

        setButton_tkButton.grid(row=0, column=self.cSet)
        delButton_tkButton.grid(row=0, column=self.cDel)
        addButton_tkButton.grid(row=0, column=self.cAdd)

        self.updateButtonCommand(currentRow, 1)
        if currentRow == 0:
            newFrameData = copy.deepcopy(self.frameData)
        else:
            #            newFrameData = copy.deepcopy(self.frameList[currentRow - 1][2])
            newFrameData = copy.deepcopy(self.frameList[self.activeFrame][2])
            if self.activeFrame >= currentRow:
                self.activeFrame += 1
        newFrameData[3] = 0  # don't add the loop tag
        vStep_tkStringVar.set('8')
        vDelay_tkIntVar.set(0)

        self.frameList.insert(currentRow, [currentRow, singleFrame_tkFrame, newFrameData])
        self.changeButtonState(currentRow)
        singleFrame_tkFrame.grid(row=currentRow + 1, column=0)


    # Called in updateButtonCommand() plus called by buttons that are set up via addFrame() itself
    # Deletes a skill frame row
    def delFrame(self, currentRow):
        self.frameList[currentRow][1].destroy()
        del self.frameList[currentRow]
        self.updateButtonCommand(currentRow, -1)
        if self.activeFrame == currentRow:
            if currentRow > 0:
                self.setFrame(self.activeFrame - 1)
            elif self.totalFrame > self.activeFrame:
                self.activeFrame += 1
                self.setFrame(self.activeFrame - 1)
        elif self.activeFrame > currentRow:
            #        if self.activeFrame >= currentRow:
            self.activeFrame -= 1
        if self.frameList == []:
            self.scrollableFrame_tkFrame.update()
            time.sleep(0.5)
            self.restartSkillEditor()


    # Called in a long list of places
    def getWidget(self, row, idx):
        frame = self.frameList[row]
        widgets = frame[1].winfo_children()
        return widgets[idx]


    # Called in addFrame()
    def updateButtonCommand(self, currentRow, shift):
        for f in range(currentRow, len(self.frameList)):
            frame = self.frameList[f]
            frame[0] += shift
            widgets = frame[1].winfo_children()
            #            widgets[cLabel].config(text = str(frame[0])) #set
            widgets[self.cLoop].config(text=str(frame[0]), command=lambda idx=frame[0]: self.setCheckBox(idx))
            widgets[self.cSet].config(command=lambda idx=frame[0]: self.setFrame(idx))  # set
            widgets[self.cDel].config(command=lambda idx=frame[0]: self.delFrame(idx))  # delete
            widgets[self.cAdd].config(command=lambda idx=frame[0]: self.addFrame(idx + 1))  # add
            frame[1].grid(row=frame[0] + 1)
        self.totalFrame += shift


    # Called in addFrame(), transformToFrame(), export()
    def changeButtonState(self, currentRow):
        if self.totalFrame > 0:
            self.getWidget(currentRow, self.cSet).config(text='=',  # +self.translate.txt('Set')
                                                    font='sans 14 bold', fg='blue')
            if currentRow != self.activeFrame:
                if 0 <= self.activeFrame < self.totalFrame:
                    self.getWidget(self.activeFrame, self.cSet).config(text='=',  # +self.translate.txt('Set')
                                                                  font='sans 12', fg='blue')
                self.activeFrame = currentRow
            self.originalAngle[0] = 0


    # Called in setFrame(), play()
    def transformToFrame(self, f):
        frame = self.frameList[f]

        indexedList = list()
        for i in range(16):
            if self.frameData[4 + i] != frame[2][4 + i]:
                indexedList += [i, frame[2][4 + i]]
        self.frameData = copy.deepcopy(frame[2])
        self.updateSliders(self.frameData)
        self.changeButtonState(f)

        if len(indexedList) > 10:
            self.ardSerial.send(['L', self.frameData[4:20], 0.05])
        elif len(indexedList):
            self.ardSerial.send(['I', indexedList, 0.05])


    # Called in delFrame(), updateButtonCommand(), loadSkillDataText(), loadSkill()
    def setFrame(self, currentRow):
        frame = self.frameList[currentRow]
        if currentRow != self.activeFrame:
            self.transformToFrame(currentRow)
            self.frameController_tkFrame.update()

        else:
            for i in range(20):
                if frame[2][4 + i] != self.frameData[4 + i]:  # the joint that's changed
                    for f in range(currentRow + 1, self.totalFrame):
                        frame1 = self.frameList[f - 1]
                        frame2 = self.frameList[f]
                        if frame1[2][4 + i] == frame2[2][4 + i]:  # carry over to the next frame
                            frame2[2][4 + i] = self.frameData[4 + i]
                        else:
                            break
            #                frame[2][4+i] = self.frameData[4+i]
            frame[2][4:] = copy.deepcopy(self.frameData[4:])

            self.getWidget(currentRow, self.cSet).config(text='=',  # +self.translate.txt('Set')
                                                    font='sans 14 bold', fg='blue')
        if self.totalFrame == 1:
            self.activeFrame = 0
    
            #


    # Called in loadSkillDataTextMul(), popImport()
    def closePop(self, popWin):
        popWin.destroy()


    # NOT currently called anywhere
    def insert_val(self, e):
        e.insert(0, 'Hello World!')


    # Called in openFile(), popImport()
    def clearSkillText(self):
        self.skillText_tkText.delete('1.0', 'end')


    # Called in popImport()
    def openFile(self, top):
        print('open')
        file = tk.filedialog.askopenfilename()      # Returns a string representing the full file path of the selected file OR an empty string ("") if no file is selected.
        if file:
            print(file)
            with open(file, 'r', encoding="utf-8") as f:
                self.clearSkillText()
                self.skillText_tkText.insert('1.0', f.read())
        top.after(1, lambda: top.focus_force())

    # NOT currently called anywhere
    def loadSkillDataText(self, top):
        skillDataString = self.skillText_tkText.get('1.0', 'end')
        if len(skillDataString) == 1:
            tk.messagebox.showwarning(title='Warning', message='Empty input!')
            print('Empty input!')
            top.after(1, lambda: top.focus_force())
            return
        self.restartSkillEditor()
        skillDataString = ''.join(skillDataString.split()).split('{')[1].split('}')[0].split(',')
        if skillDataString[-1] == '':
            skillDataString = skillDataString[:-1]
        skillData = list(map(int, skillDataString))
        print(skillData)

        if skillData[0] < 0:
            header = 7
            frameSize = 20
            loopFrom, loopTo, repeat = skillData[4:7]
            self.vRepeat_tkIntVar.set(repeat)
            copyFrom = 4
            self.gaitOrBehavior_tkStringVar.set(self.translate.txt('Behavior'))
        else:
            header = 4
            if skillData[0] == 1:  # posture
                frameSize = 16
                copyFrom = 4
            else:  # gait
                if self.model == 'DoF16':
                    frameSize = 12
                    copyFrom = 8
                else:
                    frameSize = 8
                    copyFrom = 12
            self.gaitOrBehavior_tkStringVar.set(self.translate.txt('Gait'))
        if (len(skillData) - header) % abs(skillData[0]) != 0 or frameSize != (len(skillData) - header) // abs(
                skillData[0]):
            tk.messagebox.showwarning(title='Warning', message='Wrong format!')
            print('Wrong format!')
            top.after(1, lambda: top.focus_force())
            return
        top.destroy()

        for f in range(abs(skillData[0])):
            if f != 0:
                self.addFrame(f)
            frame = self.frameList[f]
            frame[2][copyFrom:copyFrom + frameSize] = copy.deepcopy(
                skillData[header + frameSize * f:header + frameSize * (f + 1)])
            if skillData[3] > 1:
                frame[2][4:20] = list(map(lambda x: x * 2, frame[2][4:20]))
                print(frame[2][4:24])

            if skillData[0] < 0:
                if f == loopFrom or f == loopTo:
                    self.getWidget(f, self.cLoop).select()
                    frame[2][3] = 1
                else:
                    frame[2][3] = 0
                #                    print(self.getWidget(f, self.cLoop).get())
                self.getWidget(f, self.cStep).delete(0, tk.END)
                if frame[2][20] == 0:
                    self.getWidget(f, self.cStep).insert(0, self.translate.txt('max'))
                else:
                    self.getWidget(f, self.cStep).insert(0, frame[2][20])
                self.getWidget(f, self.cDelay).delete(0, tk.END)
                self.getWidget(f, self.cDelay).insert(0, frame[2][21] * 50)

                self.getWidget(f, self.cTrig).delete(0, tk.END)
                self.getWidget(f, self.cAngle).delete(0, tk.END)
                self.getWidget(f, self.cTrig).insert(0, self.triggerAxis[frame[2][22]])
                self.getWidget(f, self.cAngle).insert(0, frame[2][23])

            else:
                self.getWidget(f, self.cStep).delete(0, tk.END)
                self.getWidget(f, self.cStep).insert(0, self.translate.txt('max'))
            self.activeFrame = f
        if self.totalFrame == 1:
            self.activeFrame = -1
        self.setFrame(0)


    # Called in loadSkillDataTextMul()
    def loadSkill(self,skillData):
        print(skillData)
        self.restartSkillEditor()
        if skillData[0] < 0:
            header = 7
            frameSize = 20
            loopFrom, loopTo, repeat = skillData[4:7]
            self.vRepeat_tkIntVar.set(repeat)
            copyFrom = 4
            self.gaitOrBehavior_tkStringVar.set(self.translate.txt('Behavior'))
        else:
            header = 4
            if skillData[0] == 1:  # posture
                frameSize = 16
                copyFrom = 4
            else:  # gait
                if self.model == 'DoF16':
                    frameSize = 12
                    copyFrom = 8
                else:
                    frameSize = 8
                    copyFrom = 12
            self.gaitOrBehavior_tkStringVar.set(self.translate.txt('Gait'))
        if (len(skillData) - header) % abs(skillData[0]) != 0 or frameSize != (len(skillData) - header) // abs(
                skillData[0]):
            tk.messagebox.showwarning(title='Warning', message='Wrong format!')
            print('Wrong format!')
            
            return
        
        for f in range(abs(skillData[0])):
            if f != 0:
                self.addFrame(f)
            frame = self.frameList[f]
            frame[2][copyFrom:copyFrom + frameSize] = copy.deepcopy(
                skillData[header + frameSize * f:header + frameSize * (f + 1)])
            if skillData[3] > 1:
                frame[2][4:20] = list(map(lambda x: x * 2, frame[2][4:20]))
                print(frame[2][4:24])

            if skillData[0] < 0:
                if f == loopFrom or f == loopTo:
                    self.getWidget(f, self.cLoop).select()
                    frame[2][3] = 1
                else:
                    frame[2][3] = 0
                #                    print(self.getWidget(f, self.cLoop).get())
                self.getWidget(f, self.cStep).delete(0, tk.END)
                if frame[2][20] == 0:
                    self.getWidget(f, self.cStep).insert(0, self.translate.txt('max'))
                else:
                    self.getWidget(f, self.cStep).insert(0, frame[2][20])
                self.getWidget(f, self.cDelay).delete(0, tk.END)
                self.getWidget(f, self.cDelay).insert(0, frame[2][21] * 50)

                self.getWidget(f, self.cTrig).delete(0, tk.END)
                self.getWidget(f, self.cAngle).delete(0, tk.END)
                self.getWidget(f, self.cTrig).insert(0, self.translate.txt(self.triggerAxis[frame[2][22]]))
                self.getWidget(f, self.cAngle).insert(0, frame[2][23])

            else:
                self.getWidget(f, self.cStep).delete(0, tk.END)
                self.getWidget(f, self.cStep).insert(0, self.translate.txt('max'))
            self.activeFrame = f
        if self.totalFrame == 1:
            self.activeFrame = -1
        self.setFrame(0)


    # Called in popImport()
    def loadSkillDataTextMul(self,top):
        skillDataString = self.skillText_tkText.get('1.0', 'end')
        if len(skillDataString) == 1:
            tk.messagebox.showwarning(title='Warning', message='Empty input!')
            print('Empty input!')
            top.after(1, lambda: top.focus_force())
            return
        self.restartSkillEditor()
        skillNames = re.findall(r"int8_t\ .*\[\]",skillDataString)
        skillNames = [st[7:-2] for st in skillNames]
        skills = re.findall(r"\{[-\s\d\W,]+\}",skillDataString)
        def processing(st):
            lst = st[1:-1].split(',')
            if lst[-1] == '' or lst[-1].isspace():
                lst = lst[:-1]
            lst = list(map(int, [l.strip() for l in lst]))
            return lst
        self.skills = list(map(processing, skills))
        if len(self.skills) ==1:
            top.destroy()
            self.loadSkill(self.skills[0])
        else:
            assert len(skillNames) == len(self.skills)
            self.skillDic = dict(zip(skillNames,range(len(skillNames))))
            self.skillN = ([],[],[])
            for (n,s) in zip(skillNames,range(len(skillNames))):
                if self.skills[s][0] < 0:
                    self.skillN[2].append(n)
                elif self.skills[s][0] > 1:
                    self.skillN[1].append(n)
                else:
                    self.skillN[0].append(n)
            print(self.skillN)
            top.destroy()
            self.comboTop_tkToplevel = tk.Toplevel(self.windowSkillComposer_Tk)
            self.comboTop_tkToplevel.title(self.translate.txt("Skill List"))
            typeLabel_tkLabel = tk.Label(self.comboTop_tkToplevel,text = self.translate.txt("Type of skill"))
            typeLabel_tkLabel.grid(row=1,column=0)
            nameLabel_tkLabel = tk.Label(self.comboTop_tkToplevel,text = self.translate.txt("Name of skill"))
            nameLabel_tkLabel.grid(row=1,column=1)
            values = []
            if len(self.skillN[0]):
                values.append(self.translate.txt("Posture"))
            if len(self.skillN[1]):
                values.append(self.translate.txt("Gait"))
            if len(self.skillN[2]):
                values.append(self.translate.txt("Behavior"))
            self.typeComb_tkCombobox = tk.Combobox(self.comboTop_tkToplevel,values=values,state='readonly')
            self.typeComb_tkCombobox.grid(row=2, column=0)
            self.nameComb_tkCombobox = tk.Combobox(self.comboTop_tkToplevel,values=[])
            self.nameComb_tkCombobox.grid(row=2, column=1)
            def selectTy(event):
                V = self.typeComb_tkCombobox.get()
                self.nameComb_tkCombobox.set('')
                if V==self.translate.txt("Posture"):
                    self.nameComb_tkCombobox['values'] = self.skillN[0]
                elif V==self.translate.txt("Gait"):
                    self.nameComb_tkCombobox['values'] = self.skillN[1]
                else:
                    self.nameComb_tkCombobox['values'] = self.skillN[2]
            def select():
                v = self.nameComb_tkCombobox.get()
                print(v)
                if v=='':
                    print("No option selected")
                    return
                self.loadSkill(self.skills[self.skillDic[v]])
            
            self.typeComb_tkCombobox.bind('<<ComboboxSelected>>',selectTy)
            tk.Button(self.comboTop_tkToplevel, text=self.translate.txt('Cancel'), width=10, command=lambda: self.closePop(self.comboTop_tkToplevel)).grid(row=3, column=1)
            tk.Button(self.comboTop_tkToplevel, text=self.translate.txt('OK'), width=10, command=select).grid(row=3, column=0)


    # Called in createSkillEditor()
    def popImport(self):
        # Create a Toplevel window
        top_tkToplevel = tk.Toplevel(self.windowSkillComposer_Tk)
        # top.geometry('+20+20')
        
        entryFrame_tkFrame = tk.Frame(top_tkToplevel)
        entryFrame_tkFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        self.skillText_tkText = tk.Text(entryFrame_tkFrame, width=120, spacing1=2)
        self.skillText_tkText.insert('1.0', self.translate.txt('exampleFormat')
                              + '\n\nconst int8_t hi[] PROGMEM ={\n\
            -5,  0,   0, 1,\n\
             1,  2,   3,\n\
             0,-20, -60,   0,   0,   0,   0,   0,  35,  30, 120, 105,  75,  60, -40, -30,     4, 2, 0, 0,\n\
            35, -5, -60,   0,   0,   0,   0,   0, -75,  30, 125,  95,  40,  75, -45, -30,    10, 0, 0, 0,\n\
            40,  0, -35,   0,   0,   0,   0,   0, -60,  30, 125,  95,  60,  75, -45, -30,    10, 0, 0, 0,\n\
             0,  0, -45,   0,  -5,  -5,  20,  20,  45,  45, 105, 105,  45,  45, -45, -45,     8, 0, 0, 0,\n\
             0,  0,   0,   0,   0,   0,   0,   0,  30,  30,  30,  30,  30,  30,  30,  30,     5, 0, 0, 0,\n\
        };')
        self.skillText_tkText.grid(row=0, column=0)
        # Create an Entry Widget in the Toplevel window
        tk.Button(top_tkToplevel, text=self.translate.txt('Open File'), width=10, command=lambda: self.openFile(top_tkToplevel)).grid(row=0, column=0)
        tk.Button(top_tkToplevel, text=self.translate.txt('Clear'), width=10, command=self.clearSkillText).grid(row=0, column=1)
        # Create a Button Widget in the Toplevel Window
        tk.Button(top_tkToplevel, text=self.translate.txt('Cancel'), width=10, command=lambda: self.closePop(top_tkToplevel)).grid(row=0, column=2)
#        Button(top, text=self.translate.txt('OK'), width=10, command=lambda: self.loadSkillDataText(top)).grid(row=0, column=3)
        tk.Button(top_tkToplevel, text=self.translate.txt('OK'), width=10, command=lambda: self.loadSkillDataTextMul(top_tkToplevel)).grid(row=0, column=3)
        scrollY_tkScrollbar = tk.Scrollbar(entryFrame_tkFrame, width=20, orient=tk.VERTICAL)
        scrollY_tkScrollbar.grid(row=0, column=1, sticky='ns')
        scrollY_tkScrollbar.config(command=self.skillText_tkText.yview)
        self.skillText_tkText.config(yscrollcommand=scrollY_tkScrollbar.set)

        #        scrollX = Scrollbar(entryFrame, width = 20, orient = VERTICAL)
        #        scrollX.grid(row = 1, column = 0, sticky='ew')
        #        scrollX.config(command=self.skillText.xview)
        #        self.skillText.config(xscrollcommand=scrollX.set)
        entryFrame_tkFrame.columnconfigure(0, weight=1)
        entryFrame_tkFrame.rowconfigure(0, weight=1)


    # Called in popEyeColor()
    def changeColor(self,i):
        function_name = inspect.currentframe().f_code.co_name
        colorTuple = tk.colorchooser.askcolor(title="Tkinter Color Chooser")
        self.logger.log.debug(f"colorTuple: {colorTuple}")
        self.topEye_tkToplevel.focus_force()  # the eye color edit window gets focus
        if (colorTuple[0] is not None) and (colorTuple[1] is not None):
            colors = list(colorTuple[0])
            self.colorHex = colorTuple[1]
            # for c in range(3):
            #     colors[c] //= 2    #it's not always returning interger.
            colors = list(map(lambda x: int(x), colors))  # colors have to be integer
            self.logger.log.debug(f"RGB: {colors}")
            if self.colorBinderValue_tkBooleanVar.get():
                self.activeEye = 0
                self.eyeColors[0]=colors
                for c in range(2):
                    self.canvasFace_tkCanvas.itemconfig(self.eyes[c], fill=self.colorHex)
                    self.eyeColors[c+1] = colors
                    self.eyeBtn[c].config(text = str(colors))
                self.ardSerial.send(['C', colors+[0,3], 0])
            else:
                self.activeEye = i
                self.canvasFace_tkCanvas.itemconfig(self.eyes[i], fill=self.colorHex)
                self.eyeColors[i+1] = colors
                self.eyeBtn[i].config(text = str(colors))
                self.ardSerial.send(['C', colors+[i+1,3], 0])


    # 
    def changeEffect(self,e):
        if self.colorBinderValue_tkBooleanVar.get():
            colors = self.eyeColors[self.activeEye+1]
            self.activeEye = 0
            self.eyeColors[0]=colors
            for c in range(2):
                self.canvasFace_tkCanvas.itemconfig(self.eyes[c], fill=self.colorHex)
                self.eyeColors[c+1] = colors
                self.eyeBtn[c].config(text = str(colors))
            self.ardSerial.send(['C', colors+[0, e], 0])
        else:
            colors = self.eyeColors[self.activeEye+1]
            self.eyeBtn[self.activeEye].config(text = str(colors))
            self.ardSerial.send(['C', colors+[self.activeEye+1, e], 0])


    # Called in createMenu()
    def popEyeColor(self):
        #E_RGB_ALL = 0
        #E_RGB_RIGHT = 1
        #E_RGB_LEFT = 2
        #
        #E_EFFECT_BREATHING = 0
        #E_EFFECT_ROTATE = 1
        #E_EFFECT_FLASH = 2
        #E_EFFECT_NONE = -1
        ledEffects = ['Breath','Rotate','Flash']
        effectDictionary = {
            'Breath':0,
            'Rotate':1,
            'Flash':2,
            }
        dia = 100
        crd = [10,10]
        gap = 40
        btShift = [100,25]
        width = dia*2 + gap + 2*crd[0]
        self.eyeColors = [[0,0,0],[0,0,0],[0,0,0]]
        self.activeEye = 0
        self.topEye_tkToplevel = tk.Toplevel(self.windowSkillComposer_Tk)
        self.topEye_tkToplevel.title('Eye Color Setter')
        self.topEye_tkToplevel.geometry(str(width)+'x170+400+200')
        face_tkFrame = tk.Frame(self.topEye_tkToplevel)
        face_tkFrame.grid(row = 0,column = 0)
        self.canvasFace_tkCanvas = tk.Canvas(face_tkFrame,height=120)
        self.canvasFace_tkCanvas.grid(row = 0,column = 0, columnspan = 2)
        eyeR = self.canvasFace_tkCanvas.create_oval(crd[0], crd[1], crd[0]+dia, crd[1]+dia, outline="#000",
                    fill="#606060", width=2)
        eyeL = self.canvasFace_tkCanvas.create_oval(crd[0]+dia+gap, crd[1], crd[0]+2*dia+gap, crd[1]+dia, outline="#000",
                    fill="#606060", width=2)
        self.eyes = [eyeR,eyeL]
        btR_tkButton = tk.Button(face_tkFrame,text=str(self.eyeColors[1]),width = 7, command=lambda:self.changeColor(0))
        btR_tkButton.place(x=crd[0]+dia/2-btShift[0]/2,y=crd[1]+dia/2-btShift[1]/2)
        btL_tkButton = tk.Button(face_tkFrame,text=str(self.eyeColors[2]),width = 7, command=lambda:self.changeColor(1))
        btL_tkButton.place(x=crd[0]+dia*3/2+gap-btShift[0]/2,y=crd[0]+dia/2-btShift[1]/2)
        self.eyeBtn = [btR_tkButton,btL_tkButton]
        self.colorBinderValue_tkBooleanVar = tk.BooleanVar()
        colorBinder_tkCheckbox = tk.Checkbutton(face_tkFrame, text='<>', indicator=0, width=3,
                                         variable=self.colorBinderValue_tkBooleanVar,onvalue=True, offvalue=False)
        colorBinder_tkCheckbox.place(x=crd[0]+dia+5,y=crd[1]+dia/2-btShift[1]/2)
        
        btnsEff_tkFrame = tk.Frame(face_tkFrame)
        btnsEff_tkFrame.grid(row = 1,column = 0)
        if self.OSname == 'win32':
            wValue = 5
        else:
            wValue = 3
        for e in range(len(effectDictionary)):
            tk.Button(btnsEff_tkFrame,text=self.translate.txt(list(effectDictionary.keys())[e]),width = wValue,command = lambda eff=list(effectDictionary.values())[e]:self.changeEffect(eff)).grid(row = 0,column = e)
        tk.Button(btnsEff_tkFrame,text=self.translate.txt('Meow'),width = wValue,command = lambda :self.ardSerial.send(['u', 0])).grid(row = 0,column = 3)
        self.topEye_tkToplevel.focus_force()  # the eye color edit window gets focus
        self.topEye_tkToplevel.mainloop()


    # 
    def playThread(self):
        self.playStop = False
        self.buttonPlay_tkButton.config(text=self.translate.txt('Stop'), fg='red', command=self.stop)
        t = threading.Thread(target=self.play)
        t.start()


    # 
    def play(self):
        if self.activeFrame + 1 == self.totalFrame:
            self.getWidget(self.activeFrame, self.cSet).config(text='=',  # +self.translate.txt('Set')
                                                          font='sans 12')
            self.activeFrame = 0
        for f in range(self.activeFrame, self.totalFrame):
            if self.playStop:
                break

            self.transformToFrame(f)

        self.buttonPlay_tkButton.config(text=self.translate.txt('Play'), fg='green', command=self.playThread)
        self.playStop = False


    # Called in createSkillEditor(), play(), stop
    def stop(self):
        self.buttonPlay_tkButton.config(text=self.translate.txt('Play'), fg='green', command=self.playThread)
        self.playStop = True


    # Called in generateMirrorFrame(), export()
    def mirrorAngles(self, singleFrame):
        singleFrame[1] = -singleFrame[1]
        singleFrame[4] = -singleFrame[4]
        singleFrame[4 + 2] = -singleFrame[4 + 2]
        for i in range(4, 16, 2):
            singleFrame[4 + i], singleFrame[4 + i + 1] = singleFrame[4 + i + 1], singleFrame[4 + i]
        if abs(singleFrame[22]) == 2:
            singleFrame[22] = -singleFrame[22]
            singleFrame[23] = -singleFrame[23]


    # Called in createSkillEditor()
    def generateMirrorFrame(self):
        self.sliderValues[16 + 2].set(-1 * self.sliderValues[16 + 2].get())
        self.sliderValues[16 + 5].set(-1 * self.sliderValues[16 + 5].get())
        self.mirrorAngles(self.originalAngle)
        self.mirrorAngles(self.frameData)
        self.updateSliders(self.frameData)
        self.indicateEdit()
        self.frameController_tkFrame.update()
        self.ardSerial.send(['L', self.frameData[4:20], 0.05])


    # Called in getCreatorInfo() to create the "Creator Information" window
    def popCreator(self):
        self.creatorWin_tkToplevel = tk.Toplevel(self.windowSkillComposer_Tk)

        self.creatorWin_tkToplevel.transient(self.windowSkillComposer_Tk)  # Make the window modal
        self.creatorWin_tkToplevel.grab_set()  # Ensure all input is directed to this window
        self.creatorWin_tkToplevel.focus_force()  # Bring the window to the front and focus

        self.creatorWin_tkToplevel.title(self.translate.txt("Creator Information"))
        self.creatorWin_tkToplevel.geometry('216x110+500+400')

        fmCreInfo_tkFrame = tk.Frame(self.creatorWin_tkToplevel)    # relief=GROOVE to draw border
        fmCreInfo_tkFrame.grid(ipadx=3, ipady=3, padx=3, pady=5, sticky=tk.W + tk.E)

        # creator label and entry
        creatorLabel_tkLabel = tk.Label(fmCreInfo_tkFrame, text=self.translate.txt('Creator'))
        creatorLabel_tkLabel.grid(row=0, column=0, padx=2, pady=6, sticky=tk.W)
            # self.creator is used to populate the text of the self.creator_entry
        self.creatorEntry_tkEntry = tk.Entry(fmCreInfo_tkFrame, textvariable=self.creator_tkStringVar, font=('Arial', 10), foreground='blue', background='white')
        self.creatorEntry_tkEntry.grid(row=0, column=1,padx=2, pady=6, sticky=tk.W)

        # location label and entry
        locationLabel_tkLabel = tk.Label(fmCreInfo_tkFrame, text=self.translate.txt('Location'))
        locationLabel_tkLabel.grid(row=1, column=0, padx=2, pady=3, sticky=tk.W)
            # self.location is used to populate the text of the self.location_entry
        self.locationEntry_tkEntry = tk.Entry(fmCreInfo_tkFrame, textvariable=self.location_tkStringVar, font=('Arial', 10), foreground='blue', background='white')
        self.locationEntry_tkEntry.grid(row=1, column=1, padx=2, pady=3, sticky=tk.W)

        fmCreInfo_tkFrame.columnconfigure(0, weight=1)  # set column width
        fmCreInfo_tkFrame.columnconfigure(1, weight=3)  # set column width

        # saveID button
        saveID_tkButton = tk.Button(fmCreInfo_tkFrame, text=self.translate.txt('Save'), command=self.saveID)
        saveID_tkButton.grid(row=2, columnspan=2, padx=3, pady=6, sticky=tk.W + tk.E)

        self.creatorWin_tkToplevel.protocol('WM_DELETE_WINDOW', self.saveID)


    # Called in popCreator() by the saveID_button
    def saveID(self):
        function_name = inspect.currentframe().f_code.co_name
        creatorValue = self.creatorEntry_tkEntry.get()

        locationValue = self.locationEntry_tkEntry.get()

        if creatorValue == '':
            tk.messagebox.showwarning(self.translate.txt('Warning'), self.translate.txt('InputCreator'))
            self.creatorWin_tkToplevel.after(1, lambda: self.creatorWin_tkToplevel.focus_force())
            self.creatorEntry_tkEntry.focus()  # force the entry to get focus
            return False
        else:
            self.creator_tkStringVar.set(creatorValue)

        if locationValue == '':
            tk.messagebox.showwarning(self.translate.txt('Warning'), self.translate.txt('InputLocation'))
            self.creatorWin_tkToplevel.after(1, lambda: self.creatorWin_tkToplevel.focus_force())
            self.locationEntry_tkEntry.focus()  # force the entry to get focus
            return False
        else:
            self.location_tkStringVar.set(locationValue)

        print("Creator:", self.creator_tkStringVar.get())
        print("Location:", self.location_tkStringVar.get())

        self.configure.creator = creatorValue           # Set here and use in saveConfigToFile()
        self.configure.location =locationValue          # Set here and use in saveConfigToFile()

        self.saveConfigToFile(self.commonVar.defaultConfPath)
        self.creatorInfoAcquired = True
        self.logger.log.debug(f"saveID, self.creatorInfoAcquired: {self.creatorInfoAcquired}")
        self.creatorWin_tkToplevel.destroy()


    # Called in saveID(), on_closing()
    def saveConfigToFile(self, filename):
        function_name = inspect.currentframe().f_code.co_name

        self.configure.configuration = [self.configure.lan, self.configure.configName, self.configure.path, self.configure.swVer, self.configure.bdVer,
                                  self.configure.mode, self.configure.creator, self.configure.location, str(self.configure.goodPorts_FutureAppSession_List_Str) ]

        # new way
        self.configure.writeConfigToFile(filename)

        # old way
        '''
        f = open(filename, 'w+', encoding="utf-8")
        self.logger.log.debug(f"config: {self.configure.configuration}")
        lines = '\n'.join(self.configure.configuration) + '\n'
        print('Saving configuration file')
        f.writelines(lines)
        time.sleep(0.1)
        f.close()

        '''


    # Called in createMenu() when "Utility > Creator Information" information is accessed; export()
    def getCreatorInfo(self):
        '''
            Originally, the defaultConfig.txt file was used for
                @ Persistent storage (between app sessions) of configuration fields
                @ Temporary storage (within an session)  of configuration fields

            Now, the defaultConfig.txt file is only used for persistent storage that is read only on app initialization.
            When the configuration is changed, the appropriate attributes of the Configure class instance are updated.  
            Any changes are written to the defaultConfig.txt file when the user exits the SkillComposer app.

            Here, the creator and the location are obtained from the Configure class instance and set to the GUI StringVar objects.
        '''
        self.creatorInfoAcquired = True
        self.creator_tkStringVar.set(self.configure.creator)
        self.location_tkStringVar.set(self.configure.location)
        self.popCreator()
        return


    # Called in createSkillEditor()
    def export(self):
        function_name = inspect.currentframe().f_code.co_name
        self.getCreatorInfo()
        self.logger.log.debug(f"export, self.creatorInfoAcquired: {self.creatorInfoAcquired}")
        if not self.creatorInfoAcquired:
            return  # to avoid a bug that the creator window won't open until the file saver is closed

        self.logger.log.info(f"Creator: {self.creator_tkStringVar.get()}")
        self.logger.log.info(f"Location: {self.location_tkStringVar.get()}")
        files = [('Text Document', '*.md'),
                 ('Python Files', '*.py'),
                 ('All Files', '*.*'),
                 ]
        file = tk.filedialog.asksaveasfile(filetypes=files, defaultextension='.md')

        if self.activeFrame + 1 == self.totalFrame:
            self.getWidget(self.activeFrame, self.cSet).config(text='=',  # +self.translate.txt('Set')
                                                          font='sans 12')
            self.windowSkillComposer_Tk.update()
            self.activeFrame = 0
        skillData = list()
        loopStructure = list()
        period = self.totalFrame - self.activeFrame
        if self.model == 'DoF16':
            frameSize = 12
            copyFrom = 8
        else:
            frameSize = 8
            copyFrom = 12
        if self.gaitOrBehavior_tkStringVar.get() == self.translate.txt('Behavior'):
            period = -period
            copyFrom = 4
            frameSize = 20
        if self.totalFrame == 1:
            period = 1
            copyFrom = 4
            frameSize = 16
        angleRatio = 1
        startFrame = self.activeFrame
        inv_triggerAxis = {self.translate.txt(v): k for k, v in self.triggerAxis.items()}
        for f in range(0, self.totalFrame):
            frame = self.frameList[f]
            self.frameData = copy.deepcopy(frame[2])
            if max(self.frameData[4:20]) > 125 or min(self.frameData[4:20]) < -125:
                angleRatio = 2
            if self.frameData[3] == 1:
                loopStructure.append(f - startFrame)
            if self.getWidget(f, self.cStep).get() == self.translate.txt('max') or int(self.getWidget(f, self.cStep).get())>127:
                self.frameData[20] = 0
            else:
                self.frameData[20] = int(self.getWidget(f, self.cStep).get())
            self.frameData[21] = max(min(int(self.getWidget(f, self.cDelay).get()) // 50,127),0)
            self.frameData[22] = int(inv_triggerAxis[self.getWidget(f, self.cTrig).get()])
            self.frameData[23] = max(min(int(self.getWidget(f, self.cAngle).get()),127),-128)
            if self.mirror:
                self.mirrorAngles(self.frameData)
            self.updateSliders(self.frameData)
            self.changeButtonState(f)
            self.frameController_tkFrame.update()
            skillData.append(self.frameData[copyFrom: copyFrom + frameSize])
        print(skillData)
        if period == 1:
            print(self.frameData[4:20])
            self.ardSerial.send(['L', self.frameData[4:20], 0.05])
            return
        if angleRatio == 2:
            for r in skillData:
                if frameSize == 8 or frameSize == 12:
                    r = list(map(lambda x: x // angleRatio, r))
                elif frameSize == 20:
                    r[:16] = list(map(lambda x: x // angleRatio, r[:16]))
        if len(loopStructure) < 2:
            loopStructure = [0,0]
        if len(loopStructure) > 2:
            for l in range(1, len(loopStructure) - 1):
                f = loopStructure[l] + startFrame
                frame = self.frameList[f]
                frame[2][3] = 0
                self.getWidget(f, self.cLoop).deselect()
            self.frameRowScheduler_tkFrame.update()

        print('{')
        print('{:>4},{:>4},{:>4},{:>4},'.format(*[period, 0, 0, angleRatio]))
        if period < 0 and self.gaitOrBehavior_tkStringVar.get() == self.translate.txt('Behavior'):
            print('{:>4},{:>4},{:>4},'.format(*[loopStructure[0], loopStructure[-1], self.loopRepeat_tkEntry.get()]))
        for row in skillData:
            print(('{:>4},' * frameSize).format(*row))
        print('};')

        if file:
#            print(file.name)
            x = datetime.datetime.now()
            modeName = self.model
            fileData = '# ' + file.name.split('/')[-1].split('.')[0] + '\n'
            fileData += 'Note: '+'You may add a short description/instruction here.\n\n'
            fileData += 'Model: ' + modeName + '\n\n'
            fileData += 'Creator: ' + self.creator_tkStringVar.get() + '\n\n'
            fileData += 'Location: ' + self.location_tkStringVar.get() + '\n\n'
            fileData += 'Date: ' + x.strftime("%b")+' '+x.strftime("%d")+', '+x.strftime("%Y") + '\n\n'
            fileData += '# [Demo](www.youtube.com) You can modify the link in the round brackets\n\n'
            fileData += '# Token\nK\n\n'
            fileData += '# Data\n{\n' + '{:>4},{:>4},{:>4},{:>4},\n'.format(*[period, 0, 0, angleRatio])
            if period < 0 and self.gaitOrBehavior_tkStringVar.get() == self.translate.txt('Behavior'):
                fileData += '{:>4},{:>4},{:>4},\n'.format(*[loopStructure[0], loopStructure[-1], self.loopRepeat_tkEntry.get()])
            self.logger.log.debug(f"skillData: {skillData}")
            for row in skillData:
                self.logger.log.debug(f"row: {row}")
                self.logger.log.debug(f"frameSize: {frameSize}")
                fileData += ('{:>4},' * frameSize).format(*row)
                fileData += '\n'
            fileData += '};'

            # the file in the config directory will be saved automatically
            filePathName = self.commonVar.configDir + self.commonVar.separation + 'SkillLibrary' + self.commonVar.separation + modeName + self.commonVar.separation + file.name.split('/')[-1]
            self.logger.log.debug(f"fileName is: {filePathName}")

            filePathList = [file.name, filePathName]
            for filePath in filePathList:
                if filePath == filePathName:
                    modelDir = self.commonVar.configDir + self.commonVar.separation + 'SkillLibrary' + self.commonVar.separation + modeName
                    self.commonVar.makeDirectory(modelDir)
                try:
                    with open(filePath, 'w+', encoding="utf-8") as f:
                        f.write(fileData)
                        time.sleep(0.1)
                    self.logger.log.info(f"save successfully: {filePath}")
                except Exception as e:
                    print(f'Exception {e}:  Export failed')
                    self.logger.log.info(f"save failed:{e}")
                    return False

        if self.gaitOrBehavior_tkStringVar.get() == self.translate.txt('Behavior'):
            skillData.insert(0, [loopStructure[0], loopStructure[-1], int(self.loopRepeat_tkEntry.get())])
        skillData.insert(0, [period, 0, 0, angleRatio])
        flat_list = [item for sublist in skillData for item in sublist]
        print(flat_list)

        self.ardSerial.send(['i', 0.1])
        res = self.ardSerial.send(['K', flat_list, 0], 0)
        print(res)


    # Called in createSkillEditor(), createRowScheduler(), changeModel(), delFrame(), loadSkillDataText(), loadSkill(), loadSkillDataTextMul()
    def restartSkillEditor(self):
        for f in self.frameList:
            f[1].destroy()
        self.frameList.clear()
        self.frameData = [0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          8, 0, 0, 0, ]
        self.totalFrame = 0
        self.activeFrame = 0
        self.addFrame(0)
        self.vRepeat_tkIntVar.set(0)
        # self.window.update()
        # self.setPose('calib')


    # Called in generateMirrorFrame(), setAngle(), set6Axis(), setPose()
    def indicateEdit(self):
        frame = self.frameList[self.activeFrame]
        if frame[2] != self.frameData:
            self.getWidget(self.activeFrame, self.cSet).config(text='!'  # + self.translate.txt('Save')
                                                          , font='sans 14 bold', fg='red')
        #            print('frm',frame[2])
        #            print('dat',self.frameData)
        else:
            self.getWidget(self.activeFrame, self.cSet).config(text='=',  # +self.translate.txt('Set')
                                                          font='sans 14 bold', fg='blue')


    # Called in addFrame(), updateButtonCommand()
    def setCheckBox(self, currentRow):
        frame = self.frameList[currentRow]
        if frame[2][3] == 0:
            frame[2][3] = 1
        else:
            frame[2][3] = 0


    # Called in createController()
    def unbindAll(self):
        for i in range(16):
            self.binderValues_List_tkIntVar[i].set(0)
            self.previousBinderValues[i] = 0
            self.changeRadioColor(i, 0)
        self.controllerLabels[1].config(fg='blue')


    # Called in unbindAll(), updateRadio()
    def changeRadioColor(self, joint, value):  # -1, 0, 1
            # new way

        # Calculate indices for the two radio buttons of the joint
            # Note:  For servo joints #0-15, we have tkRadiobuttons #0-31
        indexForwardBind = joint * 2                # E.g. if joint # = 3 then indexForwardBind = 3 * 2 = 6
        indexReverseBind = indexForwardBind + 1     # E.g. if joint # = 3 then indexReverseBind = (3 * 2) + 1 = 7

        # Set colors based on value
        if value == 1:      # Forward bind
            self.binderButtons_List_tkRadioButtons[indexForwardBind].configure(background='red')
            self.binderButtons_List_tkRadioButtons[indexReverseBind].configure(background='light blue')
        elif value == -1:   # Reverse bind
            self.binderButtons_List_tkRadioButtons[indexForwardBind].configure(background='light blue')
            self.binderButtons_List_tkRadioButtons[indexReverseBind].configure(background='red')
        else:               # Unbind
            self.binderButtons_List_tkRadioButtons[indexForwardBind].configure(background='light blue')
            self.binderButtons_List_tkRadioButtons[indexReverseBind].configure(background='light blue')

        self.binderButtons_List_tkRadioButtons[indexForwardBind].update()
        self.binderButtons_List_tkRadioButtons[indexReverseBind].update()

        # Update "Unbind All" button color
        if any(v in (1, -1) for v in self.previousBinderValues):    # If any servo joints currently bound then make the "Unbind All" button red to show that state.
            self.controllerLabels[1].config(fg='red')
        else:
            self.controllerLabels[1].config(fg='blue')

            # old way
        '''
        if value:
            self.binderButton[joint * 2 + (1 - value) // 2].configure(background='red')
            self.binderButton[joint * 2 + (value + 1) // 2].configure(background='light blue')
        else:
            self.binderButton[joint * 2].configure(background='light blue')
            self.binderButton[joint * 2 + 1].configure(background='light blue')
        self.binderButton[joint * 2].update()
        self.binderButton[joint * 2 + 1].update()
        if 1 in self.previousBinderValue or -1 in self.previousBinderValue:
            self.controllerLabels[1].config(fg='red')
        else:
            self.controllerLabels[1].config(fg='blue')
        '''


    # Called in createController()
    def updateRadio(self, joint):
        # Use this simple int variable to be able to examine the logic of this function.
        currentJointBinderValue_Int = self.binderValues_List_tkIntVar[joint].get()  # Get the shared binderValues_List_tkIntVar variable current value for the two tkRadioButton objects of this joint
        if self.previousBinderValues[joint] == currentJointBinderValue_Int:         # If the current value is the same as the previous value then unbind this joint (happens when you press the same tkRadioButton twice)
            self.binderValues_List_tkIntVar[joint].set(0)
        self.previousBinderValues[joint] = self.binderValues_List_tkIntVar[joint].get()    # Get the current state again since it may have change in the preceeding "if" clause.  Store it as "previous".
        self.changeRadioColor(joint, self.binderValues_List_tkIntVar[joint].get())


    # Called in createController()
    def setAngle(self, idx, value):
        if self.ready == 1:
            value = int(value)
            if self.binderValues_List_tkIntVar[idx].get() == 0:
                self.frameData[4 + idx] = value
                if -126 < value < 126:
                    self.ardSerial.send(['I', [idx, value], 0.05])
                else:
                    self.ardSerial.send(['i', [idx, value], 0.05])
            else:
                diff = value - self.frameData[4 + idx]
                indexedList = list()
                for i in range(16):
                    if self.binderValues_List_tkIntVar[i].get():
                        self.frameData[4 + i] += diff * self.binderValues_List_tkIntVar[i].get() * self.binderValues_List_tkIntVar[idx].get()
                        indexedList += [i, self.frameData[4 + i]]
                        
                if len(indexedList) > 10:
                    self.ardSerial.send(['L', self.frameData[4:20], 0.05])
                elif len(indexedList):
                    self.ardSerial.send(['I', indexedList, 0.05])

            self.indicateEdit()
            self.updateSliders(self.frameData)


    # Called in createController()
    def set6Axis(self, i, value):  # a more precise function should be based on inverse kinematics
        value = int(value)
        if self.ready == 1:
            if self.originalAngle[0] == 0:
                self.originalAngle[4:20] = copy.deepcopy(self.frameData[4:20])
                self.originalAngle[0] = 1
            positiveGroup = []
            negativeGroup = []
            if 'Bittle' in self.model:
                self.model = 'Bittle'

            if i == 0:  # ypr
                positiveGroup = []
                negativeGroup = []
            elif i == 1:  # pitch
                if self.jointConfig[self.model] == '>>':
                    positiveGroup = [1, 4, 5, 8, 9, 14, 15]
                    negativeGroup = [2, 6, 7, 10, 11, 12, 13]
                else:
                    positiveGroup = [1, 4, 5, 8, 9, 10, 11,]
                    negativeGroup = [6, 7, 12, 13, 14, 15]
            elif i == 2:  # roll
                if self.jointConfig[self.model] == '>>':
                    positiveGroup = [4, 7, 8, 11, 13, 14]
                    negativeGroup = [0, 5, 6, 9, 10, 12, 15]
                else:
                    positiveGroup = [4, 7, 8, 10, 13, 15]
                    negativeGroup = [0, 2, 5, 6, 9, 11, 12, 14]
            elif i == 3:  # Spinal
                if self.jointConfig[self.model] == '>>':
                    positiveGroup = [8, 9, 10, 11, 12, 13, 14, 15]
                    negativeGroup = []
                else:
                    positiveGroup = [8, 9, 10, 11, 12, 13, 14, 15]
                    negativeGroup = []

            elif i == 4:  # Height
                if self.jointConfig[self.model] == '>>':
                    positiveGroup = [12, 13, 14, 15]
                    negativeGroup = [8, 9, 10, 11, ]
                else:
                    positiveGroup = [12, 13, 10, 11, ]
                    negativeGroup = [8, 9, 14, 15]
            elif i == 5:  # Sideway
                if self.jointConfig[self.model] == '>>':
                    positiveGroup = []
                    negativeGroup = []

            for j in range(16):
                leftQ = (j - 1) % 4 > 1
                frontQ = j % 4 < 2
                upperQ = j / 4 < 3
                factor = 1
                if j > 3:
                    if not upperQ:
                        factor = 2
                    else:
                        factor = 1
                    if i == 1:
                        if self.jointConfig[self.model] == '>>':
                            if upperQ:
                                if frontQ:
                                    if value < 0:
                                        factor = 0
                                else:
                                    factor *= 2
                                    
                        if self.jointConfig[self.model] == '><':
                            if upperQ:
                                factor /= 3
                            
                    if i == 2:
                        if (value > 0 and not leftQ) or (value < 0 and leftQ):
                            factor /= 2

                if j in positiveGroup:
                    self.frameData[4 + j] = self.originalAngle[4 + j] + int(value * factor)
                if j in negativeGroup:
                    self.frameData[4 + j] = self.originalAngle[4 + j] - int(value * factor)

            self.ardSerial.send(['L', self.frameData[4:20], 0.05])
            self.updateSliders(self.frameData)
            self.indicateEdit()


    # Called in createDial()
    def sendCmd(self,event=None):
        function_name = inspect.currentframe().f_code.co_name
        if self.ready == 1:
            serialCmd = self.newCmd_tkStringVar.get()
            self.logger.log.debug(f'serialCmd={serialCmd}')
            if serialCmd != '':
                try:
                    token = serialCmd[0]
                    if token == 'S': #send everything as a string
                        self.ardSerial.send([serialCmd[1:], 1])
                    else:
                        cmdList = serialCmd[1:].replace(',',' ').split()
                        if len(cmdList) <= 1:
                            self.ardSerial.send([serialCmd, 1])
                        else:
                            cmdList = list(map(lambda x:int(x),cmdList))
                            self.ardSerial.send([token, cmdList, 1])
                        self.newCmd_tkStringVar.set('')
                except Exception as e:
                    print(f'Exception {e}:  Illegal input')
                    self.logger.log.info("Exception")
                    # print("Illegal input!")
                    raise e


    # Called in createPosture()
    def setPose(self, pose):
        if self.ready == 1:
            self.getWidget(self.activeFrame, self.cNote).delete(0, tk.END)
            self.getWidget(self.activeFrame, self.cNote).insert(0, pose + str(self.activeFrame))
            self.frameData[4:20] = copy.deepcopy(self.ardSerial.postureTable[pose])
            self.originalAngle[0] = 0
            self.updateSliders(self.ardSerial.postureTable[pose])       # pose is the skill name key so as to get the list of the pose servo joint angles from class ArdSerial Skills lists and NOT from the robot itself!
            self.indicateEdit()
            for i in range(6):
                self.sliderValues[16 + i].set(0)
            self.ardSerial.send(['i',0])                                # Sent 'i' alone to turn off all servos.    (-ee- why?)
            self.ardSerial.send(['k' + pose, 0])                        # The pose skill name is sent to the robot
        # if pose == 'rest':
            # send(['d', 0])


    # NOT currently called anywhere
    def setStep(self):
        self.frameData[20] = self.getWidget(self.activeFrame, self.cStep).get()


    # NOT currently called anywhere
    def setDelay(self):
        self.frameData[21] = int(self.getWidget(self.activeFrame, self.cDelay).get())


    # Called in transformToFrame(), generateMirrorFrame(), export(), setAngle(), set6Axis(), setPose()
    def updateSliders(self, angles):
        for i in range(16):
            self.sliderValues[i].set(angles[4 + i])
            self.frameData[4 + i] = angles[4 + i]


    # Called in createDial()
    def dialChange(self, dialTableIndex):       # -ee- Changed the name from "dial" to dialChange" to be more descriptive
        # Makes changes to a specific dial (Checkbutton) in frameDials
        if self.ready == 1:
            key = list(self.dialTable_Dict_StrStr)[dialTableIndex]              # Convert dialTable_Dict_StrStr to a list of keys then get the key at dialTableIndex
            if key == 'Connect':                                                # Dial "Connect" Checkbutton widget
                # The Dial "Connect" Checkbutton widget is always "on" since the App now won't display the GUI until it is connected to the robot
                self.buttonDialActive(self.enumDialCheckbuttonValues_List_Item.Connect_Index, True)
                return

            elif len(self.ardSerial.goodPorts_Dict_SPO_to_PortNameStr) > 0:     # All other Dial Checkbutton widgets
                if key == 'Gyro' and self.boardVer[0] == 'B':                   # Gyro dial Checkbutton widget with robot having BiBoard

                    # Use enum instead of index = 2 "magic number" to access that item of dialCheckbuttonValues_List_tkBooleanVar which is the Gyro tkCheckbutton tkBooleanVar value
                    if self.dialCheckbuttonValues_List_tkBooleanVar[self.enumDialCheckbuttonValues_List_Item.Gyro_Index.value].get():
                        result = self.ardSerial.send(['gB', 0])
                        if result != -1:  # and result[0][0] == 'G':
                            # Use enum instead of index = 3 "magic number" to access the child of frameDials which is the Gyro tkCheckbutton
                            self.frameDials.winfo_children()[self.enumFrameDials_Child.Gyro_tkCheckbutton_Index.value].config(
                                fg='green'
                            )
                        else:
                            self.buttonDialActive(self.enumDialCheckbuttonValues_List_Item.Gyro_Index, False)
                    else:
                        result = self.ardSerial.send(['gb', 0])
                        if result != -1:  # and result[0][0] == 'g':
                            # Use enum instead of index = 3 "magic number" to access the child of frameDials which is the Gyro tkCheckbutton
                            self.frameDials.winfo_children()[self.enumFrameDials_Child.Gyro_tkCheckbutton_Index.value].config(
                                fg='red'
                            )
                        else:
                            self.buttonDialActive(self.enumDialCheckbuttonValues_List_Item.Gyro_Index, True)
                else:
                    result = self.ardSerial.send([self.dialTable_Dict_StrStr[key], 0])
                    if result != -1:
                        state = result[0].replace('\r', '').replace('\n', '')
                        if state == 'k':                                        # state is the robot readback from sending the command specified by self.dialTable_Dict_StrStr[key]
                            self.buttonDialActive(dialTableIndex, True)
                        elif state == 'P':
                            self.buttonDialActive(dialTableIndex, False)
                        elif state == 'g':
                            self.buttonDialActive(dialTableIndex, False)
                        elif state == 'G':
                            self.buttonDialActive(dialTableIndex, True)
                        elif state == 'z':
                            self.buttonDialActive(dialTableIndex, False)
                        elif state == 'Z':
                            self.buttonDialActive(dialTableIndex, True)


    # Called in __init__()
    def on_closing(self):
        if tk.messagebox.askokcancel(self.translate.txt('Quit'), self.translate.txt('Do you want to quit?')):
            self.saveConfigToFile(self.commonVar.defaultConfPath)
            self.keepChecking = False  # close the background thread for checking serial port
            self.windowSkillComposer_Tk.destroy()
            self.ardSerial.closeAllSerial()
            os._exit(0)

#endregion  Class


# __main__  
#region     __main__  

if __name__ == '__main__':  

   skill_composer = SkillComposer()
   skill_composer.run()

#endregion  __main__

