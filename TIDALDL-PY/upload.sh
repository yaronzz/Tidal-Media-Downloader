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
pipreqs ./ --force

# upload
twine upload dist/*