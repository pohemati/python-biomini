from distutils.core import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-biomini',
    packages=['biomini', 'biomini.examples'],
    version='1.4',
    license='MIT',
    description='A Python interface for Suprema Biomini fingerprint scanners.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='Poria Hemati',
    author_email='poria.hemati@gmail.com',
    url='https://github.com/pohemati/python-biomini',
    download_url='https://github.com/pohemati/python-biomini/archive/refs/tags/v1.4.tar.gz',
    keywords=['python', 'suprema', 'biomini', 'fingerprint', 'scanner',
              'enrollment', 'biometric'],
    install_requires=[
        'pythonnet>=3.0.1',
    ],
    extras_require = {
        'pil': ['pillow'],
        'pyqt5': ['pyqt5'],
        'pyqt6': ['pyqt6'],
        'pyside6': ['pyside6'],
    },
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
