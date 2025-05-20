# Work on the Fork of the Petoi Desktop App 

Update: 18-May-2025

## Introduction
The Petoi Desktop App (download of [v1.2.4 is here](https://github.com/PetoiCamp/OpenCat/releases/tag/1.2.4) and discussion on the Petoi website is [here](https://docs.petoi.com/desktop-app/introduction)) is actually a suite of 4 separate Python apps that facilitate working with the Petoi robots.  In particular, the Skill Composer app helps you design new skills (postures, behaviors, gaits) or tweak existing ones and the Calibrator app helps with robot servo joint calibration.  I have found these tools very useful and I wanted to add some new capabilities so I created this fork.

## Original Code Analysis
In my examination of the original Python code for the Petoi Desktop App, I found it relies heavily on global and cross-module attributes and functions as well as transitive project imports [(1)](##References).  In my experience, this makes the code logic more difficult to follow.  The transitive imports also make adding new code more difficult due to hidden dependencies and the tendency to get "circular imports".  Finally, the code is efficient and compact but sometimes this sacrifices code clarity.  I therefore decided to start with refactoring.

## Original Code Refactoring
I had several refactoring goals:  
1. Eliminate transitive project imports
2. Eliminate global and cross-module attributes and functions
3. Simplify and clarify code logic
4. Use "*Purpose_Type_Data*" descriptive naming [(2)](##References)
5. Use the Single Responsibility Principle (The "S" in the [SOLID principles](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/))
6. Use self-contained project classes [(3)](##References) with compositional design [(4)](##References)

The UI.py app is just an app launcher so I began with the Skill Composer app code in SkillComposer.py.

In the original SkillComposer.py code, there are the following import dependencies:  
* ardSerial.py 
* config.py
* commonVar.py
* translate.py
* SerialCommunication.py

In this fork, the SkillComposer.py file and most of these dependency files were refactored into self-contained classes.  In the new classes, I strived to use the Single Responsibility Principle while staying aligned with the original code layout.  

This gave these classes...
* SkillComposer() in SkillComposer_C.py
* ArdSerial() in ardSerial_C.py
* Configure() in config_C.py
* CommonVar() in commonVar_C.py
* Translate() in translate_C.py
* Logger() in logger_C.py

SkillComposer manages the GUI logic, ArdSerial handles serial communication, Configure deals with the configuration file, CommonVar becomes a utility class, Translate manages language support and Logger centralizes the logging responsibility.  SerialCommunication.py was already a self-contained class so no modifications were needed there.  

Compositional design means each class encapsulates what it needs to operate: 
* SkillComposer "has-a" set of ArdSerial, Configure, CommonVar, Translate, and Logger objects. 
* ArdSerial "has-a" set of Configure, CommonVar, Translate, and Logger objects
* Configure "has-a" set of CommonVar, Logger and Translate objects
* CommonVar "has-a" Logger object
* Translate is a data class with one function so it encapsulates nothing else.
* Logger is a class wrapper for the Python logging package so it encapsulates nothing else.

This mostly achieves refactoring goals 1, 2, 5, and 6.  Refactoring for goals 3 and 4 was performed on a case by case basis so the code is easier to understand in some areas but those objectives are also incomplete.

## Coding Fixes and New Capabilities
In the current original code version, 3 of the 4 apps that can be launched by UI.py will test all available serial ports by sending the '?' token.  If a Petoi robot is booted up and running on a serial port, it will respond with the robot model [e.g. "Bittle X"] and the board name and board version (plus the software version date) [e.g. **B02**_250330].  The app uses that information to later save the discovered robot configuration to a file, "defaultConfig.txt".  For a "Bittle X" robot having a "BiBoard v0_2", this is what the original app code gives as file output...

> English <br>
> Bittle X <br>
> .\release <br>
> 2.0 <br>
> NyBoard_V1_2 <br>
> Standard <br>
> Nature <br>
> Earth

...where the robot model is correct but the board name and board version are wrong.  This is minor but the issue was fixed in this fork, for the SkillComposer app, to give this output...

> English <br>
> Bittle X <br>
> ./release <br>
> 2.0 <br>
> BiBoard_V0_2 <br>
> Standard <br>
> Nature <br>
> Earth <br>
> ['COM7', 'COM10']

...where the board and board version are correctly identified.

This output also introduces a more important issue.  Note the serial port entries at the end of the list.  These serial ports are the USB port and the Bluetooth port, respectively, that I use to connect to my Bittle X.  In the original code, that information is not saved to the "defaultConfig.txt" file.

On my computer, there are at least 7 and sometimes more serial ports.  Some are persistent and usually associated with wireless devices (typically via Bluetooth pairing).  Others are transient and usually associated with wired (e.g. USB) devices.  In the original code, this scanning was done on multiple threads, which should speed things up but it still took about 35 sec to scan all the serial ports to find the two ports associated with my Bittle X.

This may not sound like much but I pay that time delay price ***every time*** I use 3 of the 4 apps in the Petoi Desktop App suite.  Therefore, in this fork, for the SkillComposer app, the code was changed to use only one thread ***but*** the code that tests the ports was optimized to take about half the time of the original code (about 18 sec in my case).  Furthermore, the code was changed to save those serial ports found to be "good" (that have a connected and working Petoi robot) to the "defaultConfig.txt" file.  This gives the port list shown above.  In subsequent uses of the fork SkillComposer app, only the previous "good" serial ports are looked for and tested.  In my case, once the "good" ports are found and saved, subsequent SkillComposer runs require only 3 sec of test time delay before the app opens!  

So, the fork code change provides a shorter first-time delay to find the "good" ports and then a very short delay in later usage.  Note that the original code does not check for this line with "good" serial ports but neither does the original code give an error if that line is present.  This ensures  "defaultConfig.txt" file compatibility between the fork code and the original code.

While making these code changes, I also modified how "replug" mode works. The SkillComposer app enters "replug" mode when it cannot find any ports that are "good".  When the app enters "replug" mode in the original code, the user must have a working and connected Petoi robot and, in the resulting "manual mode", must select one or more "good" ports from a list of available serial ports.  If the user selects no ports, the original code app will throw an error.  

In the fork, I fixed this but also took the opportunity to use the selection of no ports to force the SkillComposer app to repeat the scan of all ports.  This is how you can replace the earlier "good" port(s) saved in the "defaultConfig.txt" file (say from a different Petoi robot) with the "good" port(s) of the currently connected Petoi robot.  Note also that in the fork version, I have removed "Listening" mode so the SkillComposer app will not open until it finds a "good" port (normal mode) or until user selects one or more "good" ports (replug mode).  Of course you can always abort by closing the shell window in which the app was launched.

On my computer (a Windows 10 PC), in the original app code, the "replug" prompt was displayed partially off screen.  This was fixed in the fork SkillComposder app code.  Also, the "countdown to manual mode" was reduced from 10 sec to 3 sec.

**All fork releases are source code, not complied executables.  To run the SkillComposer app, first navigate to the "pyPetoiApps" folder and open a shell window.  In the shell window, use the command "python sc.py".  When done, exit the app and close the shell window.  You can also just close the shell window to abort the app at any time.**

## References
1. "*Module A imports module B imports module C imports module D...*" is a chain of transitive imports.  If module A depends on an object in module D, that is called a transitive dependency.  
2. "*Purpose_Type_Data*" descriptive naming answers the question:  "*What is the object, what type of object is it and what data type(s) does it contain?*  E.g. "dialTable" becomes "dialTable_Dict_StrStr"
3. Here, a self-contained project class only imports Python libraries and project classes from which encapsulated instances are created and managed.  Self-contained classes have advantages over transitive import chains:    
![Self-Contained Class vs Transitive Import Chain](Self-Contained%20Class%20vs%20Transitive%20Import%20Chain.png) 
4. Compositional design sets up "Has-a" relationships.  
