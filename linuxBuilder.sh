python3 ./tools.py
pyinstaller -D --clean __main__.py -n Muppet-Python-x86_64-linux -y
mv ./build_list.json ./dist/Muppet-Python-x86_64-linux/build_list.json
mv ./timer_list.json ./dist/Muppet-Python-x86_64-linux/timer_list.json
mv ./server_settings.json ./dist/Muppet-Python-x86_64-linux/server_settings.json
