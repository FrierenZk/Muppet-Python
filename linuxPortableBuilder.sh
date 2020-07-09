python3 ./tools.py
pyinstaller -F --clean __main__.py -n Muppet-Python-Portable-x86_64-linux.bin -y
if [ ! -d ./dist/Muppet-Python-Portable-x86_64-linux  ];then
	mkdir ./dist/Muppet-Python-Portable-x86_64-linux
fi
mv ./build_list.json ./dist/Muppet-Python-Portable-x86_64-linux/build_list.json
mv ./dist/Muppet-Python-Portable-x86_64-linux.bin ./dist/Muppet-Python-Portable-x86_64-linux/Muppet-Python-Portable-x86_64-linux
