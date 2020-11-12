from setuptools import setup, find_packages
from tidal_dl.printf import VERSION
setup(
    name = 'tidal-dl',
    version = VERSION,
    license = "Apache2",
    description = "Tidal Music Downloader.",

    author = 'YaronH',
    author_email = "yaronhuang@foxmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=2020.11.10.0", "requests", "pycryptodome", "pydub", "prettytable"],
    entry_points={'console_scripts': [ 'tidal-dl = tidal_dl:main', ]}
)
