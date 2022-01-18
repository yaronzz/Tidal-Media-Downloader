cd TIDALDL-PY
rm -rf dist
rm -rf build 
rm -rf exe/tidal-dl.exe 
rm MANIFEST.in
rm -rf tidal_dl.egg-info
rm -rf tidal_gui.egg-info
rm -rf tidal_dl_test.egg-info

# pack
python setup.py sdist bdist_wheel
# creat exe file
pyinstaller -F tidal_dl/__init__.py
# rename exe name
mv dist/__init__.exe exe/tidal-dl.exe

pip uninstall -y tidal-dl

# creat requirements.txt
# pipreqs ./ --force --encoding=utf8

# python setup.py install

# upload
twine upload dist/*









cd TIDALDL-PY
rm -rf dist
rm -rf build 
rm -rf exe/tidal-gui.exe 
cp -rf guiStatic.in MANIFEST.in
rm -rf tidal_dl.egg-info
rm -rf tidal_gui.egg-info
rm -rf tidal_dl_test.egg-info

# pack
python setup-gui.py sdist bdist_wheel
# creat exe file
pyinstaller -F tidal_gui/__init__.py
# rename exe name
mv dist/__init__.exe exe/tidal-gui.exe

pip uninstall -y tidal-gui

# upload
twine upload dist/*
