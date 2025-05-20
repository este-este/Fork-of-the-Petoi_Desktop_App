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
    The original file, config.py, is a simple list of module attributes.  The refactored version, configure_C.py, has a self-contained class, Configure, that encapsulates that information using class attributes.  To do its job, you must pass in a class CommonVar object to the class Configure constructor.
    Class functions readConfigFromFile() and writeConfigToFile() allow reading and writing persistent configuration information.
'''

# Import
#region     Import
    #region

# External Imports
import inspect
import time
import ast

# Project Imports
from logger_C import Logger

    #endregion
#endregion  Import

# Class
#region     Class

class Configure:
    def __init__(self, callerName, commonVar, translate, model = None, lan = None):     # Note the parameters that are passed to the constructor.

        '''
        Purpose / Responsibility:
            Create an object to hold robot configuration information.
            Manage reading / writing configuration information to / from a file.
            Manage language support.

        Project Dependencies:
            Uses classes Logger and CommonVar objects.  Note that the class CommonVar object must be passed in to the constructor.
        '''

        self.callerName = callerName
        self.selfName = self.__class__.__name__

        self.logger = Logger(self.selfName)     # Unlike other class objects a unique class Logger object must belong to each class

        self.translate = translate
        self.commonVar = commonVar

        self.model_ = ''
        self.version_ = ''
        self.modelList = []
        self.useMindPlus = False

        self.creator = ""
        self.location = ""
        self.goodPorts_FutureAppSession_List_Str = []        # Stores a string list of "good" serial ports (e.g. ["COM1", "COM2"] for saving to configuration file 
                                                                # (and therefore later used in a FUTURE APP SESSION)

        self.readConfigFromFile(model, lan)

        self._originalState = self.__dict__.copy()


    def readConfigFromFile(self, model = None, lan = None):
        # -ee- This code was moved here from SkillComposer.py
            # -ee- renamed some attributes
        function_name = inspect.currentframe().f_code.co_name
        try:
            with open(self.commonVar.defaultConfPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print("Reading configuration from file.")
                # f.close()
            lines = [line.split('\n')[0] for line in lines]  # remove the '\n' at the end of each line
            num = len(lines)
            self.logger.log.debug(f"len(lines): {num}")
            self.lan = lines[0]      # was defaultLan
            self.path = lines[2]     # was defaultPath
            self.swVer = lines[3]    # was defaultSwVer
            self.bdVer = lines[4]    # was defaultBdVer
            self.mode = lines[5]     # was defaultMode
            if len(lines) >= 8:
                self.creator = lines[6]      # was defaultCreator
                self.location = lines[7]     # was defaultLocation

            if len(lines) >= 9:
                # The next item was originally called "defaultPorts",  These known "good" ports are stored as a list, e.g. ['COM7', 'COM10'] 
                    # but must be stringified here (and de-stringified later)
                self.goodPorts_FutureAppSession_List_Str = ast.literal_eval(lines[8] )

            else:
                self.creator = self.translate.txt('Nature')    # was defaultCreator
                self.location = self.translate.txt('Earth')    # was defaultLocation

            if model == None:
                self.configName = ''
            else:
                self.model_  = model
                self.configName     = self.model_
                self.model_  = self.model_.replace(' ','')
                if 'BittleR' in self.model_:
                    self.model      = 'BittleR'
                elif self.model_== 'BittleX':
                    self.model      = 'Bittle'
                elif self.model_== 'NybbleQ':
                    self.model      = 'Nybble'
                else:
                    self.model = self.model_

            self.configuration = [
                self.lan,            # was defaultLan
                self.configName,
                self.path,           # was defaultPath
                self.swVer,          # was defaultSwVer
                self.bdVer,          # was defaultBdVer
                self.mode,           # was defaultMode
                self.creator,        # was defaultCreator
                self.location,       # was defaultLocation
                self.goodPorts_FutureAppSession_List_Str
            ]

        except Exception as e:
            print('Configuration file does not exist.  Creating configuration.')        # File is saved in e.g. SkillComposer.saveConfigToFile()
            self.lan = 'English'
            self.path = self.commonVar.releasePath[:-1]
            self.swVer = '2.0'
            self.bdVer = self.commonVar.NyBoard_version
            self.mode = 'Standard'
            self.creator = self.translate.txt('Nature')
            self.location = self.translate.txt('Earth')
            self.goodPorts_FutureAppSession_List_Str
            self.configName = ''

            self.configuration = [
                self.lan, 
                self.configName, 
                self.path, 
                self.swVer, 
                self.bdVer,
                self.mode, 
                self.creator, 
                self.location,
                self.goodPorts_FutureAppSession_List_Str
            ]


    def writeConfigToFile(self, filename):
        function_name = inspect.currentframe().f_code.co_name
        try:
            with open(filename, 'w+', encoding="utf-8") as f:
                self.logger.log.debug(f"config: {self.configuration}")
                lines = '\n'.join(self.configuration) + '\n'
                f.writelines(lines)
                print("Writing configuration to file.")
                time.sleep(0.1)
        except IOError as e:
            self.logger.log.error(f"Failed to write configuration to file {filename}: {e}")
            print(f"\nError: Unable to write configuration to file {filename}. The file may be read-only.")

#endregion  Class
    #endregion