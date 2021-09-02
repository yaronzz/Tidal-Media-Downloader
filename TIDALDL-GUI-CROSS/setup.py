from setuptools import setup, find_packages
setup(
    name = 'tidal-gui',
    version = '1.0.0.1',
    license = "Apache2",
    description = "Tidal Music Downloader.",

    author = 'YaronH',
    author_email = "yaronhuang@foxmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy", "PyQt5", "requests>=2.22.0", "pycryptodome", "pydub", "prettytable", "lyricsgenius"],
    entry_points={'console_scripts': [ 'tidal-gui = tidal_gui:main', ]}
)
