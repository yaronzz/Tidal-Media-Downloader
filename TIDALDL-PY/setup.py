from setuptools import setup, find_packages
from tidal_dl.printf import VERSION

setup(
    name='tidal-dl',
    version=VERSION,
    license="Apache2",
    description="Tidal Music Downloader.",

    author='YaronH',
    author_email="yaronhuang@foxmail.com",

    packages=find_packages(exclude=['tidal_gui*']),
    include_package_data=False,
    platforms="any",
    install_requires=["aigpy>=2022.01.18.2", "requests>=2.22.0",
                      "pycryptodome", "pydub", "prettytable", "lyricsgenius"],
    entry_points={'console_scripts': ['tidal-dl = tidal_dl:main', ]}
)
