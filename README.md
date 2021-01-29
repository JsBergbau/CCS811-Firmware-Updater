# Update firmware of CCS811 air quality sensor with Python

## Description 

A python script to update CCS811 airquality sensor firmware.

Sofar I've found no firmware flasher for Linux. Only flasher for an arduino or ESP. So I wrote a CCS811 firmware update program utility for Python3.

## Firmware download for CCS811 sensor

Firmware versions can be found here https://github.com/maarten-pennings/CCS811/tree/master/examples/ccs811flash and from manufacturers repository which is
basically a fork of the first one https://github.com/sciosense/CCS811_driver/tree/master/examples/ccs811flash

## Prerequisites for CCS811 firmware update

Smbus library for Python needs to be installed. On Raspberry PI this is done via `sudo apt install python3-smbus`

## Usage of CCS811 firmware updater

```
./ccs811Firmwareupdater.py --help
usage: ccs811Firmwareupdater.py [-h] --address 0x5A or 0x5B --firmware-file
                                FIRMWARE_FILE [--busnumber BUSNUMBER]

optional arguments:
  -h, --help            show this help message and exit
  --address 0x5A or 0x5B, -a 0x5A or 0x5B
                        Set the CCS811 address in hex format, 0x5A or 0x5B
  --firmware-file FIRMWARE_FILE, -f FIRMWARE_FILE
                        Set firmware file
  --busnumber BUSNUMBER, -b BUSNUMBER
                        Set busnumber, usally 1
```

## Advantages of firmware upgrade to version 2.0.1

Warning: NTC temperature correction is not available any more with firmware 2.x
Warning: Disabling automatic baseline calibration or adjusting interval of automatic baseline calibration between every hour and every 1023 hours is also not available anymore.

Firmware version 1.1.0 had a maximum range of 8194 ppm eCO2 and 1187 ppb TVOC. Both values correlated somehow. With firmware version 2.0.1 both values go to 64000 ppb for TVOC and 64000 for eCO2
according to datasheet. However in my tests with a permanent marker TVOC was maximum at 29206 ppb whereas eCO2 bounced between 16752 ppm and 27613 ppm. Still this is a massive increase in dynamic range.
So an update is recommended.

Upgrading to version 2.0.1 is recommended. For difference to 2.0.0 see https://github.com/maarten-pennings/CCS811/issues/8#issuecomment-580410288

## Additional information 

Most devices from China ship with firmware version 1.1.0. There is currently no binary available with this version, see https://github.com/maarten-pennings/CCS811/issues/53 If you find, please tell via issue.

You have to store a new calibration baseline after upgrade.

After upgrade my sensor worked fine. Then after powering down and enabling it again, it wasn't detected at all anymore. Then I connected all lines except wake-pin.
After a few seconds I also connected wake-pin and after that sensor worked again as expected.

## No brick danger

Since this device uses a bootloader which isn't touched there is almost no danger to brick the device, see https://github.com/maarten-pennings/CCS811/tree/master/examples/ccs811flash#a-brick
