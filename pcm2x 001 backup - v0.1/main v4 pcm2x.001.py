#
# -------------------------------------------
# Send suggestions at cristian.buru@gmail.com
# -------------------------------------------
#

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

import sys
import ctypes

from time import ctime, sleep



class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        # Set locale to en_US
        en = QtCore.QLocale ("en_US")
        QtCore.QLocale.setDefault(en)

        loadUi ("interface.ui", self)

        # Manual toggle button
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(39, 15, 121, 19))
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_connect.setText(QtCore.QCoreApplication.translate("MainWindow", "CONNECT"))
        self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
        self.pushButton_connect.setCheckable (True)

        
                

        # Disable inteface
        self.disable_interface()

        # Focus change handler
        QApplication.instance().focusChanged.connect(self.handle_focus_changed)

        # Connect/Disconnect Button
        self.pushButton_connect.clicked.connect (self.toggle_connect_disconnect)

        # Reload Parameters Button
        self.pushButton_reload_params.clicked.connect (self.reload_parameters)
        
        # Auto-range parameters input
        self.lineEdit_ar_freq.setValidator (QtGui.QDoubleValidator (0.0, 250.0, 6, notation=QtGui.QDoubleValidator.StandardNotation))
        self.lineEdit_ar_freq.editingFinished.connect (self.colorimeter_write_autorange_params)
        self.lineEdit_ar_adjmin.setValidator (QtGui.QIntValidator(1,30, self))
        self.lineEdit_ar_adjmin.editingFinished.connect (self.colorimeter_write_autorange_params)
        self.lineEdit_ar_frames.setValidator (QtGui.QIntValidator(1,255, self))
        self.lineEdit_ar_frames.editingFinished.connect (self.colorimeter_write_autorange_params)
        self.lineEdit_ar_max_int_time.setValidator (QtGui.QIntValidator(320, 1000000, self))
        self.lineEdit_ar_max_int_time.editingFinished.connect (self.colorimeter_write_autorange_params)
        self.lineEdit_ar_avg.setValidator (QtGui.QIntValidator(1,255, self))
        self.lineEdit_ar_avg.editingFinished.connect (self.colorimeter_write_autorange_params)

        # Core parameters input
        self.comboBox_autorange.currentIndexChanged.connect (self.colorimeter_write_autorange)
        self.lineEdit_int_time.setValidator (QtGui.QIntValidator(320, 1000000, self))
        self.lineEdit_int_time.editingFinished.connect (self.colorimeter_write_int_time)
        self.lineEdit_avg.setValidator (QtGui.QIntValidator(1,255, self))
        self.lineEdit_avg.editingFinished.connect (self.colorimeter_write_average)
        self.comboBox_gain.currentIndexChanged.connect (self.colorimeter_write_gain)
        self.comboBox_sbw.currentIndexChanged.connect (self.colorimeter_write_sbw)
        self.comboBox_automode.currentIndexChanged.connect (self.colorimeter_write_automode)
        self.lineEdit_dut_ar_freq.setValidator (QtGui.QDoubleValidator (0.0, 250.0, 3, notation=QtGui.QDoubleValidator.StandardNotation))
        self.lineEdit_dut_ar_freq.editingFinished.connect (self.colorimeter_write_dut_freq)

        # Other parameters input
        self.lineEdit_fixedmode.setValidator (QtGui.QDoubleValidator (4.0, 1000.0, 3, notation=QtGui.QDoubleValidator.StandardNotation))
        self.lineEdit_fixedmode.editingFinished.connect (self.colorimeter_write_fixedmode_time)
        self.lineEdit_ar_freq_two_values.setValidator (QtGui.QRegExpValidator(QRegExp(r"[0-9.]+,{1}[0-9.]+")))
        self.lineEdit_ar_freq_two_values.editingFinished.connect (self.colorimeter_write_dut_arfreq)
        self.comboBox_shutter.currentIndexChanged.connect (self.colorimeter_write_shutter_state)

        # EEPROM READ/WRITE + REBOOT
        self.pushButton_eeprom_write.clicked.connect (self.eeprom_write)
        self.pushButton_eeprom_read.clicked.connect (self.eeprom_read)
        self.pushButton_reboot.clicked.connect (self.reboot_device)
        
        # Measure buttons
        self.pushButton_measure_dut_freq.clicked.connect (self.measure_dut_freq)
        self.pushButton_measure_dut_fund_freq.clicked.connect (self.measure_dut_fund_freq)
        self.pushButton_measure_all.clicked.connect (self.measure_all)
        self.pushButton_measure_arparms.clicked.connect (self.measure_arparms)

    def handle_focus_changed(self, old_widget, now_widget):
        if self.lineEdit_ar_freq is old_widget:
            try:
                ar_freq = float (self.lineEdit_ar_freq.text())
                if (ar_freq > 250.000000) or (ar_freq < 0):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()
        
        if self.lineEdit_ar_adjmin is old_widget:
            try:
                ar_adjmin = int (self.lineEdit_ar_adjmin.text())
                if (ar_adjmin > 30) or (ar_adjmin < 1):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()
        
        if self.lineEdit_ar_frames is old_widget:
            try:
                ar_frames = int (self.lineEdit_ar_frames.text())
                if (ar_frames > 255) or (ar_frames < 1):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()

        if self.lineEdit_ar_max_int_time is old_widget:
            try:
                ar_max_int_time = int (self.lineEdit_ar_max_int_time.text())
                if (ar_max_int_time > 1000000) or (ar_max_int_time < 1):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()
        
        if self.lineEdit_ar_avg is old_widget:
            try:
                ar_avg = int (self.lineEdit_ar_avg.text())
                if (ar_avg > 255) or (ar_avg < 1):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()

        if self.lineEdit_int_time is old_widget:
            try:
                ar_max_int_time = int (self.lineEdit_int_time.text())
                if (ar_max_int_time > 1000000) or (ar_max_int_time < 1):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()

        if self.lineEdit_avg is old_widget:
            try:
                ar_avg = int (self.lineEdit_avg.text())
                if (ar_avg > 255) or (ar_avg < 1):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()

        if self.lineEdit_dut_ar_freq is old_widget:
            try:
                ar_freq = float (self.lineEdit_dut_ar_freq.text())
                if (ar_freq > 250.000000) or (ar_freq < 0):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()

        if self.lineEdit_fixedmode is old_widget:
            try:
                ar_fixed_mode = float (self.lineEdit_fixedmode.text())
                if (ar_fixed_mode > 1000) or (ar_fixed_mode < 4):
                    self.colorimeter_reload_parameters()
            except ValueError:
                self.colorimeter_reload_parameters()

        if self.lineEdit_ar_freq_two_values is old_widget:
            two_values = self.lineEdit_ar_freq_two_values.text().strip()
            try:
                value1 = float (two_values.split(",")[0])
                value2 = float (two_values.split(",")[1])
                if (value1 < 0) or (value1 > 240) or (value2 < 1) or (value2 > 250):
                    self.colorimeter_reload_parameters()
                    return
            except ValueError:
                self.colorimeter_reload_parameters()
                return

    def disable_interface (self):
        # Clear lineedits
        self.lineEdit_colorimeter.clear()
        self.lineEdit_libusbtmc_version.clear()
        self.lineEdit_ar_freq.clear()
        self.lineEdit_ar_adjmin.clear()
        self.lineEdit_ar_frames.clear()
        self.lineEdit_ar_max_int_time.clear()
        self.lineEdit_ar_avg.clear()
        self.lineEdit_int_time.clear()
        self.lineEdit_avg.clear()
        self.lineEdit_dut_ar_freq.clear()
        self.lineEdit_realint_time.clear()
        self.lineEdit_fixedmode.clear()
        self.lineEdit_ar_freq_two_values.clear()
        self.lineEdit_realint_time.clear()
        self.lineEdit_arparms_realint_time.clear()
        self.lineEdit_arparms_samples.clear()
        self.lineEdit_arparms_gain.clear()
        self.lineEdit_measured_dut_freq.clear()
        self.lineEdit_measured_dut_freq_luma.clear()
        self.lineEdit_measured_dut_freq_clip.clear()
        self.lineEdit_measured_dut_fund_freq.clear()
        self.lineEdit_measured_dut_fund_freq_luma.clear()
        self.lineEdit_measured_dut_fund_freq_clip.clear()
        self.lineEdit_measure_all_X.clear()
        self.lineEdit_measure_all_Y.clear()
        self.lineEdit_measure_all_Z.clear()
        self.lineEdit_measure_all_Y_2.clear()
        self.lineEdit_measure_all_x.clear()
        self.lineEdit_measure_all_y.clear()
        self.lineEdit_measure_all_Xoff.clear()
        self.lineEdit_measure_all_Yoff.clear()
        self.lineEdit_measure_all_Zoff.clear()
        self.lineEdit_measure_all_Xsat.clear()
        self.lineEdit_measure_all_Ysat.clear()
        self.lineEdit_measure_all_Zsat.clear()
        self.lineEdit_measure_all_clip.clear()
        self.lineEdit_measure_all_noise.clear()

        # # Disable groups of widgets
        self.widget_reload_params.setEnabled (False)
        self.widget_connection.setEnabled (False)
        self.widget_ar_params.setEnabled (False)
        self.widget_eeprom_operations.setEnabled (False)
        self.widget_core_params.setEnabled (False)
        self.widget_other_params.setEnabled (False)
        self.widget_measurements.setEnabled (False)

        # Clear comboboxes
        self.comboBox_autorange.blockSignals(True)
        self.comboBox_autorange.setCurrentIndex(-1)
        self.comboBox_autorange.blockSignals(True)

        self.comboBox_gain.blockSignals(True)
        self.comboBox_gain.setCurrentIndex(-1)
        self.comboBox_gain.blockSignals(False)

        self.comboBox_sbw.blockSignals(True)
        self.comboBox_sbw.setCurrentIndex(-1)
        self.comboBox_sbw.blockSignals(False)

        self.comboBox_automode.blockSignals(True)
        self.comboBox_automode.setCurrentIndex(-1)
        self.comboBox_automode.blockSignals(False)

        self.comboBox_shutter.blockSignals(True)
        self.comboBox_shutter.setCurrentIndex(-1)
        self.comboBox_shutter.blockSignals(False)

    def enable_interface (self):
        # Enable groups of widgets
        self.widget_reload_params.setEnabled (True)
        self.widget_connection.setEnabled (True)
        self.widget_ar_params.setEnabled (True)
        self.widget_eeprom_operations.setEnabled (True)
        self.widget_core_params.setEnabled (True)
        self.widget_other_params.setEnabled (True)
        self.widget_measurements.setEnabled (True)

    def toggle_connect_disconnect (self):
        if self.pushButton_connect.isChecked():
            self.pushButton_connect.setText ("DISCONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightcoral}")
            self.pcm2x_connect()
        else:
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.pcm2x_disconnect()

    def pcm2x_connect (self):

        # Initialization
        try:
            py_usbtmc_init()
        except ValueError:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("Error on usbtmc_init function! Reboot probe and restart application!")
            return


        # Get libusbtmc version
        libusbtmc_version = ctypes.create_string_buffer (10)
        
        try:
            py_usbtmc_get_version(libusbtmc_version, 10)
        except ValueError:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("Error on connecting to API! Reboot probe and restart application!")
            return
        
        if libusbtmc_version.value.decode("utf-8") == "":
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("Invalid API version! Reboot probe and restart application!")
            return
        
        

        # Get devices list
        buffer_size = 256 * 127
        usbtmcdevices = ctypes.create_string_buffer (buffer_size)
        error_find_devices = py_usbtmc_find_devices (usbtmcdevices, buffer_size)
   
        
        print (f"Find devices function returned error = {error_find_devices}")
        first_device_found = usbtmcdevices.value.decode("utf-8").split("\n")[0]
        print (f"First device found is -{first_device_found}-")

        if error_find_devices < 0:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.function_result_to_statusbar ("usbtmc_find_devices", error_find_devices, "")
            return

        if first_device_found == "":
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("No Admesy devices found!")
            return
        
        # Identify PCM2X
        device_string = first_device_found.split("::")[2].upper()
        if  device_string == "0X10D8":
            colorimeter_type = "PCM2X"
        else:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage (f"Admesy device 0x{device_string[-4:]} not supported!")
            return
        
 
        # Open device
        print (f"Handle of device BEFORE OPEN is {int (ptr_handle.contents.value)}")
        error_open = py_usbtmc_open (usbtmcdevices, ptr_handle)
        print (f"Open device function returned error = {error_open}")
        if error_open < 0:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.function_result_to_statusbar ("usbtmc_open", error_find_devices, "")
            return
        if int (ptr_handle.contents.value) == 77:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage (f"Something went wrong! Try rebooting probe and then restart application!")
            return

        handle_py = int (ptr_handle.contents.value)
        print (f"Handle of device is {handle_py}")

        # Enable interface
        self.enable_interface()
        self.lineEdit_libusbtmc_version.setText (libusbtmc_version.value.decode("utf-8"))
        
        # Read from device Firmware version
        command_py = ":SYSTem:VERSion?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        fw_vers_read = read_data.value.decode("utf-8")[:error_read].strip()

        # Read from device S/N
        command_py = ":EEPROM:READ:SN\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        sn_read = read_data.value.decode("utf-8")[:error_read].strip()

        self.lineEdit_colorimeter.setText (colorimeter_type + "  SN:" + sn_read + "  FW:" + fw_vers_read)

        # Load parameters
        self.eeprom_read()

    def pcm2x_disconnect (self):
        # Close device
        error_close = py_usbtmc_close (ptr_handle)
        # print (f"Close function error returned = {error_close}")

        self.disable_interface()

        if error_close == 0:
            self.statusbar.showMessage ("Device closed successfully!",10000)
        else:
            self.statusbar.showMessage ("Error closing device! Reboot probe and restart application!")

    def reload_parameters(self):
        self.colorimeter_reload_parameters()
        self.statusbar.showMessage (f"Parameters reloaded successfully at {ctime()[11:20]}",10000)

    def colorimeter_reload_parameters (self):

        print ("Colorimeter_reload_parameters launched!")

        # Read from device Autorange
        command_py = ":SENSe:AUTOrange?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)

        ar_read = read_data.value.decode("utf-8")[:error_read].strip()
        
        if (ar_read == "Closed") or (ar_read == "Opened"):
            # Reread Autorange
            print ("AUTORANGE: Closed/Opened received")
            self.colorimeter_reload_parameters()
        elif (ar_read == ""):
            print ("AUTORANGE: No reply received")
            return
        else:
            print ("AUTORANGE: " + ar_read)
            self.comboBox_autorange.blockSignals(True)
            self.comboBox_autorange.setCurrentIndex (int(ar_read))
            self.comboBox_autorange.blockSignals(False)
        

        # Read from device Int. Time
        command_py = ":SENSe:INT?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_int_time.setText (str(int_time_read))

        # Read from device Real Int. Time
        command_py = ":SENSe:REALINT?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        real_int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_realint_time.setText (str(real_int_time_read))



        # Read from device Average
        command_py = ":SENSe:AVERage?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        avg_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_avg.setText (str(avg_read))

        # Read from device Gain
        command_py = ":SENSe:GAIN?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        gain_read = int (read_data.value.decode("utf-8")[:error_read])
        # print (f"Gain index from reload parameters is {gain_read}")
        self.comboBox_gain.blockSignals(True)
        self.comboBox_gain.setCurrentIndex (gain_read-1)
        self.comboBox_gain.blockSignals(False)

        # Read from device Calibration Matrix
        command_py = ":SENSe:SBW?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        sbw_read = read_data.value.decode("utf-8")[:error_read].strip()
        # print (f"SBW is -{sbw_read}-")
        index_comboBox_sbw = self.comboBox_sbw.findText (sbw_read)
        # print (f"Index combo is {index_comboBox_sbw}")
        self.comboBox_sbw.blockSignals(True)
        self.comboBox_sbw.setCurrentIndex (index_comboBox_sbw)
        self.comboBox_sbw.blockSignals(False)

        # Read from device Automode
        command_py = ":SENSe:AUTOMODE?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        automode_read = int (read_data.value.decode("utf-8")[:error_read])
        print (f"Automode is -{automode_read}-")
        if automode_read == 255:
            automode_read = 5
        self.comboBox_automode.blockSignals(True)
        self.comboBox_automode.setCurrentIndex (automode_read)
        self.comboBox_automode.blockSignals(False)

        # Read from device Autorange parameters
        command_py = ":SENSe:ARPARMS?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        arparms_read = read_data.value.decode("utf-8")[:error_read].strip().split(",")
        # print (f"Autorange parameters are -{arparms_read}-")
        ar_freq = float (arparms_read[0])
        self.lineEdit_ar_freq.setText (f"{ar_freq:0.6f}")
        ar_adjmin = int (arparms_read[1])
        self.lineEdit_ar_adjmin.setText (str (ar_adjmin))
        ar_frames = int (arparms_read[2])
        self.lineEdit_ar_frames.setText (str (ar_frames))
        ar_max_int_time = int (arparms_read[3])
        self.lineEdit_ar_max_int_time.setText (str(ar_max_int_time))
        ar_avg = int (arparms_read[4])
        self.lineEdit_ar_avg.setText (str(ar_avg))

        # Read from device DUT Autorange Freq
        command_py = ":SENSe:FREQ?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        dut_freq_read = float (read_data.value.decode("utf-8")[:error_read])
        # print (f"dut freq is {dut_freq_read}")
        self.lineEdit_dut_ar_freq.setText (f"{dut_freq_read:0.3f}")

        # Read from device DUT Autorange Freq (ARFREQ)
        command_py = ":SENSe:ARFREQ?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        dut_arfreq_read_value1 = float (read_data.value.decode("utf-8")[:error_read].split(",")[0])
        dut_arfreq_read_value2 = float (read_data.value.decode("utf-8")[:error_read].split(",")[1])
        
        dut_arfreq_read_two_values = read_data.value.decode("utf-8")[:error_read]
        # print (f"value1 freq is {dut_arfreq_read_value1:0.3f}")
        # print (f"value2 freq is {dut_arfreq_read_value2:0.3f}")
        # print (dut_arfreq_read_two_values)
        self.lineEdit_ar_freq_two_values.setText (f"{dut_arfreq_read_value1:0.3f},{dut_arfreq_read_value2:0.3f}")

        # Read from device Shutter State
        command_py = ":SENSe:SHUTter?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        shutter_state_read = int (read_data.value.decode("utf-8")[:error_read])
        # print (f"Shutter is -{shutter_state_read}-")
        self.comboBox_shutter.blockSignals(True)
        self.comboBox_shutter.setCurrentIndex (shutter_state_read)
        self.comboBox_shutter.blockSignals(False)

    def function_result_to_statusbar (self, command_sent, error_received, extra_string):
        if not (error_received < 0):
            self.statusbar.showMessage (f"Command -- {command_sent} -- {error_received} bytes succesfully written!" + extra_string, 10000)
        else:
            if error_received == -20:
                self.statusbar.showMessage ("NO Library found! " + "Possible Reason: NI-VISA or LibUSB-WIN32 not installed!")
            elif error_received == -21:
                self.statusbar.showMessage ("NO Library Opened! " + "Possible Reason: usbtmc_find_devices is not performed!")
            elif error_received == -22:
                self.statusbar.showMessage ("Vendorid or productid emty! " + "Possible Reason: Open string must look like: USBBUS::Vendorid::productid::SERIAL::INSTR")
            elif error_received == -23:
                self.statusbar.showMessage ("No NI-VISA devices found!")
            elif error_received == -24:
                self.statusbar.showMessage ("LibUSB device to open not found!")
            elif error_received < -24:
                self.statusbar.showMessage ("NI-VISA Interface specific Error code." + f"Error code: {error_received}")
            else:
                self.statusbar.showMessage ("LIBUSB Interface specific Error code." + f"Error code: {error_received}")

    def colorimeter_write_autorange_params (self):
        
        # Write to device autorange parameters ARPARMS
        
        # Check if values are really changed
        if (not self.lineEdit_ar_freq.isModified()) and (not self.lineEdit_ar_adjmin.isModified()) and (not self.lineEdit_ar_frames.isModified()) and (not self.lineEdit_ar_max_int_time.isModified()) and (not self.lineEdit_ar_avg.isModified()) :
            return
        self.lineEdit_ar_freq.setModified(False)
        self.lineEdit_ar_adjmin.setModified(False)
        self.lineEdit_ar_frames.setModified(False)
        self.lineEdit_ar_max_int_time.setModified(False)
        self.lineEdit_ar_avg.setModified(False)

        # Check minimum value allowed for Max. Int. Time
        minimum_max_int_time = int (1000000 / float (self.lineEdit_ar_freq.text()))
        if int (self.lineEdit_ar_max_int_time.text()) < minimum_max_int_time:
            self.statusbar.showMessage (f"Minimum value for Max. Int. Time is {minimum_max_int_time} μs at {float (self.lineEdit_ar_freq.text()):0.2f} Hz",10000)
            self.colorimeter_reload_parameters()
            return

        command_py = ":SENSe:ARPARMS " + self.lineEdit_ar_freq.text() + ", " + self.lineEdit_ar_adjmin.text()+ ", " + self.lineEdit_ar_frames.text() + ", " + self.lineEdit_ar_max_int_time.text() + ", " + self.lineEdit_ar_avg.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_fixedmode_time (self):
        # Write to device fixedmode measurement time
        if (not self.lineEdit_fixedmode.isModified()):
            return
        self.lineEdit_fixedmode.setModified(False)
        command_py = ":SENSe:FIXEDMODE " + self.lineEdit_fixedmode.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()
    
    def colorimeter_write_autorange (self):
        # Write to device autorange
        ar_value = self.comboBox_autorange.currentIndex()
        # Catch if we put a placeholder on autorange combobox
        if ar_value < 0:
            return
        command_py = ":SENSe:AUTOrange " + str (ar_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_int_time (self):
        # Write to device int. time
        if (not self.lineEdit_int_time.isModified()):
            return
        self.lineEdit_int_time.setModified(False)
        command_py = ":SENSe:INT " + self.lineEdit_int_time.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_average (self):
        # Write to device average
        if (not self.lineEdit_avg.isModified()):
            return
        self.lineEdit_avg.setModified(False)
        command_py = ":SENSe:AVERage " + self.lineEdit_avg.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_gain (self):
        # Write to device gain
        gain_value = self.comboBox_gain.currentIndex()
        command_py = ":SENSe:GAIN " + str (gain_value + 1) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_sbw (self):
        # Write to device calibration matrix (sbw)
        sbw_string = self.comboBox_sbw.currentText()
        command_py = ":SENSe:SBW " + sbw_string + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_automode (self):
        # Write to device automode
        automode_value = self.comboBox_automode.currentIndex()
        if automode_value == 5:
            automode_value = 255 # Not Set!
        command_py = ":SENSe:AUTOMODE " + str(automode_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_dut_freq (self):
        # Write to device DUT freq (:SENSe:FREQ)
        if (not self.lineEdit_dut_ar_freq.isModified()):
            return
        self.lineEdit_dut_ar_freq.setModified(False)
        command_py = ":SENSe:FREQ " + self.lineEdit_dut_ar_freq.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()
    
    def colorimeter_write_dut_arfreq (self):
        # Write to device DUT AR freq (:SENSe:ARFREQ)
        
        if (not self.lineEdit_ar_freq_two_values.isModified()):
            self.colorimeter_reload_parameters()
            return
        self.lineEdit_ar_freq_two_values.setModified(False)

        two_values = self.lineEdit_ar_freq_two_values.text().strip()

        print ("-" + two_values + "-")
        try:
            value1 = float (two_values.split(",")[0])
            value2 = float (two_values.split(",")[1])
            if (value1 < 0) or (value1 > 240) or (value2 < 1) or (value2 > 250):
                self.colorimeter_reload_parameters()
                return
        except ValueError:
            self.colorimeter_reload_parameters()
            return
        
        print (f"Value 1 is {value1:03f}")
        print (f"Value 2 is {value2:03f}")
        print ("Operation permitted")
        print ("----------------------------")
            
        command_py = ":SENSe:ARFREQ " + f"{value1:03f}" + ", " + f"{value2:03f}" + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()
        
    def colorimeter_write_shutter_state (self):
        # Write to device shutter state
        shutter_state_value = self.comboBox_shutter.currentIndex()
        command_py = ":SENSe:SHUTter " + str(shutter_state_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        
        # Read from device Autorange the result of shutter command
        command_py_ar = ":SENSe:AUTOrange?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write_ar = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)

        # print ("-"+ read_data.value.decode("utf-8")[:error_read].strip() + "-")

        
        if (read_data.value.decode("utf-8")[:error_read].strip() == "Closed"):
            autorange_report_on_shutter = " Auto-range reported: Shutter closed!"
        elif (read_data.value.decode("utf-8")[:error_read].strip() == "Opened"):
            autorange_report_on_shutter = " Auto-range reported: Shutter opened!"
        else:
            autorange_report_on_shutter = " Auto-range reported: No report on shutter operation!"
            
        self.function_result_to_statusbar (command_py, error_write, autorange_report_on_shutter)
        self.colorimeter_reload_parameters()

    def eeprom_write (self):
        # :EEPROM:STARTUP:WRITE 
        command_py = ":EEPROM:STARTUP:WRITE\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, " Startup values updated!")
        sleep (1)
        self.colorimeter_reload_parameters()

    def eeprom_read (self):
        # :EEPROM:STARTUP:READ 
        command_py = ":EEPROM:STARTUP:READ\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, " Startup values copied from EEPROM to internal memory!")
        # sleep (3)
        self.colorimeter_reload_parameters()

    def reboot_device (self):
        # Reboot device
        command_py = ":BOOT:REBOOT \n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        full_result = read_data.value.decode("utf-8")[:error_read].strip()
        # print (f"BOOT result is -{full_result}-")

        # Close device
        error_close = py_usbtmc_close (ptr_handle)
        # print (f"Close function error returned = {error_close}")
        if error_close == 0:
            close_msg = " usbtmc_close report: Device closed!"
        else:
            close_msg = " usbtmc_close report: Error closing device!"

        self.pushButton_connect.setChecked (False)
        self.pushButton_connect.setText ("CONNECT")
        self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
        self.function_result_to_statusbar (command_py, error_write, close_msg + " Wait for the probe to reboot, then press CONNECT!")
        self.disable_interface()

    def measure_dut_freq (self):
        # Measure DUT Freq
        command_py = ":MEASure:FREQuency 3125\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        full_result = read_data.value.decode("utf-8")[:error_read].strip()
        
        # print (f"Measure DUT Freq result is -{full_result}-")
        
        dut_freq = float (full_result.split(",")[0])
        dut_ampl = float (full_result.split(",")[1])
        dut_clip = float (full_result.split(",")[2])

        # print (f"dut_freq is {dut_freq}")
        # print (f"dut_ampl is {dut_ampl}")
        # print (f"dut_clip is {dut_clip}")

        self.lineEdit_measured_dut_freq.setText (f"{dut_freq:0.3f}")
        self.lineEdit_measured_dut_freq_luma.setText (f"{dut_ampl:0.6f}")
        self.lineEdit_measured_dut_freq_clip.setText (f"{dut_clip:0.6f}")

        if self.checkBox_auto_set_freq.isChecked():
            # Write to device DUT freq (:SENSe:FREQ)
            command_py_freq = ":SENSe:FREQ " + f"{dut_freq:0.3f}" + "\n"
            print (command_py_freq)
            buffer_length = len (command_py_freq)
            timeout_ms = 5000
            error_write_freq = py_usbtmc_write(ptr_handle, command_py_freq.encode('ASCII'), buffer_length, timeout_ms)
            self.colorimeter_reload_parameters()

        self.function_result_to_statusbar (command_py, error_write, "")

    def measure_dut_fund_freq (self):
        # Measure DUT Freq
        command_py = ":MEASure:FUNDFREQ 3125\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        full_fund_result = read_data.value.decode("utf-8")[:error_read].strip()

        # print (f"Measure DUT Fundamental Freq result is -{full__fund_result}-")

        dut_fund_freq = float (full_fund_result.split(",")[0])
        dut_fund_ampl = float (full_fund_result.split(",")[1])
        dut_fund_clip = float (full_fund_result.split(",")[2])

        # print (f"dut_fund_freq is {dut_fund_freq}")
        # print (f"dut_fund_ampl is {dut_fund_ampl}")
        # print (f"dut_fund_clip is {dut_fund_clip}")

        self.lineEdit_measured_dut_fund_freq.setText (f"{dut_fund_freq:0.3f}")
        self.lineEdit_measured_dut_fund_freq_luma.setText (f"{dut_fund_ampl:0.6f}")
        self.lineEdit_measured_dut_fund_freq_clip.setText (f"{dut_fund_clip:0.6f}")

        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def measure_all (self):
        # Measure ALL
        command_py = ":MEASure:ALL\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        measure_all_result = read_data.value.decode("utf-8")[:error_read].strip()
        print (f"Measure ALL result is -{measure_all_result}-")

        self.lineEdit_measure_all_X.setText(measure_all_result.split(",")[0])
        self.lineEdit_measure_all_Y.setText(measure_all_result.split(",")[1])
        self.lineEdit_measure_all_Z.setText(measure_all_result.split(",")[2])
        self.lineEdit_measure_all_Y_2.setText(measure_all_result.split(",")[3])
        self.lineEdit_measure_all_x.setText(measure_all_result.split(",")[4])
        self.lineEdit_measure_all_y.setText(measure_all_result.split(",")[5])
        self.lineEdit_measure_all_Xoff.setText(measure_all_result.split(",")[6])
        self.lineEdit_measure_all_Yoff.setText(measure_all_result.split(",")[7])
        self.lineEdit_measure_all_Zoff.setText(measure_all_result.split(",")[8])
        self.lineEdit_measure_all_Xsat.setText(measure_all_result.split(",")[9])
        self.lineEdit_measure_all_Ysat.setText(measure_all_result.split(",")[10])
        self.lineEdit_measure_all_Zsat.setText(measure_all_result.split(",")[11])
        if int (measure_all_result.split(",")[12]):
            self.lineEdit_measure_all_clip.setText("Yes!!!")
        else:
            self.lineEdit_measure_all_clip.setText("No")
        if int (measure_all_result.split(",")[12]):
            self.lineEdit_measure_all_noise.setText("Yes!!!")
        else:
            self.lineEdit_measure_all_noise.setText("No")

        self.measure_arparms("from_measure_all")
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def measure_arparms (self, who_is_calling):
        # Measure Auto-range parameters used in last measurement
        command_py = ":MEASure:ARPARMS\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle, read_data, bytecount, timeout_ms)
        measure_arparms_result = read_data.value.decode("utf-8")[:error_read].strip()
        print (f"Measure ARPARMS result is -{measure_arparms_result}-")

        measure_arparms_result_int_time = int (measure_arparms_result.split(",")[0])
        measure_arparms_result_samples = int (measure_arparms_result.split(",")[1])
        measure_arparms_result_gain = int (measure_arparms_result.split(",")[2])

        self.lineEdit_arparms_realint_time.setText (f"{measure_arparms_result_int_time}")
        self.lineEdit_arparms_samples.setText (f"{measure_arparms_result_samples}")
        if measure_arparms_result_gain == 1:
            self.lineEdit_arparms_gain.setText ("Low Luminance (1)")
        elif measure_arparms_result_gain == 2:
            self.lineEdit_arparms_gain.setText ("Med. Luminance (2)")
        elif measure_arparms_result_gain == 3:
            self.lineEdit_arparms_gain.setText ("High Luminance (3)")
        else:
            self.lineEdit_arparms_gain.setText ("WTF")
        
        if not who_is_calling == "from_measure_all":
            self.function_result_to_statusbar (command_py, error_write, "")
            self.colorimeter_reload_parameters()

if __name__ == "__main__":
    
    #-------------------------------------------------------------------------------
    # Admesy API hook
    #-------------------------------------------------------------------------------
    try:
        libusbtmc = ctypes.CDLL ("./x64/libusbtmc_x64.dll")
    except:
        # print ("Library not found")
        
        # Enable High DPI display with PyQt5
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    
        app = QApplication (sys.argv)
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle ("Error")
        msg.setText ("API not found! Install API and restart application!")
        x = msg.exec_()
        exit()

    py_usbtmc_init = libusbtmc.usbtmc_init

    py_usbtmc_get_version = libusbtmc.usbtmc_get_version
    py_usbtmc_get_version.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
    py_usbtmc_get_version.restype = None

    py_usbtmc_find_devices = libusbtmc.usbtmc_find_devices
    py_usbtmc_find_devices.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
    py_usbtmc_find_devices.restype = ctypes.c_int32

    py_usbtmc_open = libusbtmc.usbtmc_open
    py_usbtmc_open.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32)]
    py_usbtmc_open.restype = ctypes.c_int32

    py_usbtmc_write = libusbtmc.usbtmc_write
    py_usbtmc_write.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32]
    py_usbtmc_write.restype = ctypes.c_int32

    py_usbtmc_read = libusbtmc.usbtmc_read
    py_usbtmc_read.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32]
    py_usbtmc_read.restype = ctypes.c_int32

    py_usbtmc_close = libusbtmc.usbtmc_close
    py_usbtmc_close.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
    py_usbtmc_close.restype = ctypes.c_int32
    #-------------------------------------------------------------------------------
    # End of Admesy API hook
    #-------------------------------------------------------------------------------

    # Global initialisation handle for colorimeter
    handle = ctypes.c_uint32 (77) # Whatever value to initialize
    ptr_handle = ctypes.pointer (handle)

    # Enable High DPI display with PyQt5
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    
    app = QApplication (sys.argv)
    window = MainUI()
    window.show()
    app.exec_()