#!/usr/bin/python3

import os
import smbus
import time
import argparse
import re

#On Rasbperry PI please install smbus via sudo apt install python3-smbus

CCS811_HW_ID = 0x20
ccs811StatusRegister = 0x00
ccs811AppRegister = 0xF2
ccs811VerifyRegister = 0xF3

ccs811ResetRegister = 0xFF
resetCode = [0x11,0xE5,0x72,0x8A]

ccs811EraseRegister = 0xF1
eraseCode = [0xE7,0xA7,0xE6,0x09]


def address_verifier(arg_value, pat=re.compile(r"0x5A|0x5B",re.IGNORECASE)):
	if not pat.match(arg_value):
		raise argparse.ArgumentTypeError
	return arg_value


parser=argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument("--address","-a", help="Set the CCS811 address in hex format, 0x5A or 0x5B", required=True, type=address_verifier, metavar="0x5A or 0x5B")
parser.add_argument("--firmware-file","-f",help="Set firmware file", required=True)
parser.add_argument("--busnumber","-b",help="Set busnumber, usally 1",type=int, default=1)

args=parser.parse_args()

ccs811Address  =  int(args.address,16)
busNum = args.busnumber
i2cInterface = smbus.SMBus(busNum)
print("Using CCS811 address: ", ccs811Address)

filename = args.firmware_file

filesize = os.path.getsize(filename)
if filesize % 8 != 0:
	print("Error firmware file must be multiple of 8 Bytes.")
	exit(1)

read = i2cInterface.read_byte_data(ccs811Address, CCS811_HW_ID) #must be 0x81 resp 129 
if read != 0x81:
	print("Error no CCS811 detected")
	exit(1)

print("Warning this program will flash your CCS811 with file ", filename)

for i in range (10, 0, -1):
	print(i," seconds left before flashing CCS811, cancel with CTRL + C")
	time.sleep(1)

#reset sensor	
i2cInterface.write_i2c_block_data(ccs811Address,ccs811ResetRegister,resetCode)	
time.sleep(1) #sleep is important here, give sensor time to come up again

#erase Firmware
i2cInterface.write_i2c_block_data(ccs811Address,ccs811EraseRegister,eraseCode)	
time.sleep(1) #Minimum wait time is 300ms
print("Flashing")
with open(filename,"rb") as f:
	while True:
		byteblock = f.read(8)
		if len(byteblock) != 0:
			#print(byteblock)
			print(".",end="",flush=True)
			i2cInterface.write_i2c_block_data(ccs811Address,ccs811AppRegister,list(byteblock))
			time.sleep(0.05)
		else:
			print("")
			break

#verify if data was transmitted successfully
i2cInterface.write_i2c_block_data(ccs811Address, ccs811VerifyRegister,[])
time.sleep(0.5)
i2cInterface.write_i2c_block_data(ccs811Address, ccs811StatusRegister,[]) #empty write before reading register. Normally not needed, but done because of important operation
status = i2cInterface.read_byte_data(ccs811Address,ccs811StatusRegister)
if (status & 0x30) == 0x30:
	print("Firmwareupdate with file", filename, "successful")
else:
	print("Firmwareupdate with file", filename, "FAILED")

print("When changing firmware version you have to re-calibrate your sensor and store a new baseline!")

print("If sensor isn't found anymore after power outage, power it without connecting wake-pin for about 30 seconds.")
print("Then it should work flawlessly again.")