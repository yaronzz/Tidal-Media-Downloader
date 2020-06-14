from setuptools import setup, find_packages
setup(
    name = 'tidal-dl',
    version="2020.6.14.0",
    license="Apache2",
    description = "Tidal Music Downloader.",

    author = 'YaronH',
    author_email = "yaronhuang@foxmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=2020.5.4.0", "requests", "ffmpeg", "pycryptodome", "pydub", ],
    entry_points={'console_scripts': [ 'tidal-dl = tidal_dl:main', ]}
)
