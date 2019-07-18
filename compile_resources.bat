
del %1/resources.py

cd %1
cd resources

python build_resources.py > resources.qrc

pyrcc5 -o resources.py resources.qrc
move /Y resources.py ../resources.py

del resources.qrc

cd ..
cd ..
