# requires Admesy_Instrument, pyvisa, time, colorama, sys

import time
from colorama import Fore, Back, init, Style
from sys import exit
from Admesy_Instrument.FindInstruments import AdmesyFindInstruments
from Admesy_Instrument.Base import AdmesyBase
from Admesy_Instrument.Instrument import AdmesyInstrument


def print_formatted_Yxy_measurement(_Yxy_list):
    meas_Y = float (_Yxy_list[0])
    meas_x = float (_Yxy_list[1])
    meas_y = float (_Yxy_list[2])
    meas_clip = bool (int (_Yxy_list[3]))
    meas_noise = bool (int (_Yxy_list[4]))
    if meas_clip:
        print ("--------------------------------------------------------------------")
        print (Back.RED + "\033[1mIncorrect reading. Sensor overexposed!\033[0m")
        print ("--------------------------------------------------------------------")
    elif meas_noise:
        print ("--------------------------------------------------------------------")
        print (Back.RED + "\033[1mIncorrect reading. Too much noise!\033[0m")
        print ("--------------------------------------------------------------------")
    else:
        print ("--------------------------------------------------------------------")
        print (Back.RED + "\033[1mY:\033[0m" + Style.RESET_ALL + f"{meas_Y:0.3f}   " + Back.RED + "\033[1mx:\033[0m" + Style.RESET_ALL + f"{meas_x:0.6f}   " + Back.RED + "\033[1my:\033[0m" + Style.RESET_ALL + f"{meas_y:0.6f}   " + Back.RED + "\033[1mClipping:\033[0m" + Style.RESET_ALL + f"{meas_clip}   " + Back.RED + "\033[1mNoise:\033[0m" + Style.RESET_ALL + f"{meas_noise}")
        print ("--------------------------------------------------------------------")
def measure_Yxy():
    print("")
    print("Measuring... Wait...")
    print("")
    tic = time.perf_counter()
    try:
        measure = admesy_instrument.query(":MEASure:Yxy")
    except:
        print ("Timeout exceeded! You will probably want to change it!")
        return
    toc = time.perf_counter()
    print(Back.RED + "\033[1mMeasured in:\033[0m" + Style.RESET_ALL + f" {toc - tic:0.2f} seconds")
    print_formatted_Yxy_measurement(measure)
    print(Back.RED + "\033[1mParameters used in this measurement:\033[0m" + Style.RESET_ALL)

    # Read Auto-range
    autorange_returned = int(admesy_instrument.query(":SENSe:SP:AUTORANGE?")[0])
    if autorange_returned:
        print (Back.RED + "\033[1mAuto-range :\033[0m" + Style.RESET_ALL + f" ON")
    else:
        print (Back.RED + "\033[1mAuto-range :\033[0m" + Style.RESET_ALL + f" OFF")

    # Read Adj.min
    adjmin_returned = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:ADJMIN?")[0])
    if autorange_returned:
        print (Back.RED + "\033[1mAdj.min:\033[0m" + Style.RESET_ALL + f"     {adjmin_returned}")
    else:
        print (Back.RED + "\033[1mAdj.min:\033[0m" + Style.RESET_ALL + f"     {adjmin_returned} (but not used)")

    # Read Int. time
    int_time_returned = int(admesy_instrument.query(":SENSe:INT?")[0])
    print(Back.RED + "\033[1mInt. time :\033[0m" + Style.RESET_ALL + f"  {int_time_returned:d} μSeconds ({(int_time_returned/1000000):0.2f} seconds)")

    # Read Average
    avg_returned = int(admesy_instrument.query(":SENSe:SP:AVERAGE?")[0])
    print (Back.RED + "\033[1mAverage :\033[0m" + Style.RESET_ALL + f"    {avg_returned}")
    print ("--------------------------------------------------------------------")
    print("")
def print_formatted_device_info():   
    print (" ")     
    print (Back.RED + "\033[1mAdmesy Device Found\033[0m")
    print ("--------------------------------------")
    print (Back.RED + "\033[1mDevice ID:\033[0m" + Style.RESET_ALL + "   " + (admesy_instrument.query(":*IDN?"))[0])
    print (Back.RED + "\033[1mFirmware:\033[0m" + Style.RESET_ALL + "    " + (admesy_instrument.query(":SYSTem:VERSion?"))[0])
    print (Back.RED + "\033[1mFw. Date:\033[0m" + Style.RESET_ALL + "    " + (admesy_instrument.query(":*FWD?"))[0].strip("Firmware date : "))
    print (" ")     
    print (" ")     
def print_hello_msg():
    print (" ")   
    print (Back.RED + "\033[1mHello!\033[0m")
    print (" ")     
def read_parameters_extended():
    print("")
    print ("--------------------------------------------------------------------")
    print ("               " + Back.RED + "\033[1m CURRENT PARAMETERS USED - EXTENDED \033[0m")
    print ("--------------------------------------------------------------------")
    
    # Read Auto-range
    autorange_returned = int(admesy_instrument.query(":SENSe:SP:AUTORANGE?")[0])
    if autorange_returned:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     ON")
    else:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     OFF")
    
    # Read Adj.min
    adjmin_returned = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:ADJMIN?")[0])
    if autorange_returned:
        print (Back.RED + "\033[1mAdj.min:\033[0m" + Style.RESET_ALL + f"        {adjmin_returned}")
    else:
        print (Back.RED + "\033[1mAdj.min:\033[0m" + Style.RESET_ALL + f"        {adjmin_returned} (but not used)")
    
    # Read Average
    avg_returned = int(admesy_instrument.query(":SENSe:SP:AVERAGE?")[0])
    print (Back.RED + "\033[1mAverage:\033[0m" + Style.RESET_ALL + f"        {avg_returned}")

    # Read Int. time
    int_time_returned = int(admesy_instrument.query(":SENSe:INT?")[0])
    print(Back.RED + "\033[1mInt. time:\033[0m" + Style.RESET_ALL + f"      {int_time_returned:d} μSeconds ({(int_time_returned/1000000):0.2f} seconds)")
    
    # Read Max. Int. time
    max_int_time_returned = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:MAXINT?")[0])
    print(Back.RED + "\033[1mMax. Int. time:\033[0m" + Style.RESET_ALL + f" {max_int_time_returned:d} μSeconds ({(max_int_time_returned/1000000):0.2f} seconds)")

    # Read Frequency
    freq_returned = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:FREQ?")[0])
    print(Back.RED + "\033[1mFrequency:\033[0m" + Style.RESET_ALL + f"      {freq_returned:d} Hz")

    # Read the current interpolation method from volatile memory
    interp_method_returned = int (admesy_instrument.query(":SENSe:INTERPOL?")[0])
    if interp_method_returned == 0:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" linear")
    elif interp_method_returned == 1:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" cosine")
    elif interp_method_returned == 2:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" cubic")
    elif interp_method_returned == 3:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Catmull-Rom")
    elif interp_method_returned == 4:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Hermite")
    else:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" ERROR!!!")

    # Read the current resolution
    resolution_returned = int(admesy_instrument.query(":EEPROM:CONFigure:RES?")[0])
    if resolution_returned == 0:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     0.5nm")
    elif resolution_returned == 1:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     1nm")
    elif resolution_returned == 2:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     2.5nm")
    elif resolution_returned == 3:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     5nm")
    elif resolution_returned == 4:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     10nm")
    else:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f" ERROR!!!")
    
    # Read Calibration matrix SP SBW (off/user)
    calib_matrix_returned = int(admesy_instrument.query(":EEPROM:CONFigure:SPSBW?")[0])
    if calib_matrix_returned:
        print (Back.RED + "\033[1mCalib. matrix:\033[0m" + Style.RESET_ALL + f"  user")
    else:
        print (Back.RED + "\033[1mCalib. matrix:\033[0m" + Style.RESET_ALL + f"  off")

    # Read Absolute Calibration Mode (factory/user)
    abs_calib_returned = int(admesy_instrument.query(":EEPROM:CONFigure:USERABS?")[0])
    if abs_calib_returned:
        print (Back.RED + "\033[1mAbs. cal. mode:\033[0m" + Style.RESET_ALL + f" user")
    else:
        print (Back.RED + "\033[1mAbs. cal. mode:\033[0m" + Style.RESET_ALL + f" factory")

    # Read Std. Illuminant
    std_illuminant_returned = admesy_instrument.query(":EEPROM:CONFigure:WHITE?")[0].strip()
    print (Back.RED + "\033[1mSt. Illuminant:\033[0m" + Style.RESET_ALL + f" {std_illuminant_returned}")

    print ("--------------------------------------------------------------------")
    print("")
def set_autorange():
    set_autorange_to = "UNDEFINED"
    print("")
    while not (set_autorange_to == "ON" or set_autorange_to == "OFF"):
        try:
            set_autorange_to = (input("Set auto-range (ON/OFF):"))
            if not (set_autorange_to == "ON" or set_autorange_to == "OFF"):
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_autorange_to == "ON":
        admesy_instrument.write(":SENSe:SP:AUTORANGE 1")
    else:
        admesy_instrument.write(":SENSe:SP:AUTORANGE 0")
    print("")
    print("Auto-range set!")
    print("")
def set_average():
    set_average_to = 0
    print("")
    while (set_average_to < 1 or set_average_to > 200):
        try:
            set_average_to = int ((input("Set average (1-200):")))
            if (set_average_to < 1 or set_average_to > 200):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":SENSe:SP:AVERAGE " + str(set_average_to))
    print("")
    print("Average set!")
    print("")
def set_int_time():
    set_int_time_to = 0
    print("")
    while (set_int_time_to < 2500 or set_int_time_to > 20000000):
        try:
            set_int_time_to = int ((input("Set integration time in μSeconds (2500-20000000):")))
            if (set_int_time_to < 2500 or set_int_time_to > 20000000):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":SENSe:INT " + str(set_int_time_to))
    print("")
    print("Integration time set!")
    print("")
def set_adj_min():
    set_adj_min_to = 0
    print("")
    while (set_adj_min_to < 1 or set_adj_min_to > 100):
        try:
            set_adj_min_to = int ((input("Set Adj. min (1-100):")))
            if (set_adj_min_to < 1 or set_adj_min_to > 100):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":EEPROM:CONFigure:AUTO:ADJMIN  " + str(set_adj_min_to))
    print("")
    print("Adj. min set!")
    print("")
def set_frequency():
    set_frequency_to = 0
    print("")
    while (set_frequency_to < 1 or set_frequency_to > 255):
        try:
            set_frequency_to = int ((input("Set Frequency in Hz (1-255):")))
            if (set_frequency_to < 1 or set_frequency_to > 255):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":EEPROM:CONFigure:AUTO:FREQ  " + str(set_frequency_to))
    print("")
    print("Frequency set!")
    print("")
def set_timeout():
    set_timeout_to = 0
    print("")
    while (set_timeout_to < 1 or set_timeout_to > 120):
        try:
            set_timeout_to = int ((input("Set Timeout in seconds (1-120):")))
            if (set_timeout_to < 1 or set_timeout_to > 120):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")

    admesy_instrument.timeout(set_timeout_to * 1000)
    print("")
    print(f"Timoeut of the device set to {set_timeout_to} seconds!")
    print("")





init(autoreset=True) # colorama autoreset
print_hello_msg() # Initial greeting msg

# Initial scan for device. If device is not found app exits.
find_instruments = AdmesyFindInstruments('',1) # Scan for NI-VISA device
instrument_list = find_instruments.getList()
if not instrument_list:
    find_instruments = AdmesyFindInstruments('@py',1) # 8Scan for libusbtmc device
    instrument_list = find_instruments.getList()
    print (instrument_list)
    if not instrument_list:
        print(Back.RED + "\033[1mNo Admesy USB device found!\033[0m")
        print("")
        print (Back.RED + "\033[1mBye!\033[0m")
        print("")
        exit()

admesy_instrument = AdmesyInstrument(instrument_list[0]) # Instantiate the device found

admesy_instrument.timeout(60000) # Timeout is set in miliseconds. Set timeout of device to 60 seconds

print_formatted_device_info() # Show initial info on device

while True:
    
    # List commands
    print ("------------------------------")
    print (Back.RED + "\033[1mCommand List\033[0m")
    print ("------------------------------")
    print ("0. Measure Yxy")
    print ("1. Read extended parameters")
    print ("2. Set Auto-range") 
    print ("3. Set Average") 
    print ("4. Set Int. time") 
    print ("5. Set Adj. min") 
    print ("6. Set Frequency")
    print ("7. Set timeout of device")
    print ("8. Exit")
    print ("------------------------------")

    # Command input
    command = -1
    while (command <0 or command>8):
        try:
            command = int(input("Waiting for command (0-8):"))
            if (command <0 or command>8):
                print("Please enter a valid command.")
        except ValueError:
            print("Please enter a valid command.")

    # Branch execution
    if command == 0:
        measure_Yxy()
    elif command == 1:
        read_parameters_extended()
    elif command == 2:
        set_autorange()
    elif command == 3:
        set_average()
    elif command == 4:
        set_int_time()
    elif command == 5:
        set_adj_min()
    elif command == 6:
        set_frequency()
    elif command == 7:
        set_timeout()
    else:
        print("")
        print (Back.RED + "\033[1mBye!\033[0m")
        print("")
        exit()













    



    
















