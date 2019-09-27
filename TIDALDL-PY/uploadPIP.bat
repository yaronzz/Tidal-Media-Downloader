REM cd to workdir
cd  %~dp0

REM remove old dir
rmdir /s/q dist
rmdir /s/q build
rmdir /s/q exe
rmdir /s/q tidal_dl.egg-info
mkdir exe

REM pack
python setup.py sdist bdist_wheel

REM creat exe file
pyinstaller -F tidal_dl/__main__.py

REM rename exe name
cd dist
ren __main__.exe tidal-dl.exe
move tidal-dl.exe ../exe/
cd ..

pip uninstall -y tidal-dl
REM python setup.py install

REM upload version to pip server
twine upload dist/*