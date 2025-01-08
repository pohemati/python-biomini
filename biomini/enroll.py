import binascii
import json
import io

from os.path import splitext


class Enroll:
    def __init__(self):
        self._status = -1
        self.template = None
        self.template_type = None
        self.template_size = 0
        self.enroll_quality = 0
        self.image = None
        self.image_format = None
        self.scanner_serial = ''
        self.scanner_type = ''
        self.scanner_id = None
        self.image_size = 0
        self.enroll_time = None
        self.resolution = 0

    @property
    def success(self):
        return self._status == 0

    def to_json(self, encoding='base64'):
        if encoding not in ('hex', 'base64'):
            raise ValueError('encoding should be \'hex\' or \'base64\'')
        return json.dumps(self.to_dict(encoding), default=str)

    def to_dict(self, encoding=None):
        if encoding not in (None, 'hex', 'base64'):
            raise ValueError('encoding should be None, \'hex\' or \'base64\'')
        d = {
            'success': self.success,
            'template': self.template,
            'template_type': self.template_type,
            'template_size': self.template_size,
            'enroll_quality': self.enroll_quality,
            'image': self.image,
            'image_format': self.image_format,
            'image_size': self.image_size,
            'scanner_serial': self.scanner_serial,
            'scanner_type': self.scanner_type,
            'scanner_id': self.scanner_id,
            'enroll_time': self.enroll_time,
            'resolution': self.resolution,
        }
        if encoding:
            if encoding == 'hex':
                encoder = binascii.b2a_hex
            else:
                encoder = binascii.b2a_base64
            d['template'] = encoder(d['template']).decode('utf-8')
            d['image'] = encoder(d['image']).decode('utf-8')
        return d

    def to_pyqt5_image(self):
        from PyQt5.QtGui import QImage
        img = QImage.fromData(self.image)
        return img

    def to_pyqt5_pixmap(self):
        from PyQt5.QtGui import QPixmap
        return QPixmap.fromImage(self.to_pyqt5_image())

    def to_pyqt6_image(self):
        from PyQt6.QtGui import QImage
        img = QImage.fromData(self.image)
        return img

    def to_pyqt6_pixmap(self):
        from PyQt6.QtGui import QPixmap
        return QPixmap.fromImage(self.to_pyqt6_image())

    def bytes_io_image(self):
        return io.BytesIO(self.image)

    def to_pil_image(self):
        from PIL import Image as PILImage
        img = PILImage.open(self.bytes_io_image())
        return img

    def save_image(self, save_path):
        path, ext = splitext(save_path)
        ext = ext[1:] if ext else ''
        if not ext:
            ext = self.image_format
            save_path += '.' + self.image_format
        if ext != self.image_format.casefold():
            img = self.to_pil_image()
            img.convert('RGB').save(save_path)
        else:
            with open(save_path, 'wb') as f:
                f.write(self.image)
