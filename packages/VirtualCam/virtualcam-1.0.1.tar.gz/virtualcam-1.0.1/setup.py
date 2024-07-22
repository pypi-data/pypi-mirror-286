import codecs
import os
from setuptools import setup, find_packages
here=os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here,"README.md"),encoding="utf-8") as fh:
    long_description="\n"+fh.read()
VERSION='1.0.1'
DESCRIPTION='A model for virtual camera, including UI.'
setup(
    name="VirtualCam",
    version=VERSION,
    author="OscarMYH(myhldh)",
    author_email='oscarmyh@163.com',
    url='https://github.com/myhldh/VirtualCam',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
        'VirtualCam':['*.dll']
    },
    packages=find_packages(),
    license='MIT',
    install_requires=['numpy','opencv-python','Pillow','pyvirtualcam','keyboard'],
    keywords=['python','virtual camera','camera','virtual','computer vision','OscarMYH','myhldh','lightweight','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)