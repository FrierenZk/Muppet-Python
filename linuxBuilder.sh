python3 ./_task/tools.py
pyinstaller -D --clean __main__.py -n Muppet-Python-x86_64-linux
mv ./_task/build_list.json ./dist/Muppet-Python-x86_64-linux/build_list.json