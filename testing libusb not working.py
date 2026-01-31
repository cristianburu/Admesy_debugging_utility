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
        measure = admesy_instrument.query(":MEASure:Yxy\n")
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
    
    ##############################
    # READ FROM INTERNAL MEMORY
    ##############################

    print ("                     " + Back.RED + "\033[1m Internal Memory Values \033[0m")
    print ("--------------------------------------------------------------------")

    # Read Auto-range from internal memory
    autorange_returned_internal_mem = int(admesy_instrument.query(":SENSe:SP:AUTORANGE?")[0])
    if autorange_returned_internal_mem:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     Internal mem.  ON")
    else:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     Internal mem.  OFF")

    # Read Int. time from internal memory
    int_time_returned_internal_mem = int(admesy_instrument.query(":SENSe:INT?")[0])
    print(Back.RED + "\033[1mInt. time:\033[0m" + Style.RESET_ALL + f"      Internal mem.  {int_time_returned_internal_mem:d} μSeconds ({(int_time_returned_internal_mem/1000000):0.2f} seconds)")
    
    # Read Average from internal memory
    avg_returned_internal_mem = int(admesy_instrument.query(":SENSe:SP:AVERAGE?")[0])
    print (Back.RED + "\033[1mAverage:\033[0m" + Style.RESET_ALL + f"        Internal mem.  {avg_returned_internal_mem}")
    
    # Read the current interpolation method from internal memory
    interp_method_returned = int (admesy_instrument.query(":SENSe:INTERPOL?")[0])
    if interp_method_returned == 0:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Internal mem.  linear")
    elif interp_method_returned == 1:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Internal mem.  cosine")
    elif interp_method_returned == 2:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Internal mem.  cubic")
    elif interp_method_returned == 3:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Internal mem.  Catmull-Rom")
    elif interp_method_returned == 4:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Internal mem.  Hermite")
    else:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" Internal mem.  ERROR!!!")

    # Read Calibration matrix SP SBW (off/user) from internal memory - does not seem to work
    # calib_matrix_returned_internal_mem = int(admesy_instrument.query(":SENSe:SP:SBW?")[0])
    # if calib_matrix_returned_internal_mem:
    #     print (Back.RED + "\033[1mCalib. matrix:\033[0m" + Style.RESET_ALL + f"  EEPROM         user")
    # else:
    #     print (Back.RED + "\033[1mCalib. matrix:\033[0m" + Style.RESET_ALL + f"  EEPROM         off")

    ##############################
    # READ FROM EEPROM
    ##############################
    
    print ("--------------------------------------------------------------------")
    print ("                         " + Back.RED + "\033[1m EEPROM Values \033[0m")
    print ("--------------------------------------------------------------------")

    # Read Auto-range from EEPROM
    autorange_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:AUTORANGE?")[0])
    if autorange_returned_EEPROM:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     EEPROM         ON")
    else:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     EEPROM         OFF")
    
    # Read Int. time from EEPROM
    int_time_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:SPINT?")[0])
    print(Back.RED + "\033[1mInt. time:\033[0m" + Style.RESET_ALL + f"      EEPROM         {int_time_returned_EEPROM:d} μSeconds ({(int_time_returned_EEPROM/1000000):0.2f} seconds)")
    
    # Read Average from EEPROM 
    avg_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:SPAVG?")[0])
    print (Back.RED + "\033[1mAverage:\033[0m" + Style.RESET_ALL + f"        EEPROM         {avg_returned_EEPROM}")

    # Read Adj.min from EEPROM
    adjmin_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:ADJMIN?")[0])
    if autorange_returned_internal_mem:
        print (Back.RED + "\033[1mAdj.min:\033[0m" + Style.RESET_ALL + f"        EEPROM         {adjmin_returned_EEPROM}")
    else:
        print (Back.RED + "\033[1mAdj.min:\033[0m" + Style.RESET_ALL + f"        EEPROM         {adjmin_returned_EEPROM} (but not used)")
    
    # Read Frequency from EEPROM
    freq_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:FREQ?")[0])
    print(Back.RED + "\033[1mFrequency:\033[0m" + Style.RESET_ALL + f"      EEPROM         {freq_returned_EEPROM:d} Hz")

    # Read Max. Int. time from EEPROM
    max_int_time_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:AUTO:MAXINT?")[0])
    print(Back.RED + "\033[1mMax. Int. time:\033[0m" + Style.RESET_ALL + f" EEPROM         {max_int_time_returned_EEPROM:d} μSeconds ({(max_int_time_returned_EEPROM/1000000):0.2f} seconds)")

    # Read the current resolution from EEPROM
    resolution_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:RES?")[0])
    if resolution_returned_EEPROM == 0:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     EEPROM         0.5nm")
    elif resolution_returned_EEPROM == 1:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     EEPROM         1nm")
    elif resolution_returned_EEPROM == 2:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     EEPROM         2.5nm")
    elif resolution_returned_EEPROM == 3:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     EEPROM         5nm")
    elif resolution_returned_EEPROM == 4:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     EEPROM         10nm")
    else:
        print (Back.RED + "\033[1mResolution:\033[0m" + Style.RESET_ALL + f"     EEPROM         ERROR!!!")
    
    # Read the current interpolation method from EEPROM
    interp_method_returned = int (admesy_instrument.query(":EEPROM:CONFigure:INTERPOL?")[0])
    if interp_method_returned == 0:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" EEPROM         linear")
    elif interp_method_returned == 1:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" EEPROM         cosine")
    elif interp_method_returned == 2:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" EEPROM         cubic")
    elif interp_method_returned == 3:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" EEPROM         Catmull-Rom")
    elif interp_method_returned == 4:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" EEPROM         Hermite")
    else:
        print (Back.RED + "\033[1mInterp. method:\033[0m" + Style.RESET_ALL + f" EEPROM         ERROR!!!")
    
    # Read Absolute Calibration Mode (factory/user) from EEPROM
    abs_calib_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:USERABS?")[0])
    if abs_calib_returned_EEPROM:
        print (Back.RED + "\033[1mAbs. cal. mode:\033[0m" + Style.RESET_ALL + f" EEPROM         user")
    else:
        print (Back.RED + "\033[1mAbs. cal. mode:\033[0m" + Style.RESET_ALL + f" EEPROM         factory")

    # Read Calibration matrix SP SBW (off/user) from EEPROM
    calib_matrix_returned_EEPROM = int(admesy_instrument.query(":EEPROM:CONFigure:SPSBW?")[0])
    if calib_matrix_returned_EEPROM:
        print (Back.RED + "\033[1mCalib. matrix:\033[0m" + Style.RESET_ALL + f"  EEPROM         user")
    else:
        print (Back.RED + "\033[1mCalib. matrix:\033[0m" + Style.RESET_ALL + f"  EEPROM         off")

    # Read Std. Illuminant from EEPROM
    std_illuminant_returned_EEPPROM = admesy_instrument.query(":EEPROM:CONFigure:WHITE?")[0].strip()
    print (Back.RED + "\033[1mSt. Illuminant:\033[0m" + Style.RESET_ALL + f" EEPROM         {std_illuminant_returned_EEPPROM}")

    print ("--------------------------------------------------------------------")
    print("")
    whatever = input("Press any key to continue...")
    print("")

def read_parameters_pcm2x():
    print("")
    print ("--------------------------------------------------------------------")
    print ("               " + Back.RED + "\033[1m CURRENT PARAMETERS USED - EXTENDED \033[0m")
    print ("--------------------------------------------------------------------")
    
    ##############################
    # READ FROM INTERNAL MEMORY
    ##############################

    print ("                     " + Back.RED + "\033[1m Internal Memory Values \033[0m")
    print ("--------------------------------------------------------------------")

    # Read Auto-range from internal memory
    autorange_returned_internal_mem = int(admesy_instrument.query(":SENSe:AUTORANGE?")[0])
    if autorange_returned_internal_mem:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     Internal mem.  ON")
    else:
        print (Back.RED + "\033[1mAuto-range:\033[0m" + Style.RESET_ALL + f"     Internal mem.  OFF")

    # Read Int. time from internal memory
    int_time_returned_internal_mem = int(admesy_instrument.query(":SENSe:INT?")[0])
    print(Back.RED + "\033[1mInt. time:\033[0m" + Style.RESET_ALL + f"      Internal mem.  {int_time_returned_internal_mem:d} μSeconds ({(int_time_returned_internal_mem/1000000):0.2f} seconds)")
    
    # Read Average from internal memory
    avg_returned_internal_mem = int(admesy_instrument.query(":SENSe:AVERAGE?")[0])
    print (Back.RED + "\033[1mAverage:\033[0m" + Style.RESET_ALL + f"        Internal mem.  {avg_returned_internal_mem}")
    
    print ("--------------------------------------------------------------------")
    print("")
    whatever = input("Press any key to continue...")
    print("")


def set_autorange_internal_mem():
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
def set_int_time_internal_mem():
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
def set_average_internal_mem():
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
def set_interpol_method_internal_mem():
    set_interpol_method_to = "UNDEFINED"
    print("")
    while set_interpol_method_to not in ["linear", "cosine", "cubic", "Catmull-Rom", "Hermite"]:
        try:
            set_interpol_method_to = str (input("Set Interpolation Method (linear/cosine/cubic/Catmull-Rom/Hermite):"))
            if set_interpol_method_to not in ["linear", "cosine", "cubic", "Catmull-Rom", "Hermite"]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_interpol_method_to == "linear":
        admesy_instrument.write(":SENSe:INTERPOL 0")
    elif set_interpol_method_to == "cosine":
        admesy_instrument.write(":SENSe:INTERPOL 1")
    elif set_interpol_method_to == "cubic":
        admesy_instrument.write(":SENSe:INTERPOL 2")
    elif set_interpol_method_to == "Catmull-Rom":
        admesy_instrument.write(":SENSe:INTERPOL 3")
    elif set_interpol_method_to == "Hermite":
        admesy_instrument.write(":SENSe:INTERPOL 4")

    print("")
    print("Interpolation method set!")
    print("")
def set_resolution_internal_mem():
    set_resolution_to = -1.5
    print("")
    while set_resolution_to not in [0.5, 1, 2.5, 5, 10]:
        try:
            set_resolution_to = float (input("Set Resolution (0.5/1/2/5/10) nm:"))
            if set_resolution_to not in [0.5, 1, 2.5, 5, 10]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_resolution_to == 0.5:
        admesy_instrument.write(":SENSe:RESolution 0")
    elif set_resolution_to == 1:
        admesy_instrument.write(":SENSe:RESolution 1")
    elif set_resolution_to == 2.5:
        admesy_instrument.write(":SENSe:RESolution 2")
    elif set_resolution_to == 5:
        admesy_instrument.write(":SENSe:RESolution 3")
    elif set_resolution_to == 10:
        admesy_instrument.write(":SENSe:RESolution 4")
def set_cal_matrix_internal_mem():
    set_cal_matrix_to = "UNDEFINED"
    print("")
    while set_cal_matrix_to not in ["user", "off"]:
        try:
            set_cal_matrix_to = str (input("Set Calibration Matrix (off/user):"))
            if set_cal_matrix_to not in ["user", "off"]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_cal_matrix_to == "off":
        admesy_instrument.write(":SENSe:SP:SBW 0")
    else:
        admesy_instrument.write(":SENSe:SP:SBW 1")

def set_autorange_EEPROM():
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
        admesy_instrument.write(":EEPROM:CONFigure:AUTORANGE 1")
    else:
        admesy_instrument.write(":EEPROM:CONFigure:AUTORANGE 0")
    print("")
    print("Auto-range set!")
    print("")
def set_int_time_EEPROM():
    set_int_time_to = 0
    print("")
    while (set_int_time_to < 2500 or set_int_time_to > 20000000):
        try:
            set_int_time_to = int ((input("Set integration time in μSeconds (2500-20000000):")))
            if (set_int_time_to < 2500 or set_int_time_to > 20000000):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":EEPROM:CONFigure:SPINT " + str(set_int_time_to))
    print("")
    print("Integration time set!")
    print("")
def set_average_EEPROM():
    set_average_to = 0
    print("")
    while (set_average_to < 1 or set_average_to > 200):
        try:
            set_average_to = int ((input("Set average (1-200):")))
            if (set_average_to < 1 or set_average_to > 200):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":EEPROM:CONFigure:SPAVG " + str(set_average_to))
    print("")
    print("Average set!")
    print("")
def set_adj_min_EEPROM():
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
def set_frequency_EEPROM():
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
def set_interpol_method_EEPROM():
    set_interpol_method_to = "UNDEFINED"
    print("")
    while set_interpol_method_to not in ["linear", "cosine", "cubic", "Catmull-Rom", "Hermite"]:
        try:
            set_interpol_method_to = str (input("Set Interpolation Method (linear/cosine/cubic/Catmull-Rom/Hermite):"))
            if set_interpol_method_to not in ["linear", "cosine", "cubic", "Catmull-Rom", "Hermite"]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_interpol_method_to == "linear":
        admesy_instrument.write(":EEPROM:CONFigure:INTERPOL 0")
    elif set_interpol_method_to == "cosine":
        admesy_instrument.write(":EEPROM:CONFigure:INTERPOL 1")
    elif set_interpol_method_to == "cubic":
        admesy_instrument.write(":EEPROM:CONFigure:INTERPOL 2")
    elif set_interpol_method_to == "Catmull-Rom":
        admesy_instrument.write(":EEPROM:CONFigure:INTERPOL 3")
    elif set_interpol_method_to == "Hermite":
        admesy_instrument.write(":EEPROM:CONFigure:INTERPOL 4")

    print("")
    print("Interpolation method set!")
    print("")
def set_max_int_time_EEPROM():
    set_max_int_time_to = 0
    print("")
    while (set_max_int_time_to < 2500 or set_max_int_time_to > 20000000):
        try:
            set_max_int_time_to = int ((input("Set Maximum integration time in μSeconds (2500-20000000):")))
            if (set_max_int_time_to < 2500 or set_max_int_time_to > 20000000):
                print("Please enter a valid value.")
        except ValueError:
            print("Please enter a valid value.")
    admesy_instrument.write(":EEPROM:CONFigure:AUTO:MAXINT " + str(set_max_int_time_to))
    print("")
    print("Maximum integration time set!")
    print("")
def set_resolution_EEPROM():
    set_resolution_to = -1.5
    print("")
    while set_resolution_to not in [0.5, 1, 2.5, 5, 10]:
        try:
            set_resolution_to = float (input("Set Resolution (0.5/1/2/5/10) nm:"))
            if set_resolution_to not in [0.5, 1, 2.5, 5, 10]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_resolution_to == 0.5:
        admesy_instrument.write(":EEPROM:CONFigure:RES 0")
    elif set_resolution_to == 1:
        admesy_instrument.write(":EEPROM:CONFigure:RES 1")
    elif set_resolution_to == 2.5:
        admesy_instrument.write(":EEPROM:CONFigure:RES 2")
    elif set_resolution_to == 5:
        admesy_instrument.write(":EEPROM:CONFigure:RES 3")
    elif set_resolution_to == 10:
        admesy_instrument.write(":EEPROM:CONFigure:RES 4")
def set_abs_cal_method_EEPROM():
    set_abs_cal_method_to = "UNDEFINED"
    print("")
    while set_abs_cal_method_to not in ["user", "factory"]:
        try:
            set_abs_cal_method_to = str (input("Set Absolute Calibration Method (factory/user):"))
            if set_abs_cal_method_to not in ["user", "factory"]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_abs_cal_method_to == "factory":
        admesy_instrument.write(":EEPROM:CONFigure:USERABS 0")
    else:
        admesy_instrument.write(":EEPROM:CONFigure:USERABS 1")
def set_cal_matrix_EEPROM():
    set_cal_matrix_to = "UNDEFINED"
    print("")
    while set_cal_matrix_to not in ["user", "off"]:
        try:
            set_cal_matrix_to = str (input("Set Calibration Matrix (off/user):"))
            if set_cal_matrix_to not in ["user", "off"]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    if set_cal_matrix_to == "off":
        admesy_instrument.write(":EEPROM:CONFigure:SPSBW 0")
    else:
        admesy_instrument.write(":EEPROM:CONFigure:SPSBW 1")
def set_std_illuminant_EEPROM():
    set_std_illuminant_to = "UNDEFINED"
    print("")
    while set_std_illuminant_to not in ["D65", "C", "D50", "D55", "D75", "FL1", "FL2", "FL3", "FL4", "FL5", "FL6", "FL7", "FL8", "FL9", "FL10", "FL11", "FL12", "HP1", "HP2", "HP3", "HP4", "HP5", "E", "A"]:
        try:
            set_std_illuminant_to = str (input("Set Std. Illuminant:"))
            if set_std_illuminant_to not in ["D65", "C", "D50", "D55", "D75", "FL1", "FL2", "FL3", "FL4", "FL5", "FL6", "FL7", "FL8", "FL9", "FL10", "FL11", "FL12", "HP1", "HP2", "HP3", "HP4", "HP5", "E", "A"]:
                print("Please enter a valid option.")
        except ValueError:
            print("Please enter a valid option.")
    admesy_instrument.write(":EEPROM:CONFigure:WHITE " + set_std_illuminant_to )
    

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
    print(f"Timeout of the device set to {set_timeout_to} seconds!")
    print("")
def write_startup_values():
    admesy_instrument.write(":EEPROM:STARTUP:WRITE")
    print("")
    print("Startup values updated!")
    print("")
def read_startup_values():
    admesy_instrument.write(":EEPROM:STARTUP:READ")
    print("")
    print("Startup values copied from EEPROM to internal memory!")
    print("")

init(autoreset=True) # colorama autoreset
print_hello_msg() # Initial greeting msg

# Initial scan for device. If device is not found app exits.
find_instruments = AdmesyFindInstruments('@py',0) # Scan for libusbtmc device
instrument_list = find_instruments.getList()
print (f"Lista py este {instrument_list}")
if not instrument_list:
    find_instruments = AdmesyFindInstruments('',0) # Scan for NI-VISA device
    instrument_list = find_instruments.getList()
    print (f"Lista NI-VISA este {instrument_list}")
    if not instrument_list:
        print(Back.RED + "\033[1mNo Admesy USB device found!\033[0m")
        print("")
        print (Back.RED + "\033[1mBye!\033[0m")
        print("")
        exit()


print (f"Prima pozitie din instrument_list este {instrument_list[0]}")

# admesy_instrument = AdmesyInstrument(instrument_list[0]) # Instantiate the device found

# admesy_instrument.timeout(5000) # Timeout is set in miliseconds. Set timeout of device to 60 seconds

# read_parameters_pcm2x()




# print_formatted_device_info() # Show initial info on device

# # admesy_instrument.write(":EEPROM:STARTUP:READ") # Copies startup values from EEPROM to internal memory

# while True:
    
#     # List commands
#     print ("------------------------------")
#     print (Back.RED + "\033[1mCommand List\033[0m")
#     print ("------------------------------")
#     print ("0. Measure Yxy")
#     print ("1. Read extended parameters")
#     print ("2. Internal Memory / Set Auto-range")
#     print ("3. Internal Memory / Set Int. time")
#     print ("4. Internal Memory / Set Average")
#     print ("5. Internal Memory / Set interpolation method")   
#     print ("6. EEPROM / Set Auto-range") 
#     print ("7. EEPROM / Set Int. time") 
#     print ("8. EEPROM / Set Average")
#     print ("9. EEPROM / Set Adj. min")
#     print ("10.EEPROM / Set Frequency")
#     print ("11.EEPROM / Set Maximum Int. time")
#     print ("12.EEPROM / Set Resolution")
#     print ("13.EEPROM / Set interpolation method")
#     print ("14.EEPROM / Set Absolute calibration method")
#     print ("15.EEPROM / Set Calibration matrix")
#     print ("16.EEPROM / Set Std. Illuminant")
#     print ("17.Set timeout of device")
#     print ("18.Write EEPROM values to startup settings")
#     print ("19.Copy startup values from EEPROM to internal memory")
#     print ("20.Internal Memory / Set Resolution (???)")
#     print ("21.Internal Memory / Set Calibration matrix (???)")
#     print ("22.Exit")
#     print ("------------------------------")

#     # Command input
#     command = -1
#     while (command <0 or command>22):
#         try:
#             command = int(input("Waiting for command (0-22):"))
#             if (command <0 or command>22):
#                 print("Please enter a valid command.")
#         except ValueError:
#             print("Please enter a valid command.")

#     # Branch execution
#     if command == 0:
#         measure_Yxy()
#     elif command == 1:
#         read_parameters_extended()
#     elif command == 2:
#         set_autorange_internal_mem()
#     elif command == 3:
#         set_int_time_internal_mem()
#     elif command == 4:
#         set_average_internal_mem()
#     elif command == 5:
#         set_interpol_method_internal_mem()
#     elif command == 6:
#         set_autorange_EEPROM()
#     elif command == 7:
#         set_int_time_EEPROM()
#     elif command == 8:
#         set_average_EEPROM()
#     elif command == 9:
#         set_adj_min_EEPROM()
#     elif command == 10:
#         set_frequency_EEPROM()
#     elif command == 11:
#         set_max_int_time_EEPROM()
#     elif command == 12:
#         set_resolution_EEPROM()
#     elif command == 13:
#         set_interpol_method_EEPROM()
#     elif command == 14:
#         set_abs_cal_method_EEPROM()
#     elif command == 15:
#         set_cal_matrix_EEPROM()
#     elif command == 16:
#         set_std_illuminant_EEPROM()
#     elif command == 17:
#         set_timeout()
#     elif command == 18:
#         write_startup_values()
#     elif command == 19:
#         read_startup_values()
#     elif command == 20:
#         set_resolution_internal_mem()
#     elif command == 21:
#         set_cal_matrix_internal_mem()
#     else:
#         print("")
#         print (Back.RED + "\033[1mBye!\033[0m")
#         print("")
#         exit()













    



    
















