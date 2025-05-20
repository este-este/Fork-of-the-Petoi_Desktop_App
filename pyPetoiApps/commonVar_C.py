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
'''
    The original file, commonVar.py, has global and cross-module attributes and functions as well as transitive project imports..  The refactored version, commonVar_C.py, has a self-contained class, CommonVar, that encapsulates those attributes and functions.
'''


# Import
#region     Import
    #region

# External Imports
import platform
import sys
import tkinter as tk                # See https://docs.python.org/3/library/tkinter.html
import tkinter.messagebox           # Import the messagebox module specifically
import os
import inspect

# Project Imports
from logger_C import Logger

    #endregion
#endregion  Import

# Class
#region     Class

class CommonVar:
    def __init__(self, callerName):     # Note the parameters that are passed to the constructor.

        '''
        Purpose / Responsibility:
            Create an object to hold important variables and manage low-level functions.

        Project Dependencies:
            Uses a class Logger object.
        '''

        self.callerName = callerName
        self.selfName = self.__class__.__name__

        self.logger =  Logger(self.selfName)        # Unlike other class objects a unique class Logger object must belong to each class

        # Attributes
        #region     Attributes

        self.modelOptions = [
            'Nybble',
            'Nybble Q',
            'Bittle',
            'Bittle X',
            'Bittle X+Arm',
            'DoF16'
        ]

        self.NaJoints = {                       # These are the "Not Available" servo joints for each robot model.
            'Nybble': [3, 4, 5, 6, 7],
            'Bittle': [1, 2, 3, 4, 5, 6, 7],
        #    'BittleX': [1, 2, 3, 4, 5, 6, 7],
             'BittleX+Arm': [3, 4, 5, 6, 7],
            'DoF16' : []
        }

        self.BittleRScaleNames = [                          # Scale Names are the names applied to the tkScale widgets (e.g. in the Joint Controller part of the Skill Composer GUI)
            'Claw Pan', 'Claw Lift', 'Claw Open', 'N/A',
            'Shoulder', 'Shoulder', 'Shoulder', 'Shoulder',
            'Arm', 'Arm', 'Arm', 'Arm',
            'Knee', 'Knee', 'Knee', 'Knee']

        self.RegularScaleNames = [
            'Head Pan', 'Head Tilt', 'Tail Pan', 'N/A',
            'Shoulder', 'Shoulder', 'Shoulder', 'Shoulder',
            'Arm', 'Arm', 'Arm', 'Arm',
            'Knee', 'Knee', 'Knee', 'Knee']

        self.scaleNames = {                             # A dictionary of lists which contain strings
            'Nybble': self.RegularScaleNames,
            'Bittle': self.RegularScaleNames,
            'BittleX+Arm': self.BittleRScaleNames
        }

        self.sideNames = ['Left Front', 'Right Front', 'Right Back', 'Left Back']       # Used in GUI (e.g. above the tkScale objects in the Joint Controller part of the Skill Composer GUI)

        #endregion  Attributes

        # Initialization
        #region     Initialization

        if platform.system() == "Windows":    # for Windows OS
            self.resourcePath = '.\\resources\\'
            self.releasePath = '.\\release\\'
            self.resourcePath = './resources/'
            self.releasePath = './release/'
        sys.path.append(self.resourcePath)

        self.NyBoard_version = 'NyBoard_V1_2'
        verNumber = sys.version.split('(')[0].split()[0]
        verNumber = verNumber.split('.')
        self.logger.log.info(f"Python version is {verNumber}")
        print(f"Python version is {verNumber}")
        #verNumber = [2,1,1] #for testing
        self.supportHoverTip = True
        if int(verNumber[0])<3 or int(verNumber[1])<7:
            print("Please upgrade your Python to 3.7.1 or above!")
            root = tk.Tk()
            root.overrideredirect(1)
            root.withdraw()
            tk.messagebox.showwarning(title='Warning', message='Please upgrade your Python\nto 3.7.1 or above\nto show hovertips!')
            root.destroy()
            self.supportHoverTip = False
        #    exit(0)

        # old way
        '''
        try:
            from idlelib.tooltip import Hovertip
        except Exception as e:
            self.logger.log.info("Cannot import hovertip!")
            raise e
        '''

        # new way
        try:
            from idlelib.tooltip import Hovertip
            self.Hovertip = Hovertip  # Store Hovertip as an instance attribute
        except Exception as e:
            print(f'Exception {e}:  Cannot import hovertip')
            self.logger.log.info("Cannot import hovertip!")
            self.Hovertip = None  # Set to None if the import fails
            raise e

        if platform.system() == "Windows":    # for Windows OS
            self.separation = '\\'
            self.homeDri = os.getenv('HOMEDRIVE') 
            self.homePath = os.getenv('HomePath') 
            self.configDir = self.homeDri + self.homePath
        else:  # for Linux & macOS
            self.separation = '/'
            self.home = os.getenv('HOME') 
            self.configDir = self.home 
        self.configDir = self.configDir + self.separation +'.config' + self.separation +'Petoi'
        self.defaultConfPath = self.configDir + self.separation + 'defaultConfig.txt'

        print(f"{self.selfName}.{self.returnFunctionName()}():\t\tConfig path & file = {self.defaultConfPath}")
        self.makeDirectory(self.configDir)

        #endregion  Initialization


    def returnFunctionName(self):
        # Returns the name of the function that called this function
        current_function_name = inspect.currentframe().f_back.f_code.co_name
        return current_function_name


    # This function is used by only Debugger.py, FirmwareUploader.py and UI.py
    def displayName(self, name):
        if 'Bittle' in name and 'Bittle' != name:
            s = name.replace(' ','')
            name = 'Bittle'+' '+s[6:]
        return name


    # This function is called by the class CommonVar constructor and by the export function of class SkillComposer
    def makeDirectory(self, path):
        # delete spaces in the path string
        path = path.strip()
        # delete the '\' at the end of path string
        path = path.rstrip("\\").rstrip("/")
        # path = path.rstrip("/")

        # check whether the path exists
        isExists = os.path.exists(path)

        if not isExists:
            # Create the directory if it does not exist
            os.makedirs(path)
            print(f"{self.selfName}.{self.returnFunctionName()}():\t{path} created successfully\n")
            return True
        else:
            # If the directory exists, it will not be created and prompt that the directory already exists.
            print(f"{self.selfName}.{self.returnFunctionName()}():\t{path} already exists\n")
            return False


    # This function is used by only Calibrator.py
    def createImage(self, frame, imgFile, imgW):
        img_tkImage = tk.Image.open(imgFile)
        ratio = img_tkImage.size[0] / imgW
        img_tkImage = img_tkImage.resize((imgW, round(img_tkImage.size[1] / ratio)))
        image_tkPhotoImage = tk.ImageTk.PhotoImage(img_tkImage)
        imageFrame_tkLabel = tk.Label(frame, image=image_tkPhotoImage)
        imageFrame_tkLabel.image = image_tkPhotoImage
        return imageFrame_tkLabel


    # new version
    def tip(self, item, note):
        if self.supportHoverTip and self.Hovertip is not None:
            self.Hovertip(item, note)
        else:
            print(note)  # Fallback behavior

#endregion  Class
