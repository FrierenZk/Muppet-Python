python3 ./_task/tools.py
pyinstaller -D --clean __main__.py -n Muppet-Python-x86_64-linux -y
mv ./build_list.json ./dist/Muppet-Python-x86_64-linux/build_list.json
