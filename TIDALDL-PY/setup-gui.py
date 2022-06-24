from setuptools import setup, find_packages
setup(
    name = 'tidal-gui',
    version = '2022.01.18.3',
    license = "Apache2",
    description = "Tidal Music Downloader-GUI.",

    author = 'YaronH',
    author_email = "yaronhuang@foxmail.com",

    packages=find_packages(exclude=['tidal_dl*']),
    include_package_data = True,
    platforms = "any",
    install_requires=["tidal-dl"],
    entry_points={'console_scripts': [ 'tidal-gui = tidal_gui:main', ]}
)
