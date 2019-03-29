from setuptools import setup, find_packages
import tidal_dl.__init__ as init
setup(
    name = 'tidal-dl',
    version=init.TIDAL_DL_VERSION,
    license = "MIT Licence",
    description = "Tidal Music Download.",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=2019.3.29.2", "requests", "ffmpeg", "futures", "pycryptodome", "pydub"],

    entry_points={'console_scripts': [
        'tidal-dl = tidal_dl:main', ]}
)
