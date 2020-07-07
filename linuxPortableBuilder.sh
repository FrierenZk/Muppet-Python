python3 ./tools.py
pyinstaller -F --clean __main__.py -n Muppet-Python-Portable-x86_64-linux -y
if [ ! -d ./dist/Portable  ];then
	mkdir ./dist/Portable
fi
mv ./build_list.json ./dist/Portable/build_list.json
mv ./dist/Muppet-Python-Portable-x86_64-linux ./dist/Portable/Muppet-Python-Portable-x86_64-linux
