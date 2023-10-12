#This is a test program for the Alfaspid MD01/02 controller and
#is written in Python 2.7

#The program was written for demonstration purposes only and as
#a template for users to fashion any custom software project
#they may be attempting.

#Before using this program, the user must:
#   1.  Install python2 followed by the pyserial module on the computer to
#       be used.
#   2.  Install and set-up the RAS Rotator and Controller in accordance
#       with the Alfaspid RAS Manual and ensure that it is working with the
#       manual controls on the controller.
#   3.  Obtain a controller program such as Ham Radio Deluxe or N1MM to
#       confirm that the RS232 or USB connection between the Computer
#       and Controller are fully functional.

#A copy of file "Program_format-Komunicacji-2005-08-10-p2.pdf" must be
#obtained from the Alfaradio website to fully understand this program.

#This program was developed on a DELL 610 Laptop with Windows XP and
#tested on computers running Windows 7, Debian Linux and OSX 10.10

#No warranty is stated nor implied by Alfaradio for this program's use.
	   

# required libraries
import serial
import time
import os 
from time import sleep

# get the Comm Port information
input_variable = raw_input ("Enter comm port: ")
port = (input_variable)
input_variable = input("Enter comm port baud rate: ")
baud = (input_variable)
#  Multiplier is fixed at 10 for MD controllers
multi = 10
# define constants.
loop = 1
zero5 = chr(0)+chr(0)+chr(0)+chr(0)+chr(0)

print ("Enter 888 to stop rotation.")
print ("Enter 999 to update rotator status.")
print ("Enter 987 to quit program.")

#Open Comm Port
ser = serial.Serial(port, baud, timeout = 0)

while loop == 1:

   #Get desired azimuth
   print (" ")
   input_variable = input ("Enter azimuth: ")
   az = int(input_variable)

   if az == 888:
      # Build the stop command word.
      out = chr(87)+zero5+zero5+chr(15)+chr(32)
      x = ser.write(out)    
      # Wait for answer from controller
      sleep (0.75)

      data = ser.read(9999)
	  # once all 12 characters are received, decode location.
      if len(data) >= 12:
         s1 = ord(data[1].encode('latin-1'))
         s2 = ord(data[2].encode('latin-1'))
         s3 = ord(data[3].encode('latin-1'))
         s4 = ord(data[4].encode('latin-1'))
         s5 = ord(data[5].encode('latin-1'))
         s6 = ord(data[6].encode('latin-1'))
         s7 = ord(data[7].encode('latin-1'))
         s8 = ord(data[8].encode('latin-1'))
         s9 = ord(data[9].encode('latin-1'))
         s10 = ord(data[10].encode('latin-1'))
         azs = s1*100 + s2*10 + s3 + s4/10
         els = s6*100 + s7*10 + s8 + s9/10
	 # Since the controller sends the status based on 0 degrees = 360
         # remove the 360 here
         azs = azs - 360
         els = els - 360
         print ("Rotator stopped at %3d " %(azs)+ "Degrees Azimuth and %3d " %(els) + "Degrees Elevation")
         print ("Azimuth multiplier is %3d "%(s5)+ "  Elevation Multiplier is %3d "%(s10))
		 
	
   elif az == 999:
      # Build the status command word.
      out = chr(87)+zero5+zero5+chr(31)+chr(32)
      x = ser.write(out)
      # Wait for answer from controller
      sleep (0.75)

      data = ser.read(9999)
      #/dev/print len(data)
      # once all 12 characters are received, decode location.
      if len(data) >= 12:
         s1 = ord(data[1].encode('latin-1'))
         s2 = ord(data[2].encode('latin-1'))
         s3 = ord(data[3].encode('latin-1'))
         s4 = ord(data[4].encode('latin-1'))
         s5 = ord(data[5].encode('latin-1'))
         s6 = ord(data[6].encode('latin-1'))
         s7 = ord(data[7].encode('latin-1'))
         s8 = ord(data[8].encode('latin-1'))
         s9 = ord(data[9].encode('latin-1'))
         s10 = ord(data[10].encode('latin-1'))
         azs = s1*100 + s2*10 + s3 + s4/10
         els = s6*100 + s7*10 + s8 + s9/10
         # Since the controller sends the status based on 0 degrees = 360
         # remove the 360 here
         #print (s1,s2,s3,s4,s5,s6,s7,s8,s9,s10)
         azs = azs - 360
         els = els - 360
         print ("Rotator currently at %3d " %(azs)+ "Degrees Azimuth and %3d " %(els) + "Degrees Elevation")
         print ("Azimuth multiplier is %3d "%(s5)+ "  Elevation Multiplier is %3d "%(s10))

         
   elif az == 987:
      # Program is ending so escape the loop.
      loop = 0

   else:    # Input the desired Elevation. Send command to rotator controller to move rotator
            # to the desired azimuth and elevation.
            
            #test to see if azimuth is in the range of 0 to 360 Degrees
      if (az >= 0 and az < 361):
         loop1 = 0
         # Now it is time to get the Elevation 
         while loop1 == 0:
           input_variable = input("Enter Elevation: ")
           el = int(input_variable)
           # Test to see if elevation is in the range of 0 to 180 Degrees
           if (el >= 0 and el < 180):
              loop1 = 1
              #Convert Azimuth and Elevation to number required by controller
              az = az + 360
              el = el + 360
              
              az = az * multi
              el = el * multi

              azm = str(az)
              elm = str(el)
              if len(azm) == 3:
                 azm = "0" + azm
              if len(elm) == 3:
                 elm = "0" + elm
  
              # Build message to be sent to controller. Note that chr(249) indicates
              # to the controller to set the azimuth and elevation without moving the rotor
              
              out = chr(87) + azm + chr(multi)+elm + chr(multi)+chr(249)+chr(32)

              #Send message to Controller
              x = ser.write(out)
              # Wait for answer from controller
              sleep (0.75)

              data = ser.read(9999)
	      # once all 12 characters are received, decode location.
              if len(data) >= 12:
               s1 = ord(data[1].encode('latin-1'))
               s2 = ord(data[2].encode('latin-1'))
               s3 = ord(data[3].encode('latin-1'))
               s4 = ord(data[4].encode('latin-1'))
               s5 = ord(data[5].encode('latin-1'))
               s6 = ord(data[6].encode('latin-1'))
               s7 = ord(data[7].encode('latin-1'))
               s8 = ord(data[8].encode('latin-1'))
               s9 = ord(data[9].encode('latin-1'))
               s10 = ord(data[10].encode('latin-1'))
               azs = s1*100 + s2*10 + s3 + s4/10
               els = s6*100 + s7*10 + s8 + s9/10
               # Since the controller sends the status based on 0 degrees = 360
               # remove the 360 here
               azs = azs - 360
               els = els - 360
               print ("Rotator started at %3d " %(azs)+ "Degrees Azimuth and %3d " %(els) + "Degrees Elevation")
               print ("Azimuth multiplier is %3d "%(s5)+ "  Elevation Multiplier is %3d "%(s10))
		 
           else:   
              print ("Invalid Elevation")
      else:   
         print ("Invalid Azimuth")
              		
ser.close()
