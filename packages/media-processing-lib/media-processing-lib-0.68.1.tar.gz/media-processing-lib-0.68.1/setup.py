"""setup.py"""
from pathlib import Path
from setuptools import setup, find_packages

NAME = "media-processing-lib"
VERSION = "0.68.1"
DESCRIPTION = "Media processing library for video, audio and images."
URL = "https://gitlab.com/mihaicristianpirvu/media-processing-lib"

with open(f"{Path(__file__).absolute().parent}/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIRED = ["imageio[ffmpeg]==2.34.2", "av==12.3.0", "scikit-image==0.24.0", "opencv-python==4.7.0.68", "pims==0.7.0",
            "librosa==0.9.2", "numba==0.60.0", "ffmpeg-python==0.2.0", "tqdm>=4.64", "decord==0.6.0", "Pillow==9.4.0",
            "natsort==8.2.0", "numpy==1.26.4", "overrides>=7.7.0", "loggez==0.3", "gdown==4.6.0"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    dependency_links=[],
    license="WTFPL",
    python_requires=">=3.9",
)
