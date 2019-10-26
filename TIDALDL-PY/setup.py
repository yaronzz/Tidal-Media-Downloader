from setuptools import setup, find_packages
setup(
    name = 'tidal-dl',
    version="2019.10.26.0",
    license="Apache2",
    description = "Tidal Music Download.",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=2019.9.20.2", "requests", "ffmpeg", "pycryptodome", "pydub", ],
    entry_points={'console_scripts': [ 'tidal-dl = tidal_dl:main', ]}
)
