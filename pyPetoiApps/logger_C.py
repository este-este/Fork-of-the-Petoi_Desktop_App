# -*- coding: UTF-8 -*-

# Class Creation
    # este este
    # https://github.com/este-este/Fork-of-the-Petoi_Desktop_App
    # 18-May-2025
    # v001.00.00
'''
    This new file, logger_C.py, has a self-contained class, Logger, that encapsulates the logging functionality formerly found in the original arderial.py file.
'''

# Import
#region     Import
    #region

# External Imports
import logging

# Project Imports
    # None

    #endregion
#endregion  Import


# Class
#region     Class

class Logger:
    def __init__(self, callerName):     # Note the parameters that are passed to the constructor.

        '''
        Purpose / Responsibility:
            Create an object to handle logging.

        Project Dependencies:
            None
        '''

        self.callerName = callerName
        self.selfName = self.__class__.__name__

        FORMAT = '%(asctime)-15s %(name)s - %(levelname)s - %(message)s'

        '''
        Level: The level determines the minimum priority level of messages to log. 
        Messages will be logged in order of increasing severity: 
        DEBUG is the least threatening, 
        INFO is also not very threatening, 
        WARNING needs attention, 
        ERROR needs immediate attention, 
        and CRITICAL means “drop everything and find out what’s wrong.” 
        The default starting point is INFO, 
        which means that the logging module will automatically filter out any DEBUG messages.
        '''

        # The next line enables showing DEBUG level and higher.  Only enable during testing.
        #logging.basicConfig(level=logging.DEBUG, format=FORMAT)

        # The next line enables showing INFO level and higher.  Always enable for release.
        logging.basicConfig(filename='./logfile.log', filemode='a+', level=logging.INFO, format=FORMAT)

        self.log = logging.getLogger(callerName)

#endregion  Class
