rm -rf dist
rm -rf build 
rm -rf exe 
rm -rf tidal_dl.egg-info
mkdir exe

# pack
python setup.py sdist bdist_wheel
# creat exe file
pyinstaller -F tidal_dl/__init__.py
# rename exe name
mv dist/__init__.exe exe/tidal-dl.exe

pip uninstall -y tidal-dl

# creat requirements.txt
# pipreqs ./ --force

# python setup.py install

# upload
twine upload dist/*







# powershell
cd TIDALDL-PY
Remove-Item dist -recurse -Force
Remove-Item build -recurse -Force
Remove-Item exe -recurse -Force
Remove-Item tidal_dl.egg-info -recurse -Force
md exe

# pack
python setup.py sdist bdist_wheel
# creat exe file
pyinstaller -F tidal_dl/__init__.py
#pyinstaller -F -i ../logo.ico tidal_dl/__init__.py
# rename exe name
cp dist/__init__.exe exe/tidal-dl.exe
rm dist/__init__.exe

pip uninstall -y tidal-dl

# creat requirements.txt
# pipreqs ./ --force

# python setup.py install

# upload
twine upload dist/*

[TEST-VERSION]
TYPE tidal-dl
USE  pip3 install tidal-dl --upgrade
#### v2020-10-13 
- [x] Settings: album folder format、track file format

If there are any bugs or suggestions, please post to this link：
https://github.com/yaronzz/Tidal-Media-Downloader/issues/491