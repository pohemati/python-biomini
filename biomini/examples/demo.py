from pprint import pprint

from biomini import Biomini, ScannerDetectionError


__version__ = (1, 2)
__app_name__ = 'python-biomini Demo App'
__author__ = 'Pouria Hemati (poria.hemati@gmail.com)'
__url__ = 'https://github.com/pohemati/python-biomini/'


bm = Biomini()
bm.detect_scanners()
if bm.scanners():
    bm.current_scanner = 0
    enroll = bm.enroll()
    pprint(enroll.to_dict(encoding='base64'))
else:
    raise ScannerDetectionError('No Suprema Biomini scanners detected.')
bm.uninit()
