#!/usr/bin/python

## ######################################################
##
## Package:             matrix_keypad
## Script:              BBb_GPIO.py
##
## Author:              Chris Crumpacker
## Date:                August 2013
##
## Project page:        http://crumpspot.blogspot.com/p/keypad-matrix-python-package.html
## PyPI package:        https://pypi.python.org/pypi/matrix_keypad
##
## Notes:               Code to handle the keypad when using with a Beagle Bone Black
##                      Updated with help Daniel Marcus, Details on his project can be found here:
##                      http://dmarcstudios.com/blog/beaglebone-hue-matrix/
##
## ######################################################
 
import Adafruit_BBIO.GPIO as GPIO
 
class keypad():
    def __init__(self, columnCount = 3):

        # Define pins to use for 3x4 Keypad
        pin1 = "P8_14"
        pin2 = "P8_16"
        pin3 = "P8_11"
        pin4 = "P9_13"
        pin5 = "P9_12"
        pin6 = "P9_26"
        pin7 = "P9_11"
        pin8 = "p9_24"

        # CONSTANTS 
        if columnCount is 3:
            self.KEYPAD = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                ["*",0,"#"]
            ]

            self.ROW         = [pin7, pin6, pin5, pin4]
            self.COLUMN      = [pin3, pin2, pin1]

        elif columnCount is 4:
            self.KEYPAD = [
                [1,2,3,"A"],
                [4,5,6,"B"],
                [7,8,9,"C"],
                ["*",0,"#","D"]
            ]

            self.ROW         = [pin8, pin7, pin6, pin5]
            self.COLUMN      = [pin4, pin3, pin2, pin1]
        else:
            return
     
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, GPIO.PUD_DOWN)
         
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, GPIO.PUD_DOWN)
         
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal <0 or colVal >2:
            self.exit()
            return
 
        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
         
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()
     
    # Loop while waiting for a keypress
    digit = None
    while digit == None:
        digit = kp.getKey()
     
    # Print the result
    print digit
