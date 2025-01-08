from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import os


from biomini import Biomini, ScannerDetectionError, match_enrolls


__version__ = (1, 2)
__app_name__ = 'python-biomini (Suprema Biomini) PyQt5 Demo App'
__author__ = 'Pouria Hemati (poria.hemati@gmail.com)'
__url__ = 'https://github.com/pohemati/python-biomini/'


class DemoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left_enroll = None
        self.right_enroll = None
        self.setMinimumSize(600, 550)

        self.glayout = QtWidgets.QGridLayout(self)
        header_label = QtWidgets.QLabel('Suprema Biomini - PyQt5 Demo')
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        header_label.setFont(font)
        self.glayout.addWidget(header_label, 0, 0)

        self.hlayout = QtWidgets.QHBoxLayout()
        self.left_vlayout = QtWidgets.QVBoxLayout()
        self.left_hlayout = QtWidgets.QHBoxLayout()
        self.left_hlayout.addItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Maximum,
                                  QtWidgets.QSizePolicy.Maximum)
        )
        self.left_finger_print_pic_lbl = QtWidgets.QLabel()
        self.left_finger_print_pic_lbl.setMaximumSize(140, 180)
        self.left_finger_print_pic_lbl.setScaledContents(True)
        self.left_finger_print_pic_lbl.setFrameStyle(QtWidgets.QFrame.Box |
                                                     QtWidgets.QFrame.Plain)
        self.left_hlayout.addWidget(self.left_finger_print_pic_lbl)
        self.left_hlayout.addItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Maximum,
                                  QtWidgets.QSizePolicy.Expanding)
        )
        self.left_vlayout.addLayout(self.left_hlayout)

        self.left_blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.left_blur_effect.setBlurRadius(6)

        self.left_blur_chk = QtWidgets.QCheckBox('Blur Fingerprint Image')
        self.left_blur_chk.toggled.connect(self.left_blur_effect.setEnabled)
        self.left_blur_chk.setChecked(True)
        self.left_vlayout.addWidget(self.left_blur_chk)

        self.left_scanner_list_cmb = QtWidgets.QComboBox()
        self.left_vlayout.addWidget(self.left_scanner_list_cmb)

        self.left_enroll_btn = QtWidgets.QPushButton('Enroll')
        self.left_vlayout.addWidget(self.left_enroll_btn)
        self.left_grid_layout = QtWidgets.QGridLayout()
        self.left_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.left_grid_layout.setSpacing(3)

        self.left_t_status_lbl = QtWidgets.QLabel('Status:')
        self.left_grid_layout.addWidget(self.left_t_status_lbl, 0, 0)
        self.left_status_lbl = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_status_lbl, 0, 1)

        self.left_t_scnr_type_label = QtWidgets.QLabel('Device Type:')
        self.left_grid_layout.addWidget(self.left_t_scnr_type_label, 1, 0)
        self.left_scnr_type_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_scnr_type_label, 1, 1)

        self.left_t_scnr_id_label = QtWidgets.QLabel('Device ID:')
        self.left_grid_layout.addWidget(self.left_t_scnr_id_label, 2, 0)
        self.left_scnr_id_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_scnr_id_label, 2, 1)

        self.left_t_scnr_serial_label = QtWidgets.QLabel('Device Serial:')
        self.left_grid_layout.addWidget(self.left_t_scnr_serial_label, 3, 0)
        self.left_scnr_serial_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_scnr_serial_label, 3, 1)

        self.left_t_enroll_time_label = QtWidgets.QLabel('Enroll Time:')
        self.left_grid_layout.addWidget(self.left_t_enroll_time_label, 4, 0)
        self.left_enroll_time_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_enroll_time_label, 4, 1)

        self.left_t_enroll_quality_label = QtWidgets.QLabel('Enroll Quality:')
        self.left_grid_layout.addWidget(self.left_t_enroll_quality_label, 5, 0)
        self.left_enroll_quality_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_enroll_quality_label, 5, 1)

        self.left_t_resolution_label = QtWidgets.QLabel('Resolution:')
        self.left_grid_layout.addWidget(self.left_t_resolution_label, 6, 0)
        self.left_resolution_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_resolution_label, 6, 1)

        self.left_t_template_size_label = QtWidgets.QLabel('Template Size:')
        self.left_grid_layout.addWidget(self.left_t_template_size_label, 7, 0)
        self.left_template_size_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_template_size_label, 7, 1)

        self.left_t_template_type_label = QtWidgets.QLabel('Template Type:')
        self.left_grid_layout.addWidget(self.left_t_template_type_label, 8, 0)
        self.left_template_type_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_template_type_label, 8, 1)

        self.left_t_image_size_label = QtWidgets.QLabel('Image Size:')
        self.left_grid_layout.addWidget(self.left_t_image_size_label, 9, 0)
        self.left_image_size_label = QtWidgets.QLabel('-')
        self.left_grid_layout.addWidget(self.left_image_size_label, 9, 1)

        self.left_vlayout.addLayout(self.left_grid_layout)
        self.hlayout.addLayout(self.left_vlayout)

        vline = QtWidgets.QFrame()
        vline.setFrameShape(QtWidgets.QFrame.VLine)
        vline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hlayout.addWidget(vline)

        self.right_vlayout = QtWidgets.QVBoxLayout()
        self.right_hlayout = QtWidgets.QHBoxLayout()
        self.right_hlayout.addItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Maximum,
                                  QtWidgets.QSizePolicy.Maximum)
        )
        self.right_finger_print_pic_lbl = QtWidgets.QLabel()
        self.right_finger_print_pic_lbl.setMaximumSize(140, 180)
        self.right_finger_print_pic_lbl.setScaledContents(True)
        self.right_finger_print_pic_lbl.setFrameStyle(QtWidgets.QFrame.Box |
                                                      QtWidgets.QFrame.Plain)
        self.right_hlayout.addWidget(self.right_finger_print_pic_lbl)
        self.right_hlayout.addItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Maximum,
                                  QtWidgets.QSizePolicy.Expanding)
        )
        self.right_vlayout.addLayout(self.right_hlayout)

        self.right_blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.right_blur_effect.setBlurRadius(6)

        self.right_blur_chk = QtWidgets.QCheckBox('Blur Fingerprint Image')
        self.right_blur_chk.toggled.connect(self.right_blur_effect.setEnabled)
        self.right_blur_chk.setChecked(True)
        self.right_vlayout.addWidget(self.right_blur_chk)

        self.right_scanner_list_cmb = QtWidgets.QComboBox()
        self.right_vlayout.addWidget(self.right_scanner_list_cmb)

        self.right_enroll_btn = QtWidgets.QPushButton('Enroll')
        self.right_vlayout.addWidget(self.right_enroll_btn)
        self.right_grid_layout = QtWidgets.QGridLayout()
        self.right_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.right_grid_layout.setSpacing(3)

        self.right_t_status_lbl = QtWidgets.QLabel('Status:')
        self.right_grid_layout.addWidget(self.right_t_status_lbl, 0, 0)
        self.right_status_lbl = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_status_lbl, 0, 1)

        self.right_t_scnr_type_label = QtWidgets.QLabel('Device Type:')
        self.right_grid_layout.addWidget(self.right_t_scnr_type_label, 1, 0)
        self.right_scnr_type_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_scnr_type_label, 1, 1)

        self.right_t_scnr_id_label = QtWidgets.QLabel('Device ID:')
        self.right_grid_layout.addWidget(self.right_t_scnr_id_label, 2, 0)
        self.right_scnr_id_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_scnr_id_label, 2, 1)

        self.right_t_scnr_serial_label = QtWidgets.QLabel('Device Serial:')
        self.right_grid_layout.addWidget(self.right_t_scnr_serial_label, 3, 0)
        self.right_scnr_serial_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_scnr_serial_label, 3, 1)

        self.right_t_enroll_time_label = QtWidgets.QLabel('Enroll Time:')
        self.right_grid_layout.addWidget(self.right_t_enroll_time_label, 4, 0)
        self.right_enroll_time_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_enroll_time_label, 4, 1)

        self.right_t_enroll_quality_label = QtWidgets.QLabel('Enroll Quality:')
        self.right_grid_layout.addWidget(self.right_t_enroll_quality_label, 5, 0)
        self.right_enroll_quality_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_enroll_quality_label, 5, 1)

        self.right_t_resolution_label = QtWidgets.QLabel('Resolution:')
        self.right_grid_layout.addWidget(self.right_t_resolution_label, 6, 0)
        self.right_resolution_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_resolution_label, 6, 1)

        self.right_t_template_size_label = QtWidgets.QLabel('Template Size:')
        self.right_grid_layout.addWidget(self.right_t_template_size_label, 7, 0)
        self.right_template_size_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_template_size_label, 7, 1)

        self.right_t_template_type_label = QtWidgets.QLabel('Template Type:')
        self.right_grid_layout.addWidget(self.right_t_template_type_label, 8, 0)
        self.right_template_type_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_template_type_label, 8, 1)

        self.right_t_image_size_label = QtWidgets.QLabel('Image Size:')
        self.right_grid_layout.addWidget(self.right_t_image_size_label, 9, 0)
        self.right_image_size_label = QtWidgets.QLabel('-')
        self.right_grid_layout.addWidget(self.right_image_size_label, 9, 1)

        self.right_vlayout.addLayout(self.right_grid_layout)
        self.hlayout.addLayout(self.right_vlayout)

        self.glayout.addLayout(self.hlayout, 1, 0)

        bottom_glayout = QtWidgets.QGridLayout()
        self.detect_scanner_btn = QtWidgets.QPushButton('Detect Scanners')
        self.detect_scanner_btn.clicked.connect(self.detect_scanners)
        bottom_glayout.addWidget(self.detect_scanner_btn, 0, 0)
        bottom_glayout.addItem(
            QtWidgets.QSpacerItem(130, 40, QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Maximum), 0, 1
        )
        self.match_button = QtWidgets.QPushButton('Match')
        self.match_button.setMinimumWidth(120)
        bottom_glayout.addWidget(self.match_button, 0, 2)
        bottom_glayout.addItem(
            QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Maximum), 0, 3
        )
        self.match_result_label = QtWidgets.QLabel()
        self.match_result_label.setAlignment(QtCore.Qt.AlignCenter)
        bottom_glayout.addWidget(self.match_result_label, 1, 2)

        self.glayout.addLayout(bottom_glayout, 2, 0)
        self.setLayout(self.glayout)

        self.pbm = Biomini()
        self.detect_scanners()

        self.left_enroll_btn.clicked.connect(self.start_left_enroll)
        self.right_enroll_btn.clicked.connect(self.start_right_enroll)
        self.match_button.clicked.connect(self.match_enrolls)

    def start_left_enroll(self):
        try:
            self.pbm.current_scanner = self.left_scanner_list_cmb.currentIndex()
            self.left_enroll = self.pbm.enroll()
        except ScannerDetectionError:
            self.left_enroll = None
            QtWidgets.QMessageBox.critical(
                self, 'Error',
                'Error detecting Suprema Biomini scanner. '
                'ensure scanner is connected and it\'s driver is already installed. '
                'also check the required libraries and dll files existence.'
            )
        else:
            self.match_result_label.clear()
            d = self.left_enroll.to_dict(encoding=None)
            if d['success']:
                enroll_time = d['enroll_time'].strftime('%Y-%m-%d %H:%M:%S')
                self.left_status_lbl.setText('OK')
                self.left_status_lbl.setStyleSheet('color: green;')
                self.left_finger_print_pic_lbl\
                    .setPixmap(self.left_enroll.to_pyqt5_pixmap())
                self.left_scnr_id_label.setText(d['scanner_id'])
                self.left_scnr_type_label.setText(d['scanner_type'])
                self.left_scnr_serial_label.setText(d['scanner_serial'])
                self.left_enroll_time_label.setText(enroll_time)
                self.left_enroll_quality_label.setText(str(d['enroll_quality']))
                self.left_resolution_label.setText(str(d['resolution']))
                self.left_template_size_label.setText(str(d['template_size']))
                self.left_template_type_label.setText(str(d['template_type']))
                self.left_image_size_label.setText(str(d['image_size']))
                self.left_finger_print_pic_lbl\
                    .setGraphicsEffect(self.left_blur_effect)
            else:
                self.left_status_lbl.setText('Failed')
                self.left_status_lbl.setStyleSheet('color: red;')
                self.left_finger_print_pic_lbl.clear()
                self.left_scnr_id_label.setText('-')
                self.left_scnr_type_label.setText('-')
                self.left_scnr_serial_label.setText('-')
                self.left_enroll_time_label.setText('-')
                self.left_enroll_quality_label.setText('-')
                self.left_resolution_label.setText('-')
                self.left_template_size_label.setText('-')
                self.left_template_type_label.setText('-')
                self.left_image_size_label.setText('-')

    def start_right_enroll(self):
        try:
            self.pbm.current_scanner = self.right_scanner_list_cmb.currentIndex()
            self.right_enroll = self.pbm.enroll()
        except ScannerDetectionError:
            self.right_enroll = None
            QtWidgets.QMessageBox.critical(
                self, 'Error',
                'Error detecting Suprema Biomini scanner. '
                'ensure scanner is connected and it\'s driver is already installed. '
                'also check the required dll files existence.'
            )
        else:
            self.match_result_label.clear()
            d = self.right_enroll.to_dict(encoding=None)
            if d['success']:
                enroll_time = d['enroll_time'].strftime('%Y-%m-%d %H:%M:%S')
                self.right_status_lbl.setText('OK')
                self.right_status_lbl.setStyleSheet('color: green;')
                self.right_finger_print_pic_lbl \
                    .setPixmap(self.right_enroll.to_pyqt5_pixmap())
                self.right_scnr_id_label.setText(d['scanner_id'])
                self.right_scnr_type_label.setText(d['scanner_type'])
                self.right_scnr_serial_label.setText(d['scanner_serial'])
                self.right_enroll_time_label.setText(enroll_time)
                self.right_enroll_quality_label\
                    .setText(str(d['enroll_quality']))
                self.right_resolution_label.setText(str(d['resolution']))
                self.right_template_size_label.setText(str(d['template_size']))
                self.right_template_type_label.setText(str(d['template_type']))
                self.right_image_size_label.setText(str(d['image_size']))
                self.right_finger_print_pic_lbl\
                    .setGraphicsEffect(self.right_blur_effect)
            else:
                self.right_status_lbl.setText('Failed')
                self.right_status_lbl.setStyleSheet('color: red;')
                self.right_finger_print_pic_lbl.clear()
                self.right_scnr_id_label.setText('-')
                self.right_scnr_type_label.setText('-')
                self.right_scnr_serial_label.setText('-')
                self.right_enroll_time_label.setText('-')
                self.right_enroll_quality_label.setText('-')
                self.right_resolution_label.setText('-')
                self.right_template_size_label.setText('-')
                self.right_template_type_label.setText('-')
                self.right_image_size_label.setText('-')

    def detect_scanners(self):
        self.pbm.detect_scanners()
        self.left_scanner_list_cmb.clear()
        self.right_scanner_list_cmb.clear()
        if self.pbm.scanners:
            for scanner in self.pbm.scanners():
                self.left_scanner_list_cmb.addItem(scanner.Serial)
                self.right_scanner_list_cmb.addItem(scanner.Serial)

    def match_enrolls(self):
        if not self.left_enroll:
            QtWidgets.QMessageBox.critical(
                self, 'Error',
                'Please enroll left side\'s fingerprint.'
            )
            return
        if not self.right_enroll:
            QtWidgets.QMessageBox.critical(
                self, 'Error',
                'Please enroll right side\'s fingerprint.'
            )
            return
        result = match_enrolls(self.left_enroll, self.right_enroll)
        if result:
            self.match_result_label.setStyleSheet('color: green;')
            self.match_result_label.setText('Fingerprin matched.')
        else:
            self.match_result_label.setStyleSheet('color: red;')
            self.match_result_label.setText('Fingerprin didn\'t match.')


if __name__ == '__main__':
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setStyle('fusion')

    demo_dialog = DemoDialog()
    demo_dialog.setWindowTitle(__app_name__)
    demo_dialog.show()
    sys.exit(app.exec())
