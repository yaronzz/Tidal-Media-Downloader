rmdir /s /q dist
rmdir /s /q build 
rmdir /s /q __init__.spec

cd TIDALDL-PY
rmdir /s /q __init__.spec 
rmdir /s /q dist
rmdir /s /q build 
rmdir /s /q exe
rmdir /s /q MANIFEST.in
rmdir /s /q *.egg-info

python setup.py sdist bdist_wheel
python -m PyInstaller -F tidal_dl/__init__.py -n "tidal-dl" --distpath "exe"
pip uninstall -y tidal-dl