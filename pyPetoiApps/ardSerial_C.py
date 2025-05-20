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
    The original file, ardSerial.py, has global and cross-module attributes and functions as well as transitive project imports.  The refactored version, ardSerial_C.py, has a self-contained class, ArdSerial, that encapsulates those attributes and functions.
'''


# Import
#region     Import
    #region

# External Imports
import inspect
import struct
import sys
import time
from types import NoneType
from SerialCommunication import *  # module SerialCommunication.py
import platform
import copy
import threading
import os
import glob
import re
from functools import singledispatch        # to do function overloading (not currently used)
import tkinter as tk                # See https://docs.python.org/3/library/tkinter.html
import tkinter.messagebox           # Import the messagebox module specifically

# Project Imports
from logger_C import Logger

    #endregion
#endregion  Import


# Class
#region     Class

class ArdSerial:
    def __init__(self, callerName, configure, translate):     # Note the parameters that are passed to the constructor.

        '''
        Purpose / Responsibility:
            Create an object to manage serial communication with the robot.

        Project Dependencies:
            Uses classes Logger, CommonVar and Configure objects plus, uniquely, in checkPortList(), it uses "serialObject" created from project class Communication as well as the static function Communication.Print_Used_Com().  Note that the class Configure object may be passed in to the constructor or created here.  The former is preferable.
        '''

        self.callerName = callerName
        self.selfName = self.__class__.__name__

        self.logger = Logger(self.selfName)     # Unlike other class objects a unique class Logger object must belong to each class

        self.configure = configure
        self.translate = translate

        # A dictionary with a structure of {SerialPort Object(<class 'SerialCommunication.Communication'>): portName(string), ...} 
            # to hold "SPO key / portName string value" pairs for app session use.
        self.goodPorts_Dict_SPO_to_PortNameStr = {}

        # A list of port strings to hold a string list of "good" serial ports (e.g. ["COM1", "COM2"] for APP SESSION USE.  
            # Note:  The list configure.ports_List_Str is used to hold and then write "good" ports to the configuration file
        self.goodPorts_CurrentAppSession_List_Str = []

        # A list of ports (as strings_ to check
        self.portsToCheck_List_Str = []

        self.delayBetweenSlice = 0.001

# Skills & Dictionaries
#region     Skills & Dictionaries

    # Skills
    #region     Skills
        # These skills are referenced in the postureTable dictionaries.

        self.balance = [
            1, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 30, 30, 30, 30, 30, 30, 30, 30]
        self.buttUp = [
            1, 0, 15, 1,
            20, 40, 0, 0, 5, 5, 3, 3, 90, 90, 45, 45, -60, -60, 5, 5]
        self.calib = [
            1, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dropped = [
            1, 0, -75, 1,
            0, 30, 0, 0, -5, -5, 15, 15, -75, -75, 45, 45, 60, 60, -30, -30]
        self.lifted = [
            1, 0, 75, 1,
            0, -20, 0, 0, 0, 0, 0, 0, 60, 60, 75, 75, 45, 45, 75, 75]
        self.rest = [
            1, 0, 0, 1,
            -30, -80, -45, 0, -3, -3, 3, 3, 70, 70, 70, 70, -55, -55, -55, -55]
        self.sit = [
            1, 0, -30, 1,
            0, 0, -45, 0, -5, -5, 20, 20, 45, 45, 105, 105, 45, 45, -45, -45]
        self.stretch = [
            1, 0, 20, 1,
            0, 30, 0, 0, -5, -5, 0, 0, -75, -75, 30, 30, 60, 60, 0, 0]
        self.zero = [
            1, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.balanceNybble = [
            1, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 30, 30, -30, -30, 30, 30, -30, -30, ]
        self.buttUpNybble = [
            1, 0, 15, 1,
            20, 40, 0, 0, 5, 5, 3, 3, 90, 90, -45, -45, -60, -60, -5, -5, ]
        self.droppedNybble = [
            1, 0, 75, 1,
            0, 30, 0, 0, -5, -5, 15, 15, -75, -75, -60, -60, 60, 60, 30, 30, ]
        self.liftedNybble = [
            1, 0, -75, 1,
            0, -70, 0, 0, 0, 0, 0, 0, 55, 55, 20, 20, 45, 45, 0, 0, ]
        self.restNybble = [
            1, 0, 0, 1,
            -30, -80, -45, 0, -3, -3, 3, 3, 60, 60, -60, -60, -45, -45, 45, 45, ]
        self.sitNybble = [
            1, 0, -20, 1,
            10, -20, -60, 0, -5, -5, 20, 20, 30, 30, -90, -90, 60, 60, 45, 45, ]
        self.strNybble = [
            1, 0, 15, 1,
            10, 70, -30, 0, -5, -5, 0, 0, -75, -75, -45, -45, 60, 60, -45, -45, ]
        self.zeroNybble = [
            1, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]


    #endregion     Skills

    # Dictionaries
    #region        Dictionaries

        #region     Posture Table Dictionaries
            # These postureTable dictionaries are referenced in the postureDict dictionary
            # Each is a dictionary of skills for a particular robot model.

        self.postureTableBittle = {
            "balance": self.balance,
            "buttUp": self.buttUp,
            # "dropped": self.dropped,
            # "lifted": self.lifted,
            # 'flat': self.flat,
            # 'table': self.table,
            "rest": self.rest,
            "sit": self.sit,
            "str": self.stretch,
            "zero": self.zero
        }

        self.postureTableBittleR = {
            "balance": self.balance,
            "buttUp": self.buttUp,
            # "dropped": self.dropped,
            # "lifted": self.lifted,
            # 'flat': self.flat,
            # 'table': self.table,
            "rest": self.rest,
            "sit": self.sit,
            "str": self.stretch,
            "zero": self.zero
        }

        self.postureTableNybble = {
            "balance": self.balanceNybble,
            "buttUp": self.buttUpNybble,
            # "dropped": self.droppedNybble,
            # "lifted": self.liftedNybble,
            # 'flat': self.flatNybble,
            # 'table': self.tableNybble,
            "rest": self.restNybble,
            "sit": self.sitNybble,
            "str": self.strNybble,
            "zero": self.zeroNybble
        }

        self.postureTableDoF16 = {
            "balance": self.balance,
            "buttUp": self.buttUp,
            # "dropped": self.dropped,
            # "lifted": self.lifted,
            # 'flat': self.flat,
            # 'table': self.table,
            "rest": self.rest,
            "sit": self.sit,
            "str": self.stretch,
            "zero": self.zero
        }

        #endregion     Posture Table Dictionaries


        #region     postureDict and SkillFullName Dictionaries
            # The postureDict dictionary is used to select the correct postureTable dictionary based on the model.
            # This is done in the class SkillComposer constructor plus function SkillComposer.changeModel() via ArdSerial.setPostureTable().

        self.postureDict = {        # This is a dictionary of dictionaries
            'Nybble': self.postureTableNybble,
            'Bittle': self.postureTableBittle,
            'BittleX+Arm': self.postureTableBittleR,
            'DoF16': self.postureTableDoF16
        }

# # NOT currently used anywhere (but, in the original code, it was used in allSkills.py)
        self.skillFullName = {
                'balance': 'balance',
                'buttUp': 'buttUp',
                'dropped': 'dropped',
                'lifted': 'lifted',
                'lnd': 'landing',
                'rest': 'rest',
                'sit': 'sit',
                'up': 'up',
                'str': 'stretch',
                'calib': 'calib',
                'zero': 'zero',
                'ang':'angry',
                 'bf': 'backFlip',
                 'bx': 'boxing',
                 'ck': 'check',
                 'cmh': 'comeHere',
                 'dg': 'dig',
                 'ff': 'frontFlip',
                 'fiv': 'highFive',
                 'gdb': 'goodboy',
                 'hds': 'handStand',
                 'hi': 'hi',
                 'hg': 'hug',
                 'hsk': 'handShake',
                 'hu': 'handsUp',
                 'jmp': 'jump',
                 'chr': 'cheers',
                 'kc': 'kick',
                 'mw': 'moonWalk',
                 'nd': 'nod',
                 'pd': 'playDead',
                 'pee': 'pee',
                 'pu': 'pushUp',
                 'pu1': 'pushUpSingleArm',
                 'rc': 'recover',
                 'rl': 'roll',
                 'scrh': 'scratch',
                 'snf': 'sniff',
                 'tbl': 'table',
                 'ts': 'testServo',
                 'wh': 'waveHead',
                 'zz': 'zz',
                 }

        #endregion     postureDict and SkillFullName Dictionaries

    #endregion        Dictionaries

#endregion     Skills & Dictionaries


        # ----------------

        self.initialized = False
        self.goodPortCount = 0      # Used in ArdSerial.testport() to count good ports and in ArdSerial.connectPort() to "Loop until at least one 'good' port is found"

        self.returnValue = ''
        self.timePassed = 0

    # -ee- new function
    def setPostureTable(self, model):
        self.postureTable = self.postureDict[model]


    # Called in serialWriteNumToByte(), __main__, SkillComposer Class, FirmwareUploader Class
    def printH(self, head, value):
        print(head, end=' ')
        print(value)


    # Called in serialWriteNumToByte(), serialWriteByte()
    def encode(self, in_str, encoding='utf-8'):
        if isinstance(in_str, bytes):
            return in_str
        else:
            return in_str.encode(encoding)


    # Accept a port_SPO, token and Skill Array Data as a list to send to the board as a byte stream.
    # Called in sendTask()
    def serialWriteNumToByte(self, port_SPO, token, var=None):  # Only to be used for c m u b I K L o within Python 
                                                        # (T_CALIBRATE, T_INDEXED_SEQUENTIAL_ASC, T_BEEP, T_INDEXED_SIMULTANEOUS_BIN, T_SKILL_DATA, T_LISTED_BIN,T_MELODY)
        function_name = inspect.currentframe().f_code.co_name
        # print("Num Token "); print(token);print(" var ");print(var);print("\n\n");
        self.logger.log.debug(f'serialWriteNumToByte, token={token}, var={var}')
        in_str = ""
        if var is None:
            var = []                    # var is the Skill Array Data (list of ASCII values that define the skill)
        if token == 'K':                # T_SKILL_DATA:  Writes complete skill data, as a binary char array, to the EEPROM
            period = var[0]
            #        print(encode(in_str))
            if period > 0:
                skillHeader = 4
            else:
                skillHeader = 7
            
            if period > 1:
                frameSize = 8  # gait
            elif period == 1:
                frameSize = 16  # posture
            else:
                frameSize = 20  # behavior
        # divide large angles by 2
            angleRatio = 1
            for row in range(abs(period)):
                for angle in var[skillHeader + row * frameSize:skillHeader + row * frameSize + min(16,frameSize)]:
                    if angle > 125 or angle < -125:
                        angleRatio = 2
                        break
                if angleRatio ==2:
                    break
        
            if angleRatio == 2:
                var[3] = 2
                for row in range(abs(period)):
                    for i in range(skillHeader + row * frameSize,skillHeader + row * frameSize + min(16,frameSize)):
                        var[i] //=2
                self.printH('rescaled:\n',var)
            
            var = list(map(int, var))
            in_str = token.encode() + struct.pack('b' * len(var), *var) + '~'.encode()

        else:
            if token.isupper():# == 'L' or token == 'I' or token == 'B' or token == 'C':
    #            if token == 'C':
    #                packType = 'B'
    #            else:
    #                packType = 'b'
    #            port.Send_data(token.encode())
                if len(var)>0:
                    message = list(map(int, var))
                    if token == 'B':
                        for l in range(len(message)//2):
                            message[l*2+1]*= 8  #change 1 to 8 to save time for tests
                            # print(message[l*2],end=",")
                            # print(message[l*2+1],end=",")
                            self.logger.log.debug(f"{message[l*2]},{message[l*2+1]}")
                if token == 'W' or token == 'C':
                    in_str = struct.pack('B' * len(message), *message)    # B - unsigned char, e.g. 'B'*3 means 'BBB'
                else:
                    in_str = struct.pack('b' * len(message), *message)    # b - signed char, e.g. 'b'*3 means 'bbb'
                in_str = token.encode() + in_str + '~'.encode()

            else:   #if token == 'c' or token == 'm' or token == 'i' or token == 'b' or token == 'u' or token == 't':
                message = ""
                for element in var:
                    message +=  (str(round(element))+" ")
                in_str = token.encode()+self.encode(message) +'\n'.encode()

        slice = 0
        while len(in_str) > slice:
            if len(in_str) - slice >= 20:
                port_SPO.Send_data(in_str[slice:slice+20])
            else:
                port_SPO.Send_data(in_str[slice:])
            slice+=20
            time.sleep(self.delayBetweenSlice)
        self.logger.log.debug(f"!!!! {in_str}")



    # Accept a port_SPO and var (typically a single token character but could be a list of elements such as a string task of a token plus a command or data) to send to the board as a byte.
    # Called in sendTask()
    def serialWriteByte(self, port_SPO, var=None):
        function_name = inspect.currentframe().f_code.co_name
        self.logger.log.debug(f'serial_write_byte, var={var}')
        if var is None:
            var = []
        token = var[0][0]           # For the first element of list var, take the first character and set = token.
        # printH("token:",token)
        # print var

        if (token == 'c' or token == 'm' or token == 'i' or token == 'b' or token == 'u' or token == 't') and len(var) >= 2:
            # Creates in_str as a space delimited string of the elements in var
            in_str = ""
            for element in var:
                in_str = in_str + element + " "
            in_str += '\n'
        elif token == 'L' or token == 'I':
            # Creates in_str as a list of integers which are binary (byte) representations of joint / servo angles pairs, terminated by '~'.
            if len(var[0]) > 1:
                var.insert(1, var[0][1:])
            var[1:] = list(map(int, var[1:]))
            in_str = token.encode() + struct.pack('b' * (len(var) - 1), *var[1:]) + '~'.encode()
        elif token == 'w' or token == 'k' or token == 'X' or token == 'g':
            # # Creates in_str as a single character containing the value of var[0]
            in_str = var[0] + '\n'
        else:
            # Creates in_str a string consisting of token plus \n (the string terminator).
            in_str = token + '\n'

        self.logger.log.debug(f"!!!!!!! {in_str}")

        port_SPO.Send_data(self.encode(in_str))      # -ee- Robot makes a beep when characters are sent to the board.
        time.sleep(0.01)


    # After sending a token to the board in sendTask(), this function loops, looking for a response from the board for a token-dependent amount of time.
    # Returns the response as a list or as a literal ("-1").
    # Called in sendTask()
    def printSerialMessage(self, port_SPO, token, timeout=0):   # TD-ee Probably should be named "getSerialMessage()"
        function_name = inspect.currentframe().f_code.co_name
        if token == 'k' or token == 'K':
            threshold = 8
        else:
            threshold = 3
        if 'X' in token:
            token = 'X'
        startTime = time.time()
        allPrints = ''
        while True:
            time.sleep(0.001)
            #            return 'err'
            if port_SPO:
                response = port_SPO.main_engine.readline().decode('ISO-8859-1')
                if response != '':
                    self.logger.log.debug(f"response is: {response}")
                    responseTrim = response.split('\r')[0]
                    self.logger.log.debug(f"responseTrim is: {responseTrim}")
                    if responseTrim.lower() == token.lower(): 
                        return [response, allPrints]
                    elif token == 'p' and responseTrim == 'k':
                        return [response, allPrints]
                    else:
                        # print(response, flush=True)
                        allPrints += response
            now = time.time()
            if (now - startTime) > threshold:
                # print('Elapsed time: ', end='')
                # print(threshold, end=' seconds\n', flush=True)
                self.logger.log.debug(f"Elapsed time: {threshold} seconds")
                threshold += 2
                if threshold > 5:
                    return -1
            if 0 < timeout < now - startTime:
                return -1


    # Low-level function to send a task to a single port (e.g. token plus command) to a port (or, in the original code, to multiple ports in parallel).
    # Called in testPort(), sendTaskParallel(), selectList(), send(), bCallback()
    def sendTask(self, port_SPO, task, timeout=0):
                                                                # task Structure is [token, var=[], time]
        function_name = inspect.currentframe().f_code.co_name
        self.logger.log.debug(f"Task is '{task}'")
        if port_SPO:
            try:
                previousBuffer = port_SPO.main_engine.read_all().decode('ISO-8859-1')
                if previousBuffer:
                    self.logger.log.debug(f"Previous buffer: {previousBuffer}")

                if len(task) == 2:
                    #        print('a')
                    #        print(task[0])
                    self.serialWriteByte(port_SPO, [task[0]])
                elif isinstance(task[1][0], int):
                    #        print('b')
                    self.serialWriteNumToByte(port_SPO, task[0], task[1])
                else:
                    #        print('c') #which case
                    self.serialWriteByte(port_SPO, task[1])
                token = task[0][0]
    #            printH("token",token)
                if token == 'I' or token =='L':
                    timeout = 1 # in case the UI gets stuck
                lastMessage = self.printSerialMessage(port_SPO, token, timeout)      # get any response from the board
                time.sleep(task[-1])
            #    with lock:
            #        sync += 1
            #        printH('sync',sync)
            #    if self.initialized:
            #        printH('thread',portDictionary[port])
            except Exception as e:
                #        printH('Fail to send to port',PortList[port])
                print(f'Exception {e}:  Failed to send to port {port_SPO}')
                if port_SPO in self.goodPorts_Dict_SPO_to_PortNameStr:
                    self.goodPorts_Dict_SPO_to_PortNameStr.pop(port_SPO)
                lastMessage = -1
        else:
            lastMessage = -1
        self.returnValue = lastMessage
        return lastMessage


    # Called in send()
    def splitTaskForLargeAngles(self, task):
        token = task[0]
        queue = list()
        if len(task)>2 and (token == 'L' or token == 'I'):
            var = task[1]
            indexedList = list()
            if token == 'L':
                for i in range(4):
                    for j in range(4):
                        angle = var[4 * j + i]
                        if angle < -125 or angle > 125:
                            indexedList += [4 * j + i, angle]
                            var[4 * j + i] = max(min(angle, 125), -125)
                if len(var):
                    queue.append(['L', var, task[-1]])
                if len(indexedList):
                    queue[0][-1] = 0.01
                    queue.append(['i', indexedList, task[-1]])
            #                print(queue)
            elif token == 'I':
                if min(var) < -125 or max(var) > 125:
                    task[0] = 'i'
                queue.append(task)
        else:
            queue.append(task)
        return queue


    # Called in many places including Calibrator Class, SkillComposer Class, Debugger Class, FirmwareUploader Class, TunerMu Class
    def send(self, task, timeout=0):
    #    printH('*** @@@ open port ',port) #debug
        if isinstance(self.goodPorts_Dict_SPO_to_PortNameStr, dict):
            port_SPO = list(self.goodPorts_Dict_SPO_to_PortNameStr.keys())      # Make the SPO keys from the dictionary into a list

        queue = self.splitTaskForLargeAngles(task)
        for task in queue:

            # new way
            print(f"\nUsing Port: {port_SPO[0].port}\tWith Task: {task}")
            # self.printH("\nUsing Port: ", p[0].port)
            # self.printH("With Task: ", task)
            returnResult = self.sendTask(port_SPO[0], task, timeout)   # just use the first port in the list
            print(f"Reply:  \n{returnResult}")

        return returnResult


    # Called in closeAllSerial()
    def closeSerialBehavior(self, port_SPO):
        function_name = inspect.currentframe().f_code.co_name
        try:
            port_SPO.Close_Engine()
        except Exception as e:
            print(f'Exception {e}:  Error closing port {port_SPO}')
            port_SPO.Close_Engine()
            raise e
        self.logger.log.info("Closed the serial port(s).")


    # Called in many places including Calibrator Class, SkillComposer Class, Debugger Class, TunerMu Class
    def closeAllSerial(self, clearPorts=True):
        if clearPorts is True:
            self.send(['d', 0], 1)

        for port_SPO in self.goodPorts_Dict_SPO_to_PortNameStr:
            t = threading.Thread(target=self.closeSerialBehavior, args=(port_SPO,))
            t.daemon = True
            t.start()
            t.join()

        if clearPorts is True:
            self.goodPorts_Dict_SPO_to_PortNameStr.clear()


    # NOT currently called anywhere             # Note:  -ee- If this function is later used, remember to initialize self.postureTable by calling setPostureTable(model).
    def schedulerToSkill(self, ports, testSchedule):
        compactSkillData = []
        newSkill = []
        outputStr = ""      # Not currently used

        for task in testSchedule:  # execute the tasks in the testSchedule
            print(task)
            token = task[0][0]
            if token == 'k' and task[0][1:] in self.postureTable:
                currentRow = self.postureTable[task[0][1:]][-16:]
                skillRow = copy.deepcopy(currentRow)
                compactSkillData.append(skillRow + [8, int(task[1] * 1000 / 500), 0, 0])
                newSkill = newSkill + skillRow + [8, int(task[1] * 1000 / 500), 0, 0]

            elif token == 'i' or token == 'I':
                currentRow = copy.deepcopy(skillRow)
                for e in range(0, len(task[1]), 2):
                    #                    print(task[1][e],task[1][e+1])
                    currentRow[task[1][e]] = task[1][e + 1]
                skillRow = copy.deepcopy(currentRow)
                compactSkillData.append(skillRow + [8, int(task[2] * 1000 / 500), 0, 0])
                newSkill = newSkill + skillRow + [8, int(task[2] * 1000 / 500), 0, 0]
            elif token == 'L':
                skillRow = copy.deepcopy(task[1][:16])
                compactSkillData.append(skillRow + [8, int(task[2] * 1000 / 500), 0, 0])
                newSkill = newSkill + skillRow + [8, int(task[2] * 1000 / 500), 0, 0]

            elif token == 'm':
                currentRow = copy.deepcopy(skillRow)
                for e in range(0, len(task[1]), 2):
                    currentRow[task[1][e]] = task[1][e + 1]
                    skillRow = copy.deepcopy(currentRow)
                    compactSkillData.append(skillRow + [8, int(task[2] * 1000 / 500), 0, 0])
                    newSkill = newSkill + skillRow + [8, int(task[2] * 1000 / 500), 0, 0]
        if len(compactSkillData) > 0:
            print('{')
            print('{:>4},{:>4},{:>4},{:>4},'.format(*[-len(compactSkillData), 0, 0, 1]))
            print('{:>4},{:>4},{:>4},'.format(*[0, 0, 0]))
        else:
            return
        angleRatio = 1
        for row in compactSkillData:
            if min(row) < -125 or max(row) > 125:
                angleRatio = 2
            print(('{:>4},' * 20).format(*row))
        print('};')
        newSkill = list(map(lambda x: x // angleRatio, newSkill))
        newSkill = [-len(compactSkillData), 0, 0, angleRatio, 0, 0, 0] + newSkill
        print(newSkill)
        #    sendTaskParallel(['K', newSkill, 1])
        self.send(['K', newSkill, 1])

    # Parse "result" from board readback and print the robot model and software version
    # Called in testPort(), replug(), selectList()
    def getModelAndVersion(self, result):
        if result != -1:
            parseOnNewline_List = result[1].replace('\r','').split('\n')

            for l in range(len(parseOnNewline_List)):
                if 'Nybble' in parseOnNewline_List[l] or 'Bittle' in parseOnNewline_List[l] or 'DoF16' in parseOnNewline_List[l]:
                    self.configure.model_ = parseOnNewline_List[l]
                    self.configure.version_ = parseOnNewline_List [l+1]

                    parseOnUnderscore_Str = self.configure.version_.split('_')
                    _bdVer = parseOnUnderscore_Str[0]
                    if _bdVer == "B01":
                        self.configure.bdVer = "BiBoard_V0_1"
                    elif _bdVer == "B02":
                        self.configure.bdVer = "BiBoard_V0_2"
                    elif _bdVer == "B10":
                        self.configure.bdVer = "BiBoard_V1_0"

                    self.configure.modelList += [self.configure.model_]
                    print(self.configure.model_)
                    print(self.configure.version_)
                    return

        self.configure.model_ = 'Bittle'
        self.configure.version_ = 'Unknown'


    # NOT currently called anywhere
    def deleteDuplicatedUsbSerial(self, list):
        for item in list:
            if 'modem' in item: # prefer the USB modem device because it can restart the NyBoard
                serialNumber = item[item.index('modem')+5:]
                for name in list:
                    if serialNumber in name and 'modem' not in name:    # remove the "wch" device
                        list.remove(name)
            elif 'serial-' in item: # prefer the "serial-" device 
                serialNumber = item[item.index('serial-')+7:]
                for name in list:
                    if serialNumber in name and 'wch' in name:    # remove the "wch" device
                        list.remove(name)
            elif 'cu.SLAB_USBtoUART' in item:
                list.remove(item)
        return list


    # Tests each port by sending a command and checking the response
    # Called in checkPortList()
    def testPort(self, port_SPO, port_Str):
        function_name = inspect.currentframe().f_code.co_name
        try:
            # time.sleep(3)
            waitTime = 0
            result = port_SPO.main_engine
            if result != None:
                result = result.read_all().decode('ISO-8859-1')
                if result != '':
                    print('Waiting for the robot to boot up')
                    time.sleep(2)
                    waitTime = 3
                else:
                    waitTime = 2
                function_name = inspect.currentframe().f_code.co_name
                self.logger.log.info(f"Sending token '?' to port {port_Str} in {function_name}()")            # -ee- Added

                result = self.sendTask(port_SPO, ['?', 0], waitTime)          # Send the query token, '?' and receive the board readback in "result"
                self.logger.log.info(f"Received '{result}' from port '{port_Str}' in testPort()")      # -ee- Added
                if result != -1:
                    self.logger.log.debug(f"Adding in testPort: {port_Str}")
                    self.goodPorts_Dict_SPO_to_PortNameStr.update({port_SPO: port_Str})     # Update dictionary with SPO (key) : port_Str (value) pair
                    self.goodPortCount += 1
                    self.getModelAndVersion(result)
                else:
                    port_SPO.Close_Engine()
                    self.logger.log.info(f"Port '{port_Str}' is not connected to a Petoi device.")      # -ee- Added
                    print(f"Port '{port_Str}' is not connected to a Petoi device.")
        #    sync +=1
        except Exception as e:
            print(f'Exception {e}:  Port ' + port_Str + ' cannot be opened!')
            raise e

        pass


    # Runs testPort() [Originally used different threads, one thread for each port in allPorts.  Now uses a single thread and checks ports one at a time.]
    # Called in connectPort(), keepCheckingPort()
    def checkPortList(self, portsToCheck_List_Str, needTesting=True):
        function_name = inspect.currentframe().f_code.co_name

        matchingPortsWithConfiguration_List_Str = [port for port in self.configure.goodPorts_FutureAppSession_List_Str if port in portsToCheck_List_Str]
        if len(matchingPortsWithConfiguration_List_Str) > 0:
            print(f"Found the following port(s) that match the configuration file: {matchingPortsWithConfiguration_List_Str}\nWill check only the matching port(s)")
            portsToCheck_List_Str.clear()
            portsToCheck_List_Str = matchingPortsWithConfiguration_List_Str

        # Test the ports in the order given
        for port_Str in (portsToCheck_List_Str):
            # if p == '/dev/ttyAMA0':
            #     continue
            print(f"\nChecking port: {port_Str}")
            port_SPO = Communication(port_Str, 115200, 1)          # Create Communication object, specifically a port_SerialPortObject or "port_SPO", in checkPortList()

            if port_SPO.main_engine == None:
                # Failed to create port_SPO so skip this port
                self.logger.log.info(f"Port '{port_Str}' is not connected to a Petoi device.")      # -ee- Added
                print(f"Port '{port_Str}' is not connected to a Petoi device.")
                continue
            else:
                # Set a write timeout (in sec)
                port_SPO.main_engine.write_timeout = 2

            if needTesting is True:

                self.testPort(port_SPO, port_Str.split('/')[-1])    # Split the port string to get the port name (e.g. /dev/ttyUSB0 -> ttyUSB0) and pass it to testPort()
            else:
                # -ee- As far as I can tell, this block is only used by FirmwareUploader.py when that file is directly run.  It has no relevance for SkillComposer_C.
                self.logger.log.debug(f"Adding in checkPortList: {port_Str}")
                self.goodPorts_Dict_SPO_to_PortNameStr.update({port_SPO: port_Str.split('/')[-1]})    # remove '/dev/' in the port name
                self.goodPortCount += 1
                self.logger.log.info(f"Connected to serial port: {port_Str}")
                print("Connected to serial port: " + port_Str)
        pass


    # Called in showSerialPorts()
    def get_raspberry_pi_model(self):
        """Detects the Raspberry pi model."""
        try :
            with open('/proc/cpuinfo','r')as cpuinfo:
                for line in cpuinfo:
                    if "Model" in line:
                        model_info = line.split(':')[1].strip()
                        if "Raspberry Pi 3" in model_info:
                            return "Raspberry Pi 3"
                        elif "Raspberry Pi 4" in model_info:
                            return "Raspberry pi 4"
                        elif "Raspberry Pi 5" in model_info:
                            return "Raspberry Pi 5"
                        else:
                            #if not 3,4,or 5,attempt to get revision code
                            with open('/proc/cpuinfo','r')as cpuinfo2:
                                for line2 in cpuinfo2:
                                    if"Revision" in line2:
                                        revision_code =line2.split(':')[1].strip()
                                        #basic check for revision codes that indicate pi5
                                        if re.match(r'^d[0-3]8', revision_code):
                                            return "Raspberry Pi 5"
                                        else:
                                            return "Raspberry Pi(Unknown Model)"
            return "Not a Raspberry pi"
        except FileNotFoundError:
            return "Not a Raspberry Pi"


    # Checks ports and automatically connects to a port that is connected to a Petoi robot (if any).
    # Called in each App's constructor.
    def connectPort(self, needTesting = True, needSendTask = True, needOpenPort = True):
        # Note:  Only FirmwareUploader requires needTesting = False, needSendTask = False, needOpenPort = False
        #       All other calls to connectPort require that all these three parameters are True

        function_name = inspect.currentframe().f_code.co_name
        while  self.goodPortCount < 1:                          # Loop until at least one "good" port is found

            allPorts_List_Str = Communication.Print_Used_Com()      # Get a list of available serial ports

            if len(self.portsToCheck_List_Str) == 0:                # If there are no ports in self.portsToCheck_List_Str then we must check allPorts_List_Str
                self.portsToCheck_List_Str = copy.deepcopy(allPorts_List_Str)

            if len(self.portsToCheck_List_Str) > 0:                      # Do if there are ports
                if needOpenPort is True:
                    self.checkPortList(self.portsToCheck_List_Str, needTesting)      # Runs testPort() for each port in allPorts
                    print(f'\n')    # Print blank line after all ports have been checked.
            else:                                               # Do if there are NO ports
                print(f"Found NO ports")
                return

            if len(self.goodPorts_Dict_SPO_to_PortNameStr) > 0:     # Do if some ports are GOOD
                self.logger.log.info(f"Serial port(s) connected to a robot:")
                self.goodPorts_CurrentAppSession_List_Str.clear()   # Clear any stale entries then update with new entries
                for port_SPO in self.goodPorts_Dict_SPO_to_PortNameStr:
                    self.logger.log.debug(f"datatype of p : {type(port_SPO)}")
                    self.logger.log.info(f"\t\t{self.goodPorts_Dict_SPO_to_PortNameStr[port_SPO]}")
                    self.goodPorts_CurrentAppSession_List_Str.append(self.goodPorts_Dict_SPO_to_PortNameStr[port_SPO])

                # At this point, self.portStrList is a list of good COM ports.
                    # Store list of this session's good COM ports in configure object for later saving to the configuration file to try for future app sessions.
                self.configure.goodPorts_FutureAppSession_List_Str = self.goodPorts_CurrentAppSession_List_Str

            else:                                                   # Do if NO ports are GOOD
                print('\nNo "good" port(s) found!  "Good" ports are those that are connected to a powered up robot attached.')
                print('Please make sure the serial port(s) can be recognized by the computer and that your robot has power.')
                if not self.configure.useMindPlus:
                    print('\nReplug mode:')
                    self.replug()  # self.goodPorts_Dict_SPO_to_PortNameStr will have good ports, if there are any.     # -ee- Removed needSendTask, needOpenPort from the function call


    # Show replug (disconnect then reconnect) window with countdown to manual port selection
    # Called in connectPort()
    def replug(self):     # -ee- Removed needSendTask, needOpenPort from the function call
        '''
            -ee-
            Replug was violating the Single Responsibility Principle (SRP, the "S" in SOLID principles programming)
                @ Responsibility #1:  It gathered a list of user manually selected existing (but not necessarily good) ports via a GUI
                @ Responsibility #2:  It used its own code [not that checkPortList() ] to the check of ports in the list.

            Only Responsibility #1 should be performed 

            Refactored:  eliminated Responsibility #2
        '''

        print('Please disconnect and reconnect the device from the COMPUTER side')

        # Create a tkinter root window.  There can only be one root window in a tkinter app, so it is destroyed before SkillComposer creates its own root window (windowSkillComposer)
        windowReplugPrompt_Tk = tk.Tk()
       # window.geometry('+800+500')    # old values
        windowReplugPrompt_Tk.geometry('+100+10')      # new values

        def on_closing():
            windowReplugPrompt_Tk.destroy()
            os._exit(0)

        windowReplugPrompt_Tk.protocol('WM_DELETE_WINDOW', on_closing)

        windowReplugPrompt_Tk.title(self.translate.txt('Replug mode'))

        thres = 3       # Time out for the manual plug and unplug.  Prefer 3 sec for release but use 10 sec for testing.
        print(f'Counting down {thres} sec to manual mode:')

        def buttonConfirm():
            replugPrompt_tkLabel.destroy()
            confirm_tkButton.destroy()

            countingDownMsg_tkLabel['text']= self.translate.txt('Counting down to manual mode: ')
            countingDownMsg_tkLabel.grid(row=0,column=0)

            secondsCountdown_tkLabel.grid(row=1,column=0)
            secondsCountdown_tkLabel['text']="{} s (label)".format(thres)
            countdown(time.time(),copy.deepcopy(Communication.Print_Used_Com()))    # start time is now, and the current port list is the argument

        replugPrompt_tkLabel = tk.Label(windowReplugPrompt_Tk, font='sans 14 bold', justify='left')
        replugPrompt_tkLabel['text'] = self.translate.txt('Replug prompt')
        replugPrompt_tkLabel.grid(row=0, column=0)
        confirm_tkButton = tk.Button(windowReplugPrompt_Tk, text=self.translate.txt('Confirm'), command=buttonConfirm)
        confirm_tkButton.grid(row=1, column=0, pady=10)
        countingDownMsg_tkLabel = tk.Label(windowReplugPrompt_Tk, font='sans 14 bold')
        secondsCountdown_tkLabel = tk.Label(windowReplugPrompt_Tk, font='sans 14 bold')

        def countdown(start,ap):
            if time.time() - start > thres:                 # This is the exit condition for countdown()
                countingDownMsg_tkLabel.destroy()
                secondsCountdown_tkLabel.destroy()
                self.manualSelect(windowReplugPrompt_Tk)    # Shows the windowReplugPrompt defined above
                return                                      # return to replug() caller
            elif (time.time() - start) % 1 < 0.1:           # This is the update condition for countdown()
                print(thres - round(time.time() - start) // 1)
                secondsCountdown_tkLabel['text'] = "{} s".format((thres - round(time.time() - start) // 1))
            windowReplugPrompt_Tk.after(100, lambda: countdown(start, ap))     # Causes the countdown window to refresh every 100 ms

        windowReplugPrompt_Tk.focus_force()  # new window gets focus
        windowReplugPrompt_Tk.mainloop()


    # Called in manualSelect() by OK button
    def selectList(self, listOfPorts_tkListbox, win):     # -ee- Removed needSendTask, needOpenPort from the function call

        self.portsToCheck_List_Str.clear()

        # build list of ports (as strings) to check
        for item in listOfPorts_tkListbox.curselection():
            port = listOfPorts_tkListbox.get(item)
            port = port.split('/')[-1]                  # Need when ports have "path-like" names (Mac OS, Linux)
            self.portsToCheck_List_Str.append(port)

        # Need to clear both "goodPorts" objects since we will return to connectPort() to check the ports that were selected
            # If none were selected, we still need to clear these objects since connectPort() will, in such a case, check all currently existing ports.
        self.configure.goodPorts_FutureAppSession_List_Str.clear()
        self.goodPorts_CurrentAppSession_List_Str.clear()

        win.destroy()


    # Called in replug()
    def manualSelect(self, window):     # -ee- Removed needSendTask, needOpenPort from the function call
        allPorts = Communication.Print_Used_Com()
        window.title(self.translate.txt('Manual mode'))

        manualMode_tkLabel = tk.Label(window, font = 'sans 14 bold')
        manualMode_tkLabel['text'] = self.translate.txt('Manual mode')
        manualMode_tkLabel.grid(row=0,column = 0)

        selectPortFromList_tkLabel = tk.Label(window, font='sans 14 bold')
        selectPortFromList_tkLabel["text"]=self.translate.txt('Please select the port from the list')
        selectPortFromList_tkLabel.grid(row=1,column=0)

        selectNoPortTriggersAllPortScan_tkLabel = tk.Label(window, font='sans 10 italic')

        selectNoPortTriggersAllPortScan_tkLabel["text"]=self.translate.txt('(Click "OK" with no port selected to trigger a scan of ALL ports.  \n\
Selecting ports with no Petoi devices will also trigger a scan of ALL ports.)')     # TD-ee   Added this label so also need this in all the language dictionaries of class Translate

        selectNoPortTriggersAllPortScan_tkLabel.grid(row=2,column=0)

        listOfPorts_tkListbox = tk.Listbox(window,selectmode="multiple")
        listOfPorts_tkListbox.grid(row=3, column=0, pady=(10, 10) )  # Add vertical padding of 10 pixels above and below the widget

        def refreshBox(tk_listbox):
            allPorts = Communication.Print_Used_Com()
            tk_listbox.delete(0,tk.END)
            for p in allPorts:
                tk_listbox.insert(tk.END,p)

        for p in allPorts:
            listOfPorts_tkListbox.insert(tk.END,p)

        ok_tkButton = tk.Button(window, text=self.translate.txt('OK'), command=lambda:self.selectList(listOfPorts_tkListbox, window))   # -ee- Removed needSendTask, needOpenPort from the function call
        ok_tkButton.grid(row=2, column=1)

        refresh_tkButton = tk.Button(window, text=self.translate.txt('Refresh'), command=lambda:refreshBox(listOfPorts_tkListbox))
        refresh_tkButton.grid(row=1, column=1, padx=(0, 10))       # Add right padding of 10 pixels

        window.mainloop()


    # NOT currently called anywhere
    def monitoringVoltage(self, ports, VoltagePin, timer, callback):
        while True and len(ports):
            time.sleep(timer)
            voltage = self.send(["R", [97, VoltagePin], 0])
            if callback is not None:
                callback(voltage)
            else:
                print("Current Voltage:" + str(voltage))


    # NOT currently called anywhere
    def monitoringDistance(self, ports, trigerPin, echoPin, timer, callback):
        while True and len(ports):
            time.sleep(timer)
            distance = self.send(["XU", [trigerPin, echoPin], 0])
            if callback is not None:
                callback(distance)
            else:
                print("Current Distance:" + str(distance))   


    # NOT currently called anywhere
    def monitoringJoint(self, ports, jointIndex, timer, callback):
        while True and len(ports):
            time.sleep(timer)
            if jointIndex == 0:
                angel = self.send(["j", jointIndex])
            else:
                angel = self.send(["j", [jointIndex], 0])
            if callback is not None:
                callback(angel)
            else:
                print("Current Angel:" + str(angel))

#endregion  Class

