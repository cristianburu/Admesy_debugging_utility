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
from numpy import frombuffer, set_printoptions, savetxt
import numpy
import time




class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        # Set locale to en_US
        en = QtCore.QLocale ("en_US")
        QtCore.QLocale.setDefault(en)

        # Load interface
        loadUi ("interface.ui", self)

        # Focus change handler
        QApplication.instance().focusChanged.connect(self.handle_focus_changed)

        # Manual toggle button for PCM2X
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        self.pushButton_connect = QtWidgets.QPushButton(self.tab_pcm2x)
        self.pushButton_connect.setGeometry(QtCore.QRect(58, 13, 77, 19))
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_connect.setText(QtCore.QCoreApplication.translate("MainWindow", "CONNECT"))
        self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
        self.pushButton_connect.setCheckable (True)

        # Manual toggle button for Hera
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        self.pushButton_connect_hera = QtWidgets.QPushButton(self.tab_hera)
        self.pushButton_connect_hera.setGeometry(QtCore.QRect(58, 13, 77, 19))
        self.pushButton_connect_hera.setFont(font)
        self.pushButton_connect_hera.setObjectName("pushButton_connect")
        self.pushButton_connect_hera.setText(QtCore.QCoreApplication.translate("MainWindow", "CONNECT"))
        self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
        self.pushButton_connect_hera.setCheckable (True)

        # Disable inteface
        self.disable_interface_pcm2x()
        self.disable_interface_hera()

        ##################################
        #     TAB PCM2X Signals/Slots    #
        ##################################

        # Connect/Disconnect Button
        self.pushButton_connect.clicked.connect (self.toggle_connect_disconnect_pcm2x)

        # Reload Parameters Button
        self.pushButton_reload_params.clicked.connect (self.reload_parameters_for_colorimeter_on_click)
        
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
        self.pushButton_eeprom_write.clicked.connect (self.colorimeter_eeprom_write)
        self.pushButton_eeprom_read.clicked.connect (self.colorimeter_eeprom_read)
        self.pushButton_reboot.clicked.connect (self.reboot_device)
        
        # Measure buttons
        self.pushButton_measure_dut_freq.clicked.connect (self.measure_dut_freq)
        self.pushButton_measure_dut_fund_freq.clicked.connect (self.measure_dut_fund_freq)
        self.pushButton_measure_all.clicked.connect (self.measure_all)
        self.pushButton_measure_arparms.clicked.connect (self.measure_arparms)


        # EEPROM Parameters
        self.lineEdit_eeprom_avg.setValidator (QtGui.QIntValidator(1,255, self))
        self.lineEdit_eeprom_avg.editingFinished.connect (self.colorimeter_eeprom_write_average)


        ##############################
        #  TAB HERA Signals/Slots    #
        ##############################

        self.pushButton_connect_hera.clicked.connect (self.toggle_connect_disconnect_hera)

        # Reload Parameters Button
        self.pushButton_hera_reload_params.clicked.connect (self.reload_parameters_for_hera_on_click)

        # EEPROM READ/WRITE + REBOOT
        self.pushButton_hera_eeprom_write.clicked.connect (self.hera_eeprom_write)
        self.pushButton_hera_eeprom_read.clicked.connect (self.hera_eeprom_read)

        # Core parameters

        
        self.comboBox_hera_autorange.currentIndexChanged.connect (self.hera_write_autorange_memory)
        

        self.lineEdit_hera_int_time.setValidator (QtGui.QIntValidator(2500,20000000, self))
        self.lineEdit_hera_int_time.editingFinished.connect (self.hera_write_int_time_memory)

        self.lineEdit_hera_avg.setValidator (QtGui.QIntValidator(1,200, self))
        self.lineEdit_hera_avg.editingFinished.connect (self.hera_write_avg_memory)

        self.lineEdit_hera_adjmin_2.setValidator (QtGui.QIntValidator(1,100, self))
        self.lineEdit_hera_adjmin_2.editingFinished.connect (self.hera_write_adjmin_eeprom_2)

        self.lineEdit_hera_freq_2.setValidator (QtGui.QIntValidator(1,255, self))
        self.lineEdit_hera_freq_2.editingFinished.connect (self.hera_write_freq_eeprom_2)

        # Other parameters
        self.comboBox_hera_interp_method.currentIndexChanged.connect (self.hera_write_interp_method_memory)

        
        
        self.comboBox_hera_cal_memory.currentIndexChanged.connect (self.hera_write_cal_memory)



        self.comboBox_hera_res_write_only.currentIndexChanged.connect (self.hera_write_res_memory_write_only)
        self.comboBox_hera_sbw_write_only.currentIndexChanged.connect (self.hera_write_sbw_memory_write_only)


        


        
        

        # EEPROM Parameters

        
        self.comboBox_hera_autorange_eeprom.currentIndexChanged.connect (self.hera_write_autorange_eeprom)

        self.comboBox_hera_interp_method_eeprom.currentIndexChanged.connect (self.hera_write_interp_method_eeprom)


        
        

        self.lineEdit_hera_int_time_eeprom.setValidator (QtGui.QIntValidator(1000,500000, self))
        self.lineEdit_hera_int_time_eeprom.editingFinished.connect (self.hera_write_int_time_eeprom)

        self.lineEdit_hera_avg_eeprom.setValidator (QtGui.QIntValidator(1,200, self))
        self.lineEdit_hera_avg_eeprom.editingFinished.connect (self.hera_write_avg_eeprom)
        

        self.lineEdit_hera_adjmin.setValidator (QtGui.QIntValidator(1,100, self))
        self.lineEdit_hera_adjmin.editingFinished.connect (self.hera_write_adjmin_eeprom)

        self.lineEdit_hera_freq.setValidator (QtGui.QIntValidator(1,255, self))
        self.lineEdit_hera_freq.editingFinished.connect (self.hera_write_freq_eeprom)

        
        self.lineEdit_hera_max_int_time.setValidator (QtGui.QIntValidator(2500,20000000, self))
        self.lineEdit_hera_max_int_time.editingFinished.connect (self.hera_write_max_int_time_eeprom)


        self.comboBox_hera_res_eeprom.currentIndexChanged.connect (self.hera_write_res_eeprom)
        self.comboBox_hera_abs_cal_method_eeprom.currentIndexChanged.connect (self.hera_write_userabs_eeprom)

        self.comboBox_hera_sbw.currentIndexChanged.connect (self.hera_write_sbw_eeprom)

        self.comboBox_hera_std_illuminant_eeprom.currentIndexChanged.connect (self.hera_write_std_illuminant_eeprom)


        
        

        # Measure buttons
        self.pushButton_hera_measure_spectrum.clicked.connect (self.hera_measure_spectrum)
        self.pushButton_hera_get_wavelengths.clicked.connect (self.hera_get_wavelengths)
        self.pushButton_hera_measure_Yxy.clicked.connect (self.hera_measure_Yxy)
        self.pushButton_hera_measure_XYZ.clicked.connect (self.hera_measure_XYZ)
 

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
            
        ###############
        #  HERA TAB   #
        ###############
        
        if self.lineEdit_hera_int_time is old_widget:
            try:
                int_time = int (self.lineEdit_hera_int_time.text())
                if (int_time > 20000000) or (int_time < 2500):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_int_time_eeprom is old_widget:
            try:
                int_time = int (self.lineEdit_hera_int_time_eeprom.text())
                if (int_time > 20000000) or (int_time < 2500):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_avg is old_widget:
            try:
                avg = int (self.lineEdit_hera_avg.text())
                if (avg > 200) or (avg < 1):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_avg_eeprom is old_widget:
            try:
                avg = int (self.lineEdit_hera_avg_eeprom.text())
                if (avg > 200) or (avg < 1):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_adjmin_2 is old_widget:
            try:
                adjmin = int (self.lineEdit_hera_adjmin_2.text())
                if (adjmin > 100) or (adjmin < 1):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_adjmin is old_widget:
            try:
                adjmin = int (self.lineEdit_hera_adjmin.text())
                if (adjmin > 100) or (adjmin < 1):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_freq_2 is old_widget:
            try:
                freq = int (self.lineEdit_hera_freq_2.text())
                if (freq > 255) or (freq < 1):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_freq is old_widget:
            try:
                freq = int (self.lineEdit_hera_freq.text())
                if (freq > 255) or (freq < 1):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

        if self.lineEdit_hera_max_int_time is old_widget:
            try:
                max_int_time = int (self.lineEdit_hera_max_int_time.text())
                if (max_int_time > 20000000) or (max_int_time < 2500):
                    self.hera_reload_parameters()
            except ValueError:
                self.hera_reload_parameters()

    


    def disable_interface_pcm2x (self):
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
        self.widget_00_reload_params.setEnabled (False)
        self.widget_01_connection.setEnabled (False)
        self.widget_02_ar_params.setEnabled (False)
        self.widget_03_measure_all.setEnabled (False)
        self.widget_04_measure_arparms.setEnabled (False)
        self.widget_05_core_params.setEnabled (False)
        self.widget_06_other_params.setEnabled (False)
        self.widget_07_measure_freq.setEnabled (False)
        self.widget_08_eeprom_operations.setEnabled (False)
        self.widget_09_eeprom_params.setEnabled (False)

        # Clear comboboxes
        self.comboBox_autorange.blockSignals(True)
        self.comboBox_autorange.setCurrentIndex(-1)
        self.comboBox_autorange.blockSignals(False)

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

    def disable_interface_hera (self):

        # Clear lineedits
        self.lineEdit_spectro.clear()
        self.lineEdit_libusbtmc_version_hera.clear()
        self.lineEdit_hera_int_time.clear()
        self.lineEdit_hera_avg.clear()
        self.lineEdit_hera_adjmin_2.clear()
        self.lineEdit_hera_freq_2.clear()
        self.lineEdit_hera_measure_Yxy_clip.clear()
        self.lineEdit_hera_measure_Yxy_clip.setStyleSheet ("")
        self.lineEdit_hera_measure_Yxy_noise.clear()
        self.lineEdit_hera_measure_Yxy_noise.setStyleSheet ("")
        self.lineEdit_hera_measure_Yxy_Y.clear()
        self.lineEdit_hera_measure_Yxy_x.clear()
        self.lineEdit_hera_measure_Yxy_y.clear()
        self.lineEdit_hera_measure_XYZ_clip.clear()
        self.lineEdit_hera_measure_XYZ_clip.setStyleSheet ("")
        self.lineEdit_hera_measure_XYZ_noise.clear()
        self.lineEdit_hera_measure_XYZ_noise.setStyleSheet ("")
        self.lineEdit_hera_measure_XYZ_X.clear()
        self.lineEdit_hera_measure_XYZ_Y.clear()
        self.lineEdit_hera_measure_XYZ_Z.clear()
        self.lineEdit_hera_int_time_eeprom.clear()
        self.lineEdit_hera_avg_eeprom.clear()
        self.lineEdit_hera_adjmin.clear()
        self.lineEdit_hera_freq.clear()
        self.lineEdit_hera_max_int_time.clear()

        # Clear labels
        self.label_meas_time_XYZ.clear()
        self.label_meas_time_Yxy.clear()

        # Disable groups of widgets
        self.widget_hera_00_reload_params.setEnabled (False)
        self.widget_hera_01_connection.setEnabled (False)
        self.widget_hera_02_core_params.setEnabled (False)
        self.widget_hera_03_other_params.setEnabled (False)
        self.widget_hera_04_measure_all.setEnabled (False)
        self.widget_hera_05_eeprom_operations.setEnabled (False)
        self.widget_hera_06_eeprom_parameters.setEnabled (False)
        self.widget_hera_07_measure_spectrum.setEnabled (False)

        # Clear comboboxes
        self.comboBox_hera_autorange.blockSignals(True)
        self.comboBox_hera_autorange.setCurrentIndex(-1)
        self.comboBox_hera_autorange.blockSignals(False)

        self.comboBox_hera_interp_method.blockSignals(True)
        self.comboBox_hera_interp_method.setCurrentIndex(-1)
        self.comboBox_hera_interp_method.blockSignals(False)

        self.comboBox_hera_autorange_eeprom.blockSignals(True)
        self.comboBox_hera_autorange_eeprom.setCurrentIndex(-1)
        self.comboBox_hera_autorange_eeprom.blockSignals(False)

        self.comboBox_hera_res_eeprom.blockSignals(True)
        self.comboBox_hera_res_eeprom.setCurrentIndex(-1)
        self.comboBox_hera_res_eeprom.blockSignals(False)

        self.comboBox_hera_interp_method_eeprom.blockSignals(True)
        self.comboBox_hera_interp_method_eeprom.setCurrentIndex(-1)
        self.comboBox_hera_interp_method_eeprom.blockSignals(False)

        self.comboBox_hera_std_illuminant_eeprom.blockSignals(True)
        self.comboBox_hera_std_illuminant_eeprom.setCurrentIndex(-1)
        self.comboBox_hera_std_illuminant_eeprom.blockSignals(False)

        self.comboBox_hera_abs_cal_method_eeprom.blockSignals(True)
        self.comboBox_hera_abs_cal_method_eeprom.setCurrentIndex(-1)
        self.comboBox_hera_abs_cal_method_eeprom.blockSignals(False)

        self.comboBox_hera_sbw.blockSignals(True)
        self.comboBox_hera_sbw.setCurrentIndex(-1)
        self.comboBox_hera_sbw.blockSignals(False)

        self.comboBox_hera_sbw_write_only.blockSignals(True)
        self.comboBox_hera_sbw_write_only.setCurrentIndex(-1)
        self.comboBox_hera_sbw_write_only.blockSignals(False)

        self.comboBox_hera_res_write_only.blockSignals(True)
        self.comboBox_hera_res_write_only.setCurrentIndex(-1)
        self.comboBox_hera_res_write_only.blockSignals(False)

        self.comboBox_hera_cal_memory.blockSignals(True)
        self.comboBox_hera_cal_memory.setCurrentIndex(-1)
        self.comboBox_hera_cal_memory.blockSignals(False)

        
    
    def enable_interface_pcm2x (self):
        # Enable groups of widgets
        self.widget_00_reload_params.setEnabled (True)
        self.widget_01_connection.setEnabled (True)
        self.widget_02_ar_params.setEnabled (True)
        self.widget_03_measure_all.setEnabled (True)
        self.widget_04_measure_arparms.setEnabled (True)
        self.widget_05_core_params.setEnabled (True)
        self.widget_06_other_params.setEnabled (True)
        self.widget_07_measure_freq.setEnabled (True)
        self.widget_08_eeprom_operations.setEnabled (True)
        self.widget_09_eeprom_params.setEnabled (True)

    def enable_interface_hera (self):
        # Disable groups of widgets
        self.widget_hera_00_reload_params.setEnabled (True)
        self.widget_hera_01_connection.setEnabled (True)
        self.widget_hera_02_core_params.setEnabled (True)
        self.widget_hera_03_other_params.setEnabled (True)
        self.widget_hera_04_measure_all.setEnabled (True)
        self.widget_hera_05_eeprom_operations.setEnabled (True)
        self.widget_hera_06_eeprom_parameters.setEnabled (True)
        # self.widget_hera_07_measure_spectrum.setEnabled (False)   - TO BE DONE

    def toggle_connect_disconnect_pcm2x (self):
        if self.pushButton_connect.isChecked():
            self.pushButton_connect.setText ("DISCONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightcoral}")
            self.pcm2x_connect()
        else:
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.pcm2x_disconnect()

    def toggle_connect_disconnect_hera (self):
        if self.pushButton_connect_hera.isChecked():
            self.pushButton_connect_hera.setText ("DISCONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightcoral}")
            self.hera_connect()
        else:
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.hera_disconnect()

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

        list_of_devices = usbtmcdevices.value.decode("utf-8").split("\n")
        print (list_of_devices)
        print (type(list_of_devices))
       
        

        if list_of_devices[0] == "":
            del list_of_devices[0]

        print (f"Lungimea listei este {len(list_of_devices)}")
        print (not list_of_devices)

        if error_find_devices < 0:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.function_result_to_statusbar ("usbtmc_find_devices", error_find_devices, "")
            return

        if not list_of_devices:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("No Admesy devices found!")
            return
        
        pcm2x_found = False
        for device_colorimeter in list_of_devices:
            # Identify PCM2X
            device_string = device_colorimeter.split("::")[2].upper()
            if  device_string == "0X10D8":
                colorimeter_type = "PCM2X"
                my_pcm2x = device_colorimeter
                pcm2x_found = True
        
        if not pcm2x_found:
            # Identify first Admesy device
            device_string = list_of_devices[0].split("::")[2].upper()
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            if device_string == "0X1020":
                self.statusbar.showMessage (f"HERA 01 (0x1020) not supported on this tab!", 10000)
            else:
                self.statusbar.showMessage (f"Admesy device 0x{device_string[-4:]} not supported!", 10000)
            return
        
        print (f"Device identified as PCM2X is {my_pcm2x}")
 
        # Open device
        print (f"Handle of device BEFORE OPEN is {int (ptr_handle_colorimeter.contents.value)}")
        error_open = py_usbtmc_open (my_pcm2x.encode ('ASCII'), ptr_handle_colorimeter)
        print (f"Open device function returned error = {error_open}")
        if error_open < 0:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.function_result_to_statusbar ("usbtmc_open", error_find_devices, "")
            return
        if int (ptr_handle_colorimeter.contents.value) == 77:
            self.pushButton_connect.setChecked (False)
            self.pushButton_connect.setText ("CONNECT")
            self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage (f"Something went wrong! Try rebooting probe and then restart application!")
            return

        handle_py_colorimeter = int (ptr_handle_colorimeter.contents.value)
        print (f"Handle of colorimeter device is {handle_py_colorimeter}")

        # Enable interface
        self.enable_interface_pcm2x()
        self.lineEdit_libusbtmc_version.setText (libusbtmc_version.value.decode("utf-8"))
        
        # Read from device Firmware version
        command_py = ":SYSTem:VERSion?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        fw_vers_read = read_data.value.decode("utf-8")[:error_read].strip()

        # Read from device S/N
        command_py = ":EEPROM:READ:SN\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        sn_read = read_data.value.decode("utf-8")[:error_read].strip()

        self.lineEdit_colorimeter.setText (colorimeter_type + "  SN:" + sn_read + "  FW:" + fw_vers_read)

        # Load parameters
        self.colorimeter_eeprom_read()

    def hera_connect (self):
        # Initialization
        try:
            py_usbtmc_init()
        except ValueError:
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("Error on usbtmc_init function! Reboot probe and restart application!")
            return


        # Get libusbtmc version
        libusbtmc_version = ctypes.create_string_buffer (10)
        
        try:
            py_usbtmc_get_version(libusbtmc_version, 10)
        except ValueError:
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("Error on connecting to API! Reboot probe and restart application!")
            return
        
        if libusbtmc_version.value.decode("utf-8") == "":
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("Invalid API version! Reboot probe and restart application!")
            return
        
        

        # Get devices list
        buffer_size = 256 * 127
        usbtmcdevices = ctypes.create_string_buffer (buffer_size)
        error_find_devices = py_usbtmc_find_devices (usbtmcdevices, buffer_size)
          
        list_of_devices = usbtmcdevices.value.decode("utf-8").split("\n")
        print ("Hera CONNECT: List of devices is")
        print (list_of_devices)
        print ("----- END OF LIST")
       
        

        if list_of_devices[0] == "":
            del list_of_devices[0]

        print (f"Hera CONNECT: Lungimea listei este {len(list_of_devices)}")
        print (f"Hera CONNECT: error_find_devices is {error_find_devices}")

        if error_find_devices < 0:
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.function_result_to_statusbar ("usbtmc_find_devices", error_find_devices, "")
            return

        if not list_of_devices:
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage ("No Admesy devices found!")
            return
        
        hera_found = False
        for device_spectro in list_of_devices:
            # Identify HERA
            device_string = device_spectro.split("::")[2].upper()
            if  device_string == "0X1020":
                spectro_type = "HERA 01"
                my_spectro = device_spectro
                hera_found = True
        
        if not hera_found:
            # Identify first Admesy device
            device_string = list_of_devices[0].split("::")[2].upper()
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage (f"Admesy device 0x{device_string[-4:]} not supported!", 10000)
            return
        
        print (f"Hera CONNECT: Device identified as HERA is {my_spectro}")
 
        # Open device
        print (f"Hera CONNECT: Handle of device BEFORE OPEN is {int (ptr_handle_spectro.contents.value)}")
        error_open = py_usbtmc_open (my_spectro.encode ('ASCII'), ptr_handle_spectro)
        print (f"Hera CONNECT: Open device function returned error = {error_open}")
        if error_open < 0:
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.function_result_to_statusbar ("usbtmc_open", error_find_devices, "")
            return
        if int (ptr_handle_spectro.contents.value) == 99:
            self.pushButton_connect_hera.setChecked (False)
            self.pushButton_connect_hera.setText ("CONNECT")
            self.pushButton_connect_hera.setStyleSheet ("QPushButton {background-color:lightgreen}")
            self.statusbar.showMessage (f"Something went wrong! Try rebooting probe and then restart application!")
            return

        handle_py_spectro = int (ptr_handle_spectro.contents.value)
        print (f"Hera CONNECT: Handle of spectro device is {handle_py_spectro}")

        # Enable interface
        self.enable_interface_hera()
        self.lineEdit_libusbtmc_version_hera.setText (libusbtmc_version.value.decode("utf-8"))
        
        # Read from device Firmware version
        command_py = ":SYSTem:VERSion?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        fw_vers_read = read_data.value.decode("utf-8")[:error_read].strip()

        # Read from device S/N
        command_py = ":EEPROM:READ:SN\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        sn_read = read_data.value.decode("utf-8")[:error_read].strip()

        self.lineEdit_spectro.setText (spectro_type + "  SN:" + sn_read + "  FW:" + fw_vers_read)

        # Load parameters
        self.hera_eeprom_read()
 
    def pcm2x_disconnect (self):
        # Close device
        error_close = py_usbtmc_close (ptr_handle_colorimeter)
        # print (f"Close function error returned = {error_close}")

        self.disable_interface_pcm2x()

        if error_close == 0:
            self.statusbar.showMessage ("Device closed successfully!",10000)
        else:
            self.statusbar.showMessage ("Error closing device! Reboot probe and restart application!")

    def hera_disconnect (self):
        # Close device
        error_close = py_usbtmc_close (ptr_handle_spectro)
        # print (f"Close function error returned = {error_close}")

        self.disable_interface_hera()

        if error_close == 0:
            self.statusbar.showMessage ("Device closed successfully!",10000)
        else:
            self.statusbar.showMessage ("Error closing device! Reboot probe and restart application!")
 
    def reload_parameters_for_colorimeter_on_click(self):
        self.colorimeter_reload_parameters()
        self.statusbar.showMessage (f"Parameters reloaded successfully at {ctime()[11:20]}",10000)

    def reload_parameters_for_hera_on_click(self):
        self.hera_reload_parameters()
        self.statusbar.showMessage (f"Parameters reloaded successfully at {ctime()[11:20]}",10000)

    def colorimeter_reload_parameters (self):

        print ("Colorimeter_reload_parameters launched!")

        # Read from device Autorange
        command_py = ":SENSe:AUTOrange?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)

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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_int_time.setText (str(int_time_read))

        # Read from device Real Int. Time
        command_py = ":SENSe:REALINT?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        real_int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_realint_time.setText (str(real_int_time_read))



        # Read from device Average
        command_py = ":SENSe:AVERage?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        avg_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_avg.setText (str(avg_read))

        # Read from device Average - EEPROM
        command_py = ":EEPROM:CONFigure:AVG?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        avg_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_eeprom_avg.setText (str(avg_read))

        # Read from device Gain
        command_py = ":SENSe:GAIN?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        gain_read = int (read_data.value.decode("utf-8")[:error_read])
        # print (f"Gain index from reload parameters is {gain_read}")
        self.comboBox_gain.blockSignals(True)
        self.comboBox_gain.setCurrentIndex (gain_read-1)
        self.comboBox_gain.blockSignals(False)

        # Read from device Calibration Matrix
        command_py = ":SENSe:SBW?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        dut_freq_read = float (read_data.value.decode("utf-8")[:error_read])
        # print (f"dut freq is {dut_freq_read}")
        self.lineEdit_dut_ar_freq.setText (f"{dut_freq_read:0.3f}")

        # Read from device DUT Autorange Freq (ARFREQ)
        command_py = ":SENSe:ARFREQ?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        shutter_state_read = int (read_data.value.decode("utf-8")[:error_read])
        # print (f"Shutter is -{shutter_state_read}-")
        self.comboBox_shutter.blockSignals(True)
        self.comboBox_shutter.setCurrentIndex (shutter_state_read)
        self.comboBox_shutter.blockSignals(False)

    def hera_reload_parameters (self):
        # print ("Hera_reload_parameters launched!")

        # Read from device Autorange - internal memory
        command_py = ":SENSe:SP:AUTORANGE?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)

        ar_read = read_data.value.decode("utf-8")[:error_read].strip()
        
        if (ar_read == "Closed") or (ar_read == "Opened"):
            # Reread Autorange
            print ("AUTORANGE: Closed/Opened received")
            self.hera_reload_parameters()
        elif (ar_read == ""):
            print ("AUTORANGE: No reply received")
            return
        else:
            print ("AUTORANGE: " + ar_read)
            self.comboBox_hera_autorange.blockSignals(True)
            self.comboBox_hera_autorange.setCurrentIndex (int(ar_read))
            self.comboBox_hera_autorange.blockSignals(False)

        # Read from device Int. Time - Internal Memory
        command_py = ":SENSe:INT?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_int_time.setText (str(int_time_read))

        # Read from device Average - internal memory
        command_py = ":SENSe:SP:AVERAGE?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        avg_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_avg.setText (str(avg_read))

        # Read from device Interp Method - from Internal Memory
        command_py = ":SENSe:INTERPOL?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        interpol_method_read = int (read_data.value.decode("utf-8")[:error_read])
        print (f"Interpolation index from reload parameters is {interpol_method_read}")
        self.comboBox_hera_interp_method.blockSignals(True)
        self.comboBox_hera_interp_method.setCurrentIndex (interpol_method_read)
        self.comboBox_hera_interp_method.blockSignals(False)


        # Read from device Calibration Mode - from Internal Memory
        command_py = ":SENSe:CAL?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        cal_mode_read = int (read_data.value.decode("utf-8")[:error_read].strip())
        print (f"Calibration mode from reload parameters is --{cal_mode_read}--")
        self.comboBox_hera_cal_memory.blockSignals(True)
        self.comboBox_hera_cal_memory.setCurrentIndex (cal_mode_read)
        self.comboBox_hera_cal_memory.blockSignals(False)


        ######################
        #  Read from EEPROM  #
        ######################

        # Read from device Autorange - EEPROM
        command_py = ":EEPROM:CONFigure:AUTORANGE?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)

        ar_read = read_data.value.decode("utf-8")[:error_read].strip()
        
        if (ar_read == "Closed") or (ar_read == "Opened"):
            # Reread Autorange
            print ("AUTORANGE: Closed/Opened received")
            self.hera_reload_parameters()
        elif (ar_read == ""):
            print ("AUTORANGE: No reply received")
            return
        else:
            print ("AUTORANGE: " + ar_read)
            self.comboBox_hera_autorange_eeprom.blockSignals(True)
            self.comboBox_hera_autorange_eeprom.setCurrentIndex (int(ar_read))
            self.comboBox_hera_autorange_eeprom.blockSignals(False)

        # Read from device Int. Time - from EEPROM
        command_py = ":EEPROM:CONFigure:SPINT?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_int_time_eeprom.setText (str(int_time_read))
      
        # Read from device Average - from EEPROM
        command_py = ":EEPROM:CONFigure:SPAVG?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        avg_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_avg_eeprom.setText (str(avg_read))

        # Read from device Adj min from EEPROM
        command_py = ":EEPROM:CONFigure:AUTO:ADJMIN?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        adjmin_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_adjmin.setText (str(adjmin_read))
        self.lineEdit_hera_adjmin_2.setText (str(adjmin_read))

        # Read from device Freq from EEPROM
        command_py = ":EEPROM:CONFigure:AUTO:FREQ?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        freq_error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        hera_freq_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_freq.setText (f"{hera_freq_read}")
        self.lineEdit_hera_freq_2.setText (f"{hera_freq_read}")

        # Read from device Max Int. Time from EEPROM
        command_py = ":EEPROM:CONFigure:AUTO:MAXINT?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        int_time_read = int (read_data.value.decode("utf-8")[:error_read])
        self.lineEdit_hera_max_int_time.setText (str(int_time_read))

        # Read from device Resolution - from EEPROM
        command_py = ":EEPROM:CONFigure:RES?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        resolution_read = int (read_data.value.decode("utf-8")[:error_read])
        self.comboBox_hera_res_eeprom.blockSignals(True)
        self.comboBox_hera_res_eeprom.setCurrentIndex (resolution_read)
        self.comboBox_hera_res_eeprom.blockSignals(False)

        # Read from device Interp Method - from EEPROM
        command_py = ":EEPROM:CONFigure:INTERPOL?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        interpol_method_read = int (read_data.value.decode("utf-8")[:error_read])
        self.comboBox_hera_interp_method_eeprom.blockSignals(True)
        self.comboBox_hera_interp_method_eeprom.setCurrentIndex (interpol_method_read)
        self.comboBox_hera_interp_method_eeprom.blockSignals(False)

        # Read from device Std. Illuminant - from EEPROM
        command_py = ":EEPROM:CONFigure:WHITE?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        white_read = read_data.value.decode("utf-8")[:error_read].strip()
        print (f"White is -{white_read}-")
        index_comboBox_white = self.comboBox_hera_std_illuminant_eeprom.findText (white_read)
        # print (f"Index combo is {index_comboBox_white}")
        self.comboBox_hera_std_illuminant_eeprom.blockSignals(True)
        self.comboBox_hera_std_illuminant_eeprom.setCurrentIndex (index_comboBox_white)
        self.comboBox_hera_std_illuminant_eeprom.blockSignals(False)

        # Read from device Abs. Calibration Method - from EEPROM
        command_py = ":EEPROM:CONFigure:USERABS?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        abs_calib_mode_read = int (read_data.value.decode("utf-8")[:error_read])
        self.comboBox_hera_abs_cal_method_eeprom.blockSignals(True)
        self.comboBox_hera_abs_cal_method_eeprom.setCurrentIndex (abs_calib_mode_read)
        self.comboBox_hera_abs_cal_method_eeprom.blockSignals(False)

        # Read from device Calibration Matrix - from EEPROM
        command_py = ":EEPROM:CONFigure:SPSBW?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        sbw_error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        sbw_error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        sbw_read = read_data.value.decode("utf-8")[:sbw_error_read].strip()
        print (f"SBW is -{sbw_read}-")
        print (f"sbw_error_write is -{sbw_error_write}-")
        print (f"sbw_error_read is -{sbw_error_read}-")
        index_comboBox_sbw = int (sbw_read)
        self.comboBox_hera_sbw.blockSignals(True)
        self.comboBox_hera_sbw.setCurrentIndex (index_comboBox_sbw)
        self.comboBox_hera_sbw.blockSignals(False)
  
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
            elif error_received == -1073807339:
                self.statusbar.showMessage (f"NI-VISA Timeout! Error code: {error_received} on " + command_sent + " Physically reboot probe and restart application!")
            elif error_received < -24:
                self.statusbar.showMessage (f"NI-VISA Interface specific error code: {error_received} on " + command_sent + " Physically reboot probe and restart application!")
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_eeprom_write_average (self):
        # Write to device EEPROM - average
        if (not self.lineEdit_eeprom_avg.isModified()):
            return
        self.lineEdit_eeprom_avg.setModified(False)
        command_py = ":EEPROM:CONFigure:AVG " + self.lineEdit_eeprom_avg.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_gain (self):
        # Write to device gain
        gain_value = self.comboBox_gain.currentIndex()
        command_py = ":SENSe:GAIN " + str (gain_value + 1) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def colorimeter_write_sbw (self):
        # Write to device calibration matrix (sbw)
        sbw_string = self.comboBox_sbw.currentText()
        command_py = ":SENSe:SBW " + sbw_string + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def hera_write_freq_eeprom (self):
        print ("Freq working!")
        # Write to device freq - EEPROM
        if (not self.lineEdit_hera_freq.isModified()):
            return
        self.lineEdit_hera_freq.setModified(False)
        command_py = ":EEPROM:CONFigure:AUTO:FREQ " + self.lineEdit_hera_freq.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_freq_eeprom_2 (self):
        print ("Freq 2 working!")
        # Write to device freq - EEPROM
        if (not self.lineEdit_hera_freq_2.isModified()):
            return
        self.lineEdit_hera_freq_2.setModified(False)
        command_py = ":EEPROM:CONFigure:AUTO:FREQ " + self.lineEdit_hera_freq_2.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()
    
    def hera_write_avg_eeprom (self):
        print ("Avg EEPROM working!")
        # Write to device avg - EEPROM
        if (not self.lineEdit_hera_avg_eeprom.isModified()):
            return
        self.lineEdit_hera_avg_eeprom.setModified(False)
        command_py = ":EEPROM:CONFigure:SPAVG " + self.lineEdit_hera_avg_eeprom.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_autorange_memory (self):
        # Write to device autorange - Internal memory
        ar_value = self.comboBox_hera_autorange.currentIndex()
        # Catch if we put a placeholder on autorange combobox
        if ar_value < 0:
            return
        command_py = ":SENSe:SP:AUTORANGE " + str (ar_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_autorange_eeprom (self):
        # Write to device autorange - EEPROM
        ar_value = self.comboBox_hera_autorange_eeprom.currentIndex()
        # Catch if we put a placeholder on autorange combobox
        if ar_value < 0:
            return
        command_py = ":EEPROM:CONFigure:AUTORANGE " + str (ar_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()
        
    def hera_write_userabs_eeprom (self):
        # Write to device abolute calibration mode - EEPROM
        userabs_value = self.comboBox_hera_abs_cal_method_eeprom.currentIndex()
        command_py = ":EEPROM:CONFigure:USERABS " + str (userabs_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_cal_memory (self):
        # Write to device calibration mode - Internal Memory
        cal_value = self.comboBox_hera_cal_memory.currentIndex()
        command_py = ":SENSe:CAL " + str (cal_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_res_eeprom (self):
        # Write to device resolution - EEPROM
        res_value = self.comboBox_hera_res_eeprom.currentIndex()
        command_py = ":EEPROM:CONFigure:RES " + str (res_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_res_memory_write_only (self):
        # Write to device resolution - Internal Memory
        res_value = self.comboBox_hera_res_write_only.currentIndex()
        command_py = ":SENSe:RES " + str (res_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        print ("#######################################")
        print ("Executed resolution write-only to memory")
        print ("#######################################")
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_avg_memory (self):
        print ("Avg memory working!")
        # Write to device avg - Internal memory
        if (not self.lineEdit_hera_avg.isModified()):
            return
        self.lineEdit_hera_avg.setModified(False)
        command_py = ":SENSe:SP:AVERAGE " + self.lineEdit_hera_avg.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()


    def hera_write_int_time_eeprom (self):
        print ("Int. time EEPROM working!")
        # Write to device int time - EEPROM
        if (not self.lineEdit_hera_int_time_eeprom.isModified()):
            return
        self.lineEdit_hera_int_time_eeprom.setModified(False)
        command_py = ":EEPROM:CONFigure:SPINT " + self.lineEdit_hera_int_time_eeprom.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_int_time_memory (self):
        print ("Int. time Internal memory working!")
        # Write to device int time - memory
        if (not self.lineEdit_hera_int_time.isModified()):
            return
        self.lineEdit_hera_int_time.setModified(False)
        command_py = ":SENSe:INT " + self.lineEdit_hera_int_time.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_max_int_time_eeprom (self):
        print ("Max. Int. time EEPROM working!")
        # Write to device max int time - EEPROM
        if (not self.lineEdit_hera_max_int_time.isModified()):
            return
        self.lineEdit_hera_max_int_time.setModified(False)

        # Check minimum value allowed for Max. Int. Time
        minimum_max_int_time = int (1000000 / int (self.lineEdit_hera_freq.text()))
        if int (self.lineEdit_hera_max_int_time.text()) < minimum_max_int_time:
            self.statusbar.showMessage (f"Minimum value for Max. Int. Time is {minimum_max_int_time} μs at {int (self.lineEdit_hera_freq.text())} Hz",10000)
            self.colorimeter_reload_parameters()
            return


        command_py = ":EEPROM:CONFigure:AUTO:MAXINT " + self.lineEdit_hera_max_int_time.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()


    def hera_write_adjmin_eeprom (self):
        print ("Adj min working!")
        # Write to device adjmin - EEPROM
        if (not self.lineEdit_hera_adjmin.isModified()):
            return
        self.lineEdit_hera_adjmin.setModified(False)
        command_py = ":EEPROM:CONFigure:AUTO:ADJMIN " + self.lineEdit_hera_adjmin.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()
   
    def hera_write_adjmin_eeprom_2 (self):
        print ("Adj min working!")
        # Write to device adjmin - EEPROM
        if (not self.lineEdit_hera_adjmin_2.isModified()):
            return
        self.lineEdit_hera_adjmin_2.setModified(False)
        command_py = ":EEPROM:CONFigure:AUTO:ADJMIN " + self.lineEdit_hera_adjmin_2.text() + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()
    
    def hera_write_sbw_eeprom (self):
        # Write to device calibration matrix (sbw) - eeprom
        sbw_string = self.comboBox_hera_sbw.currentText()
        if sbw_string == "off":
            command_py = ":EEPROM:CONFigure:SPSBW 0\n"
        else:
            command_py = ":EEPROM:CONFigure:SPSBW 1\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        print ("#################")
        print (f"I am working sbw_string is {sbw_string}")
        print ("#################")
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_sbw_memory_write_only (self):
        # Write to device calibration matrix (sbw) - eeprom
        sbw_string = self.comboBox_hera_sbw_write_only.currentText()
        command_py = ":SENSe:SP:SBW " + sbw_string + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        print ("#################")
        print ("I am working")
        print ("#################")
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()


    def hera_write_std_illuminant_eeprom (self):
        # Write to device std illuminant - EEPROM
        std_illuminant_string = "{:>4}".format(self.comboBox_hera_std_illuminant_eeprom.currentText())
        command_py = ":EEPROM:CONFigure:WHITE " + std_illuminant_string + "\n"
        # command_py = ":EEPROM:CONFigure:WHITE FL5\n"
        print (command_py)
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()





    def hera_write_interp_method_eeprom (self):
        # Write to device interp method - EEPROM
        interp_method_value = self.comboBox_hera_interp_method_eeprom.currentIndex()
        command_py = ":EEPROM:CONFigure:INTERPOL " + str(interp_method_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()

    def hera_write_interp_method_memory (self):
        # Write to device interp method - Internal Memory
        interp_method_value = self.comboBox_hera_interp_method.currentIndex()
        command_py = ":SENSe:INTERPOL " + str(interp_method_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        print ("#######################################")
        print ("Executed interp method to memory")
        print ("#######################################")
        self.function_result_to_statusbar (command_py, error_write, "")
        self.hera_reload_parameters()


    def colorimeter_write_automode (self):
        # Write to device automode
        automode_value = self.comboBox_automode.currentIndex()
        if automode_value == 5:
            automode_value = 255 # Not Set!
        command_py = ":SENSe:AUTOMODE " + str(automode_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()
        
    def colorimeter_write_shutter_state (self):
        # Write to device shutter state
        shutter_state_value = self.comboBox_shutter.currentIndex()
        command_py = ":SENSe:SHUTter " + str(shutter_state_value) + "\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        
        # Read from device Autorange the result of shutter command
        command_py_ar = ":SENSe:AUTOrange?\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write_ar = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)

        # print ("-"+ read_data.value.decode("utf-8")[:error_read].strip() + "-")

        
        if (read_data.value.decode("utf-8")[:error_read].strip() == "Closed"):
            autorange_report_on_shutter = " Auto-range reported: Shutter closed!"
        elif (read_data.value.decode("utf-8")[:error_read].strip() == "Opened"):
            autorange_report_on_shutter = " Auto-range reported: Shutter opened!"
        else:
            autorange_report_on_shutter = " Auto-range reported: No report on shutter operation!"
            
        self.function_result_to_statusbar (command_py, error_write, autorange_report_on_shutter)
        self.colorimeter_reload_parameters()

    def colorimeter_eeprom_write (self):
        # :EEPROM:STARTUP:WRITE 
        command_py = ":EEPROM:STARTUP:WRITE\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, " Startup values updated!")
        sleep (1)
        self.colorimeter_reload_parameters()

    def hera_eeprom_write (self):
        # :EEPROM:STARTUP:WRITE 
        command_py = ":EEPROM:STARTUP:WRITE\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, " Startup values updated!")
        sleep (1)
        self.hera_reload_parameters()

    def colorimeter_eeprom_read (self):
        # :EEPROM:STARTUP:READ 
        command_py = ":EEPROM:STARTUP:READ\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, " Startup values copied from EEPROM to internal memory!")
        # sleep (3)
        self.colorimeter_reload_parameters()

    def hera_eeprom_read (self):
        # :EEPROM:STARTUP:READ 
        command_py = ":EEPROM:STARTUP:READ\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        self.function_result_to_statusbar (command_py, error_write, " Startup values copied from EEPROM to internal memory!")
        # sleep (3)
        self.hera_reload_parameters()

    def reboot_device (self):
        # Reboot device
        command_py = ":BOOT:REBOOT \n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
        full_result = read_data.value.decode("utf-8")[:error_read].strip()
        # print (f"BOOT result is -{full_result}-")

        # Close device
        error_close = py_usbtmc_close (ptr_handle_colorimeter)
        # print (f"Close function error returned = {error_close}")
        if error_close == 0:
            close_msg = " usbtmc_close report: Device closed!"
        else:
            close_msg = " usbtmc_close report: Error closing device!"

        self.pushButton_connect.setChecked (False)
        self.pushButton_connect.setText ("CONNECT")
        self.pushButton_connect.setStyleSheet ("QPushButton {background-color:lightgreen}")
        self.function_result_to_statusbar (command_py, error_write, close_msg + " Wait for the probe to reboot, then press CONNECT!")
        self.disable_interface_pcm2x()

    def measure_dut_freq (self):
        # Measure DUT Freq
        command_py = ":MEASure:FREQuency 3125\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
            error_write_freq = py_usbtmc_write(ptr_handle_colorimeter, command_py_freq.encode('ASCII'), buffer_length, timeout_ms)
            self.colorimeter_reload_parameters()

        self.function_result_to_statusbar (command_py, error_write, "")

    def measure_dut_fund_freq (self):
        # Measure DUT Freq
        command_py = ":MEASure:FUNDFREQ 3125\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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
            self.lineEdit_measure_all_clip.setStyleSheet ("QLineEdit {background-color:lightcoral}")
        else:
            self.lineEdit_measure_all_clip.setText("No")
            self.lineEdit_measure_all_clip.setStyleSheet ("")
        if int (measure_all_result.split(",")[13]):
            self.lineEdit_measure_all_noise.setText("Yes!!!")
            self.lineEdit_measure_all_noise.setStyleSheet ("QLineEdit {background-color:lightcoral}")
        else:
            self.lineEdit_measure_all_noise.setText("No")
            self.lineEdit_measure_all_noise.setStyleSheet ("")

        self.measure_arparms("from_measure_all")
        self.function_result_to_statusbar (command_py, error_write, "")
        self.colorimeter_reload_parameters()

    def hera_measure_Yxy (self):
        # Measure Yxy - HERA
        
        self.clean_measure_Yxy_interface()
        self.label_meas_time_Yxy.setText("Measuring...")
        self.label_meas_time_Yxy.repaint()
        
        command_py = ":MEASure:Yxy\n"
        buffer_length = len (command_py)
        timeout_ms = 30000
        tic = time.perf_counter()
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        if not (error_write < 0):
            bytecount = 4096
            read_data = ctypes.create_string_buffer (bytecount)
            error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
            print (f"measure Yxy error read is {error_read}")
            toc = time.perf_counter()
            if not (error_read < 0):
                measure_all_result = read_data.value.decode("utf-8")[:error_read].strip()
                print (f":MEASure:Yxy result is -{measure_all_result}-")

                self.label_meas_time_Yxy.setText (f"Measured in: {toc - tic:0.2f} sec.")
                self.lineEdit_hera_measure_Yxy_Y.setText(str(float (measure_all_result.split(",")[0])))
                self.lineEdit_hera_measure_Yxy_x.setText(str(float (measure_all_result.split(",")[1])))
                self.lineEdit_hera_measure_Yxy_y.setText(str(float (measure_all_result.split(",")[2])))
                
                if int (measure_all_result.split(",")[3]):
                    self.lineEdit_hera_measure_Yxy_clip.setText("Yes!!!")
                    self.lineEdit_hera_measure_Yxy_clip.setStyleSheet ("QLineEdit {background-color:lightcoral}")
                else:
                    self.lineEdit_hera_measure_Yxy_clip.setText("No")
                    self.lineEdit_hera_measure_Yxy_clip.setStyleSheet ("")
                if int (measure_all_result.split(",")[4]):
                    self.lineEdit_hera_measure_Yxy_noise.setText("Yes!!!")
                    self.lineEdit_hera_measure_Yxy_noise.setStyleSheet ("QLineEdit {background-color:lightcoral}")
                else:
                    self.lineEdit_hera_measure_Yxy_noise.setText("No")
                    self.lineEdit_hera_measure_Yxy_noise.setStyleSheet ("")
                
                self.function_result_to_statusbar (command_py, error_write, "")
                self.hera_reload_parameters()
            else:
                self.function_result_to_statusbar (command_py, error_read, "")
                return
        else:
            self.function_result_to_statusbar (command_py, error_write, "")



    def clean_measure_Yxy_interface (self):
        # Clean command interface
        self.label_meas_time_Yxy.clear()
        self.lineEdit_hera_measure_Yxy_clip.clear()
        self.lineEdit_hera_measure_Yxy_clip.setStyleSheet ("")
        self.lineEdit_hera_measure_Yxy_noise.clear()
        self.lineEdit_hera_measure_Yxy_noise.setStyleSheet ("")
        self.lineEdit_hera_measure_Yxy_Y.clear()
        self.lineEdit_hera_measure_Yxy_x.clear()
        self.lineEdit_hera_measure_Yxy_y.clear()

        self.label_meas_time_Yxy.repaint()
        self.lineEdit_hera_measure_Yxy_clip.repaint()
        self.lineEdit_hera_measure_Yxy_noise.repaint()
        self.lineEdit_hera_measure_Yxy_Y.repaint()
        self.lineEdit_hera_measure_Yxy_x.repaint()
        self.lineEdit_hera_measure_Yxy_y.repaint()


    def hera_measure_XYZ (self):
        # Measure XYZ - HERA

        self.clean_measure_XYZ_interface()
        self.label_meas_time_XYZ.setText("Measuring...")
        self.label_meas_time_XYZ.repaint()

        command_py = ":MEASure:XYZ\n"
        buffer_length = len (command_py)
        timeout_ms = 30000
        tic = time.perf_counter()
        error_write = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        if not (error_write < 0):
            bytecount = 4096
            read_data = ctypes.create_string_buffer (bytecount)
            error_read = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
            toc = time.perf_counter()
            if not (error_read < 0):
                measure_all_result = read_data.value.decode("utf-8")[:error_read].strip()
                print (f":MEASure:XYZ result is -{measure_all_result}-")

                self.label_meas_time_XYZ.setText (f"Measured in: {toc - tic:0.2f} sec.")
                self.lineEdit_hera_measure_XYZ_X.setText(str(float (measure_all_result.split(",")[0])))
                self.lineEdit_hera_measure_XYZ_Y.setText(str(float (measure_all_result.split(",")[1])))
                self.lineEdit_hera_measure_XYZ_Z.setText(str(float (measure_all_result.split(",")[2])))
                
                if int (measure_all_result.split(",")[3]):
                    self.lineEdit_hera_measure_XYZ_clip.setText("Yes!!!")
                    self.lineEdit_hera_measure_XYZ_clip.setStyleSheet ("QLineEdit {background-color:lightcoral}")
                else:
                    self.lineEdit_hera_measure_XYZ_clip.setText("No")
                    self.lineEdit_hera_measure_XYZ_clip.setStyleSheet ("")
                if int (measure_all_result.split(",")[4]):
                    self.lineEdit_hera_measure_XYZ_noise.setText("Yes!!!")
                    self.lineEdit_hera_measure_XYZ_noise.setStyleSheet ("QLineEdit {background-color:lightcoral}")
                else:
                    self.lineEdit_hera_measure_XYZ_noise.setText("No")
                    self.lineEdit_hera_measure_XYZ_noise.setStyleSheet ("")

                self.function_result_to_statusbar (command_py, error_write, "")
                self.hera_reload_parameters()
            else:
                self.function_result_to_statusbar (command_py, error_read, "")
                return
        else:
            self.function_result_to_statusbar (command_py, error_write, "")


    def clean_measure_XYZ_interface (self):
        # Clean command interface
        self.label_meas_time_XYZ.clear()
        self.lineEdit_hera_measure_XYZ_clip.clear()
        self.lineEdit_hera_measure_XYZ_clip.setStyleSheet ("")
        self.lineEdit_hera_measure_XYZ_noise.clear()
        self.lineEdit_hera_measure_XYZ_noise.setStyleSheet ("")
        self.lineEdit_hera_measure_XYZ_X.clear()
        self.lineEdit_hera_measure_XYZ_Y.clear()
        self.lineEdit_hera_measure_XYZ_Z.clear()

        self.label_meas_time_XYZ.repaint()
        self.lineEdit_hera_measure_XYZ_clip.repaint()
        self.lineEdit_hera_measure_XYZ_noise.repaint()
        self.lineEdit_hera_measure_XYZ_X.repaint()
        self.lineEdit_hera_measure_XYZ_Y.repaint()
        self.lineEdit_hera_measure_XYZ_Z.repaint()

    def measure_arparms (self, who_is_calling):
        # Measure Auto-range parameters used in last measurement
        command_py = ":MEASure:ARPARMS\n"
        buffer_length = len (command_py)
        timeout_ms = 5000
        error_write = py_usbtmc_write(ptr_handle_colorimeter, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 4096
        read_data = ctypes.create_string_buffer (bytecount)
        error_read = py_usbtmc_read (ptr_handle_colorimeter, read_data, bytecount, timeout_ms)
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

    def hera_measure_spectrum (self):
        # Measure Hera spectrum
        command_py = ":MEASure:SPECtrum\n"
        buffer_length = len (command_py)
        timeout_ms = 30000
        error_write_spectrum = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 8192
        read_data = ctypes.create_string_buffer (bytecount)
        
        error_read_spectrum = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
        
        print (f"error_write_spectrum is {error_write_spectrum}")
        print (f"error_read_spectrum is {error_read_spectrum}")
         
        spectrum = frombuffer (read_data, dtype='>f', count=int (error_read_spectrum/4)) # >f = big-endian (MSB first)
        set_printoptions(suppress=True)
        print (spectrum[0:])
        print (type(spectrum))
        print("Shape:", spectrum.shape)  
        print("Dimensions:", spectrum.ndim)  
        print("Size:", spectrum.size) 
        print("Data type:", spectrum.dtype)  
        print("Item size:", spectrum.itemsize)
        savetxt("foo.csv", [spectrum], delimiter=",", fmt="%.6f")

    def hera_get_wavelengths (self):
        # Measure Hera spectrum
        command_py = ":GET:WAVElengths\n"
        buffer_length = len (command_py)
        timeout_ms = 30000
        error_write_get_wavelengths = py_usbtmc_write(ptr_handle_spectro, command_py.encode('ASCII'), buffer_length, timeout_ms)
        bytecount = 8192
        read_data = ctypes.create_string_buffer (bytecount)
        
        error_read_get_wavelengths = py_usbtmc_read (ptr_handle_spectro, read_data, bytecount, timeout_ms)
              
        print (f"error_write_get_wavelengths is {error_write_get_wavelengths}")
        print (f"error_read_get_wavelengths is {error_read_get_wavelengths}")

        # get_wavelengths_result = read_data.value.decode("utf-8")[:error_read_get_wavelengths].strip()
        # print (f":GET:WAVElengths result is -{get_wavelengths_result}-")
   
        wl = numpy.frombuffer (read_data, dtype='>f', count=int (error_read_get_wavelengths/4)) # >f = big-endian (MSB first)
        print (wl[0:])
        print (type(wl))
        print("Shape:", wl.shape)  
        print("Dimensions:", wl.ndim)  
        print("Size:", wl.size) 
        print("Data type:", wl.dtype)  
        print("Item size:", wl.itemsize)

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
    handle_colorimeter = ctypes.c_uint32 (77) # Whatever value to initialize
    ptr_handle_colorimeter = ctypes.pointer (handle_colorimeter)

    # Global initialisation handle for spectro
    handle_spectro = ctypes.c_uint32 (99) # Whatever value to initialize
    ptr_handle_spectro = ctypes.pointer (handle_spectro)

    # Enable High DPI display with PyQt5
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    
    app = QApplication (sys.argv)
    window = MainUI()
    window.show()
    app.exec_()