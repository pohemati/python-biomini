from datetime import datetime

import clr

from .utils import TemplateType
from .enroll import Enroll
from .exceptions import ScannerDetectionError
from .decorators import check_initialization

clr.AddReference('Suprema.UFScanner')
clr.AddReference('System')
clr.AddReference('System.Windows.Forms')

import System
from System.Windows.Forms import Form
from System import Array, Byte
from System.Drawing import Bitmap
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream
from Suprema import UFScanner, UFScannerManager, UFS_STATUS


class Biomini:
    def __init__(self):
        self._winform = Form()
        self._current_scanner = None
        self._initialized = False
        self._scanners = []
        self._scanner_manager = UFScannerManager(self._winform)

    def _init_manager(self):
        if not self._initialized:
            self._scanner_manager.Init()
            self._initialized = True
        self._current_scanner = None
        self._scanners.clear()

    @check_initialization
    def scanners(self):
        return self._scanners

    @check_initialization
    def scanners_count(self):
        return len(self._scanners)

    def detect_scanners(self):
        self._init_manager()
        self._scanners.clear()
        num_scanners = self._scanner_manager.Scanners.Count
        for i in range(num_scanners):
            scanner = self._scanner_manager.Scanners[i]
            self._scanners.append(scanner)
        if num_scanners == 1:
            self.current_scanner = self._scanners[0]
        return num_scanners

    @property
    @check_initialization
    def current_scanner(self):
        return self._current_scanner

    @current_scanner.setter
    def current_scanner(self, scanner):
        if self.scanners_count() == 0:
            self.detect_scanners()
        try:
            if scanner in self._scanners:
                self._current_scanner = scanner
            elif isinstance(scanner, int):
                self._current_scanner = self._scanners[scanner]
            elif isinstance(scanner, str):
                for i, s in enumerate(self._scanners):
                    if s.Serial == scanner:
                        self._current_scanner = self._scanners[i]
                        break
                else:
                    raise ScannerDetectionError(
                        f'Scanner with serial {scanner} '
                        f'not found.')
            else:
                raise ScannerDetectionError('Please select your target scanner'
                                            ' using it\'s index, serial or '
                                            'scanner object itself')
        except IndexError:
            raise ScannerDetectionError('Scanner index out of range')

    @check_initialization
    def enroll(self, template_type=TemplateType.ISO19794, image_format='png'):
        if self.scanners_count() == 0:
            raise ScannerDetectionError('No Biomini scanners detected. '
                                        'connect your scanner and call '
                                        '"detect_scanners" method '
                                        'to detect your scanner.')

        if template_type not in (TemplateType.ISO19794, TemplateType.SUPREMA,
                                 TemplateType.ANSI378):
            raise ValueError('Invalid template_type. '
                             'accepted values are TemplateType.ISO19794, '
                             'TemplateType.SUPREMA, and TemplateType.ANSI378.')

        if self.current_scanner is None:
            self.current_scanner = 0

        scanner = self.current_scanner
        enroll_ = Enroll()
        scanner.ClearCaptureImageBuffer()
        scanner.nTemplateType = template_type

        img_format_name = image_format.casefold()
        if img_format_name == 'png':
            _image_format = ImageFormat.Png
        elif img_format_name in ('jpg', 'jpeg'):
            _image_format = ImageFormat.Jpeg
        elif img_format_name == 'gif':
            _image_format = ImageFormat.Gif
        elif img_format_name == 'bmp':
            _image_format = ImageFormat.Bmp
        else:
            raise TypeError('Invalid image format. '
                            'supported types are png, jpg, gif and bmp.')

        extract_status, get_image_status = '', ''
        capture_status = scanner.CaptureSingleImage()
        enroll_.scanner_serial = scanner.Serial
        enroll_.scanner_type = str(scanner.ScannerType)
        enroll_.scanner_id = scanner.ID
        enroll_.template_type = scanner.nTemplateType
        if capture_status == UFS_STATUS.OK:
            template = Array.CreateInstance(Byte, 512)
            template_size = 50
            enroll_quality = 50
            extract_status, template_size, enroll_quality = scanner.Extract(
                template, template_size, enroll_quality
            )

            if extract_status == UFS_STATUS.OK:
                template = bytearray(template)
                _bitmap = Bitmap(256, 256)
                resolution = 500
                get_image_status, _bitmap, resolution = scanner.GetCaptureImageBuffer(
                    _bitmap, resolution
                )

                if get_image_status == UFS_STATUS.OK:
                    m_stream = MemoryStream()
                    _bitmap.Save(m_stream, _image_format)
                    image = bytearray(m_stream.ToArray())

        if (capture_status, extract_status, get_image_status) == \
                (UFS_STATUS.OK, UFS_STATUS.OK, UFS_STATUS.OK):
            enroll_.template = template
            enroll_.template_size = template_size
            enroll_.enroll_quality = enroll_quality
            enroll_.resolution = resolution
            enroll_.image = image
            enroll_.image_format = img_format_name
            enroll_.image_size = len(image)
            enroll_._status = 0
        else:
            enroll_._status = -1
        enroll_.enroll_time = datetime.now()
        return enroll_

    def uninit(self):
        if self._initialized:
            self._scanner_manager.Uninit()
        self._initialized = False
